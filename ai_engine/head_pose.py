import cv2

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def estimate_head_pose(face_img):

    if face_img is None or face_img.size == 0:
        return "Forward"

    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(gray, 1.2, 5)

    if len(faces) == 0:
        return "Forward"

    x, y, w, h = faces[0]

    face_center_x = x + w / 2
    face_center_y = y + h / 2

    frame_center_x = face_img.shape[1] / 2
    frame_center_y = face_img.shape[0] / 2

    dx = face_center_x - frame_center_x
    dy = face_center_y - frame_center_y

    # Horizontal direction
    if dx < -25:
        return "Left"

    if dx > 25:
        return "Right"

    # Vertical direction
    if dy > 25:
        return "Down"

    return "Forward"