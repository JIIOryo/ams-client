import datetime
import json
import sys
import time

import requests

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.errors import (
    AlbumNotFound,
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
    generate_md5_hash,
    get_json_file,
    ls,
    make_dir,
    set_json_file,
    zero_padding,
    zero_padding_month,
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
    cameras: list,
    resolution: dict,
    camera_warm_up_time: float,
    aws: dict = {},
    mqtt: dict = {},
) -> None:

    request_json = {
        'cameras': [
            {
                'objectName': camera['object_name'],
                'topic': camera['topic'],
                'trimming': {
                    'top': camera['trimming']['top'],
                    'bottom': camera['trimming']['bottom'],
                    'left': camera['trimming']['left'],
                    'right': camera['trimming']['right'],
                },
            }
            for camera in cameras
        ],
        'resolution': {
            'x': resolution['x'],
            'y': resolution['y'],
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
    
def generate_camera_id(tank_id: str) -> str:
    now_unix = time.time()
    key = f'{tank_id}_{now_unix}'
    return generate_md5_hash(key)

def generate_picture_url(camera_id: str, year: int, month: int, day: int, file_name: str) -> str:
    config = get_config_items([
        'TANK_ID',
        'CAMERA'
    ])
    return '/'.join([
        config['CAMERA']['PICTURE_URL'],
        config['TANK_ID'],
        camera_id,
        str(year),
        zero_padding_month(month),
        zero_padding(day, 2),
        file_name,
    ])

def take_picture(camera_id: str) -> None:
    take_pictures([camera_id])
    return

# take_pictures用のfunction
# camera_deviceの配列のcamerasにcameraを追加
def __append_camera_to_camera_device(camera_devices: list, camera: dict) -> None:
    # camera_devicesはrequest_camera_devicesと同じスキーマ
    # cameraはconfigと同じスキーマ
    for camera_device in camera_devices:
        if camera_device['camera_device_id'] == camera['camera_device_id']:
            camera_device['cameras'].append(camera)
            return
    return

def take_pictures(camera_id_list: list) -> None:

    if len(camera_id_list) == 0:
        return
    
    config = get_config_items([
        'TANK_ID',
        'MQTT',
        'CAMERA'
    ])

    camera_device_config = get_camera_device_config()

    # camera_device一覧と、今回撮影するカメラが紐づいた配列request_camera_devicesを作成
    """
    example
    request_camera_devices = [
        {
            'camera_device_id': 1,
            'host': CAMERA_HOST,
            'port': CAMERA_PORT,
            'cameras': [
                {
                    'camera_id',
                    'name': 'sump_sub_box',
                    'camera_device_id'
                    'resolution': {'x': 1700, 'y': 1024},
                    'trimming': {'bottom': 750, 'left': 1000, 'right': 1300, 'top': 620},
                    'timer': [{'hour': 10, 'minute': 0}, {'hour': 12, 'minute': 0}, {'hour': 18, 'minute': 0}],
                    'latest_picture_url': 'https://hoge.cloudfront.net/tank_id-sample/fuga/2020/08/16/12_05_10.jpg',
                    'object_name': 'tank_id-sample/camera_id_hoge/2020/09/22/14_15_51.jpg',
                    'latest_picture_topic': 'tank/tank_id-sample/camera_id_hoge/latest_picture'
                }
            ]
        }
    ]
    """
    request_camera_devices = []
    # camera_device_configのスキーマにcamerasフィールドを追加したものをrequest_camera_devicesとする
    for camera_device in camera_device_config:
        camera_device['cameras'] = []
        request_camera_devices.append(camera_device)

    # 今回撮影するcamera_id全てに対して以下を行う
    for camera_id in camera_id_list:
        camera = get_camera_config_by_id(camera_id)

        # cameraが存在しない場合はエラー
        if camera == {}:
            logger(
                WARN,
                'Camera not found.\n' + 
                f'camera_id = {camera_id}',
                True,
                False
            )
            raise CameraNotFound
        
        # cameraにobject_nameを追加
        object_name = generate_object_name(
            tank_id = config['TANK_ID'],
            camera_id = camera['camera_id'],
            ext = 'jpg'
        )
        camera['object_name'] = object_name
        
        # cameraにpublish用のtopicを追加
        latest_picture_topic = get_publish_topics()['CAMERA_LATEST_PICTURE']
        # camera_idをtopicに反映
        camera['latest_picture_topic'] = latest_picture_topic.format(camera_id = camera['camera_id'])
        
        # cameraが指定するcamera_device_idのcamera_deviceのところに追加
        __append_camera_to_camera_device(
            camera_devices = request_camera_devices,
            camera = camera
        )

    # 対象のcamera_deviceに対して以下を行う
    for request_camera_device in request_camera_devices:
        # 撮影したいカメラがない場合は次へ
        if len(request_camera_device['cameras']) == 0:
            continue
        
        # take a picture
        camera_request(
            host = request_camera_device['host'],
            port = request_camera_device['port'],
            cameras = [
                {
                    'object_name': camera['object_name'],
                    'topic': camera['latest_picture_topic'],
                    'trimming': camera['trimming'],
                }
                for camera in request_camera_device['cameras']
            ],
            resolution = request_camera_device['cameras'][0]['resolution'], # TODO resolution はcamera deviceごとに設定するのが理想 仮でcameraの先頭のresolutionを利用する
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
            }
        )

        # 以降撮影後の処理

        # 撮影した画像のURL(logger用)
        picture_urls = []

        # 撮影した画像それぞれに対して、latest_pictureを登録、アルバム用ディレクトリに追加する処理を行う
        for camera in request_camera_device['cameras']:
            picture_url = config['CAMERA']['PICTURE_URL'] + '/' + camera['object_name']
            picture_urls.append(picture_url)
            # 撮影した画像のURLをconfigのlatest_picture_urlに登録
            add_latest_picture_url(
                camera_id = camera['camera_id'],
                url = picture_url
            )
            # picturesディレクトリに追加
            register_picture(camera['object_name'])

        logger(
            INFO,
            'Take a tank picture 📸\n' + 
            f'pictures: {picture_urls}',
            True,
            False
        )
    return

def create_camera(name: str, camera_device_id: int, timer: list, resolution: dict, trimming: dict) -> None:
    cameras = get_camera_config()
    tank_id = get_config_item('TANK_ID')

    camera_id = generate_camera_id(tank_id)

    new_camera = {
        'camera_id': camera_id,
        'name': name,
        'camera_device_id': camera_device_id,
        'resolution': {
            'x': resolution['x'],
            'y': resolution['y'],
        },
        'timer': list(timer),
        'trimming': {
            'top': trimming['top'],
            'bottom': trimming['bottom'],
            'left': trimming['left'],
            'right': trimming['right'],
        },
        'latest_picture_url': ''
    }
    cameras.append(new_camera)

    set_camera_config(cameras)

    logger(
        INFO,
        'Create new camera 📸\n' + json.dumps(new_camera),
        True,
        False
    )
    return

def update_camera(
    camera_id: str,
    name: str,
    camera_device_id: int,
    resolution: dict,
    timer: list,
    trimming: dict
) -> None:
    cameras = get_camera_config()

    updated_camera = {
        'camera_id': camera_id,
        'name': name,
        'camera_device_id': camera_device_id,
        'resolution': {
            'x': resolution['x'],
            'y': resolution['y'],
        },
        'timer': list(timer),
        'trimming': {
            'top': trimming['top'],
            'bottom': trimming['bottom'],
            'left': trimming['left'],
            'right': trimming['right'],
        },
        'latest_picture_url': ''
    }

    for camera in cameras:
        if camera['camera_id'] == camera_id:
            camera['name'] = name
            camera['camera_device_id'] = camera_device_id
            camera['resolution'] = resolution
            camera['timer'] = timer
            camera['trimming'] = trimming
            updated_camera['latest_picture_url'] = camera['latest_picture_url']
        
    set_camera_config(cameras)

    logger(
        INFO,
        f'Update camera 📸\ncamera_id = {camera_id}\n' + json.dumps(updated_camera),
        True,
        False
    )
    return

def get_album_exist_years(camera_id: str) -> dict:
    taeget_path = '/'.join([AMS_ROOT_PATH, 'pictures', camera_id])
    try:
        list_ = ls(taeget_path)
    except FileNotFoundError:
        logger(
            ERROR,
            f'camera not found. camera_id = {camera_id}',
            True,
            False
        )
        raise CameraNotFound
    
    return {
        'camera_id': camera_id,
        'list': sorted(list_),
        'type': 'year',
    }

def get_album_exist_months(camera_id: str, year: int) -> dict:
    # to raise CameraNotFound if camera_id is invalid
    album_exist_years = get_album_exist_years(camera_id)['list']

    if str(year) not in album_exist_years:
        raise AlbumNotFound

    taeget_path = '/'.join([AMS_ROOT_PATH, 'pictures', camera_id, str(year)])
    
    return {
        'camera_id': camera_id,
        'list': sorted(ls(taeget_path)),
        'type': 'month',
    }

def get_album_exist_days(camera_id: str, year: int, month: int) -> dict:
    # to raise CameraNotFound if camera_id is invalid
    # and 
    # to raise AlbumNotFound if album is not found at taeget year
    album_exist_months = get_album_exist_months(camera_id, year)['list']

    if zero_padding_month(month) not in album_exist_months:
        raise AlbumNotFound

    taeget_path = '/'.join([AMS_ROOT_PATH, 'pictures', camera_id, str(year), zero_padding_month(month)])
    
    file_list = ls(taeget_path)
    return {
        'camera_id': camera_id,
        'list': sorted(
            [f.split('.')[0] for f in file_list] # remove '.json'
        ),
        'type': 'day',
    }

def get_album_pictures(camera_id: str, year: int, month: int, day: int) -> dict:
    # to raise CameraNotFound if camera_id is invalid
    # and 
    # to raise AlbumNotFound if album is not found at taeget year
    # and
    # to raise AlbumNotFound if album is not found at taeget month
    album_exist_days = get_album_exist_days(camera_id, year, month)['list']

    _day = zero_padding(day, 2)

    if _day not in album_exist_days:
        raise AlbumNotFound

    target_file = '/'.join([
        AMS_ROOT_PATH,
        'pictures',
        camera_id,
        str(year),
        zero_padding_month(month),
        _day + '.json'
    ])

    pictures = get_json_file(target_file)['pictures']

    return {
        'camera_id': camera_id,
        'list': [
            generate_picture_url(
                camera_id = camera_id,
                year = year,
                month = month,
                day = day,
                file_name = picture,
            ) for picture in pictures
        ],
        'type': 'url',
    }
