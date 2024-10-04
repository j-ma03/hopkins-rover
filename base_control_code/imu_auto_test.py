#UNTESTED

import os
import sys
from time import sleep
import smbus
from gpiozero import Robot, Motor

from imusensor.MPU9250 import MPU9250

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

rover = Robot(left = (7,8), right = (10, 9))

try:
    while True:
        rover.forward()
        sleep(3)
        imu.readSensor()
        imu.computeOrientation()
        angle = imu.yaw
        while imu.yaw - angle < 89.9:
            imu.readSensor()
            imu.computeOrientation()
            rover.right()
        sleep(0.1)
except KeyboardInterrupt:
    rover.stop()