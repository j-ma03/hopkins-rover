import qwiic_icm20948
import time
import math
import numpy

class IMU:
    def __init__(self):
        self.imu = qwiic_icm20948.QwiicIcm20948()
        self.rotation = [0, 0, 0] # x, y, z
        self.position = 0
        self.time = time.time()
        self.imu.begin()
    
    def read_data(self):
        if self.imu.dataReady():
            self.imu.getAgmt() # get data
            self.time = time.time() # get timestamp
            acc = [self.imu.axRaw, self.imu.ayRaw, self.imu.azRaw] # accel values
            gyro = [self.imu.gxRaw, self.imu.gyRaw, self.imu.gzRaw] # gyro values

            # roll, pitch, yaw
            self.rotation[0] = numpy.arctan2(math.radians(acc[1]), math.radians(acc[2] + 0.05 * acc[0]))
            self.rotation[1] = numpy.arctan2(math.radians(-acc[0]), math.radians(math.sqrt(acc[1]**2 + acc[2]**2)))

            # convert back to degrees
            for i in range(3):
                self.rotation[i] = math.degrees(self.rotation[i])

