from ultralytics import YOLO
import cv2
import cvzone
import math
import torch
import time
import threading
import logging
import os
import serial
import mysql.connector
import time
from datetime import datetime

# This removes the output of ultralytics
logging.getLogger('ultralytics').setLevel(logging.WARNING)

# Initialize values
mydb = False
sql = False
# sql.execute("SHOW DATABASES")
# for x in sql:
#     print(x)
# sql.execute("USE traffic_density")

port = 'COM4'  # Replace with your port if different
baudrate = 9600  # Standard baud rate for HC-06
timeout = 1


light_pattern = 0
light_pattern_list = []
traffic_light_pattern = 0

source_values = [{} for _ in range(4)]
max_units = 900
seconds = 0

focused_lane = 1
green_light_timer = 0

area_class_1 = 1.25
area_class_2 = 6.6
area_class_3 = 13.38
area_class_4 = 25.74

lane_1_green_time = 5
lane_2_green_time = 10
lane_3_green_time = 15
lane_4_green_time = 20

yellow_timer = 3

lane_1_red_time = 0
lane_2_red_time = lane_1_green_time
lane_3_red_time = lane_1_green_time + lane_2_green_time 
lane_4_red_time = lane_1_green_time + lane_2_green_time + lane_3_green_time

traffic_lane_1_density = 0
traffic_lane_2_density = 0
traffic_lane_3_density = 0
traffic_lane_4_density = 0

traffic_lane_density=[]

light_pos = (100, 100, 50, 50)  # (x, y, width, height)
colors = [(0, 0, 255), (0, 255, 255), (0, 255, 0)]  # Red, Yellow, Green
traffic_light_width = 50
traffic_light_height = 50

lane_1_color = 0
lane_2_color = 0
lane_3_color = 0
lane_4_color = 0

fps = 0
highest_fps = 0
lowest_fps = 0

inference = 0

# Define the position for the text
x, y = 10, 30
spacing = 240  # Space between lines

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

video_sources = [
    # cv2.VideoCapture(0, cv2.CAP_DSHOW),
    # cv2.VideoCapture(0, cv2.CAP_DSHOW),
    # cv2.VideoCapture(0, cv2.CAP_DSHOW),
    # cv2.VideoCapture(0, cv2.CAP_DSHOW),
    cv2.VideoCapture('C:/xampp/htdocs/TRAFFIC-DENSITY-ALGORITHM/Trial Files/video-source/video-source-1.mp4'),
    cv2.VideoCapture('C:/xampp/htdocs/TRAFFIC-DENSITY-ALGORITHM/Trial Files/video-source/video-source-2.mp4'),
    cv2.VideoCapture('C:/xampp/htdocs/TRAFFIC-DENSITY-ALGORITHM/Trial Files/video-source/video-source-3.mp4'),
    cv2.VideoCapture('C:/xampp/htdocs/TRAFFIC-DENSITY-ALGORITHM/Trial Files/video-source/video-source-4.mp4')
    # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/video-source-1.mp4'),
    # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/video-source-2.mp4'),
    # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/video-source-3.mp4'),
    # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/video-source-4.mp4'),
    # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/sample_2.mp4'),
    # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/sample_2.mp4'),
    # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/sample_2.mp4'),
    # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/sample_2.mp4'),
]

model = YOLO('C:/xampp/htdocs/TRAFFIC-DENSITY-ALGORITHM/weights/vehicle-detection-3.pt')
# model = YOLO('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/weights/vehicle-detection-3.pt')
class_names = ["Class 1", "Class 2", "Class 3", "Class 4"]

# DISPLAY

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

def draw_lane_timer(img, lane):
    
    traffic_timer = ""

    if lane == 1:
        if lane_1_green_time > 3:
            traffic_timer = f"GREEN {lane_1_green_time - yellow_timer} RED: {lane_1_red_time}"
        else:
            traffic_timer = f"YELLOW {lane_1_green_time} RED: {lane_1_red_time}"

    elif lane == 2:
        if lane_2_green_time > 3:
            traffic_timer = f"GREEN {lane_2_green_time - yellow_timer} RED: {lane_2_red_time}"
        else:
            traffic_timer = f"YELLOW {lane_2_green_time} RED: {lane_2_red_time}"

    elif lane == 3:
        if lane_3_green_time > 3:
            traffic_timer = f"GREEN {lane_3_green_time - yellow_timer} RED: {lane_3_red_time}"
        else:
            traffic_timer = f"YELLOW {lane_3_green_time} RED: {lane_3_red_time}"

    elif lane == 4:
        if lane_4_green_time > 3:
            traffic_timer = f"GREEN {lane_4_green_time - yellow_timer} RED: {lane_4_red_time}"
        else:
            traffic_timer = f"YELLOW {lane_4_green_time} RED: {lane_4_red_time}"

    
    cvzone.putTextRect(img, traffic_timer, (x + 2 * 200, y + 125), scale=2, thickness=3, colorR=(0, 0, 0))

