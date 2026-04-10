from flask import Flask, render_template, Response, jsonify
import cv2
from ultralytics import YOLO

app = Flask(__name__)

# Load trained model
model = YOLO("runs/detect/train5/weights/best.pt")

mask_count = 0
no_mask_count = 0


def generate_frames():
    global mask_count, no_mask_count

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)

        current_mask = 0
        current_no_mask = 0

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                if label == "with_mask":
                    current_mask += 1
                    color = (0, 255, 0)
                    text = "Mask"
                else:
                    current_no_mask += 1
                    color = (0, 0, 255)
                    text = "No Mask"

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # ✅ FIXED COUNT (per frame, not cumulative)
        mask_count = current_mask
        no_mask_count = current_no_mask

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stats')
def stats():
    return jsonify({
        "mask": mask_count,
        "no_mask": no_mask_count
    })


if __name__ == "__main__":
    app.run(debug=True)