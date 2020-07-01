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

"""
# message 
type: json str
-----
{
    "device_id": 1
}
"""

def device_auto_feeder(message: str) -> None:
    auto_feeder_action = json.loads(message)
    
    devices = get_gpio_config()
    target_device_id = auto_feeder_action['device_id']

    for device in devices:
        if device['device_id'] == target_device_id:

            if device['device'] == {}:
                raise DeviceNotFound('Device does not found.')

            if device['device']['type'] != DEVICE_TYPE['AUTO_FEEDER']:
                raise DeviceOtherError('This is not auto feeder.')
            
            ams_root_path = get_root_path()
            entry_point = '/'.join([ams_root_path, 'entry_points', 'auto_feeder.py'])
            cmd = 'python3 {entry_point} {device_id}'.format(
                entry_point = entry_point,
                device_id = target_device_id,
            )
            subprocess.Popen(cmd.split())
            
            
            
