import numpy as np
import pickle
from deepface import DeepFace


class FaceRecognizer:

    def __init__(self, embedding_path):

        with open(embedding_path,"rb") as f:
            data = pickle.load(f)

        self.embeddings = data["embeddings"]
        self.labels = data["labels"]

        # Track memory (prevents flickering)
        self.identity_memory = {}

        print("Loaded embeddings:",len(self.embeddings))


    def recognize(self, face, track_id):

        # If already known → reuse
        if track_id in self.identity_memory:
            return self.identity_memory[track_id]

        try:

            result = DeepFace.represent(
                img_path=face,
                model_name="Facenet",
                enforce_detection=False
            )

            vector = result[0]["embedding"]

            distances = []

            for emb in self.embeddings:

                dist = np.linalg.norm(
                    np.array(vector)-np.array(emb)
                )

                distances.append(dist)

            min_distance = min(distances)

            index = distances.index(min_distance)

            if min_distance < 1.1:

                label = self.labels[index]

                self.identity_memory[track_id] = label

                return label

        except:
            pass

        return "Unknown"