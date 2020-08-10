import datetime
import json
import sys

import requests

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.errors import (
    CameraNotFound,
    CameraServerNotRunningError,
    S3UploadFailedError,
    MqttNotAuthorisedError,
    MqttNoRouteToHostError,
    UnknownError,
)
from lib.config import (
    get_config_item,
    get_config_items,
    get_camera_config,
    get_camera_device_config,
    set_camera_config,
)
from lib.topic import get_publish_topics
from lib.util import (
    is_exist_file,
    get_json_file,
    make_dir,
    set_json_file,
)
from service.logger import (
    logger,
    DEBUG,
    INFO,
    WARN,
    ERROR,
    FATAL,
)

AMS_ROOT_PATH = get_config_item('ROOT_PATH').rstrip('/')

def get_camera_config_by_id(camera_id: str) -> dict:
    cameras = get_camera_config()
    for camera in cameras:
        if camera['camera_id'] == camera_id:
            return camera
    return {}

def get_camera_device_config_by_id(camera_device_id: int) -> dict:
    camera_devices = get_camera_device_config()
    for camera_device in camera_devices:
        if camera_device['camera_device_id'] == camera_device_id:
            return camera_device
    return {}

def register_picture(object_name: str) -> None:
    # object_name example: 'tank_id-sample/sample_camera_id/2020/01/01/00_00_00.jpg'
    object_name_elements = object_name.split('/')
    camera_id = object_name_elements[1] # sample_camera_id
    year = object_name_elements[2] # 2020
    month = object_name_elements[3] # 01
    day = object_name_elements[4] # 01
    file_name = object_name_elements[5] # 00_00_00.jpg

    target_dir_path = f'{AMS_ROOT_PATH}/pictures/{camera_id}/{year}/{month}'
    target_file_path = f'{target_dir_path}/{day}.json'

    # make new directory
    make_new_dir = make_dir(target_dir_path)
    if make_new_dir: logger(INFO, f'make new directory: {target_dir_path}', True)
    
    target_day_pictures = {'pictures': []}
    if is_exist_file(target_file_path):
        target_day_pictures = get_json_file(target_file_path)
    
    # register new picture
    target_day_pictures['pictures'].append(file_name)
    set_json_file(
        file_path = target_file_path,
        data = target_day_pictures
    )
    return

def add_latest_picture_url(camera_id: str, url: str) -> None:
    cameras = gcameras = get_camera_config()
    for camera in cameras:
        if camera['camera_id'] == camera_id:
            camera['latest_picture_url'] = url
    set_camera_config(new_camera_config = cameras)
    return
    
def camera_request(
    host: str,
    port: int,
    object_name: str,
    resolution: dict,
    trimming: dict,
    camera_warm_up_time: float,
    aws: dict = {},
    mqtt: dict = {},
) -> None:

    request_json = {
        'objectName': object_name,
        'resolution': {
            'x': resolution['x'],
            'y': resolution['y'],
        },
        'trimming': {
            'top': trimming['top'],
            'bottom': trimming['bottom'],
            'left': trimming['left'],
            'right': trimming['right'],
        },
        'cameraWarmUpTime': camera_warm_up_time,
        'uploader': {}
    }

    if aws != {}:
        request_json['uploader']['aws'] = {
            'accessKeyId': aws['aws_access_key_id'],
            'secretAccessKey': aws['aws_secret_access_key'],
            's3Bucket': aws['s3_bucket'],
            'region': aws['region'],
        }
    
    if mqtt != {}:
        request_json['uploader']['mqtt'] = {
            'host': mqtt['host'],
            'port': mqtt['port'],
            'userName': mqtt['user_name'],
            'password': mqtt['password'],
            'retain': mqtt['retain'],
            'topic': mqtt['topic'],
        }

    # request to camera api server
    try:
        res = requests.post(
            url = f'http://{host}:{port}/picture',
            json = request_json
        )
    except requests.exceptions.RequestException:
        logger(ERROR, 'camera is not running', True)
        raise CameraServerNotRunningError
    except Exception:
        logger(FATAL, '[camera.request] Unknown Error', True)
        raise UnknownError

    status_code = res.status_code

    # error response from camera api
    if status_code != 200:
        response_json = json.loads(res.text)

        error_text = f'Status code from camera: {status_code}\n'
        error_text += res.text
        logger(ERROR, error_text, True)
    
        if response_json['error'] == 'S3UploadFailedError': raise S3UploadFailedError
        elif response_json['error'] == 'MqttNotAuthorisedError': raise MqttNotAuthorisedError
        elif response_json['error'] == 'MqttNoRouteToHostError': raise MqttNoRouteToHostError
        else: raise UnknownError
    
    return

def generate_object_name(tank_id: str, camera_id: str, ext: str):
    # now = '2020/08/09/10_14_42'
    now = datetime.datetime.now().strftime('%Y/%m/%d/%H_%M_%S')
    return f'{tank_id}/{camera_id}/{now}.{ext}'
    
def take_picture(camera_id: str) -> None:
    camera = get_camera_config_by_id(camera_id)

    if camera == {}:
        logger(
            WARN,
            'Camera not found.\n' + 
            f'camera_id = {camera_id}',
            True,
            False
        )
        raise CameraNotFound

    config = get_config_items([
        'TANK_ID',
        'MQTT',
        'CAMERA'
    ])

    camera_device = get_camera_device_config_by_id(camera['camera_device_id'])

    object_name = generate_object_name(
        tank_id = config['TANK_ID'],
        camera_id = camera['camera_id'],
        ext = 'jpg'
    )
    latest_picture_topic = get_publish_topics()['CAMERA_LATEST_PICTURE']

    # take a picture
    camera_request(
        host = camera_device['host'],
        port = camera_device['port'],
        object_name = object_name,
        resolution = camera['resolution'],
        trimming = camera['trimming'],
        camera_warm_up_time = config['CAMERA']['CAMERA_WARM_UP_TIME'],
        aws = {
            'aws_access_key_id': config['CAMERA']['AWS_ACCESS_KEY_ID'],
            'aws_secret_access_key': config['CAMERA']['AWS_SECRET_ACCESS_KEY'],
            's3_bucket': config['CAMERA']['S3_BUCKET'],
            'region': config['CAMERA']['REGION'],
        },
        mqtt = {
            'host': config['MQTT']['MQTT_BROKER'],
            'port': config['MQTT']['MQTT_BROKER_PORT'],
            'user_name': config['MQTT']['MQTT_BROKER_USERNAME'],
            'password': config['MQTT']['MQTT_BROKER_PASSWORD'],
            'retain': False, # TODO this is true
            'topic': latest_picture_topic,
        }
    )

    picture_url = config['CAMERA']['PICTURE_URL'] + '/' + object_name
    add_latest_picture_url(
        camera_id = camera_id,
        url = picture_url
    )

    logger(
        INFO,
        'Take a tank picture 📸\n' + 
        f'ObjectName is {picture_url}',
        True,
        False
    )

    register_picture(object_name)

    return
