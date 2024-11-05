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
max_units = 900
seconds = 0

first_instance = True
focused_lane = 1
green_light_timer = 0

traffic_lane_density = []

area_class_1 = 1.25
area_class_2 = 6.6
area_class_3 = 13.38
area_class_4 = 25.74

lane_1_green_time = 5
lane_2_green_time = 10
lane_3_green_time = 15
lane_4_green_time = 20

lane_1_red_time = 0
lane_2_red_time = lane_1_green_time
lane_3_red_time = lane_1_green_time + lane_2_green_time 
lane_4_red_time = lane_1_green_time + lane_2_green_time + lane_3_green_time

traffic_lane_1_density = 0
traffic_lane_2_density = 0
traffic_lane_3_density = 0
traffic_lane_4_density = 0

light_pos = (100, 100, 50, 50)  # (x, y, width, height)
colors = [(0, 0, 255), (0, 255, 255), (0, 255, 0)]  # Red, Yellow, Green
traffic_light_width = 50
traffic_light_height = 50

lane_1_color = 0
lane_2_color = 0
lane_3_color = 0
lane_4_color = 0

# Define the position for the text
x, y = 10, 30
spacing = 240  # Space between lines

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

video_sources = [
    # cv2.VideoCapture(0, cv2.CAP_DSHOW),
    # cv2.VideoCapture(0, cv2.CAP_DSHOW),
    # cv2.VideoCapture(0, cv2.CAP_DSHOW),
    # cv2.VideoCapture(0, cv2.CAP_DSHOW),
    cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/video-source-1.mp4'),
    cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/video-source-2.mp4'),
    cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/video-source-3.mp4'),
    cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/video-source-4.mp4'),
]

model = YOLO('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/weights/vehicle-detection-3.pt')
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

def process_video(img):
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
                total_units+= area_class_1
            elif cls == 1:
                class_values[cls] += 1
                total_units+= area_class_2
            elif cls == 2:
                class_values[cls] += 1
                total_units+= area_class_3
            elif cls == 3:
                class_values[cls] += 1
                total_units+= area_class_4

            cvzone.putTextRect(img, f'{class_names[cls]} {conf}', (max(0, x1), max(35, y1)), scale=2, thickness=3, colorR=(123, 17, 19))

    return class_values, total_units

def draw_lane_density(img, percentage):
    traffic_density_text = f"Traffic Lane Density: {percentage:.2f} %"
    cvzone.putTextRect(img, traffic_density_text, (x+ 5 * spacing, y + 125), scale=2, thickness=3, colorR=(0, 0, 0))

def draw_traffic_light(img, lane):
    if lane == 1:
        if lane_1_green_time >= 3 and lane_1_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[2], thickness= -1)  # RYG
        elif lane_1_green_time <= 3 and lane_1_green_time > 0 and lane_1_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[1], thickness= -1)
        else:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[0], thickness= -1)

    elif lane == 2:
        if lane_2_green_time >= 3 and lane_2_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[2], thickness= -1)  # RYG
        elif lane_2_green_time <= 3 and lane_2_green_time > 0 and lane_2_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[1], thickness= -1)
        else:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[0], thickness= -1)

    elif lane == 3:
        if lane_3_green_time >= 3 and lane_3_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[2], thickness= -1)  # RYG
        elif lane_3_green_time <= 3 and lane_3_green_time > 0 and lane_3_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[1], thickness= -1)
        else:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[0], thickness= -1)

    elif lane == 4:
        if lane_4_green_time >= 3 and lane_4_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[2], thickness= -1)  # RYG
        elif lane_4_green_time <= 3 and lane_4_green_time > 0 and lane_4_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[1], thickness= -1)
        else:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[0], thickness= -1)

