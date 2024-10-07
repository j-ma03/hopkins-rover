# work in progress

"""
Tools that help organize how the rover, and it's different computers/motors
treat communicating with each other through CAN
"""

from enum import Enum
from dataclasses import dataclass

"""
These are the arbitration ids for determining what CAN packet has what data
and establishes the priorities of each packet
"""
class ARBITRATION_IDS(Enum):
    # for jetson computer general comms (may not be used)
    JETSON = 1

    # for raspberry pi general comms (may not be used)
    RPI_0 = 2
    RPI_1 = 3

    # for sensor data (could represent multiple sensors)
    # may not need this many
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


# defines some value in the data bits
@dataclass
class FormatItem:
    id: str
    start_bit: int
    length: int
    parsed_data: int = None

    # gets data based on bits the item exists in
    def get_data_from_bits(self, bits: int) -> int:
        #
        self.parsed_data = (bits >> self.start_bit) & int("1" * self.length, base=2)
        return self.parsed_data

# do we want to include a function that simplifies the can library or is this nearly enough?

if __name__ == "__main__":
    # some testing stuff, will be removed
    item = FormatItem("some value", 10, 10)
    print(item.get_data_from_bits(0b0010011001001001))
