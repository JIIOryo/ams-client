import json
import os
import subprocess
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    DEVICE_TYPE,
)
from commons.errors import (
    DeviceNotFound,
    DeviceOtherError,
)
from lib.config import get_gpio_config, get_root_path
from service.feed_pump import feed_pump

"""
# message 
type: json str
-----
{
    "device_id": 1,
    "water_supply_time": 30
}
"""

def device_feed_pump(message: dict) -> None:
    feed_pump_action = json.loads(message)
    
    devices = get_gpio_config()
    target_device_id = feed_pump_action['device_id']

    for device in devices:
        if device['device_id'] == target_device_id:

            if device['device'] == {}:
                raise DeviceNotFound('Device does not found.')

            if device['device']['type'] != DEVICE_TYPE['FEED_PUMP']:
                raise DeviceOtherError('This is not feed pump.')
            
            ams_root_path = get_root_path()
            entry_point = '/'.join([ams_root_path, 'entry_points', 'feed_pump.py'])
            cmd = 'python3 {entry_point} {device_id} {water_supply_time}'.format(
                entry_point = entry_point,
                device_id = target_device_id,
                water_supply_time = feed_pump_action['water_supply_time'],
            )
            subprocess.Popen(cmd.split())
            
            
            
