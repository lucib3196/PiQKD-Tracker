import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector
from . import initialize_camera_feed, load_camera_calibration
from gpiozero import AngularServo
import numpy as np
import time
print("OpenCV version:", cv2.__version__)
# Initialize the FaceDetector object
# minDetectionCon: Minimum detection confidence threshold
# modelSelection: 0 for short-range detection (2 meters), 1 for long-range detection (5 meters)
face_detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

# Initialize the camera feed
camera = initialize_camera_feed(0)
width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Camera Width: {int(width)}, Camera Height: {int(height)}")

# Load camera calibration parameters
camera_matrix, camera_distortion_coefficients = load_camera_calibration()

print("Press 'q' to quit.")

# Define Servo
# Initialize the base servo on GPIO pin 17 with a range from -90 to 90 degrees
base_servo = AngularServo(17, min_angle=-90, max_angle=90)

# Initialize the upper servo on GPIO pin 27 with a range from -90 to 90 degrees
upper_servo = AngularServo(27, min_angle=-90, max_angle=90)


servo_x = 0
servo_y = 0

base_servo.angle = servo_x
upper_servo.angle = servo_y

time.sleep(1)


target_frequency = 1 / 30
camera.set(cv2.CAP_PROP_FPS, target_frequency)


while True:
    # Read a frame from the camera
    ret, frame = camera.read()
    if not ret:
        print("Failed to read frame from camera.")
        break

    # Detect faces in the frame
    frame, face_bboxes = face_detector.findFaces(frame, draw=False)

    if face_bboxes:
        for bbox in face_bboxes:
            # Extract bounding box details
            x, y, w, h = bbox['bbox']
            center = bbox["center"]
            score = int(bbox['score'][0] * 100)

            # Draw face annotations
            cv2.circle(frame, center, 5, (255, 0, 255), cv2.FILLED)  # Mark the center of the face
            cvzone.putTextRect(frame, f'{score}%', (x, y - 10))  # Display confidence score
            cvzone.cornerRect(frame, (x, y, w, h))  # Draw bounding box with corners

            # Servo and Position Mapping
            servo_x = np.interp(x,[0,width],[-90,90])
            # servo_y = np.interp(y,[0,height],[-90,90])

            print(f'Value x {servo_x}, Values y {servo_y}')

            base_servo.angle = servo_x
            # upper_servo.angle = servo_y
            time.sleep(1)

            # Display x and y position below the bounding box
            position_text = f"x: {x}, y: {y}"
            cv2.putText(
                frame, 
                position_text, 
                (x, y + h + 30),  # Position below the bounding box
                cv2.FONT_HERSHEY_PLAIN, 
                2, 
                (0, 255, 0), 
                2
            )

    cv2.putText(frame, f'Servo X: {servo_x} deg', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)    

    # Display the frame in a window named 'Image'
    cv2.imshow("Image", frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()
