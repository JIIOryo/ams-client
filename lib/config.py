from typing import Any, List
import json
import os

WTMS_ROOT_PATH = os.path.join(os.path.dirname(__file__), '../')
CONFIG_PATH = WTMS_ROOT_PATH + 'config/config.json'
GPIO_CONFIG_PATH = WTMS_ROOT_PATH + 'config/gpio.json'
SENSOR_CONFIG_PATH = WTMS_ROOT_PATH + 'config/sensor.json'
CAMERA_CONFIG_PATH = WTMS_ROOT_PATH + 'config/camera.json'
CAMERA_DEVICE_CONFIG_PATH = WTMS_ROOT_PATH + 'config/camera_device.json'

class KeyNotExist(Exception):
    pass

def read_config_file(config_file_path: str) -> dict:
     with open(config_file_path) as f:
         return json.load(f)

def get_config() -> dict:
    return read_config_file(CONFIG_PATH)

def set_config(new_config: dict) -> None:
    with open(CONFIG_PATH, 'w') as f:
        json.dump(new_config, f, indent = 4)

def get_gpio_config() -> dict:
    return read_config_file(GPIO_CONFIG_PATH)

def get_sensor_config() -> dict:
    return read_config_file(SENSOR_CONFIG_PATH)

def get_camera_config() -> dict:
    return read_config_file(CAMERA_CONFIG_PATH)

def get_camera_device_config() -> dict:
    return read_config_file(CAMERA_DEVICE_CONFIG_PATH)

def get_config_items(keys: List[str]) -> dict:
    config = get_config()
    result = {}
    for key in keys:
        if key not in config:
            raise KeyNotExist('key: {key} does not exist.'.format(key = key))
        result[key] = config[key]
    return result

def get_config_item(key: str) -> Any:
    return get_config_items([key])[key]

def set_gpio_config(new_gpio_config: dict) -> None:
    with open(GPIO_CONFIG_PATH, 'w') as f:
        json.dump(new_gpio_config, f, indent = 4)

def set_sensor_config(new_sensor_config: dict) -> None:
    with open(SENSOR_CONFIG_PATH, 'w') as f:
        json.dump(new_sensor_config, f, indent = 4)

def get_root_path() -> str:
    return get_config_item('ROOT_PATH').rstrip('/')