def show_output():
    while True:
        imgList = []
        for i, video_source in enumerate(video_sources):
            success, img = video_source.read()
            if not success:
                break
            
            class_values, total_units = process_video(img)
            source_values[i]['class_values'] = class_values
            source_values[i]['total_units'] = total_units
            imgList.append(img)

            source_values[i]['source_percentage'] = (source_values[i]['total_units'] / max_units) * 100
            draw_class_texts(imgList[i], source_values[i]['class_values'])
            draw_total_unit_text(imgList[i], source_values[i]['total_units'])
            draw_percentage_unit_text(imgList[i], source_values[i]['source_percentage'])
            draw_lane_timer(imgList[i], i+1)
            draw_traffic_light(imgList[i], i+1)


        traffic_lane_1_density = source_values[0]['source_percentage']
        traffic_lane_2_density = source_values[1]['source_percentage']
        traffic_lane_3_density = source_values[2]['source_percentage']
        traffic_lane_4_density = source_values[3]['source_percentage']

        traffic_lane_density = [traffic_lane_1_density, traffic_lane_2_density, traffic_lane_3_density, traffic_lane_4_density]

        for i in range(4):
            draw_lane_density(imgList[i], traffic_lane_density[i])


        stackedImg = cvzone.stackImages(imgList, 2, 0.4)
        cv2.imshow("stackedImg", stackedImg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def get_traffic_lane_density(lane):
    return traffic_lane_density[lane]

def calculate_timer(lane, density):
    if lane == 1:
        if density <= 33.333:
            return 21
        elif density <= 66.666:
            return 42
        else:
            return 65
    elif lane == 2:
        if density <= 33.333:
            return 35
        elif density <= 66.666:
            return 70
        else:
            return 105
    elif lane == 3:
        if density <= 33.333:
            return 11
        elif density <= 66.666:
            return 22
        else:
            return 35
    elif lane == 4:
        if density <= 33.333:
            return 13
        elif density <= 66.666:
            return 26
        else:
            return 40
    else:
        return 0

def calculate_red_light_timer(lane):
    if lane == 1:
        return lane_2_green_time + lane_3_green_time + lane_4_green_time
    elif lane == 2:
        return lane_1_green_time + lane_3_green_time + lane_4_green_time
    elif lane == 3:
        return lane_1_green_time + lane_2_green_time + lane_4_green_time
    elif lane == 4:
        return lane_1_green_time + lane_2_green_time + lane_3_green_time

def lane_timer(focused_lane):
    time.sleep(10)
    global lane_1_green_time, lane_2_green_time, lane_3_green_time, lane_4_green_time
    global lane_1_red_time, lane_2_red_time, lane_3_red_time, lane_4_red_time
    global traffic_lane_1_density, traffic_lane_2_density, traffic_lane_3_density, traffic_lane_4_density
    while True:
        time.sleep(1)  # Simulate the passing of time

        if focused_lane == 1:
            if lane_1_green_time > 0:
                lane_1_green_time -= 1
                lane_2_red_time -= 1
                lane_3_red_time -= 1
                lane_4_red_time -= 1
            else:
                focused_lane = 2
                lane_1_green_time = calculate_timer(1, traffic_lane_1_density)
                lane_1_red_time = calculate_red_light_timer(1)

        elif focused_lane == 2:
            if lane_2_green_time > 0:
                lane_2_green_time -= 1
                lane_1_red_time -= 1
                lane_3_red_time -= 1
                lane_4_red_time -= 1
            else:
                focused_lane = 3
                lane_2_green_time = calculate_timer(2,traffic_lane_2_density)
                lane_2_red_time = calculate_red_light_timer(2)

        elif focused_lane == 3:
            if lane_3_green_time > 0:
                lane_3_green_time -= 1
                lane_2_red_time -= 1
                lane_1_red_time -= 1
                lane_4_red_time -= 1
            else:
                focused_lane = 4
                lane_3_green_time = calculate_timer(3, traffic_lane_3_density)
                lane_3_red_time = calculate_red_light_timer(3)

        elif focused_lane == 4:
            if lane_4_green_time > 0:
                lane_4_green_time -= 1
                lane_1_red_time -= 1
                lane_2_red_time -= 1
                lane_3_red_time -= 1
            else:
                focused_lane = 1
                lane_4_green_time = calculate_timer(4, traffic_lane_4_density)
                lane_4_red_time = calculate_red_light_timer(4)


        output = (f"LANE 1: {'GREEN' if focused_lane == 1 else 'RED'} {lane_1_green_time if focused_lane == 1 else lane_1_red_time} | "
                f"LANE 2: {'GREEN' if focused_lane == 2 else 'RED'} {lane_2_green_time if focused_lane == 2 else lane_2_red_time} | "
                f"LANE 3: {'GREEN' if focused_lane == 3 else 'RED'} {lane_3_green_time if focused_lane == 3 else lane_3_red_time} | "
                f"LANE 4: {'GREEN' if focused_lane == 4 else 'RED'} {lane_4_green_time if focused_lane == 4 else lane_4_red_time}")
        
        print(f"{output}")
    l   

def draw_lane_timer(img, lane):
    
    traffic_timer = ""

    if lane == 1:
        traffic_timer = f"GREEN {lane_1_green_time} RED: {lane_1_red_time}"
    elif lane == 2:
        traffic_timer = f"GREEN {lane_2_green_time} RED: {lane_2_red_time}"

    elif lane == 3:
        traffic_timer = f"GREEN {lane_3_green_time} RED: {lane_3_red_time}"

    elif lane == 4:
        traffic_timer = f"GREEN {lane_4_green_time} RED: {lane_4_red_time}"
        
    
    
    cvzone.putTextRect(img, traffic_timer, (x + 2 * 200, y + 125), scale=2, thickness=3, colorR=(0, 0, 0))


threading.Thread(target=show_output).start()
threading.Thread(target=lane_timer, args=(1,)).start()

