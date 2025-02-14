import gevent
from imu import IMU
from gps import GPS

imu = IMU()
gps = GPS("/dev/ttyUSB0")
imu_data = open("imu_data.txt", "w+")
gps_data = open("gps_data.txt", "w+")    

def get_imu_data():
    imu.read_data()
    imu_data.write(f'{imu.rotation[0]},{imu.rotation[1]},{imu.rotation[2]}')

def get_gps_data():
    gps.read_data()
    gps_data.write(f'{gps.time},{gps.lon},{gps.lat},{gps.alt}')

try:
    while True:
        gevent.joinall(
	    gevent.spawn(get_imu_data),
	    gevent.spawn(get_gps_data)
        )
except:
    imu_data.close()
    gps_data.close()
