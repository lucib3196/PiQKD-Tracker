"""
This script captures images from a webcam for calibration purposes.

Usage:
1. Camera Setup:
   - Plug in the desired camera.
   - If the camera feed does not appear, change `cv2.VideoCapture(1)` to `cv2.VideoCapture(0)` or try other indices.
     - `0` for the default webcam.
     - `1` for an external or secondary camera.

2. Key Controls:
   - Press 's' to save an image (recommended: 10-20 images for calibration).
   - Press 'Esc' to close the webcam feed and exit the script.

3. Saved Images:
   - All images are saved in the `images` folder in the current working directory.
   - Images are saved in the format `img_0.png`, `img_1.png`, etc.

Dependencies:
- OpenCV (`cv2`)
- OS
"""
import cv2
import os

from matplotlib import image
from . import initialize_camera_feed


camera = initialize_camera_feed(1) # Change to 0 or other indices if needed

# Creates a path to store calibration images 
base_path = os.path.dirname(os.path.abspath(__file__))
image_path = base_path+"/images"
calibration_path = image_path+ '/calibration_images'
if not os.path.exists(image_path):
    os.makedirs(image_path)
if not os.path.exists(calibration_path):
    os.makedirs(calibration_path)


num = 0
while camera.isOpened(): # While webcam is open
    ret, frame =  camera.read()
    k = cv2.waitKey(5)

    if k == 27:  # 'Esc' key to exit
        break

    elif k == ord('s'):  # 's' key to save an image
        imgpath = f"{calibration_path}/img_{str(num)}.png"
        cv2.imwrite(imgpath, frame)
        print("Image saved!")
        num += 1
    cv2.imshow('Img', frame)

camera.release()
cv2.destroyAllWindows()


