import cv2
import pickle
import numpy as np
from deepface import DeepFace

print("Loading embeddings...")

with open("embeddings/face_embeddings.pkl","rb") as f:
    data = pickle.load(f)

known_embeddings = data["embeddings"]
known_labels = data["labels"]

print("Loaded embeddings:", len(known_embeddings))

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

print("Camera started")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:

        face = frame[y:y+h, x:x+w]

        face = cv2.resize(face,(160,160))

        label = "Unknown"

        try:

            result = DeepFace.represent(
                img_path=face,
                model_name="Facenet",
                enforce_detection=False
            )

            embedding = np.array(result[0]["embedding"])

            embedding = embedding / np.linalg.norm(embedding)

            distances = []

            for known in known_embeddings:

                known = np.array(known)

                dist = np.linalg.norm(embedding - known)

                distances.append(dist)

            min_distance = min(distances)

            index = distances.index(min_distance)

            print("Distance:",min_distance)

            if min_distance < 0.9:
                label = known_labels[index]

        except Exception as e:
            print("Recognition error:", e)

        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.putText(frame,label,(x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,(0,255,0),2)

    cv2.imshow("EduVision Face Recognition",frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()