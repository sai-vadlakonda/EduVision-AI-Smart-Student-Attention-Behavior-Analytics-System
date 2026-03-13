import os
import cv2
import pickle
import numpy as np
from deepface import DeepFace

dataset_path = "dataset"

embeddings = []
labels = []

print("Training started...")

for student in os.listdir(dataset_path):

    student_path = os.path.join(dataset_path, student)

    if not os.path.isdir(student_path):
        continue

    print("Processing:", student)

    for img in os.listdir(student_path):

        img_path = os.path.join(student_path, img)

        try:

            image = cv2.imread(img_path)

            if image is None:
                continue

            image = cv2.resize(image,(160,160))

            result = DeepFace.represent(
                img_path=image,
                model_name="Facenet",
                enforce_detection=False
            )

            embedding = np.array(result[0]["embedding"])

            # normalize embedding
            embedding = embedding / np.linalg.norm(embedding)

            embeddings.append(embedding)
            labels.append(student)

            print("Added:", img)

        except:
            print("Skipped:", img)

data = {
    "embeddings": embeddings,
    "labels": labels
}

os.makedirs("embeddings", exist_ok=True)

with open("embeddings/face_embeddings.pkl","wb") as f:
    pickle.dump(data,f)

print("Training finished")
print("Total embeddings:",len(embeddings))