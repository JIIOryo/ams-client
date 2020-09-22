import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from service.camera import update_camera

"""
# message 
type: json str
-----
{
    "camera_id": "camera_id"
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
def camera_update(message: str) -> None:
    updated_camera = json.loads(message)
    update_camera(
        camera_id = updated_camera['camera_id'],
        name = updated_camera['name'],
        camera_device_id = updated_camera['camera_device_id'],
        resolution = updated_camera['resolution'],
        timer = updated_camera['timer'],
        trimming = updated_camera['trimming']
    )
    return
