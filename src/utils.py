from math import dist
import cv2
import pickle
import os


def initialize_camera_feed(camera_index = 0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Unable to access camera with index {camera_index}")
        exit()
    return cap

CameraMatrixPath = "src/CameraCalibration/cameraMatrix.pkl"
CameraDistortionPath = "src/CameraCalibration/dist.pkl"

def load_camera_calibration():
    # Use os.path.join to construct file paths
    camera_matrix_path = os.path.join(os.getcwd(), CameraMatrixPath)
    camera_distortion_path = os.path.join(os.getcwd(), CameraDistortionPath)

    print(f"Camera matrix path: {camera_matrix_path}")  # Debugging
    print(f"Camera distortion path: {camera_distortion_path}")  # Debugging

    return define_camera_settings(camera_matrix_path, camera_distortion_path)

def define_camera_settings(camera_matrix_path, camera_distortion_path):
    # Load the camera calibration data
    with open(camera_matrix_path, "rb") as file:
        camera_matrix = pickle.load(file)

    with open(camera_distortion_path, "rb") as file:
        camera_distortion_coefficients = pickle.load(file)

    return camera_matrix, camera_distortion_coefficients
