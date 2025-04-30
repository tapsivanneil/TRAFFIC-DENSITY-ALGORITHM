import cv2
import time
from ultralytics import YOLO
import os

model = YOLO("../weights/train_data_version_4_map_91_9_best.pt")

video_path = 'Trial Files/video-source/video-source-1.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    print("Current working directory:", os.getcwd())
    exit()
else:
    print("Video opened successfully.")

frame_count = 0
total_inference_time = 0
lowest_inference_time = 200

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    start_time = time.time()

    results = model(frame)

    if isinstance(results, list):
        results = results[0]

    inference_time = (time.time() - start_time) * 1000
    total_inference_time += inference_time

    if (inference_time < lowest_inference_time):
        lowest_inference_time = inference_time

    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

average_inference_time = total_inference_time / frame_count if frame_count > 0 else 0
print(f"Average inference time: {average_inference_time:.2f} ms")
print(f"Best inference time: {lowest_inference_time:.2f} ms")

cap.release()
cv2.destroyAllWindows()
