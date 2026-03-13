import mediapipe as mp
import cv2

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


def detect_hand_raise(frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = pose.process(rgb)

    if result.pose_landmarks:

        landmarks = result.pose_landmarks.landmark

        wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        if wrist.y < shoulder.y:
            return True

    return False