import math
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device
Device.pin_factory = PiGPIOFactory()
from gpiozero import AngularServo
from time import sleep


# Initialize the base servo on GPIO pin 17 with a range from -90 to 90 degrees
base_servo = AngularServo(17,min_angle=-90,max_angle = 90)
t=0
while True:
    servo_angle = 45 * math.sin(2 * math.pi * 0.5 * t)
    base_servo.angle = servo_angle
    print(servo_angle)
    t += 0.1
    sleep(0.1)