def draw_lane_density(img, percentage):
    traffic_density_text = f"Traffic Lane Density: {percentage:.2f} %"
    cvzone.putTextRect(img, traffic_density_text, (x+ 5 * spacing, y + 125), scale=2, thickness=3, colorR=(0, 0, 0))

def draw_traffic_light(img, lane):
    global light_pattern, light_pattern_list, traffic_light_pattern
    if lane == 1:
        if lane_1_green_time > 3 and lane_1_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[2], thickness= -1)  # RYG
            # light_pattern = 1
            # light_pattern_list.append(light_pattern)
        elif lane_1_green_time <= 3 and lane_1_green_time >= 0 and lane_1_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[1], thickness= -1)
            # light_pattern = 2
            # light_pattern_list.append(light_pattern)
        else:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[0], thickness= -1)
            # light_pattern = 3
            # light_pattern_list.append(light_pattern)


    elif lane == 2:
        if lane_2_green_time > 3 and lane_2_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[2], thickness= -1)  # RYG
            # light_pattern = 3
            # light_pattern_list.append(light_pattern)
        elif lane_2_green_time <= 3 and lane_2_green_time >= 0 and lane_2_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[1], thickness= -1)
            # light_pattern = 4
            # light_pattern_list.append(light_pattern)
        else:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[0], thickness= -1)
            # light_pattern = 5
            # light_pattern_list.append(light_pattern)

    elif lane == 3:
        if lane_3_green_time > 3 and lane_3_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[2], thickness= -1)  # RYG
            # light_pattern = 5
            # light_pattern_list.append(light_pattern)
        elif lane_3_green_time <= 3 and lane_3_green_time >= 0 and lane_3_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[1], thickness= -1)
            # light_pattern = 6
            # light_pattern_list.append(light_pattern)
        else:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[0], thickness= -1)
            # light_pattern = 7
            # light_pattern_list.append(light_pattern)

    elif lane == 4:
        if lane_4_green_time > 3 and lane_4_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[2], thickness= -1)  # RYG
            # light_pattern = 7
            # light_pattern_list.append(light_pattern)
        elif lane_4_green_time <= 3 and lane_4_green_time >= 0 and lane_4_red_time == 0:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[1], thickness= -1)
            # light_pattern = 8
            # light_pattern_list.append(light_pattern)
        else:
            cv2.rectangle(img, (100, 100), (200 + traffic_light_width, 200 + traffic_light_height), colors[0], thickness= -1)
            # light_pattern = 1
            # light_pattern_list.append(light_pattern)

def draw_fps(img):
    global fps
    cvzone.putTextRect(img, str(fps), (x + 2 * 200, y + 525), scale=2, thickness=3, colorR=(255, 0, 0))

#CALCULATION

def calculate_timer(lane, density):
    if lane == 1:
        if density <= 33.333:
            return 21 + yellow_timer
        elif density <= 66.666:
            return 42 + yellow_timer
        else:
            return 65 + yellow_timer
    elif lane == 2:
        if density <= 33.333:
            return 35 + yellow_timer
        elif density <= 66.666:
            return 70 + yellow_timer
        else:
            return 105 + yellow_timer
    elif lane == 3:
        if density <= 33.333:
            return 11
        elif density <= 66.666:
            return 22 + yellow_timer
        else:
            return 35 + yellow_timer
    elif lane == 4:
        if density <= 33.333:
            return 13 + yellow_timer
        elif density <= 66.666:
            return 26 + yellow_timer
        else:
            return 40 + yellow_timer
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
    global lane_1_red_time, lane_2_red_time, lane_3_red_time, lane_4_red_time, yellow_timer
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
                lane_1_green_time = calculate_timer(1, traffic_lane_1_density) + yellow_timer
                lane_1_red_time = calculate_red_light_timer(1)

        elif focused_lane == 2:
            if lane_2_green_time > 0:
                lane_2_green_time -= 1
                lane_1_red_time -= 1
                lane_3_red_time -= 1
                lane_4_red_time -= 1
            else:
                focused_lane = 3
                lane_2_green_time = calculate_timer(2,traffic_lane_2_density) + yellow_timer
                lane_2_red_time = calculate_red_light_timer(2)

        elif focused_lane == 3:
            if lane_3_green_time > 0:
                lane_3_green_time -= 1
                lane_2_red_time -= 1
                lane_1_red_time -= 1
                lane_4_red_time -= 1
            else:
                focused_lane = 4
                lane_3_green_time = calculate_timer(3, traffic_lane_3_density) + yellow_timer
                lane_3_red_time = calculate_red_light_timer(3)

        elif focused_lane == 4:
            if lane_4_green_time > 0:
                lane_4_green_time -= 1
                lane_1_red_time -= 1
                lane_2_red_time -= 1
                lane_3_red_time -= 1
            else:
                focused_lane = 1
                lane_4_green_time = calculate_timer(4, traffic_lane_4_density) + yellow_timer
                lane_4_red_time = calculate_red_light_timer(4)

        # print(f"{output}")
    l   

