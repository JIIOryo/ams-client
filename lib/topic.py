from typing import Dict
import json
import os

AMS_ROOT_PATH = os.path.join(os.path.dirname(__file__), '../')
TOPICS_PATH = AMS_ROOT_PATH + 'subscriber/topics.json'

from .config import get_config_items

ids = get_config_items(['TANK_ID', 'CLIENT_ID'])
tank_id, client_id = ids['TANK_ID'], ids['CLIENT_ID']

class KeyNotExist(Exception):
    pass

def read_topics_file(topics_file_path: str) -> dict:
     with open(topics_file_path) as f:
         return json.load(f)

def get_all_topics() -> Dict[str, str]:
    return read_topics_file(TOPICS_PATH)

def apply_tank_id_and_client_id(topics: Dict[str, str]) -> Dict[str, str]:
    result = {}
    for key in topics:
        result[key] = topics[key].format(tank_id = tank_id, client_id = client_id)
    return result

def get_publish_topics() -> Dict[str, str]:
    publish_topics = get_all_topics()['PUBLISH']
    return apply_tank_id_and_client_id(publish_topics)

def get_subscribe_topics() -> Dict[str, str]:
    subscribe_topics = get_all_topics()['SUBSCRIBE']
    return apply_tank_id_and_client_id(subscribe_topics)

