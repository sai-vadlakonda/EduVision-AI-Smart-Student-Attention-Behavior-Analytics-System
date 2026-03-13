import pickle

with open("embeddings/face_embeddings.pkl","rb") as f:
    data = pickle.load(f)

print("Embeddings:", len(data["embeddings"]))
print("Labels:", len(data["labels"]))
print("Students:", set(data["labels"]))