from can_utils import Computer
import time
import can

can_pkt = Computer("rpi0")
bus = can.interface.Bus('can0', interface='socketcan', bitrate=1000000, can_filters=can_pkt.get_filters())
can.Notifier(bus, [can_pkt.process_message])

while True:
    time.sleep(1)
