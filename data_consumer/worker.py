import os
import json
import time
from celery import Celery
from models import Devices, DevicesHistory

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')


celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='tasks.location')
def send_location(data) -> dict:
    time.sleep(1)
    print(f"Received data {data}")
    data = json.loads(data)
    device_id = data.get("device_id"),
    device_location = data.get("device_location")
    print(f"Device {device_id} is at {device_location}")

    if send_device := Devices.filter(
        Devices.device_id == device_id
    ).first():
        device_history = DevicesHistory()
        device_history.device_id = send_device.device_id,
        device_history.device_location = device_location
        send_device.device_last_location = device_location
        send_device.save()
        send_device.history.append(device_history)
        device_history.save()
        return {
            "message": "Device location updated",
            "device": send_device.device_id,
            "location": send_device.device_last_location
        }

    raise Exception("Device not found")
