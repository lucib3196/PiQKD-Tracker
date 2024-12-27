from datetime import datetime
from threading import Thread
import argparse
import cv2


class CountsPerSec:
    def __init__(self) -> None:
        self._start_time = None 
        self._num_occurrences  = 0
    def start(self):
        self._start_time = datetime.now()
        return self
    def increment(self):
        self._num_occurrences +=1
    def count_per_second(self):
        elapsed_time = (datetime.now() -self._start_time).total_seconds()
        return self._num_occurrences  / elapsed_time

def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame


def noThreading(source=0):
    cap = cv2.VideoCapture(source)
    cps = CountsPerSec().start()
    while True:
        grabbed, frame = cap.read()
        if not grabbed or cv2.waitKey(1) == ord("q"):
            break
        frame = putIterationsPerSec(frame, cps.count_per_second())
        cv2.imshow("Video", frame)
        cps.increment()
    
    
class VideoGet:
    def __init__(self,src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
    def start(self):
        Thread(target=self.get, args=()).start()
        return self
    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True
def threadVideoGet(source = 0):
    video_getter = VideoGet(source).start()
    cps = CountsPerSec().start()
    while True:
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break
        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.count_per_second())
        cv2.imshow("Video", frame)
        cps.increment()

class VideoShow:
    def __init__(self,frame=None):
        self.frame = frame
        self.stopped = False
    def start(self):
        Thread(target = self.show, args = ()).start()
        return self
    def show(self):
        while not self.stopped:
            cv2.imshow('Video',self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True
    def stop(self):
        self.stopped = True

def threadVideoShow(source=0):
    """
    Dedicated thread for showing video frames with VideoShow object.
    Main thread grabs video frames.
    """

    cap = cv2.VideoCapture(source)
    (grabbed, frame) = cap.read()
    video_shower = VideoShow(frame).start()
    cps = CountsPerSec().start()

    while True:
        (grabbed, frame) = cap.read()
        if not grabbed or video_shower.stopped:
            video_shower.stop()
            break

        frame = putIterationsPerSec(frame, cps.count_per_second())
        video_shower.frame = frame
        cps.increment()
def threadBoth(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.count_per_second())
        video_shower.frame = frame
        cps.increment()
threadBoth()