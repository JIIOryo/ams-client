import sys

from paho.mqtt.publish import single

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config

config = get_config()

def publish(
        topic: str,
        message: str,
        qos: int = 1,
        retain: bool = False,
        keepalive: int = config['MQTT']['KEEPALIVE']
    ) -> None:
    auth = {
        'username': config['MQTT']['MQTT_BROKER_USERNAME'], 
        'password': config['MQTT']['MQTT_BROKER_PASSWORD'],
    }
    single(
        topic = topic,
        payload = message,
        qos = qos,
        retain = retain,
        hostname = config['MQTT']['MQTT_BROKER'],
        port = config['MQTT']['MQTT_BROKER_PORT'],
        keepalive = keepalive,
        auth = auth
    )
    
