import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.topic import get_subscribe_topics
from on_message.device_control import device_control
from on_message.device_create import device_create

subscribe_topics = get_subscribe_topics()

def topic_router(topic, message):
    

    if topic == subscribe_topics['TEST_TOPIC']:
        print( 'hello' )
    
    elif topic == subscribe_topics['DEVICE_CONTROL']:
        device_control(message)
    
    elif topic == subscribe_topics['DEVICE_CREATE']:
        device_create(message)

    # elif topic == SUBSCRIBE_DEVICE_CONTROL_TOPIC:
    #     device_control( json.loads(message) )


    # except Exception as e:
    #     error_message = ''.join(traceback.TracebackException.from_exception(exc).format())
    #     post_slack(
    #         channel = '#error',
    #         username = 'error notification',
    #         text = error_message,
    #         icon_emoji = ':warning:'
    #     )
    #     print('*************************************')
    #     print('               ERROR!                ')
    #     print(error_message)
    #     print('*************************************')
    #     pass
    
