import datetime
import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    SLACK_DELETE_SENSOR_NOTIFICATION_FORMAT,
    SLACK_NOTIFICATION_TYPE,
)
from commons.errors import (
    SensorNotFound,
)

from lib.config import get_sensor_config, set_sensor_config
from lib.notification import post_slack_by_type
from lib.util import formated_str_now_date

from service.sensor import publish_sensor_config

"""
# message 
type: json str
-----
{
  "sensor_id": 1,
}
"""

def sensor_delete(message):
    delete_sensor = json.loads(message)
    sensor_config = get_sensor_config()

    delete_sensor_id = delete_sensor['sensor_id']

    for sensor in sensor_config:
        if sensor['sensor_id'] == delete_sensor_id:

            # Sensor does not found.
            if sensor['sensor'] == {}:
                raise SensorNotFound('Sensor does not found.')
            
            deleted_sensor = sensor['sensor']
               
            sensor['sensor'] = {}
            break
    
    set_sensor_config(sensor_config)

    slack_post_text = SLACK_DELETE_SENSOR_NOTIFICATION_FORMAT.format(
        now = formated_str_now_date(),
        sensor_id = delete_sensor_id,
        name = deleted_sensor['name'],
        description = deleted_sensor['description'],
        type_ = deleted_sensor['type']
    )
    post_slack_by_type(
        text = slack_post_text,
        type_ = SLACK_NOTIFICATION_TYPE['NOTIFICATION']
    )

    publish_sensor_config()
