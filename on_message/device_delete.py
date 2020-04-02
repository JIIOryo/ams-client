import datetime
import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    SLACK_DELETE_DEVICE_NOTIFICATION_FORMAT,
    SLACK_NOTIFICATION_TYPE,
)
from commons.errors import (
    DeviceNotFound,
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
    "device_id": 1
}
"""

def device_delete(message):
    
    delete_device = json.loads(message)
    gpio_config = get_gpio_config()
    delete_device_id = delete_device['device_id']

    for device in gpio_config:
        if device['device_id'] == delete_device_id:

            if device['device'] == {}:
                raise DeviceNotFound('Device does not found.')
            
            deleted_device = device['device']
            
            # delete device_data
            device['device'] = {}
            break
    
    set_gpio_config(gpio_config)
    set_new_timer()
    publish_device_state()

    slack_post_text = SLACK_DELETE_DEVICE_NOTIFICATION_FORMAT.format(
        now = formated_str_now_date(),
        device_id = delete_device_id,
        name = deleted_device['name'],
        description = deleted_device['description'],
        type = deleted_device['type'],
        run_type = deleted_device['run_type'],
    )
    post_slack_by_type(
        text = slack_post_text,
        type = SLACK_NOTIFICATION_TYPE['NOTIFICATION']
    )
