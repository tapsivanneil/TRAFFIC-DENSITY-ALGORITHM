from ultralytics import YOLO

# Load the trained model
model = YOLO("path/to/your/model.pt")

# Validate the model
metrics = model.val(data="path/to/your/data.yaml")

# Access mAP metrics
print(f"mAP@0.5: {metrics['metrics/mAP50']}")
print(f"mAP@0.5:0.95: {metrics['metrics/mAP50-95']}")