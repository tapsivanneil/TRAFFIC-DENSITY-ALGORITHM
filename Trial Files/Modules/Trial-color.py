import cv2
import numpy as np
from cvzone.ColorModule import ColorFinder

# Initialize a blank image
height, width = 600, 800
img = np.zeros((height, width, 3), np.uint8)

# Define rectangle positions and colors
rect1_pos = (100, 100, 200, 150)  # (x, y, width, height)
rect2_pos = (400, 100, 200, 150)  # (x, y, width, height)
colors = [(0, 0, 255), (0, 255, 255), (0, 255, 0)]  # Red, Yellow, Green
current_color = 0  # Start with red

# Function to change color
def change_color(key):
    global current_color
    if key == ord('r'):  # Press 'r' for Red
        current_color = 0
    elif key == ord('y'):  # Press 'y' for Yellow
        current_color = 1
    elif key == ord('g'):  # Press 'g' for Green
        current_color = 2

while True:
    img[:] = (0, 0, 0)  # Clear the image

    # Draw rectangles with the current color
    cv2.rectangle(img, (rect1_pos[0], rect1_pos[1]), 
                  (rect1_pos[0] + rect1_pos[2], rect1_pos[1] + rect1_pos[3]),
                  colors[current_color], -1)
    
    cv2.rectangle(img, (rect2_pos[0], rect2_pos[1]), 
                  (rect2_pos[0] + rect2_pos[2], rect2_pos[1] + rect2_pos[3]),
                  colors[current_color], -1)

    cv2.imshow("Rectangles", img)

    # Wait for a key press and change color
    key = cv2.waitKey(1) & 0xFF
    change_color(key)

    # Exit if 'q' is pressed
    if key == ord('q'):
        break

cv2.destroyAllWindows()