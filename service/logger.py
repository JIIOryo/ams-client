import datetime
import json
import os
import sys
import traceback

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    SLACK_NOTIFICATION_TYPE,
    SLACK_MENTION_TYPE,
)
from lib.config import get_config_item
from lib.color import Color, color_text
from lib.notification import post_log_to_slack

DEBUG = "DEBUG"
INFO = "INFO"
WARN = "WARN"
ERROR = "ERROR"
FATAL = "FATAL"

LOG_LEVEL = {
    "DEBUG": {
        "LEVEL": 1,
        "COLOR": Color.CYAN,
        "SLACK_COLOR": '#00FFFF',
    },
    "INFO": {
        "LEVEL": 2,
        "COLOR": Color.GREEN,
        "SLACK_COLOR": '#01DF01',
    },
    "WARN": {
        "LEVEL": 3,
        "COLOR": Color.YELLOW,
        "SLACK_COLOR": '#D7DF01',
    },
    "ERROR": {
        "LEVEL": 4,
        "COLOR": Color.RED,
        "SLACK_COLOR": '#FF4000',
    },
    "FATAL": {
        "LEVEL": 5,
        "COLOR": Color.PURPLE,
        "SLACK_COLOR": '#FF00BF',
    },
}
MIN_FILE_OUTPUT_LEVEL = 2

AMS_ROOT_PATH = get_config_item('ROOT_PATH')
OUTPUT_LOG_FILE_PATH = '/'.join([AMS_ROOT_PATH, 'log', 'logger'])
UNSENT_LOG_FILE_PATH = '/'.join([AMS_ROOT_PATH, 'log', 'tmp', 'unsent.json'])

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

# logger
def logger(log_level: str, message: str, require_slack: bool = False) -> None:

    prefix = log_message_prefix_generator(log_level)

    # stdout
    print('{colored_prefix} {message}'.format(
        colored_prefix = color_text(text=prefix, color=LOG_LEVEL[log_level]['COLOR']),
        message = message
    ))

    # out to log file
    if LOG_LEVEL[log_level]['LEVEL'] >= MIN_FILE_OUTPUT_LEVEL:
        output_log_file(
            text = f'{prefix} {message}\n'
        )
    
    # slack
    slack_notification = get_config_item('SLACK')['SLACK_NOTIFICATION']

    if require_slack and slack_notification:
        mention = ''
        if log_level == ERROR or log_level == FATAL:
            mention = SLACK_MENTION_TYPE['CHANNEL']

        # Error handling is required in HTTP Request
        try:
            post_log_to_slack(
                pretext = mention,
                color = LOG_LEVEL[log_level]['SLACK_COLOR'],
                title = f'[{log_level}]',
                text = message,
                footer = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        except Exception as e:
            error_message = ''.join(traceback.TracebackException.from_exception(e).format())
            error_message += """
-----------------------------------------------
This message can not post to slack.

{message} 
-----------------------------------------------
""".format(message = message)
            logger(ERROR, error_message)
            add_unsent_message(
                log_level = log_level,
                message = message,
            )
            pass

    return

def unsent_file_exist() -> bool:
    return os.path.isfile(UNSENT_LOG_FILE_PATH)

def output_unsent_log_file(new_messges: list) -> None:
    with open(UNSENT_LOG_FILE_PATH, 'w') as f:
        json.dump(new_messges, f, indent = 4)

def get_unsent_log_file() -> list:
    with open(UNSENT_LOG_FILE_PATH) as f:
        return json.load(f)

def add_unsent_message(log_level: str, message: str) -> None:

    new_message = [{
        "log_level": log_level,
        "message": message,
        "footer_timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }]

    # generate unsent log file if it does not exist
    if not unsent_file_exist():
        output_unsent_log_file(new_message)
        return
    
    unsent_messages = get_unsent_log_file()
    unsent_messages.extend(new_message)
    output_unsent_log_file(unsent_messages)
    return
