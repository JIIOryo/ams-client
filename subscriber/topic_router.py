import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

def topic_router(topic, message):

    if topic == 'aaa':
        print( 'hello' )

    # elif topic == SUBSCRIBE_DEVICE_CONTROL_TOPIC:
    #     device_control( json.loads(message) )
    
