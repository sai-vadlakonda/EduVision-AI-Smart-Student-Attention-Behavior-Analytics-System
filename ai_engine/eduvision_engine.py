import sys
import os
import json
import threading
import time
import csv
import cv2
import pickle
import numpy as np
from datetime import datetime

from flask import Flask, Response
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from deepface import DeepFace

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from head_pose import estimate_head_pose
from emotion_detection import detect_emotion
from attention_score import calculate_attention, classify_attention, classroom_productivity


# -----------------------------
# Paths
# -----------------------------

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

phone_evidence_dir = os.path.join(ROOT, "phone_evidence")
os.makedirs(phone_evidence_dir, exist_ok=True)

phone_log_file = os.path.join(ROOT, "phone_violations.csv")
alert_log_file = os.path.join(ROOT, "alerts_log.csv")
attendance_file = os.path.join(ROOT, "attendance.csv")


# -----------------------------
# CSV initialization
# -----------------------------

if not os.path.exists(phone_log_file):
    with open(phone_log_file, "w", newline="") as f:
        csv.writer(f).writerow(["Time", "RollNo", "Student", "Image"])

if not os.path.exists(alert_log_file):
    with open(alert_log_file, "w", newline="") as f:
        csv.writer(f).writerow(["Time", "RollNo", "Student", "Alert"])

if not os.path.exists(attendance_file):
    with open(attendance_file, "w", newline="") as f:
        csv.writer(f).writerow(["RollNo", "Name", "Time", "Status"])


# -----------------------------
# Flask streaming
# -----------------------------

app = Flask(__name__)
output_frame = None
lock = threading.Lock()

@app.route("/video")
def video_feed():

    def generate():
        global output_frame

        while True:
            with lock:

                if output_frame is None:
                    continue

                ret, buffer = cv2.imencode(".jpg", output_frame)
                frame = buffer.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame +
                b"\r\n"
            )

    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def start_server():
    app.run(host="0.0.0.0", port=5000, threaded=True)

threading.Thread(target=start_server, daemon=True).start()


# -----------------------------
# Models
# -----------------------------

model = YOLO("yolov8n.pt")
tracker = DeepSort(max_age=30)

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# -----------------------------
# Load embeddings
# -----------------------------

with open("../student_recognition/embeddings/face_embeddings.pkl", "rb") as f:
    data = pickle.load(f)

known_embeddings = np.array(data["embeddings"])
known_labels = data["labels"]


# -----------------------------
# Memory
# -----------------------------

track_identity = {}
marked_students = set()

frame_count = 0
emotion_counts = {}
last_phone_capture = 0


# -----------------------------
# Camera
# -----------------------------

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

print("EduVision AI Engine Running...")


