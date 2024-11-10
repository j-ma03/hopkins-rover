import time
from imu import IMU

imu = IMU()

while True:
    time.sleep(1)
    imu.read_data()
    if imu.rotation[0] > 45 or imu.rotation[1] > 45 or imu.rotation[2] > 45:
        print("we are in trouble")
    print(f'X: {imu.rotation[0]}\tY: {imu.rotation[1]}\tZ: {imu.rotation[2]}')
