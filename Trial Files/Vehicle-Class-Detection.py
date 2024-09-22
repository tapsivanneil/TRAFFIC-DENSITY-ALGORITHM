from ultralytics import YOLO
import cv2
import cvzone
import math
import torch


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# # For Webcam
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)

# For video file
cap = cv2.VideoCapture('C:/Users/tapsi/OneDrive/Desktop/YOLO-ALGORITHM/Trial Files/vehicle-detect.mp4')


model = YOLO('C:/Users/tapsi/OneDrive/Desktop/YOLO-ALGORITHM/vehicle-detection-3.pt')

# Class names and values
class_names = ["Class 1", "Class 2", "Class 3", "Class 4"]
car_values = [1,2,3,4]


#Initialize values
class1_value = 0
class2_value = 0
class3_value = 0
class4_value = 0
total_units = 0
max_units = 40

# Define the position for the text
x, y = 10, 30
spacing = 40  # Space between lines

# Function to draw text with variables
def draw_class_texts(img, positions, class_names, values):
    for i, (class_name, value) in enumerate(zip(class_names, values)):
        text = f"{class_name}: {value}"
        # Draw text on the image
        cvzone.putTextRect(img, text, (positions[0], positions[1] + i * spacing), scale=1, thickness=1, colorR=(0, 0, 0))

def draw_total_unit_text(img, positions, total_units ):
    total_units_text = f"Total Units: {total_units}"
    cvzone.putTextRect(img, total_units_text, (positions[0], positions[1] + 4 * spacing), scale=1, thickness=1, colorR=(0, 0, 0))


def draw_percentage_unit_text(img, positions, percentage ):
    traffic_density_text = f"Traffic Density: {percentage} %"
    cvzone.putTextRect(img, traffic_density_text, (positions[0], positions[1] + 5 * spacing), scale=1, thickness=1, colorR=(0, 0, 0))

# Draw the class texts on the image

while True:
    success, img = cap.read()

    values = [class1_value, class2_value, class3_value, class4_value]
    
    percentage = (total_units / max_units) * 100 

    draw_class_texts(img, (x, y), class_names, values)
    draw_total_unit_text(img, (x, y), total_units )
    draw_percentage_unit_text(img, (x, y), percentage)

    #reset count values after each iteration of detection
    class1_value = 0
    class2_value = 0
    class3_value = 0
    class4_value = 0
    total_units = 0

    results = model(img, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # for open cvzone bounding box
            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))
            
            # rounded confidence level
            conf = math.ceil(box.conf[0] *100 )/ 100
                                    # prevents out of bounds conf
            
            cls = int(box.cls[0])

            if cls == 0:
                class1_value += 1
                total_units+= 1
            elif cls == 1:
                class2_value += 1
                total_units+= 2
            elif cls == 2:
                class3_value += 1
                total_units+= 3
            elif cls == 3:
                class4_value += 1
                total_units+= 4
                                   
            # accessing the class - confidence value - bounding box limit  - size
            cvzone.putTextRect(img, f'{class_names[cls]} {conf}', (max(0,x1) ,max(35,y1)), scale = 1, thickness=1, colorR = (0,0,0))


    cv2.imshow("Image", img)

    #continues the process until the user press q button
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
