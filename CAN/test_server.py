from CAN.can_utils import Computer, ARBITRATION_ID
import time
import can
import random

can_pkt = Computer("rpi0")
bus = can.interface.Bus(channel='socketcan', interface='can0', bitrate=1000000, can_filters=can_pkt.get_filters())

while True:
    bits = 0
    can_pkt.populate_bits(ARBITRATION_ID.SENSOR_PKT_0, "sensor 1", bits, random.randint(0, 4096))
    can_pkt.populate_bits(ARBITRATION_ID.SENSOR_PKT_0, "sensor 2", bits, random.randint(0, 1048576))
    msg = can.Message(arbitration_id=can_pkt.sensor_packets[0].arbitration_id.value,
                      data=can_pkt.get_bytearray(ARBITRATION_ID.SENSOR_PKT_0, bits), is_extended_id=False)

    bus.send(msg)
    time.sleep(1)