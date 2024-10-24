# CAN Stuff

## References
[Can Frame](https://embedclogic.com/can-protocol/standard-can-vs-extended-can-protocol-frame/) - how the bits are
 organized in the frame

[Cubemars python library](https://pypi.org/project/TMotorCANControl/) - for controlling the motor

[General python CAN library](https://python-can.readthedocs.io/en/stable/index.html) - for all other data

[Setup + code for specific CAN rpi hat we are using](https://www.waveshare.com/wiki/RS485_CAN_HAT)

## Using `can_utils`

### Setup
Make sure to run the command
```bash
python3 -m pip install -r requirements.txt
```

### Arbitration IDs
These are the ids that set the priority for CAN packets. Each sensor packet, motor, and computer has one of these.

*Note: we might not need the computer ones at all - we'll figure that out as we decide sensor readings (hopefully soon)*

#### Usage

```python
from CAN.can_utils import ARBITRATION_ID

# reference type of arbitration id (type ARBITRATION_ID)
ARBITRATION_ID.SENSOR_PKT_0 # = ARBITRATION_ID.SENSOR_PKT_0

# reference value of arbitration id (int)
ARBITRATION_ID.SENSOR_PKT_0.value # = 4
```

### Storing/Reading bits

Consider a 16 bit data section

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

If we want to dedicate the first byte to sensor **k** and the second byte to sensor **j**.

Let **k** = `247` or `11110111` in binary, and **j** = `132` or `10000100` in binary.
When we set the LSB byte to **k** and the second byte to **j** we get:

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | <- **j** | **k** -> | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|----------|----------|---|----|----|----|---|----|----|---|
| 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |          |          | 1 | 1  | 1  | 1  | 0 | 1  | 1  | 1 |

Which will then be represented as `1000010011110111` in binary. The next step is to convert it to a bytestring that can be used by the  `python-can` library.
calling `can_pkt.get_bytearray(<Arbitration id for packet>, <bits to convert>)` will accomplish this. There are a few reasons why we use this instead of just calling `bytestring(bits)` so if you're interested just reach out to me.

It will not always be as clean as 8 bits per number (that's why this library exists lol) but the total number of bits will always have to be a multiple of 8 since that is how data is explained in CAN protocol (DLC bits).
The max size is 64 bits I'm decently sure.

### Configuration

```json
{
  // this section configures what sensor packets need to be loaded for what computers
  // I'm still deciding how I will add implementation of motor stuff here
  "computers": {
    "jetson": [

    ],
    "rpi0": [
      "SENSOR_PKT_0"
    ],
    "rpi1": [

    ]
  },
  // the sets of sensors that we want to send in one packet - add more with the same style
  // we can change the name of these at some point
  "sensor_packets": {
    "SENSOR_PKT_0": {
      "sensors": { // sensors that are in the packet
        "sensor1": {
          "start_bit": 20, // where to start the bits of this sensor with lsb being bit 0
          "length": 12 // how many bits to dedicate to this sensor value
        },
        "sensor2": {
          "start_bit": 0,
          "length": 20
        }
      },
      "size_of_packet": 32 // total size of packet
    }
  }
}
```

### Example

#### Sending Data
```python
import can # not used here but you will need to import it at some point
from CAN.can_utils import ARBITRATION_ID, Computer

bus = can.interface.Bus("can0", interface='socketcan', bitrate=1e9)
# initialization of this computer
can_pkt = Computer("rpi0")

# Sending
can_pkt.send_message(bus, ARBITRATION_ID.SENSOR_PKT_0, sensor1=3239, sensor2=23222)
```

#### Receiving Data
```python
from CAN.can_utils import Computer
import can
import time

can_pkt = Computer("rpi0")
bus = can.interface.Bus('can0', interface='socketcan', bitrate=1000000, filters=can_pkt.get_filters())

# set the notifier to call process message when we get data
can.Notifier(bus, [can_pkt.process_message])

while True:
    # keeping program running
    time.sleep(1)
```
