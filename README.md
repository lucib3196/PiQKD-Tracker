# QKD Senior Design

## Getting Started


1. **Create a virtual environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install required packages

```bash
pip install -r requirements.txt
```

Thought for a couple of seconds



## Project Structure

### Camera System

Modules for capturing and streaming images/video from PiCamera2 or USB webcams.

* `capture_image_pi`
  Capture a single image with the Raspberry Pi Camera.
* `calibration_image_capture`
  Grab frames for calibration from USB or PiCamera (save with `s`/`c`, exit with `Esc` or `q`).
* `calibration.py`
  Process calibration images → compute camera matrix & distortion coeffs → save pickle files & report.
* `pi_streamtest`
  Serve raw PiCamera video over HTTP via Flask.
* `camera_streamer`
  Load calibration data, undistort PiCamera frames, and stream via Flask.

> **Deprecated**
>
> * `threaded_video_capture` – legacy webcam capture with FPS overlay.

### Face Tracking

Real-time face detection and streaming through Flask.

* `picamera_facedetection`
  Detect faces on PiCamera feed, overlay annotations, and stream over HTTP.

### Servo Control

Scripts for testing pan-tilt servos.

* `servo_test`
  Move servos to their min/max angles.
* `servo_test2`
  Sweep servos continuously between endpoints.

### ARuco Marker Detection

Detect ARuco markers, apply PID pan-tilt control, and log data.

* `vs_motion`
  Stream video, use PID to adjust pan/tilt for marker tracking, log errors to CSV.
* `full_tracking_usb` *(legacy)*
  USB-camera ARuco tracking + pan/tilt PID + CSV logging.
* `utils`
  Helper functions for marker detection, ID lookup, and pose estimation.

### PID Control

Generic PID controller for motion and servo adjustments.

* `PID`
  Class implementing Kp/Ki/Kd control loops.

---

## Wiring Guide

* **Pan servo** → GPIO17 (pin 11)
* **Tilt servo** → GPIO13 (pin 13)
* **Ground** → Pin 9
* **Camera** → PiCamera port
* **Power supply** → DC supply to servos

---

## Resources

* [gpiozero documentation](https://gpiozero.readthedocs.io/en/stable/)
* [OpenCV](https://opencv.org/)

```

