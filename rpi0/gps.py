import serial
import pynmea2
from geopy.distance import geodesic 

class GPS:
    def __init__(self, port: str):
        # set up port to read from
        self.serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.5)  
        self.time = 0
        self.lon = 0
        self.lat = 0
        self.alt = 0

    def read_data(self):
        line = self.serialPort.readline().strip().decode("ascii")
        # get GPS fix data
        if line.find("GGA") > 0:    
            msg = pynmea2.parse(str)

        # time format: hr:min:sec in UTC; e.g. 12:30:29 -> 123029
        self.time = msg.timestamp
        # lat/lon format: deg, min; e.g. 40 degrees 7.122' -> 4007.122
        self.lon = msg.lon
        self.lat = msg.lat
        # meters above sea level
        self.alt = msg.altitude
    
    def calc_distance(self, other):
        loc = (self.lon, self.lat)
        # does not account for altitude
        dist = geodesic(loc, other).km
        return dist
