from gpiozero import Robot, Motor
import pygame
from pygame.locals import *
from time import sleep

# define motors of Robot - GPIO pins 7,8 for motor 1, and 10,9 for motor 2
# we did 10,9 instead of 9,10 because of how the motor is wired to the motor controller

motor_r = Motor(10, 9)
motor_l = Motor(7, 8)

pygame.init()
joystick = pygame.joystick.Joystick(0)


try:
    while True:
        pygame.event.pump()  # Ensure all events are processed

        # Read joystick axis values
        left_y_axis = -joystick.get_axis(1)
        right_x_axis = joystick.get_axis(2)

        # Calculate the directions each motor needs to turn
        # Moving the left joystick in the y-direction makes it move forward/backward
        # Moving the right in the x-direction makes it turn
        # This formula combines the two into values between 0 and 1
        right_dir = left_y_axis * 0.5 - right_x_axis * 0.5
        left_dir = left_y_axis * 0.5 + right_x_axis * 0.5

        # Stops the motor if the value is close to zero
        if (abs(right_dir) < 0.05):
            motor_r.stop()
        # Turns backward if the direction is negative
        elif right_dir < 0:
            motor_r.backward(-right_dir)
        # Turns forward if direction is positive
        else:
            motor_r.forward(right_dir)

        # Do the same for the left motor
        if (abs(left_dir) < 0.05):
            motor_l.stop()
        elif left_dir < 0:
            motor_l.backward(-left_dir)
        else:
            motor_l.forward(left_dir)


        sleep(0.1)  # Optional: Add a small delay to reduce CPU load
except KeyboardInterrupt:
    rover.stop()