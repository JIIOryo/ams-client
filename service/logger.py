import datetime
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

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

