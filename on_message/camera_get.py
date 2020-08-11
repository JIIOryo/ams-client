import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_camera_config

def get_cameras() -> list:

    cameras = get_camera_config()
    return cameras
