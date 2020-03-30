import datetime
import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.mqtt import publish
from lib.topic import get_publish_topics

publish_topics = get_publish_topics()

def publish_ack():
    message = {
        "timestamp": int( datetime.datetime.now().strftime('%s') ),
    }
    publish(
        topic = publish_topics['ACK'],
        message = json.dumps(message),
        qos = 1,
        retain = False,
    )
