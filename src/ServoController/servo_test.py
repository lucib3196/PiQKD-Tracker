from gpiozero import AngularServo
from time import sleep

"""
This script demonstrates basic control of two servos using the GPIO Zero library.

Servos:
- Base Servo: Controls the base and oscillates between -90° and 90°.
- Upper Servo: Controls the upper section and oscillates between -45° and 45°.

How it works:
1. The script initializes two AngularServo objects, each tied to specific GPIO pins.
2. In an infinite loop, it moves the base servo and upper servo to their minimum and maximum angles with a delay.
3. Use this script to verify servo connections and test basic movement.

Note:
- Ensure the Raspberry Pi GPIO pins are properly connected to the servo's signal pin.
- Provide external power to the servos if needed, as GPIO pins cannot supply sufficient current for servos under load.
- If running this script over SSH, use `sudo` to ensure GPIO permissions.

Requirements:
- GPIO Zero library: Install it with `pip install gpiozero`
"""

# Initialize the base servo on GPIO pin 17 with a range from -90 to 90 degrees
base_servo = AngularServo(17, min_angle=-90, max_angle=90)

# Initialize the upper servo on GPIO pin 27 with a range from -45 to 45 degrees
upper_servo = AngularServo(27, min_angle=-90, max_angle=90)

# Infinite loop to test the servos
try:
    while True:
        # Move the base servo to its minimum angle (-90 degrees)
        base_servo.angle = -90
        print("Base servo set to -90 degrees")
        sleep(2)  # Wait for 2 seconds

        # Move the base servo to its maximum angle (90 degrees)
        base_servo.angle = 90
        print("Base servo set to 90 degrees")
        sleep(2)  # Wait for 2 seconds

        # Move the upper servo to its minimum angle (-45 degrees)
        upper_servo.angle = -90
        print("Upper servo set to -45 degrees")
        sleep(2)  # Wait for 2 seconds

        # Move the upper servo to its maximum angle (45 degrees)
        upper_servo.angle = 90
        print("Upper servo set to 45 degrees")
        sleep(2)  # Wait for 2 seconds

except KeyboardInterrupt:
    # Handle exit gracefully on Ctrl+C
    print("\nTest interrupted. Exiting...")