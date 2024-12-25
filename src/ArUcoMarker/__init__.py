from ..utils import initialize_camera_feed, define_camera_settings
import os

camera_matrix_path = r"\src\camera_calibration\cameraMatrix.pkl"
camera_distortion_path = r"\src\camera_calibration\dist.pkl"

camera_matrix, camera_distortion_coefficients = define_camera_settings(os.getcwd()+camera_matrix_path,os.getcwd()+camera_distortion_path)