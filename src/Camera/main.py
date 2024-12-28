from .threaded_video_capture import thread_video_get

if __name__ == "__main__":
    """
    Main function to execute the threaded camera test.

    - Starts a threaded video stream.
    - Displays the live video with FPS overlay.
    - Provides a basic test to verify camera functionality and threading.
    """
    thread_video_get()