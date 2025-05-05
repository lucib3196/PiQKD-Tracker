"""
This script captures a simple image using the Raspberry Pi camera (Picamera2) and saves it to a predefined folder.

Features:
- Determines the script's directory and creates a folder for storing images.
- Initializes the Pi camera, configures it, and captures an image.
- Saves the captured image to the specified directory.

Requirements:
- Raspberry Pi with a supported camera module.
- Picamera2 library installed.

Usage:
Run the script on a Raspberry Pi with:
    python -m capture_image_pi

Author: Luciano Bermudez 
Date: 2/26/2025
"""

import os
from picamera2 import Picamera2, Preview
import time

def main():
    """
    Main function to capture an image using the Raspberry Pi Camera and save it.
    """
    # Get the current script directory and define save path
    dir_name = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(dir_name, 'test_images/pi_camera/')
    
    # Create the save directory if it does not exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    # Define the filename for the captured image
    filename = 'picamera_capture_test.jpg'
    save_file = os.path.join(save_path, filename)

    # Initialize the PiCamera2 instance
    picam2 = Picamera2()
    
    # Create and configure a preview configuration
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    
    # Start the camera
    picam2.start()
    
    # Allow time for camera exposure adjustment (important for better image quality)
    time.sleep(2)
    
    # Print the file path where the image will be saved
    print(f"Image will be saved at: {save_file}")
    
    # Capture and save the image
    picam2.capture_file(save_file)
    
    # Stop the camera (optional but recommended for clean exit)
    picam2.stop()

if __name__ == "__main__":
    main()
