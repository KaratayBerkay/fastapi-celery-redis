import datetime
import json
import random
import socket
import sys
import time
import uuid

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print(sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)


def send_device_info(send_data):
    try:
        message_body = json.dumps(send_data)
        print(sys.stderr, 'sending "%s"' % message_body)
        sock.sendall(message_body.encode())

        amount_received = 0
        amount_expected = len(message_body)
        data_string = ""
        data_json = {}

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            data_string += data.decode()

        try:
            with open('received.json', 'r') as f:
                data_json = json.loads(f.read() or data_json)
        except Exception as e:
            print(e)

        with open('received.json', 'w') as f:
            data_json[datetime.datetime.now().__str__()] = data_string
            f.write(json.dumps(data_json, indent=2))
    except Exception as e:
        print(e)
        sock.close()


for i in range(250):
    device_info = {
        "device_id": uuid.uuid4().__str__(),
        "device_name": f"device_{i}",
        "device_type": "device_type",
        "device_model": "device_model",
        "device_serial": "device_serial",
        "device_location": f"{random.randint(100, 999)}, {random.randint(100, 999)}",
        "device_status": "device_status"
    }
    send_device_info(send_data=device_info)
