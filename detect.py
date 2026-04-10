import cv2
from ultralytics import YOLO

# Load trained model
model = YOLO("models/mask_detector.pt")

# Global counters
mask_count = 0
no_mask_count = 0

def run_detection():
    global mask_count, no_mask_count

    # Open camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Camera not working")
        return

    print("✅ Camera started")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                # Count logic
                if label == "with_mask":
                    mask_count += 1
                    color = (0, 255, 0)
                    text = "Mask"
                elif label == "without_mask":
                    no_mask_count += 1
                    color = (0, 0, 255)
                    text = "No Mask"
                    print("🚨 ALERT: No Mask Detected!")
                else:
                    color = (0, 165, 255)
                    text = "Incorrect"

                # Draw box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow("VisionGuard AI", frame)

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()