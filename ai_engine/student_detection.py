import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

# Start camera
cap = cv2.VideoCapture(0)

print("Starting student detection...")

while True:

    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection
    results = model(frame)

    for r in results:
        boxes = r.boxes

        for box in boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            # class 0 = person in COCO dataset
            if cls == 0 and conf > 0.5:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, "Student", (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    cv2.imshow("EduVision AI - Student Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()