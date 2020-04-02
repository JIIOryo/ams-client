import datetime
import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    SLACK_CREATE_DEVICE_NOTIFICATION_FORMAT,
    SLACK_NOTIFICATION_TYPE,
    DEVICE_TYPE,
    DEVICE_RUN_TYPE,
)
from commons.errors import (
    DeviceAlreadyExist,
    DeviceTypeUndefined,
    DeviceRunTypeUndefined,
)

from lib.config import get_config, get_gpio_config, set_gpio_config
from lib.gpio import gpio_write
from lib.notification import post_slack_by_type
from lib.util import formated_str_now_date

from service.device_state import publish_device_state
from service.timer import set_new_timer

"""
# message 
type: json str
-----
{
    "device_id": 1,
    "name": "My main light",
    "description": "This is my main light!",
    "type": "main_light",
    "run_type": "daily",
    "options": {
        "timer": {
            "on_hour": 10,
            "on_minute": 30,
            "off_hour": 17,
            "off_minute": 30
        } 
    }
}
"""

def device_create(message):
    new_device = json.loads(message)

    if new_device['type'] not in DEVICE_TYPE.values():
        raise DeviceTypeUndefined('This device type is undefined.')
    
    if new_device['run_type'] not in DEVICE_RUN_TYPE.values():
        raise DeviceRunTypeUndefined('This run type is undefined.')
    
    gpio_config = get_gpio_config()
    new_device_id = new_device['device_id']

    for device in gpio_config:
        if device['device_id'] == new_device_id:

            if device['device']:
                raise DeviceAlreadyExist('This device id is already used.')
            
            device['device'] = {
                'name': new_device['name'],
                'description': new_device['description'],
                'type': new_device['type'],
                'run_type': new_device['run_type'],
                'options': new_device['options'],
                'created_at': int( datetime.datetime.now().strftime('%s') ),
                'updated_at': int( datetime.datetime.now().strftime('%s') ),
            }
            break

    set_gpio_config(gpio_config)
    set_new_timer()
    publish_device_state()

    slack_post_text = SLACK_CREATE_DEVICE_NOTIFICATION_FORMAT.format(
        now = formated_str_now_date(),
        device_id = new_device_id,
        name = new_device['name'],
        description = new_device['description'],
        type = new_device['type'],
        run_type = new_device['run_type'],
    )
    post_slack_by_type(
        text = slack_post_text,
        type = SLACK_NOTIFICATION_TYPE['NOTIFICATION']
    )
