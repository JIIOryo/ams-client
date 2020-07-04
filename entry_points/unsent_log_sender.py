import sys
import time

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    SLACK_MENTION_TYPE,
)
from lib.notification import post_log_to_slack
from service.logger import (
    unsent_file_exist,
    get_unsent_log_file,
    output_unsent_log_file,
    LOG_LEVEL,
)

"""
python3 unsent_log_sender.py
"""

if __name__ == '__main__':

    # unsent messages file does not exist
    if not unsent_file_exist():
        sys.exit(0)
    
    unsent_messages = get_unsent_log_file()
    
    while len(unsent_messages) > 0:
        unsent_message = unsent_messages.pop(0)
        post_log_to_slack(
            pretext = SLACK_MENTION_TYPE['CHANNEL'] + '\n⚠️This is unsent message.',
            color = LOG_LEVEL[unsent_message['log_level']]['SLACK_COLOR'],
            title = '[{log_level}]'.format(log_level = unsent_message['log_level']),
            text = unsent_message['message'],
            footer = unsent_message['footer_timestamp'],
        )
        output_unsent_log_file(unsent_messages)
        time.sleep(0.5)
