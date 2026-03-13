import cv2
from deepface import DeepFace

# cache last emotion to avoid flickering
last_emotion = "neutral"


def detect_emotion(face_img):

    global last_emotion

    if face_img is None or face_img.size == 0:
        return last_emotion

    try:

        # Resize for faster inference
        face = cv2.resize(face_img, (224, 224))

        result = DeepFace.analyze(
            face,
            actions=["emotion"],
            enforce_detection=False,
            detector_backend="opencv"
        )

        emotion = result[0]["dominant_emotion"].lower()

        valid_emotions = [
            "happy",
            "neutral",
            "sad",
            "angry",
            "surprise",
            "fear",
            "disgust"
        ]

        if emotion not in valid_emotions:
            emotion = "neutral"

        last_emotion = emotion

        return emotion

    except Exception:
        # fallback to last detected emotion
        return last_emotion