def calculate_traffic_density(source_values, i):
    source_values[i]['source_percentage'] = (source_values[i]['total_units'] / max_units) * 100
#MODEL AND PROCESS

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

def show_output(video_sources, unit_testing):
    global traffic_light_pattern

    # if (unit_testing == 0):
    #     print('here')
    #     start_bluetooth_connection()
    
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
            
            calculate_traffic_density(source_values, i)
            set_fps()
            
            draw_class_texts(imgList[i], source_values[i]['class_values'])
            draw_total_unit_text(imgList[i], source_values[i]['total_units'])
            draw_percentage_unit_text(imgList[i], source_values[i]['source_percentage'])
            draw_lane_timer(imgList[i], i+1)
            draw_traffic_light(imgList[i], i+1) #shows undelayed display output
            # draw_fps(imgList[i])
            set_traffic_light_patter(imgList[i], i+1)


        initialize_traffic_light()
        print(traffic_light_pattern)
        light_pattern_list.clear()

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

def initialize_traffic_light():
    global traffic_light_pattern
    # print('here')
    traffic_light_pattern = int("".join(map(str, light_pattern_list)))
    # print(traffic_light_pattern)

# PERFORMANCE TESTING

def set_fps():
    global fps, lowest_fps, highest_fps
    fps += 1

    if fps > highest_fps:
        highest_fps = fps

    if fps < lowest_fps:
        lowest_fps = fps

def get_fps():
    global fps, lowest_fps, highest_fps
    while True:
        time.sleep(1)
        os.system('cls')
        print(f"FPS: {fps}")
        print(f"H-FPS: {highest_fps}")
        # print(f"L-FPS: {lowest_fps}")insin     
        
        fps = 0

# SEND SIGNAL TO ARDUINO

def start_bluetooth_connection():
    global ser
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Give time to establish
        print("Connected to HC-06")
        return ser
    except serial.SerialException as e:
        print(f"Error connecting to Bluetooth module: {e}")
        exit()

def change_light_pattern(unit_test):
    global light_pattern, traffic_light_pattern
    start_bluetooth_connection()
    
    while True:
        time.sleep(1.2)
        switch_dict = {
            1571: 1,
            2571: 2,
            3371: 3,
            3471: 4,
            3551: 5,
            3561: 6,
            3577: 7,
            3578: 8,
            1234: 9,
            0000: 10,
            1111: 11,

        }
        if (unit_test != 0):
            while True:
                pattern = input('Light Pattern: \t')
                arduino_light_pattern = switch_dict.get(int(pattern), -1)
                print(f"Traffic Light Pattern: \t{arduino_light_pattern}")
                ser.write(str(arduino_light_pattern).encode())

        else:
            arduino_light_pattern = switch_dict.get(traffic_light_pattern, -1)  # Default to -1 if not found

        print(f"Traffic Light Pattern: \t{arduino_light_pattern}")

        ser.write(str(arduino_light_pattern).encode())


def set_traffic_light_patter(img, lane):
    global light_pattern, light_pattern_list, traffic_light_pattern

    if lane == 1:
        if lane_1_green_time > 5 and lane_1_red_time == 0:
            light_pattern_list.append(1)  # Green
        elif lane_1_green_time <= 5 and lane_1_green_time >= 2 and lane_1_red_time == 0:
            light_pattern_list.append(2)  # Yellow
        else:
            light_pattern_list.append(3)  # Red

    elif lane == 2:
        if lane_2_green_time > 5 and lane_2_red_time == 0:
            light_pattern_list.append(3)  # Green
        elif lane_2_green_time <= 5 and lane_2_green_time >= 2 and lane_2_red_time == 0:
            light_pattern_list.append(4)  # Yellow
        else:
            light_pattern_list.append(5)  # Red

    elif lane == 3:
        if lane_3_green_time > 5 and lane_3_red_time == 0:
            light_pattern_list.append(5)  # Green
        elif lane_3_green_time <= 5 and lane_3_green_time >= 2 and lane_3_red_time == 0:
            light_pattern_list.append(6)  # Yellow
        else:
            light_pattern_list.append(7)  # Red

    elif lane == 4:
        if lane_4_green_time > 5 and lane_4_red_time == 0:
            light_pattern_list.append(7)  # Green
        elif lane_4_green_time <= 5 and lane_4_green_time >= 2 and lane_4_red_time == 0:
            light_pattern_list.append(8)  # Yellow
        else:
            light_pattern_list.append(1)  # Red

