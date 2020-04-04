import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.topic import get_subscribe_topics
from on_message.device_control import device_control
from on_message.device_create import device_create
from on_message.device_update import device_update
from on_message.device_delete import device_delete
from on_message.device_feed_pump import device_feed_pump
from on_message.sensor_create import sensor_create
from on_message.sensor_update import sensor_update
from on_message.sensor_delete import sensor_delete
from on_message.publish_ack import publish_ack

subscribe_topics = get_subscribe_topics()

def topic_router(topic: str, message: str):
    

    if topic == subscribe_topics['PING']:
        publish_ack()
    
    elif topic == subscribe_topics['DEVICE_CONTROL']:
        device_control(message)
    
    elif topic == subscribe_topics['DEVICE_CREATE']:
        device_create(message)
    
    elif topic == subscribe_topics['DEVICE_UPDATE']:
        device_update(message)
    
    elif topic == subscribe_topics['DEVICE_DELETE']:
        device_delete(message)
    
    elif topic == subscribe_topics['DEVICE_FEED_PUMP']:
        device_feed_pump(message)
    
    elif topic == subscribe_topics['SENSOR_CREATE']:
        sensor_create(message)

    elif topic == subscribe_topics['SENSOR_UPDATE']:
        sensor_update(message)
    
    elif topic == subscribe_topics['SENSOR_DELETE']:
        sensor_delete(message)
    
    elif topic == 'mcp_test':
        from lib.notification import post_slack_by_type
        from lib.mcp import read_mcp
        import time

        for _ in range(10):
            data = read_mcp(0)
            
            post_slack_by_type(
                text = str(data),
                type_ = 'notification',
            )
            time.sleep(1)


