from can_utils import Computer, ARBITRATION_ID
import time
import can
import random

can_pkt = Computer("rpi0")
bus = can.interface.Bus('can0', interface='socketcan', bitrate=1000000, filters=can_pkt.get_filters())

while True:
    can_pkt.send_message(bus, ARBITRATION_ID.SENSOR_PKT_0, sensor1=random.randint(0, 4096), sensor2=random.randint(0, 1048576))
    time.sleep(1)