# REPORT
def check_minute():
    last_minute = datetime.now().minute
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "cavitestateuniversity"
    )

    sql = mydb.cursor()
    sql.execute("USE traffic_density")
    while True:
        time.sleep(1)
        current_minute = datetime.now().minute

        if current_minute != last_minute:
            print('report generated')
            generate_report(mydb, sql) 
            last_minute = current_minute 

def generate_report(mydb, sql):
    now = datetime.now()

    minute = now.minute          # Minute (0-59)
    hour = now.hour              # Hour (0-23)
    day = now.isoweekday() % 7   # Day (0-6, where 0 = Sunday, 6 = Saturday)
    date = now.day               # Date (1-31)
    month = now.month            # Month (1-12)
    year = now.year              # Year (e.g., 2024)

    for i in range(4):
        sql.execute("""
            INSERT INTO report (minute, hour, day, date, month, year, lane, density)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (minute, hour, day, date, month, year, i + 1, source_values[i]['source_percentage'])) 

    sql.execute("""SELECT density FROM report ORDER BY id DESC LIMIT 4""")
    rows = sql.fetchall()

    rows = rows[::-1] #reverse output

    for row in rows:
        print(row)

    mydb.commit() # comment for testing purposes


# UNIT TESTING

def unit_vehicle_classification_module():
    unit_video = [
        # cv2.VideoCapture(0, cv2.CAP_DSHOW),
        # cv2.VideoCapture(0, cv2.CAP_DSHOW),
        # cv2.VideoCapture(0, cv2.CAP_DSHOW),
        # cv2.VideoCapture(0, cv2.CAP_DSHOW),
        cv2.VideoCapture('C:/xampp/htdocs/TRAFFIC-DENSITY-ALGORITHM/Trial Files/video-source/video-source-1.mp4'),
        cv2.VideoCapture('C:/xampp/htdocs/TRAFFIC-DENSITY-ALGORITHM/Trial Files/video-source/video-source-2.mp4'),
        cv2.VideoCapture('C:/xampp/htdocs/TRAFFIC-DENSITY-ALGORITHM/Trial Files/video-source/video-source-3.mp4'),
        cv2.VideoCapture('C:/xampp/htdocs/TRAFFIC-DENSITY-ALGORITHM/Trial Files/video-source/video-source-4.mp4')
        # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/video-source-1.mp4'),
        # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/video-source-2.mp4'),
        # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/video-source-3.mp4'),
        # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/video-source-4.mp4'),
        # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/sample_2.mp4'),
        # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/sample_2.mp4'),
        # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/sample_2.mp4'),
        # cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/yolo-algorithm/Trial Files/video-source/sample_2.mp4'),
    ]

    show_output(unit_video, 1)

def unit_traffic_density_calculation_module(class_1_count, class_2_count, class_3_count, class_4_count, expected_result):
    
    print('UNIT TESTING - Traffic Density Calculation ')
    source_values[0]['total_units'] = (class_1_count * area_class_1) + (class_2_count * area_class_2) + (class_3_count * area_class_3) + (class_4_count * area_class_4)
    calculate_traffic_density(source_values, 0)

    if (round(source_values[0]['source_percentage'],2) == expected_result):
        print(f"PASS, Expected Result: {expected_result}, Actual Result: {round(source_values[0]['source_percentage'],2)}")
    else:
        print(f"FAIL, Expected Result: {expected_result}, Actual Result: {round(source_values[0]['source_percentage'],2)}")

def unit_traffic_light_module(lane_1_density, lane_2_density, lane_3_density, lane_4_density, 
                              expected_lane_1_green_timer, expected_lane_2_green_timer, expected_lane_3_green_timer, expected_lane_4_green_timer,
                              expected_lane_1_red_timer, expected_lane_2_red_timer, expected_lane_3_red_timer, expected_lane_4_red_timer,):

    lane_1_green_time = calculate_timer(1, lane_1_density)
    lane_2_green_time = calculate_timer(2, lane_2_density)
    lane_3_green_time = calculate_timer(3, lane_3_density)
    lane_4_green_time = calculate_timer(4, lane_4_density)

    lane_1_red_timer = calculate_red_light_timer(1)
    lane_2_red_timer = calculate_red_light_timer(2)
    lane_3_red_timer = calculate_red_light_timer(3)
    lane_4_red_timer = calculate_red_light_timer(4)

    if (lane_1_green_time == expected_lane_1_green_timer and 
        lane_2_green_time == expected_lane_2_green_timer and 
        lane_3_green_time == expected_lane_3_green_timer and 
        lane_4_green_time == expected_lane_4_green_timer and
        lane_1_red_timer == expected_lane_1_red_timer and 
        lane_2_red_timer == expected_lane_2_red_timer and 
        lane_3_red_timer == expected_lane_3_red_timer and 
        lane_4_red_timer == expected_lane_4_red_timer):

        print("PASS:")
        print(f"Lane 1 Green Timer - Expected: {expected_lane_1_green_timer}, Actual: {lane_1_green_time}")
        print(f"Lane 2 Green Timer - Expected: {expected_lane_2_green_timer}, Actual: {lane_2_green_time}")
        print(f"Lane 3 Green Timer - Expected: {expected_lane_3_green_timer}, Actual: {lane_3_green_time}")
        print(f"Lane 4 Green Timer - Expected: {expected_lane_4_green_timer}, Actual: {lane_4_green_time}")
        print(f"Lane 1 Red Timer   - Expected: {expected_lane_1_red_timer}, Actual: {lane_1_red_timer}")
        print(f"Lane 2 Red Timer   - Expected: {expected_lane_2_red_timer}, Actual: {lane_2_red_timer}")
        print(f"Lane 3 Red Timer   - Expected: {expected_lane_3_red_timer}, Actual: {lane_3_red_timer}")
        print(f"Lane 4 Red Timer   - Expected: {expected_lane_4_red_timer}, Actual: {lane_4_red_timer}")

    else:
        print("FAIL:")
        print(f"Lane 1 Green Timer - Expected: {expected_lane_1_green_timer}, Actual: {lane_1_green_time}")
        print(f"Lane 2 Green Timer - Expected: {expected_lane_2_green_timer}, Actual: {lane_2_green_time}")
        print(f"Lane 3 Green Timer - Expected: {expected_lane_3_green_timer}, Actual: {lane_3_green_time}")
        print(f"Lane 4 Green Timer - Expected: {expected_lane_4_green_timer}, Actual: {lane_4_green_time}")
        print(f"Lane 1 Red Timer   - Expected: {expected_lane_1_red_timer}, Actual: {lane_1_red_timer}")
        print(f"Lane 2 Red Timer   - Expected: {expected_lane_2_red_timer}, Actual: {lane_2_red_timer}")
        print(f"Lane 3 Red Timer   - Expected: {expected_lane_3_red_timer}, Actual: {lane_3_red_timer}")
        print(f"Lane 4 Red Timer   - Expected: {expected_lane_4_red_timer}, Actual: {lane_4_red_timer}")

def unit_traffic_light_control_module(pattern):
    # start_bluetooth_connection()
    change_light_pattern(pattern)

def unit_traffic_density_report_module(lane_1_density, lane_2_density, lane_3_density, lane_4_density):
    source_values[0]['source_percentage'] = lane_1_density
    source_values[1]['source_percentage'] = lane_2_density
    source_values[2]['source_percentage'] = lane_3_density
    source_values[3]['source_percentage'] = lane_4_density

    check_minute()
    generate_report(sql)



# threading.Thread(target=get_fps).start()

threading.Thread(target=show_output, args=(video_sources, 0,)).start()
threading.Thread(target=change_light_pattern, args=(0,)).start()
threading.Thread(target=lane_timer, args=(1,)).start()
threading.Thread(target=check_minute).start()

#light pattern guide
# 1571: 1, Lane 1 - Green
# 2571: 2, Lane 1 - Yellow
# 3371: 3, Lane 2 - Green
# 3471: 4, Lane 2 - Yellow
# 3551: 5, Lane 3 - Green
# 3561: 6, Lane 3 - Yellow
# 3577: 7, Lane 4 - Green
# 3578: 8  Lane 4 - Yellow
# 1234: 9, Series
# 0000: 10, All Off
# 1111: 11, All On

# unit_traffic_density_calculation_module(1,2,3,4,17.51)
# unit_traffic_light_module(1,2,3,4,5,6,7,8,9,10,11,12)
# unit_vehicle_classification_module()
# unit_traffic_light_control_module(1)
# unit_traffic_density_report_module(10,12,13,14)