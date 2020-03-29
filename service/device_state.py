import datetime
import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_gpio_config
from lib.gpio import gpio_read
from lib.mqtt import publish
from lib.topic import get_publish_topics

publish_topics = get_publish_topics()

def get_all_device_state():
    devices = get_gpio_config()
    all_device_state = []
    for device in devices:
        if device['device']:
            all_device_state.append({
                'device_id': device['device_id'],
                'state': gpio_read(device['BCM']),
                'name': device['device']['name'],
                'description': device['device']['description'],
                'type': device['device']['type'],
                'options': device['device']['options'],
                'created_at': device['device']['created_at'],
                'updated_at': device['device']['updated_at'],
            })
    return all_device_state

def publish_device_state():
    message = {
        "timestamp": int( datetime.datetime.now().strftime('%s') ),
        "devices": get_all_device_state(),
    }
    publish(
        topic = publish_topics['DEVICE_STATE'],
        message = json.dumps(message),
        qos = 1,
        retain = True,
    )

