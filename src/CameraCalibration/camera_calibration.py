"""
This script performs camera calibration using a series of images of a checkerboard pattern. 
It calculates the camera matrix (intrinsic parameters) and distortion coefficients, and saves 
them to pickle files for later use. The calibration is based on detecting the internal corners 
of the checkerboard pattern in the input images.

The camera matrix includes the focal lengths and optical centers of the camera. 
The distortion coefficients correct lens distortion.

Steps:
1. Prepares object points based on the real-world dimensions of the checkerboard.
2. Reads images from the specified directory and processes them to detect chessboard corners.
3. If successful, stores the corresponding 2D and 3D points for calibration.
4. Calculates and saves the camera matrix and distortion coefficients.
5. Computes the calibration success rate and the mean re-projection error.

Outputs:
- `calibration.pkl`: Contains the camera matrix and distortion coefficients.
- `cameraMatrix.pkl`: Contains only the camera matrix.
- `dist.pkl`: Contains only the distortion coefficients.

A debug folder is created to store images with successful or failed detections.
"""

import pickle
import numpy as np
import cv2 as cv
import os

# Termination criteria for cornerSubPix (used to refine corner detection)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Define checkerboard size (internal corners along width and height)
num_squares_width = 8
num_squares_height = 7

# Prepare object points (3D points in real-world space, Z=0 for planar checkerboard)
objp = np.zeros((num_squares_width * num_squares_height, 3), np.float32)
objp[:, :2] = np.mgrid[0:num_squares_width, 0:num_squares_height].T.reshape(-1, 2)

# Arrays to store object points (3D) and image points (2D) from all the images
objpoints = []  # 3D points in the real world
imgpoints = []  # 2D points in the image plane

# Define the imaga paths
base_path = os.path.dirname(os.path.abspath(__file__))
image_path = base_path+"/images"
calibration_path = image_path+ '/calibration_images'
debug_image_path = image_path+'/debug'
success_path = debug_image_path + '/success'
failure_path = debug_image_path + '/failure'

# Validate input directory and create debug directories if needed
if not os.path.exists(calibration_path):
    print(f"Error: Directory {calibration_path} does not exist. Run calibration_image_capture to get calibration image")
    exit()

if not os.path.exists(debug_image_path):
    print(f"Creating debug path: {debug_image_path}")
    os.makedirs(debug_image_path)
    os.makedirs(success_path)
    os.makedirs(failure_path)

# Initialize counters for image processing
total_images = 0
success_count = 0
failure_count = 0

for root, _, files in os.walk(image_path):
    for fname in files:
        total_images += 1
        img_path = os.path.join(root, fname)
        print(f"Processing image: {img_path}")

        # Read the image
        img = cv.imread(img_path)
        if img is None:
            print(f"Error: Unable to load image {img_path}")
            failure_count += 1
            continue
        # Convert image to grayscale for corner detection
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv.findChessboardCorners(gray, (num_squares_width, num_squares_height), None)
        if ret:  # If corners are found
            # Refine corner detection
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        #Append object points and refined image points
            objpoints.append(objp)
            imgpoints.append(corners2)
            cv.drawChessboardCorners(img, (num_squares_width, num_squares_height), corners2, ret)
            cv.imwrite(os.path.join(success_path, f"{fname}"), img)
            cv.imshow('img', img)
            cv.waitKey(500)
            success_count += 1
        else:
            # Save the image to the failure path if corners are not found
            print(f"Chessboard not found in {img_path}")
            cv.imwrite(os.path.join(failure_path, f"{fname}"), img)
            failure_count += 1

# Print summary of image processing
print("\nProcessing Summary:")
print(f"Total Images Processed: {total_images}")
print(f"Successfully Processed: {success_count}")
print(f"Failed to Process: {failure_count}")
if success_count < 10:
    print("Total success less than 10. Calibration may be off. Retry image capture.")
# Cleanup windows
cv.destroyAllWindows()

# Perform camera calibration to obtain intrinsic parameters
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Save calibration results to pickle files
pickle.dump((mtx, dist), open(base_path+'/calibration.pkl', 'wb'))
pickle.dump(mtx, open(base_path+'/cameraMatrix.pkl', 'wb'))
pickle.dump(dist, open(base_path+'/dist.pkl', 'wb'))

# Print camera matrix (intrinsic parameters)
print(f"Camera Matrix: {mtx}")

# Calculate and print the mean re-projection error
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
    mean_error += error

print("Total error: {:.6f}".format(mean_error / len(objpoints)))