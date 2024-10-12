from CAN.can_utils import Computer, ARBITRATION_ID
import time
import can

can_pkt = Computer("rpi0")
bus = can.interface.Bus(channel='socketcan', interface='can0', bitrate=1000000, can_filters=can_pkt.get_filters())

while True:
    msg = bus.recv()

    d = can_pkt.process_message(msg)
    print(d)

    time.sleep(1)
