import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_camera_device_config

def get_camera_devices() -> list:
    camera_devices = get_camera_device_config()
    return camera_devices
