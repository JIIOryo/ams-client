import datetime
import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    SENSOR_TYPE,
    SLACK_CREATE_SENSOR_NOTIFICATION_FORMAT,
    SLACK_NOTIFICATION_TYPE,
)
from commons.errors import (
    SensorAlreadyExist,
    SensorTypeNotExist,
)

from lib.config import get_sensor_config, set_sensor_config
from lib.notification import post_slack_by_type
from lib.util import formated_str_now_date


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

def sensor_create(message):
    new_sensor = json.loads(message)
    sensor_config = get_sensor_config()

    new_sensor_id = new_sensor['sensor_id']

    for sensor in sensor_config:
        if sensor['sensor_id'] == new_sensor_id:

            # Sensor already exists.
            if sensor['sensor']:
                raise SensorAlreadyExist('Sensor already exists.')
            
            # This sensor type does not exist.
            if new_sensor['type'] not in SENSOR_TYPE.values():
                raise SensorTypeNotExist('This sensor type does not exist.')
            
            sensor['sensor'] = {
                'name': new_sensor['name'],
                'description': new_sensor['description'],
                'type': new_sensor['type'],
                'calibration': [],
                'created_at': int( datetime.datetime.now().strftime('%s') ),
                'updated_at': int( datetime.datetime.now().strftime('%s') ),
            }
            break
    
    set_sensor_config(sensor_config)

    slack_post_text = SLACK_CREATE_SENSOR_NOTIFICATION_FORMAT.format(
        now = formated_str_now_date(),
        sensor_id = new_sensor_id,
        name = new_sensor['name'],
        description = new_sensor['description'],
        type = new_sensor['type']
    )
    post_slack_by_type(
        text = slack_post_text,
        type = SLACK_NOTIFICATION_TYPE['NOTIFICATION']
    )
