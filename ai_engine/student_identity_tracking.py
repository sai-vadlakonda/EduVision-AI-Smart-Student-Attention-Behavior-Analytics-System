import cv2
import pickle
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from deepface import DeepFace

# Load YOLO model
model = YOLO("yolov8n.pt")

# Load tracker
tracker = DeepSort(max_age=30)

# Load face embeddings
with open("../student_recognition/embeddings/face_embeddings.pkl", "rb") as f:
    data = pickle.load(f)

known_embeddings = data["embeddings"]
known_labels = data["labels"]

# Start webcam
cap = cv2.VideoCapture(0)

print("Starting EduVision AI Identity Tracking...")

while True:

    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    detections = []

    for r in results:
        boxes = r.boxes

        for box in boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if cls == 0 and conf > 0.5:  # person class

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                w = x2 - x1
                h = y2 - y1

                detections.append(([x1, y1, w, h], conf, "person"))

    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:

        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, w, h = map(int, track.to_ltrb())

        face = frame[t:t+h, l:l+w]

        label = "Unknown"

        try:

            embedding = DeepFace.represent(
                img_path=face,
                model_name="Facenet",
                enforce_detection=False
            )

            vector = embedding[0]["embedding"]

            distances = []

            for known_vector in known_embeddings:
                dist = np.linalg.norm(np.array(vector) - np.array(known_vector))
                distances.append(dist)

            min_distance = min(distances)
            index = distances.index(min_distance)

            if min_distance < 10:
                label = known_labels[index]

        except:
            pass

        cv2.rectangle(frame, (l, t), (l+w, t+h), (0,255,0), 2)

        cv2.putText(frame,
                    f"ID {track_id} | {label}",
                    (l, t-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2)

    cv2.imshow("EduVision AI - Identity Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()