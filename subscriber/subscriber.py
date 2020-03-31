import datetime
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

from lib.color import Color, color_text, print_color_log
from commons.consts import (
    SLACK_NOTIFICATION_TYPE,
    LOG_TITLE,
)
from lib.config import get_config, get_config_item
from lib.notification import post_slack_by_type
from lib.topic import get_subscribe_topics

from topic_router import topic_router

config = get_config()
host = config['MQTT']['MQTT_BROKER']
port = config['MQTT']['MQTT_BROKER_PORT']
username = config['MQTT']['MQTT_BROKER_USERNAME']
password = config['MQTT']['MQTT_BROKER_PASSWORD']
protocol = mqtt.MQTTv311
keepalive = config['MQTT']['KEEPALIVE']
QOS = config['MQTT']['SUBSCRIBER_QOS']
SUBSCRIBE_TOPICS = [(topic, QOS) for topic in get_subscribe_topics().values() ]

def on_connect(client, userdata, flags, rc):
    print('Result Code: {}\n'.format(rc))
    client.subscribe(SUBSCRIBE_TOPICS)

def on_message(client, userdata, msg):
    
    print_color_log(
        title = LOG_TITLE['SUBSCRIBER'],
        title_color = Color.CYAN,
        text = '{unixtime}: {topic}: {message}'.format(
            unixtime = datetime.datetime.now().strftime('%s'),
            topic = color_text(msg.topic, Color.GREEN),
            message = msg.payload.decode(),
        )
    )

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
