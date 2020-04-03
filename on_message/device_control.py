import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import DEVICE_TYPE
from lib.config import get_config, get_gpio_config
from lib.gpio import gpio_write

from service.device import publish_device_state

"""
# message 
type: json str
-----
{
    "devices": [
        {
            "device_id": 1,
            "state": false
        },
        {
            "device_id": 2,
            "state": true
        }
    ]
}
"""

def device_control(message):
    target_devices = json.loads(message)['devices']
    devices = get_gpio_config()

    for target_device in target_devices:
        target_device_id = target_device['device_id']
        next_state = target_device['state']

        for device in devices:
            if device['device_id'] == target_device_id:

                # feed pump should not be controlled by this function
                if device['device']['type'] == DEVICE_TYPE['FEED_PUMP']:
                    continue
                
                BCM = device['BCM']
                gpio_write(BCM, int(next_state))
                break
    
    publish_device_state()   
