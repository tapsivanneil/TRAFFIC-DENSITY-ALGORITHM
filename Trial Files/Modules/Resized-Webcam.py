import cv2

# Define video sources
video_sources = [
    cv2.VideoCapture(0, cv2.CAP_DSHOW),  # Webcam (Source 1)
    cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source-2.mp4'),  # Source 2
    cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source-3.mp4'),  # Source 3
    cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source-4.mp4'),  # Source 4
]

# Set the width and height for video sources 2, 3, and 4
for i in range(0, 4):  # Indices 1, 2, and 3 correspond to video sources 2, 3, and 4
    if video_sources[i].isOpened():
        video_sources[i].set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        video_sources[i].set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Iterate over each video source and print dimensions
for i, cap in enumerate(video_sources):
    if cap.isOpened():
        # Get frame width and height
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Video Source {i + 1}: Width = {width}, Height = {height}")
    else:
        print(f"Video Source {i + 1}: Unable to open")

# Release video sources
for cap in video_sources:
    cap.release()
