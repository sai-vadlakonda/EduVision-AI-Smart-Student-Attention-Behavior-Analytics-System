import cv2
import os

roll_no = input("Enter Roll Number: ")
name = input("Enter Student Name: ")

student_folder = f"dataset/{roll_no}_{name}"

os.makedirs(student_folder, exist_ok=True)

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

count = 0
max_images = 30

print("Capturing images... Look at the camera")

while True:

    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        face = frame[y:y+h, x:x+w]

        # Resize for FaceNet
        face = cv2.resize(face, (160,160))

        img_path = f"{student_folder}/img_{count}.jpg"

        cv2.imwrite(img_path, face)

        count += 1

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        print(f"Captured image {count}")

    cv2.imshow("Register Student", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if count >= max_images:
        break

cap.release()
cv2.destroyAllWindows()

print("Student registered successfully!")