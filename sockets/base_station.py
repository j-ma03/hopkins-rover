# import socket
# import json
#
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('169.254.187.145', 8080))
#
# client.send(json.dumps({"imu":324234, "gps":324.432}).encode())
# from_server = client.recv(1024).decode()
# client.close()
# print(from_server)

import asyncio
import time
from websockets.sync.client import connect

def hello():
    with connect("ws://10.42.0.5:8765") as websocket:
        while True:
            websocket.send("Some data 123")
            message = websocket.recv()
            print(f"Received: {message}")
            time.sleep(1)

hello()