"""
File Name: calibration_image_capture.py

This script captures images from a USB webcam or Raspberry Pi Camera (PiCamera2) for calibration purposes.

Features:
- Allows the user to specify the directory where images will be saved.
- Supports capturing images from either a USB camera or a Pi Camera.
- Press 's' to save an image and 'Esc' to exit (for USB cameras).
- For Pi Camera, press 'c' to capture an image and 'q' to exit.

Usage:
1. The script asks the user to confirm or specify the calibration image save path.
2. The user selects between USB Camera and PiCamera.
3. The script starts capturing images based on the selected camera.

Dependencies:
- OpenCV (`cv2`)
- Picamera2 (for Pi Camera usage)
- OS module
- Time module

Author: Luciano Bermudez
Date: 2/26/2025
"""

import os
import cv2
import time
from picamera2 import Picamera2

def get_calibration_path(file_path='calibration_path'):
    """Returns the calibration path where images will be saved."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "test_images", file_path)

def main():
    """
    Main function to ask the user for calibration path and camera selection, then capture images.
    """
    # Get and define the calibration path
    while True:
        confirm = input(
            f"The following is the current calibration path settings\n"
            f"Calibration Path: {get_calibration_path()}\n"
            "Would you like to continue with these settings or provide a new base folder path?\n"
            "Note: It will override the current images. (yes/no): "
        ).strip().lower()
        
        if confirm in ['yes', 'y']:
            calibration_path = get_calibration_path()
            break
        elif confirm in ['no', 'n']:
            filepath = input("Enter the directory where the images will be placed: ").strip()
            calibration_path = get_calibration_path(filepath)
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    
    print(f"Calibration Path Set: {calibration_path}")
    
    # Determine what is being calibrated
    options = ["USB", "PiCamera"]
    while True:
        camera = input(f"Choose a camera ({', '.join(options)}): ").strip()
        if camera in options:
            print(f"You selected: {camera}")
            break
        print("Invalid choice. Please select from the options.")
    
    # Ensure the calibration directory exists
    os.makedirs(calibration_path, exist_ok=True)
    
    # Capture images from USB Camera
    if camera == "USB":
        cam = cv2.VideoCapture(0)
        num = 0
        while cam.isOpened():
            ret, frame = cam.read()
            k = cv2.waitKey(5)
            print("Press 's' to save an image, 'Esc' to quit.")
            
            if k == 27:  # 'Esc' key to exit
                break
            elif k == ord('s'):  # 's' key to save an image
                img_path = os.path.join(calibration_path, f"img_{num}.png")
                cv2.imwrite(img_path, frame)
                print(f"Image saved: {img_path}")
                num += 1
            
            cv2.imshow('Img', frame)
        
        cam.release()
        cv2.destroyAllWindows()
        print("\nEnding script.")
    
    # Capture images from PiCamera
    elif camera == "PiCamera":
        picam2 = Picamera2()
        config = picam2.create_video_configuration(
            main={"size": (1280, 720), "format": 'XBGR8888'}
        )
        picam2.configure(config)
        picam2.start()
        time.sleep(2)  # Allow camera to adjust
        
        while True:
            key = input("Press 'c' to capture an image or 'q' to quit: ").strip().lower()
            
            if key == "c":
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"image_{timestamp}.jpg"
                save_path = os.path.join(calibration_path, filename)
                picam2.capture_file(save_path)
                print(f"Image saved: {save_path}")
            elif key == "q":
                print("Exiting...")
                break
            else:
                print("Invalid input, press 'c' to capture or 'q' to quit.")
        
        picam2.stop()
    
if __name__ == "__main__":
    main()
