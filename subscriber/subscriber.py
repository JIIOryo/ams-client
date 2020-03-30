import json
import os
import subprocess
import sys
import time
import traceback

import paho.mqtt.client as mqtt

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    SLACK_NOTIFICATION_TYPE,
)
from lib.config import get_config, get_config_item
from lib.notification import post_slack_by_type

from topic_router import topic_router

config = get_config()
host = config['MQTT']['MQTT_BROKER']
port = config['MQTT']['MQTT_BROKER_PORT']
username = config['MQTT']['MQTT_BROKER_USERNAME']
password = config['MQTT']['MQTT_BROKER_PASSWORD']
protocol = mqtt.MQTTv311
keepalive = config['MQTT']['KEEPALIVE']
qos = config['MQTT']['SUBSCRIBER_QOS']
sub_topic = '#' 

def on_connect(client, userdata, flags, rc):
    print('Result Code: {}\n'.format(rc))
    client.subscribe(sub_topic)

def on_message(client, userdata, msg):
    print('==========================================')
    print('topic: {0} , message: {1}'.format(msg.topic, msg.payload))

    try:
        topic_router(
            topic = msg.topic,
            message = msg.payload.decode()
        )
    except Exception as e:
        error_message = ''.join(traceback.TracebackException.from_exception(e).format())
        post_slack_by_type(
            text = error_message,
            type = SLACK_NOTIFICATION_TYPE['ERROR'],
        )
        print(error_message)
        pass
    
if __name__ == '__main__':

    client = mqtt.Client(protocol = protocol)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port = port, keepalive = keepalive)
    client.loop_forever()
