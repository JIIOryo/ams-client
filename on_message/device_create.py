import datetime
import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config, get_gpio_config
from lib.gpio import gpio_write

from service.device_state import publish_device_state

"""
# message 
type: json str
-----
{
	"device_id": 1,
	"name": "My main light", // str
  "description": "This is my main light!", // str
  "type": "main_light", // str
  "options": { // object
  	"continuous": false, // boolean required
    "timer": { // object required (if "continuous": false)
   		"on_hour": 10, // int required (if "timer" exists)
      "on_minute": 30, // int required (if "timer" exists)
      "off_hour": 17, // int required (if "timer" exists)
      "off_minute": 30 // int required (if "timer" exists)
    }
  }
}
"""

def device_create(message):
    new_device = json.loads(message)
    gpio_config = get_gpio_config()

    new_device_id = new_device['device_id']

    for device in gpio_config:
        if device['device_id'] == new_device_id:

            if device['device']:
                return
            
            device['device'] = {
                'name': new_device['name'],
                'description': new_device['description'],
                'type': new_device['type'],
                'options': new_device['options'],
                'created_at': int( datetime.datetime.now().strftime('%s') ),
                'updated_at': int( datetime.datetime.now().strftime('%s') ),
            }
            break
    
    # todo write to gpio_config
    print(gpio_config)
    
    publish_device_state()   
