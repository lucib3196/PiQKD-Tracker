import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import time
import numpy as np

# Global variables for communication between threads
position_data = []
time_data = []
running = True

def update_plot(i):
    """Function to update the Matplotlib plot."""
    plt.cla()
    plt.plot(time_data, position_data, label='Position vs. Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Position')
    plt.legend(loc='upper left')

def video_capture():
    """Function to capture video frames and simulate position data."""
    global running
    cap = cv2.VideoCapture(0)  # Open the default camera
    start_time = time.time()

    while running:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Display the video frame
        cv2.imshow("Video Frame", frame)

        # Simulate position data (example: moving sinusoidal signal)
        current_time = time.time() - start_time
        position = 10 * np.sin(current_time)
        
        # Update the data
        time_data.append(current_time)
        position_data.append(position)

        # Limit the size of the data to avoid memory issues
        if len(time_data) > 100:
            time_data.pop(0)
            position_data.pop(0)

        # Check for exit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

    cap.release()
    cv2.destroyAllWindows()

# Start the video capture in a separate thread
video_thread = threading.Thread(target=video_capture)
video_thread.start()

# Set up the Matplotlib animation
fig, ax = plt.subplots()
ani = FuncAnimation(fig, update_plot, interval=100)

# Show the plot (blocking call)
plt.show()

# Wait for the video thread to finish
video_thread.join()
