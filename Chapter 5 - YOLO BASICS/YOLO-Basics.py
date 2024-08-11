from ultralytics import YOLO
import cv2
 
model = YOLO('yolov8n.pt')
results = model("Chapter 5 - YOLO BASICS/Images/1.jpeg", show=True)
cv2.waitKey(0)