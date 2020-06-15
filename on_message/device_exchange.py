import datetime
import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )


# from commons.errors import (
#     # DeviceNotFound,
# )
from commons.consts import (
    SLACK_NOTIFICATION_TYPE,
)

from lib.config import get_config, get_gpio_config, set_gpio_config
from lib.notification import post_slack_by_type

from service.device import publish_device_state
from service.timer import set_new_timer

"""
input
A: [6, 4, 5, 2, 3, 1]
B: [
    {"device_id":1, "BCM": 26, "name":"a", other keys1 ...},
    {"device_id":2, "BCM": 24, "name":"b", other keys2 ...},
    {"device_id":3, "BCM": 23, "name":"c", other keys3 ...},
    {"device_id":4, "BCM": 19, "name":"d", other keys4 ...},
    {"device_id":5, "BCM": 18, "name":"e", other keys5 ...},
    {"device_id":6, "BCM": 14, "name":"f", other keys6 ...}
]

output
X: [
    {"device_id":1," "BCM": 26, name":"f", other keys6 ...},
    {"device_id":2," "BCM": 24, name":"d", other keys4 ...},
    {"device_id":3," "BCM": 23, name":"e", other keys5 ...},
    {"device_id":4," "BCM": 19, name":"b", other keys2 ...},
    {"device_id":5," "BCM": 18, name":"c", other keys3 ...},
    {"device_id":6," "BCM": 14, name":"a", other keys1 ...}
]
"""
def exchanged(A: list, B: list) -> list:
    only_exchanged, result = [dict(B[a-1]) for a in A], []
    for i, o in enumerate(only_exchanged):
        o.update(device_id = i+1, BCM = B[i]['BCM'])
        result.append(o)
    return result

"""
# message 
type: json str
-----
{
    "devices": [1, 2, 3, 6, 4, 5]
}
"""

def device_exchange(message: dict) -> None:
    exchange_devices = json.loads(message)['devices']
    gpio_config = get_gpio_config()

    result = exchanged(exchange_devices, gpio_config)
    
    set_gpio_config(result)
    set_new_timer()
    publish_device_state()

    post_slack_by_type(
        text = 'Devices are exchanged.',
        type_ = SLACK_NOTIFICATION_TYPE['NOTIFICATION']
    )
