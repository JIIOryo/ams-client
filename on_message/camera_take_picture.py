import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from service.camera import take_picture

"""
# message 
type: json str
-----
{
    "cameras": [
        {
            "camera_id": "82900309bfb57e7c6173cad57daefba9",
        }
    ]
}
"""

def camera_take_picture(message: str) -> None:
    target_cameras = json.loads(message)['cameras']
    
    for target_camera in target_cameras:
        target_camera_id = target_camera['camera_id']
        take_picture(target_camera_id)