# -----------------------------
# Main Loop
# -----------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    frame_count += 1

    results = model(frame, conf=0.6)

    detections = []
    phones = []
    alerts = []

    # -----------------------------
    # YOLO detection
    # -----------------------------

    for r in results:

        for box in r.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if conf < 0.6:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            w = x2 - x1
            h = y2 - y1

            if w < 80 or h < 80:
                continue

            if cls == 0:
                detections.append(([x1, y1, w, h], conf, "person"))

            if cls == 67:
                phones.append((x1, y1, x2, y2))

    tracks = tracker.update_tracks(detections, frame=frame)

    students_detected = len(tracks)

    phone_users = 0
    total_attention = 0
    counted_students = 0


    # -----------------------------
    # Process tracks
    # -----------------------------

    for track in tracks:

        if not track.is_confirmed():
            continue

        track_id = track.track_id

        l, t, w, h = map(int, track.to_ltrb())

        # SAFE CROP
        frame_h, frame_w = frame.shape[:2]

        x1 = max(0, l)
        y1 = max(0, t)
        x2 = min(frame_w, l + w)
        y2 = min(frame_h, t + h)

        person = frame[y1:y2, x1:x2]

        if person is None or person.size == 0:
            continue

        if person.shape[0] < 40 or person.shape[1] < 40:
            continue

        roll_no = "Unknown"
        student = "Unknown"

        emotion = "neutral"
        head_direction = "Forward"
        phone_detected = False

        # -----------------------------
        # Face recognition
        # -----------------------------

        if track_id in track_identity:

            roll_no, student = track_identity[track_id]

        elif frame_count % 10 == 0:

            gray = cv2.cvtColor(person, cv2.COLOR_BGR2GRAY)

            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            for (fx, fy, fw, fh) in faces:

                face = person[fy:fy+fh, fx:fx+fw]

                if face.size == 0:
                    continue

                face = cv2.resize(face, (160, 160))

                try:

                    result = DeepFace.represent(
                        img_path=face,
                        model_name="Facenet",
                        enforce_detection=False
                    )

                    embedding = np.array(result[0]["embedding"])
                    embedding = embedding / np.linalg.norm(embedding)

                    distances = np.linalg.norm(
                        known_embeddings - embedding,
                        axis=1
                    )

                    min_distance = np.min(distances)
                    index = np.argmin(distances)

                    if min_distance < 0.9:

                        label = known_labels[index]

                        roll_no, student = label.split("_", 1)

                        track_identity[track_id] = (roll_no, student)

                        if label not in marked_students:

                            with open(attendance_file, "a", newline="") as f:
                                csv.writer(f).writerow([
                                    roll_no,
                                    student,
                                    datetime.now().strftime("%H:%M:%S"),
                                    "Present"
                                ])

                            marked_students.add(label)

                except:
                    pass


        # -----------------------------
        # Phone detection
        # -----------------------------

        for (px1, py1, px2, py2) in phones:

            if l < px1 < l+w and t < py1 < t+h:

                phone_detected = True
                phone_users += 1

                now = time.time()

                if now - last_phone_capture > 5:

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    image_name = f"{timestamp}.jpg"

                    filepath = os.path.join(phone_evidence_dir, image_name)

                    phone_crop = frame[py1:py2, px1:px2]

                    if phone_crop.size == 0:
                        phone_crop = person

                    cv2.imwrite(filepath, phone_crop)

                    with open(phone_log_file, "a", newline="") as f:
                        csv.writer(f).writerow([
                            datetime.now().strftime("%H:%M:%S"),
                            roll_no,
                            student,
                            image_name
                        ])

                    last_phone_capture = now


        # -----------------------------
        # Emotion + head pose
        # -----------------------------

        try:
            emotion = detect_emotion(person)
            head_direction = estimate_head_pose(person)

            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        except:
            pass


        # -----------------------------
        # Attention score
        # -----------------------------

        attention_score = calculate_attention(
            head_direction,
            emotion,
            phone_detected
        )

        state = classify_attention(
            attention_score,
            phone_detected
        )

        total_attention += attention_score
        counted_students += 1


        # -----------------------------
        # Draw box
        # -----------------------------

        cv2.rectangle(frame, (l, t), (l+w, t+h), (0, 255, 0), 2)

        label = f"{roll_no} {student} | {state}"

        cv2.putText(
            frame,
            label,
            (l, t-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )


    # -----------------------------
    # Classroom stats
    # -----------------------------

    avg_attention = 0

    if counted_students > 0:
        avg_attention = round(total_attention / counted_students, 2)

    productivity = classroom_productivity(
        avg_attention,
        phone_users,
        students_detected
    )

    stats = {
        "students": students_detected,
        "attention": avg_attention,
        "phones": phone_users,
        "productivity": productivity
    }

    with open(os.path.join(ROOT, "stats.json"), "w") as f:
        json.dump(stats, f)

    with open(os.path.join(ROOT, "alerts.json"), "w") as f:
        json.dump(alerts, f)

    with open(os.path.join(ROOT, "emotion_stats.json"), "w") as f:
        json.dump(emotion_counts, f)

    with lock:
        output_frame = frame.copy()


cap.release()
cv2.destroyAllWindows()