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

cap = cv2.VideoCapture(1)  # Change to 0 or other indices if needed
num = 0

base_path = os.getcwd()
savepath = base_path + "/images"
if not os.path.exists(savepath):
    os.makedirs(savepath)

while cap.isOpened():  # While webcam is active
    success, img = cap.read()

    k = cv2.waitKey(5)
    if k == 27:  # 'Esc' key to exit
        break
    elif k == ord('s'):  # 's' key to save an image
        imgpath = f"{savepath}/img_{str(num)}.png"
        cv2.imwrite(imgpath, img)
        print("Image saved!")
        print(f"Save location: {imgpath}")
        num += 1

    cv2.imshow('Img', img)

cap.release()
cv2.destroyAllWindows()
