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

def define_camera_settings(camera_matrix_path,camera_distortion_path):
    with open(camera_matrix_path,"rb") as file:
        print(f'Debugging: {file}')
        camera_matrix = pickle.load(file)

    with open(camera_distortion_path, "rb") as dist_file:
        print(f'Debugging: {dist_file}')
        camera_distortion = pickle.load(dist_file)

    return camera_matrix, camera_distortion

CameraMatrixPath =r'\src\CameraCalibration\cameraMatrix.pkl'
CameraDistortionPath =r"\src\CameraCalibration\dist.pkl"
def load_camera_calibration():
    camera_matrix, camera_distortion_coefficients = define_camera_settings(os.getcwd()+CameraMatrixPath,os.getcwd()+CameraDistortionPath)
    return camera_matrix,camera_distortion_coefficients
