import qwiic_icm20948

class IMU:
    def __init__(self):
        self.imu = qwiic_icm20948.QwiicIcm20948()
        self.rotation = [0, 0, 0] # x, y, z
        self.position = 0
        self.time = 0
        self.imu.begin()
    
    def read_data(self):
        if self.imu.dataReady():
            self.imu.getAgmt()
            # will change stuff below later 
            self.rotation[0] = self.imu.axRaw
            self.rotation[1] = self.imu.ayRaw
            self.rotation[2] = self.imu.azRaw
