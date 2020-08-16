import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from service.camera import create_camera

"""
# message 
type: json str
-----
{
    "name": "new camera",
    "camera_device_id": 1,
    "resolution": {
        "x": 1700,
        "y": 1024
    },
    "timer": [
        {
            "hour": 10,
            "minute": 0
        },
        {
            "hour": 13,
            "minute": 0
        }
    ],
    "trimming": {
        "top": 100,
        "bottom": 1024,
        "left": 720,
        "right": 1700
    }
}
"""
def camera_create(message: str) -> None:
    new_camera = json.loads(message)
    cameras = create_camera(
        name = new_camera['name'],
        camera_device_id = new_camera['camera_device_id'],
        timer = new_camera['timer'],
        resolution = new_camera['resolution'],
        trimming = new_camera['trimming']
    )
    return
