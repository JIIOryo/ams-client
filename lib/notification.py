import json

import requests

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config

def post_slack(channel, username, text, icon_emoji):

    post_data = {
        "channel": channel,
        "username": username,
        "text": text,
        "icon_emoji": icon_emoji
    }
    slack_webhook_url = get_config_item('SLACK_WEBHOOK_URL')

    response = requests.post(slack_webhook_url, data=json.dumps(post_data))