# from evdev import InputDevice, ecodes
from gpiozero import Motor, PWMOutputDevice, AngularServo
import cv2
import asyncio
from time import sleep


servo = AngularServo(17)

while True:
    servo.min()
    sleep(2)
    servo.mid()
    sleep(2)
    servo.max()
    sleep(2)