# work in progress

"""
Tools that help organize how the rover, and it's different computers/motors
treat communicating with each other through CAN
"""

from enum import Enum
from dataclasses import dataclass
import math
from typing import List, Dict
import json

import can

"""
These are the arbitration ids for determining what CAN packet has what data
and establishes the priorities of each packet
"""
class ARBITRATION_ID(Enum):
    # for jetson computer general comms (may not be used)
    JETSON = 1

    # for raspberry pi general comms (may not be used)
    RPI_0 = 2
    RPI_1 = 3

    # for sensor data (could represent multiple sensors)
    # may not need this many and should probably change names to be more descriptive
    SENSOR_PKT_0 = 4
    SENSOR_PKT_1 = 5
    SENSOR_PKT_2 = 6
    SENSOR_PKT_3 = 7

    # movement motors on the rover
    ROVER_MOTOR_0 = 8
    ROVER_MOTOR_1 = 9
    ROVER_MOTOR_2 = 10
    ROVER_MOTOR_3 = 11
    ROVER_MOTOR_4 = 12
    ROVER_MOTOR_5 = 13

    # motors that move the arm
    ARM_MOTOR_0 = 14
    ARM_MOTOR_1 = 15
    ARM_MOTOR_2 = 16
    ARM_MOTOR_3 = 17
    ARM_MOTOR_4 = 18
    ARM_MOTOR_5 = 19


# defines some value in the data bits
@dataclass
class Sensor:
    id: str
    start_bit: int
    length: int
    parsed_data: int = None
    send_data: int = None

    # gets data based on bits the item exists in
    def get_data_from_bits(self, bits: int) -> int:
        # kinda a jeink way to generate the bitmask but apparently it's faster for 20+ bits
        self.parsed_data = (bits >> self.start_bit) & int("1" * self.length, base=2)
        return self.parsed_data

    def add_data_to_bits(self, bits: int, data: int) -> int:
        return bits | data << self.start_bit


@dataclass
class Sensor_Packet():
    arbitration_id: ARBITRATION_ID
    sensors: Dict[str, Sensor]
    size: int

# get arb id should also use value
# function to get data just given message
class Computer():
    def __init__(self, computer_id: str):
        self.computer_id = computer_id
        self.config = json.load(open("CAN_config.json", "r"))
        self.sensor_packets: Dict[int, Sensor_Packet] = {}

        for sensor_pkt in self.config["computers"][self.computer_id]:
            data = self.config["sensor_packets"][sensor_pkt]
            self.sensor_packets[ARBITRATION_ID[sensor_pkt].value] = Sensor_Packet(
                arbitration_id=ARBITRATION_ID[sensor_pkt],
                sensors={sensor: Sensor(
                    id=sensor,
                    start_bit=sensor_data["start_bit"],
                    length=sensor_data["length"]
                ) for sensor, sensor_data in data["sensors"].items()},
                size=data["size_of_packet"]
            )

    def populate_bits(self, AF_id: ARBITRATION_ID, sensor_name: str, bits: int, value: int) -> int:

        pkt = self.sensor_packets.get(AF_id.value)
        if pkt is None:
            raise KeyError(f"The config for this computer doesn't contain arbitration id: {AF_id}")

        sensor = pkt.sensors.get(sensor_name)
        if sensor is None:
            raise KeyError(f"The config for this computer doesn't contain sensor name: {sensor_name}")

        return sensor.add_data_to_bits(bits, value)

    def read_bits(self, AF_id: ARBITRATION_ID, sensor_name: str, bits: int) -> int:
        pkt = self.sensor_packets.get(AF_id.value)
        if pkt is None:
            raise KeyError(f"The config for this computer doesn't contain arbitration id: {AF_id}")

        sensor = pkt.sensors.get(sensor_name)
        if sensor is None:
            raise KeyError(f"The config for this computer doesn't contain sensor name: {sensor_name}")

        return sensor.get_data_from_bits(bits)

    def get_length(self, AF_id: ARBITRATION_ID) -> int:
        pkt = self.sensor_packets.get(AF_id.value)
        if pkt is None:
            raise KeyError(f"The config for this computer doesn't contain arbitration id: {AF_id}")

        return pkt.size

    """
    this bypasses integer overflow problems by just storing int as groups of 8 bits
    """
    def get_bytearray(self, AF_id: ARBITRATION_ID, bits: int) -> bytearray:
        bytes_in_bits: List[int] = []
        for byte in range(math.ceil(self.get_length(AF_id) / 8)):
            # get first 8 bits and shift the data to remove them
            bytes_in_bits.insert(0, bits & 0xFF)
            bits = bits >> 8

        return bytearray(bytes_in_bits)

    def get_filters(self) -> List[Dict[str, int]]:
        return [{"can_id": i, "can_mask": 0x7FF, "extended": False} for i in self.sensor_packets.keys()]

    """
    params:
    - the declared can.interface.Bus object
    - arbitration id for the packet you want to send
    - the sensors for the packet you want to send
    """
    def send_message(self, can_bus: can.interface.Bus, AF_id: ARBITRATION_ID, **kwargs) -> None:
        bits = 0
        for name, value in kwargs.items():
            sensor = self.sensor_packets[AF_id.value].sensors.get(name)
            if sensor is None:
                raise KeyError(f"The config for this computer doesn't contain sensor name: {name}")

            bits += sensor.add_data_to_bits(bits, value)

        can_bus.send(can.Message(arbitration_id=AF_id.value, data=self.get_bytearray(AF_id, bits)))

    def process_message(self, message: can.Message) -> None:
        arbitration_id: ARBITRATION_ID = ARBITRATION_ID(message.arbitration_id)

        recv_data: int = int.from_bytes(message.data, byteorder="big")
        return_data = {"arbitration_id": arbitration_id, "sensors": {}}

        for sensor in self.sensor_packets[arbitration_id.value].sensors.keys():
            return_data["sensors"][sensor] = self.read_bits(arbitration_id, sensor, recv_data)

        # we only use this function for jetson and I haven't decided how to implement that yet
        print(return_data)
