from ultralytics import YOLO
import cv2
import cvzone
import math
import torch
import time
import threading
import logging

# This removes the output of ultralytics
logging.getLogger('ultralytics').setLevel(logging.WARNING)

# Initialize values
source_values = [{} for _ in range(4)]
max_units = 40
seconds = 0
timer_seconds = 0
calculated_seconds = 0

focused_lane = 1  # Initialize the focused lane
lane_1_calculated_seconds = 5  # Example value, set according to your needs
lane_2_calculated_seconds = 5  # Example value, set according to your need

rect1_pos = (100, 100, 50, 50)  # (x, y, width, height)
colors = [(0, 0, 255), (0, 255, 255), (0, 255, 0)]  # Red, Yellow, Green

lane_1_color = 0
lane_2_color = 0

top_left = (50, 50)      # Top-left corner at (50, 50)
bottom_right = (350, 300)  # Bottom-right corner at (350, 300)
thickness = -1  

traffic_light_width = 50
traffic_light_height = 50


# Define the position for the text
x, y = 10, 30
spacing = 240  # Space between lines

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

video_sources = [
    # cv2.VideoCapture(0, cv2.CAP_DSHOW),
    # cv2.VideoCapture(0, cv2.CAP_DSHOW),
    # cv2.VideoCapture(0, cv2.CAP_DSHOW),
    # cv2.VideoCapture(0, cv2.CAP_DSHOW),
    cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source-1.mp4'),
    cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source-2.mp4'),
    cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source-3.mp4'),
    cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source-4.mp4'),
]


model = YOLO('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/vehicle-detection-3.pt')
class_names = ["Class 1", "Class 2", "Class 3", "Class 4"]

# Function to draw text with variables
def draw_class_texts(img, values):
    for i, (class_name, value) in enumerate(zip(class_names, values)):
        text = f"{class_name}: {value}"
        cvzone.putTextRect(img, text, (x+ i * spacing, y ), scale=2, thickness=3, colorR=(0, 0, 0))

def draw_total_unit_text(img, total_units):
    total_units_text = f"Total Units: {total_units}"
    cvzone.putTextRect(img, total_units_text, (x+ 4 * spacing, y ), scale=2, thickness=3, colorR=(0, 0, 0))

def draw_percentage_unit_text(img, percentage):
    traffic_density_text = f"Traffic Density: {percentage:.2f} %"
    cvzone.putTextRect(img, traffic_density_text, (x+ 6 * spacing, y ), scale=2, thickness=3, colorR=(0, 0, 0))

def draw_lane_density(img, percentage):
    traffic_density_text = f"Traffic Lane Density: {percentage:.2f} %"
    cvzone.putTextRect(img, traffic_density_text, (x+ 5 * spacing, y + 125), scale=2, thickness=3, colorR=(0, 0, 0))

def draw_lane_number(img, lane_num):
    traffic_density_text = f"Lane: {lane_num}"
    cvzone.putTextRect(img, traffic_density_text, (x+ 1 * spacing, y + 125), scale=2, thickness=3, colorR=(0, 0, 0))

def draw_lane_timer(img, seconds):
    traffic_timer = f"{seconds}"
    cvzone.putTextRect(img, traffic_timer, (x + 2 * 200, y + 125), scale=2, thickness=3, colorR=(0, 0, 0))

def draw_traffic_light(img, lane):
    global lane_1_color, lane_2_color
    if lane == 1 or lane == 2:
        cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[lane_1_color], thickness)
    elif lane == 3 or lane == 4:
        cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[lane_2_color], thickness)
        
def process_video(source_index, img):
    results = model(img, stream=True)
    class_values = [0] * 4
    total_units = 0

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))
            conf = math.ceil(box.conf[0] * 100) / 100
            cls = int(box.cls[0])

            if cls == 0:
                class_values[cls] += 1
                total_units+= 1
            elif cls == 1:
                class_values[cls] += 1
                total_units+= 2
            elif cls == 2:
                class_values[cls] += 1
                total_units+= 3
            elif cls == 3:
                class_values[cls] += 1
                total_units+= 4

            cvzone.putTextRect(img, f'{class_names[cls]} {conf}', (max(0, x1), max(35, y1)), scale=2, thickness=3, colorR=(123, 17, 19))

    return class_values, total_units
 
