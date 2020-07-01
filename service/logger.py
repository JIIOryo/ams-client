import datetime
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config_item
from lib.color import Color, color_text

DEBUG = "DEBUG"
INFO = "INFO"
WARN = "WARN"
ERROR = "ERROR"
FATAL = "FATAL"

LOG_LEVEL = {
    "DEBUG": {
        "LEVEL": 1,
        "COLOR": Color.CYAN
    },
    "INFO": {
        "LEVEL": 2,
        "COLOR": Color.GREEN
    },
    "WARN": {
        "LEVEL": 3,
        "COLOR": Color.YELLOW
    },
    "ERROR": {
        "LEVEL": 4,
        "COLOR": Color.RED
    },
    "FATAL": {
        "LEVEL": 5,
        "COLOR": Color.PURPLE
    },
}
MIN_FILE_OUTPUT_LEVEL = 2

AMS_ROOT_PATH = get_config_item('ROOT_PATH')
OUTPUT_LOG_FILE_PATH = '/'.join([AMS_ROOT_PATH, 'log', 'logger'])

def log_message_prefix_generator(log_level: str) -> str:
    """
    Parameters
    ----------
    text: log_level
        log level
        e.g. "INFO", "WARN", ...

    Returns
    ----------
    str
        logger prefix
        e.g.
        "[2020-06-17 20:21:12] [INFO]"
    """
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f'[{now}] [{log_level}]'

def today_log_file_name() -> str:
    """    
    Returns
    ----------
    str
        log_file_name
        e.g.
        /home/pi/ams-client/log/logger/log_2019_10_10.log
    """
    prefix, ext = 'log', 'log'
    file_name = '{prefix}_{date}.{ext}'.format(
        prefix = prefix,
        date = datetime.datetime.now().strftime('%Y_%m_%d'),
        ext = ext
    )
    return '/'.join([OUTPUT_LOG_FILE_PATH, file_name])

def output_log_file(text: str):
    log_file_name = today_log_file_name()
    with open(log_file_name, 'a') as f:
        f.write(text)
    return

