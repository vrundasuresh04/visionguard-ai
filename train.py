from ultralytics import YOLO

print("🚀 Starting training...")

model = YOLO("yolov8n.pt")

results = model.train(
    data="data.yaml",
    epochs=5,
    imgsz=640,
    verbose=True
)

print("✅ Training completed!")