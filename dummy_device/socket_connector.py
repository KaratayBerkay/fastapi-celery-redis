import json
import random
import socket
import sys


def send_device_info(send_data, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = host, port
    print(sys.stderr, 'connecting to %s port %s' % server_address)
    sock.connect(server_address)
    try:
        message_body = f"<->" + json.dumps(send_data) + f"<+>"
        sock.sendall(message_body.encode())

        amount_received = 0
        amount_expected = len(message_body)
        data_string = ""

        while amount_received < amount_expected:
            data = sock.recv(32)
            amount_received += len(data)
            data_string += data.decode()
    except Exception as e:
        print(e)
        sock.close()


def iter_device_location(host: str, port: int, r: int = 1, device_id=None):
    for i in range(r):
        device_info = {
            "device_id": device_id,
            "device_location": f"{random.randint(100, 999)}, {random.randint(100, 999)}",
        }
        send_device_info(send_data=device_info, host=host, port=port)
