from ultralytics import YOLO
import cv2
import cvzone
import math

# For Webcam
# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)


# For video file
cap = cv2.VideoCapture('Chapter 6 - YOLO WEBCAM\Videos\cars.mp4')

# adding mask image
mask = cv2.imread('Project 1 - Car Counter\mask.png')

# adding object detection model
model = YOLO('yolov8n.pt')

# classes of the model used
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]
 


while True:
    success, img = cap.read()

    # adding mask and applying in the img
    imgRegion = cv2.bitwise_and(img, mask)

    # getting the detected results
    results = model(imgRegion, stream=True)


    for r in results:
        boxes = r.boxes
        for box in boxes:
            
            # for open cv bounding box
            # x1,y1,x2,y2 = box.xyxy[0]
            # x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
            ##               source   bounding boxes(position) color   thickness
            # cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,255.), 3)

            # for open cvzone bounding box
            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1


            # rounded confidence level
            conf = math.ceil(box.conf[0] *100 )/ 100
            cls = int(box.cls[0])

            currentClass = classNames[cls]

            # selects only with the given class names and given that their confidence value is higher than the said values

            if currentClass == "car" or currentClass == "bus" or currentClass == "motorbike" and conf > 0.3:    
                                # source -    bbox    -   line length
                cvzone.cornerRect(img, (x1, y1, w, h), l= 9)        
                                    # accessing the class - confidence value - bounding box limit  - size
                cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0,x1) ,max(35,y1)), scale = 1, thickness=1, offset=5)
            
        
            # print values
            
            # confidence
            # print(conf)

            # bounding boxes
            # print(x1,y1,w,h)

    cv2.imshow("Image", img)
    cv2.imshow("ImageRegion", imgRegion)
    
    # add 0 if you want to stop the process and wait for command 1 for continous detection
    cv2.waitKey(1)
