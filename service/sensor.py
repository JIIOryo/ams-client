import datetime
import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_sensor_config
from lib.mqtt import publish
from lib.topic import get_publish_topics

publish_topics = get_publish_topics()

def get_sensor_config_no_calibration():
    sensor_config = get_sensor_config()
    for sensor in sensor_config: del sensor['sensor']['calibration']
    return sensor_config


def publish_sensor_config():
    message = {
        "timestamp": int( datetime.datetime.now().strftime('%s') ),
        "sensors": get_sensor_config_no_calibration(),
    }
    publish(
        topic = publish_topics['SENSOR_CONFIG'],
        message = json.dumps(message),
        qos = 1,
        retain = True,
    )

