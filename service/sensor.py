import datetime
import json
import sys
import time

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.color import Color, color_text, print_color_log
from commons.consts import (
    LOG_TITLE,
)

from lib.config import get_sensor_config, get_config_item, get_root_path
from lib.mcp import read_mcp
from lib.mqtt import publish
from lib.topic import get_publish_topics
from lib.util import least_squares

publish_topics = get_publish_topics()
ams_root_path = get_root_path()
current_sensor_value_file_path = '/'.join([ams_root_path, 'log', 'current_sensor_value.json'])


def get_sensor_config_no_calibration() -> dict:
    sensor_config = get_sensor_config()
    for sensor in sensor_config:
        if sensor['sensor']:
            del sensor['sensor']['calibration']
    return sensor_config


def publish_sensor_config() -> None:
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

def get_current_sensor_values() -> str:
    with open(current_sensor_value_file_path) as f:
        current_sensor_values = json.load(f)
    return current_sensor_values

def write_current_sensor_values(sensor_data_json: str) -> None:
    with open(current_sensor_value_file_path, 'w') as f:
        f.write(sensor_data_json)

def publish_sensor_data() -> None:

    sensing_config = get_config_item('SENSING')
    sensor_data_publish_period = sensing_config['SENSOR_DATA_PUBLISH_PERIOD']
    sensing_number = sensing_config['SENSING_NUMBER']
    sensor_config = get_sensor_config()

    total_value = {}
    for sensor in sensor_config:
        # if a sensor exists
        if sensor['sensor']: total_value[sensor['sensor_id']] = 0

    for _ in range(sensing_number):
        for sensor_id in total_value.keys():
            sensor_value = read_mcp(sensor_id)
            total_value[sensor_id] += sensor_value
        time.sleep(sensor_data_publish_period / sensing_number)

    publish_data = {
        "timestamp": int( datetime.datetime.now().strftime('%s') ),
        "sensors": [],
    }

    for sensor in sensor_config:
        # if a sensor does not exists
        if sensor['sensor'] == {}:
            continue

        # Least squares coefficients
        if sensor['sensor']['calibration']:
            a, b = least_squares( sensor['sensor']['calibration'] )
        else:
            # use raw value
            a, b = 1, 0

        publish_data['sensors'].append({
            "sensor_id": sensor['sensor_id'],
            "name": sensor['sensor']['name'],
            "type": sensor['sensor']['type'],
            "value": round( a * total_value[sensor['sensor_id']] / sensing_number + b, 2),
        })
    

    publish_topic = publish_topics['SENSOR_DATA'] 
    publish_data_json = json.dumps(publish_data)

    write_current_sensor_values(publish_data_json)

    publish(
        topic = publish_topic,
        message = publish_data_json,
        qos = 0,
        retain = True,
    )

    print_color_log(
        title = LOG_TITLE['SENSOR'],
        title_color = Color.YELLOW,
        text = '{unixtime}: {topic}: {message}'.format(
            unixtime = datetime.datetime.now().strftime('%s'),
            topic = color_text(publish_topic, Color.GREEN),
            message = publish_data_json,
        )
    )
    
    
