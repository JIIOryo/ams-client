import json
import sys

import requests

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    SLACK_NOTIFICATION_TYPE,
)
from commons.errors import NotificationTypeUndefined
from lib.config import get_config_item

def post_slack(channel, username, text, icon_emoji):

    post_data = {
        "channel": channel,
        "username": username,
        "text": text,
        "icon_emoji": icon_emoji
    }
    slack_webhook_url = get_config_item('SLACK')['WEBHOOK_URL']
    response = requests.post(slack_webhook_url, data=json.dumps(post_data))

def post_slack_by_type(text, type_):

    slack_config = get_config_item('SLACK')

    if type_ == SLACK_NOTIFICATION_TYPE['NOTIFICATION']:
        post_slack(
            channel = slack_config['NOTIFICATION']['CHANNEL'],
            username = slack_config['NOTIFICATION']['USERNAME'],
            text = slack_config['NOTIFICATION']['MESSAGE_FORMAT'].format(message = text),
            icon_emoji = slack_config['NOTIFICATION']['ICON_EMOJI'],
        )

    elif type_ == SLACK_NOTIFICATION_TYPE['ERROR']:
        post_slack(
            channel = slack_config['ERROR']['CHANNEL'],
            username = slack_config['ERROR']['USERNAME'],
            text = slack_config['ERROR']['MESSAGE_FORMAT'].format(message = text),
            icon_emoji = slack_config['ERROR']['ICON_EMOJI'],
        )
        
    else:
        raise NotificationTypeUndefined('This type does not exist.')

