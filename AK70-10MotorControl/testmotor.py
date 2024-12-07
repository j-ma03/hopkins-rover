import can
import time
import numpy as np

bus = can.interface.Bus(interface='socketcan', channel='can0', bitrate=1000000,)
class motor_listener(can.Listener):
    def __init__(   self, **kwargs) -> None:
        pass

    def on_message_received(self, msg: can.Message) -> None:
        b = bytes(msg.data)
        pos_int = np.int32(b[0] << 8 | b[1])
        spd_int = np.int32(b[2] << 8 | b[3])
        cur_int = np.int32(b[4] << 8 | b[5])
        motor_pos = float(pos_int * 0.1)  # motor position
        motor_spd = float(spd_int/21)  # motor speed
        motor_cur = float(cur_int * 0.01)  # motor current
        motor_temp = np.int16(b[6])  # motor temperature
        motor_error = b[7]
        print(msg.arbitration_id, msg.arbitration_id&0xFF, msg.data, motor_pos, motor_spd, motor_cur, motor_temp, motor_error)

    def stop(self) -> None:
        pass

listener = motor_listener()


print_listener = can.Printer()
CAN1_notifier = can.Notifier(bus, [listener])
msg = can.Message(
        arbitration_id=0x8,
        data = [ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0XFC],
        is_extended_id=True
        )
print("Send Start: ", msg)
msg = can.Message(
        arbitration_id=0x508,
        data = [0],
        is_extended_id=True
        )
print("Send Origin: ", msg)

bus.send(msg)

dt = .2
try:
    # for _ in range(10):
    #     msg = can.Message(
    #         arbitration_id=0x308,
    #         data = [0x00, 0x00, 0x03, 0xE8 ],
    #         is_extended_id=True
    #         )
    #     print("Send Speed: ", msg)
    #     bus.send(msg)
    #     time.sleep(dt)
    #
    # msg = can.Message(
    #     arbitration_id=0x208,
    #     data=[0x00, 0x00, 0xff, 0xff],
    #     is_extended_id=True
    # )
    # print("Send Brake: ", msg)
    # bus.send(msg)

    #0ABA9500 given 180
    #1B7740 actual 180
    #00 02 BF 20
    pos = [0x00, 0x02, 0xBF, 0x20]
    speed = [0x03, 0x88]
    acc = [0x01, 0x30]
    msg = can.Message(
            arbitration_id=0x608,
            data = pos + speed + acc,
            is_extended_id=True
        )
    print("Send S/Pos: ", msg)
    bus.send(msg)
    time.sleep(5)

    # pos = [0x00, 0x00, 0xB9, 0xB0]
    # speed = [0x03, 0x88]
    # acc = [0x01, 0x30]
    # msg = can.Message(
    #         arbitration_id=0x408,
    #         data = pos,
    #         is_extended_id=True
    #     )
    # print("Send S/Pos: ", msg)
    # bus.send(msg)
    # time.sleep(5)
    time.sleep(10)
except KeyboardInterrupt:
    pass


msg = can.Message(
    arbitration_id=0x8,
    data = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0XFD],
    is_extended_id=True
    )
print("Send Shutdown: ", msg)
bus.send(msg)