def timer():
    print('timer has restarted')
    time.sleep(5)
    global seconds, focused_lane, lane_1_color, lane_2_color
    while True:
        while seconds > 0:
            mins, secs = divmod(seconds, 60)  # Convert total seconds to minutes and seconds
            timer_display = '{:02d}:{:02d}'.format(mins, secs)  # Format the timer
            
            if focused_lane == 1:
                if seconds <= 2:
                    print(f"LANE 1 YELLOW: {timer_display}\tLANE 2 RED: {timer_display}", end='\r')
                    lane_1_color = 1
                    lane_2_color = 0

                else:
                    print(f"LANE 1 GREEN: {timer_display}\tLANE 2 RED: {timer_display}", end='\r')
                    lane_1_color = 2
                    lane_2_color = 0

            else:
                if seconds <= 2:
                    print(f"LANE 1 RED: {timer_display}\tLANE 2 YELLOW: {timer_display}", end='\r')
                    lane_1_color = 0
                    lane_2_color = 1

                else:
                    print(f"LANE 1 RED: {timer_display}\tLANE 2 GREEN: {timer_display}", end='\r')
                    lane_1_color = 0
                    lane_2_color = 2
        
            time.sleep(1)  # Wait for one second
            seconds -= 1  # Decrease the seconds
            
            # if seconds == 2 & focused_lane == 1:
            #     print('YELLOW LIGHT ON LANE 1')
            # elif seconds == 2 & focused_lane == 2:
            #     print('YELLOW LIGHT ON LANE 2')


        while seconds == 0:
            seconds = calculated_seconds
            print(f'\nTimer reset to {calculated_seconds} seconds.')

        # When the timer hits zero, switch lanes
        if focused_lane == 1:
            # print(f'\nTimer finished for Lane 1. Switching to Lane 2.')
            focused_lane = 2  # Switch to Lane 2
        else:
            # print(f'\nTimer finished for Lane 2. Switching to Lane 1.')
            focused_lane = 1  # Switch back to Lane 1
        
def show_output():
    global calculated_seconds, seconds
    while True:
        imgList = []
        for i, video_source in enumerate(video_sources):
            success, img = video_source.read()
            if not success:
                break
            class_values, total_units = process_video(i, img)
            source_values[i]['class_values'] = class_values
            source_values[i]['total_units'] = total_units
            imgList.append(img)

        for i in range(4):
            source_values[i]['source_percentage'] = (source_values[i]['total_units'] / max_units) * 100
            draw_class_texts(imgList[i], source_values[i]['class_values'])
            draw_total_unit_text(imgList[i], source_values[i]['total_units'])
            draw_percentage_unit_text(imgList[i], source_values[i]['source_percentage'])
            draw_lane_number(imgList[i], i + 1)
            draw_lane_timer(imgList[i], seconds)
            draw_traffic_light(imgList[i], i+1)
        

        traffic_lane_1_density = (source_values[0]['source_percentage'] + source_values[1]['source_percentage']) / 2
        traffic_lane_2_density = (source_values[2]['source_percentage'] + source_values[3]['source_percentage']) / 2

        draw_lane_density(imgList[0], traffic_lane_1_density)
        draw_lane_density(imgList[1], traffic_lane_1_density)
        draw_lane_density(imgList[2], traffic_lane_2_density)
        draw_lane_density(imgList[3], traffic_lane_2_density)

        if focused_lane == 1:
            if traffic_lane_1_density >= 0 and traffic_lane_1_density <= 25:
                calculated_seconds = 10
            elif traffic_lane_1_density > 25 and traffic_lane_1_density <= 50:
                calculated_seconds = 20
            elif traffic_lane_1_density > 50 and traffic_lane_1_density <= 75:
                calculated_seconds = 30
            elif traffic_lane_1_density > 75 and traffic_lane_1_density <= 100:
                calculated_seconds = 40
            elif traffic_lane_1_density > 100:
                calculated_seconds = 50

        else:
            if traffic_lane_2_density >= 0 and traffic_lane_2_density <= 25:
                calculated_seconds = 10
            elif traffic_lane_2_density > 25 and traffic_lane_2_density <= 50:
                calculated_seconds = 20
            elif traffic_lane_2_density > 50 and traffic_lane_2_density <= 75:
                calculated_seconds = 30
            elif traffic_lane_2_density > 75 and traffic_lane_2_density <= 100:
                calculated_seconds = 40
            elif traffic_lane_2_density > 100:
                calculated_seconds = 50


        # print(traffic_lane_1_density)
        # print(traffic_lane_2_density)

        stackedImg = cvzone.stackImages(imgList, 2, 0.4)
        cv2.imshow("stackedImg", stackedImg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

threading.Thread(target=show_output).start()
threading.Thread(target=timer).start()




        
