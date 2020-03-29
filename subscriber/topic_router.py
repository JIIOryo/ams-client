import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.topic import get_subscribe_topics

subscribe_topics = get_subscribe_topics()

def topic_router(topic, message):

    if topic == subscribe_topics['TEST_TOPIC']:
        print( 'hello' )
    
    elif topic == subscribe_topics['DEVICE_CONTROL']:
        print('control')

    # elif topic == SUBSCRIBE_DEVICE_CONTROL_TOPIC:
    #     device_control( json.loads(message) )
    
