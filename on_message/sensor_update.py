import datetime
import json
import sys
from typing import List

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    SENSOR_TYPE,
    SLACK_UPDATE_SENSOR_NOTIFICATION_FORMAT,
    SLACK_NOTIFICATION_TYPE,
)
from commons.errors import (
    SensorNotFound,
    SensorTypeNotExist,
)

from lib.config import get_sensor_config, set_sensor_config
from lib.notification import post_slack_by_type
from lib.util import formated_str_now_date

from service.sensor import publish_sensor_config, calibration_format

"""
# message 
type: json str
-----
{
  "sensor_id": 1,
  "name": "name",
  "description": "my description",
  "type": "water_temperature"
}
"""

def sensor_update(message: str) -> None:
    update_sensor = json.loads(message)
    sensor_config = get_sensor_config()

    update_sensor_id = update_sensor['sensor_id']

    for sensor in sensor_config:
        if sensor['sensor_id'] == update_sensor_id:

            # Sensor does not found.
            if sensor['sensor'] == {}:
                raise SensorNotFound('Sensor does not found.')
            
            # This sensor type does not exist.
            if update_sensor['type'] not in SENSOR_TYPE.values():
                raise SensorTypeNotExist('This sensor type does not exist.')

            before_sensor = dict(sensor['sensor'])
            
            sensor['sensor']['name'] = update_sensor['name']
            sensor['sensor']['description'] = update_sensor['description']
            sensor['sensor']['type'] = update_sensor['type']
            sensor['sensor']['updated_at'] = int( datetime.datetime.now().strftime('%s') )
            break
    
    set_sensor_config(sensor_config)

    slack_post_text = SLACK_UPDATE_SENSOR_NOTIFICATION_FORMAT.format(
        now = formated_str_now_date(),
        sensor_id = update_sensor_id,
        before_name = before_sensor['name'],
        before_description = before_sensor['description'],
        before_type = before_sensor['type'],
        after_name = update_sensor['name'],
        after_description = update_sensor['description'],
        after_type = update_sensor['type'],
    )
    post_slack_by_type(
        text = slack_post_text,
        type_ = SLACK_NOTIFICATION_TYPE['NOTIFICATION']
    )

    publish_sensor_config()

"""
# message 
type: json str
-----
{
  "calibration": [[1900, 21], [1910, 21.3], [2010, 23.8]]
}
"""

def sensor_calibration_update(sensor_id: int, calibration: List[List[int]]) -> None:
    sensor_config = get_sensor_config()

    for sensor in sensor_config:
        if sensor['sensor_id'] == sensor_id:

            # Sensor does not found.
            if sensor['sensor'] == {}:
                raise SensorNotFound('Sensor does not found.')

            before_sensor = dict(sensor['sensor'])
            
            sensor['sensor']['calibration'] = calibration_format(calibration)
            break
    
    set_sensor_config(sensor_config)

    publish_sensor_config()