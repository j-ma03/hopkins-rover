import time
from imu import IMU

imu = IMU()

while True:
    time.sleep(1)
    imu.read_data()
    print(f'X: {imu.rotation[0]}\tY: {imu.rotation[1]}\tZ: {imu.rotation[2]}')
