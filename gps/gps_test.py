import serial
import pynmea2
from gps import GPS

# port = "/dev/ttyS0" 
port = "/dev/ttyACM0" # USB port (supposedly)
gps = GPS(port)

while True:
   gps.read_data()
   print(f'Time: {gps.time}\tLongitude: {gps.lon}\tLatitude: {gps.lat}\tAltitude: {gps.alt}')
