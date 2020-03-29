import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config, get_gpio_config
from lib.gpio import gpio_write

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
    gpio_config = get_gpio_config()

    for target_device in target_devices:
        target_device_id = target_device['device_id']
        next_state = target_device['state']

        for device in gpio_config:
            if device['device_id'] == target_device_id:
                BCM = device['BCM']
                gpio_write(BCM, int(next_state))
                break
    
    # publish_device_state()   
