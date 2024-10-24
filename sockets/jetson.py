# import socket
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(('169.254.187.150', 8080))
#
# server.listen(5)
# while True:
#     conn, addr = server.accept()
#     from_client = ""
#     while True:
#         data = conn.recv(1024)
#         if not data: break;
#         from_client += data.decode("utf-8")
#         print(from_client)
#         conn.send("test from server".encode("utf-8"))
#     conn.close()

import asyncio

import websockets
from websockets.asyncio.server import serve

def seabreeze(data: websockets.):

async def process_message(websocket):
    async for message in websocket:


async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever

asyncio.run(main())