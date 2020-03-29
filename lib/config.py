import json
import os

WTMS_ROOT_PATH = os.path.join(os.path.dirname(__file__), '../')
CONFIG_PATH = WTMS_ROOT_PATH + 'config/config.json'
GPIO_CONFIG_PATH = WTMS_ROOT_PATH + 'config/gpio.json'

class KeyNotExist(Exception):
    pass

def read_config_file(config_file_path):
     with open(config_file_path) as f:
         return json.load(f)

def get_config():
    return read_config_file(CONFIG_PATH)

def get_gpio_config():
    return read_config_file(GPIO_CONFIG_PATH)

def get_config_item(key):
    config = get_config()
    if key not in config:
        raise KeyNotExist('key: {key} does not exist.'.format(key = key))
    return config[key]
