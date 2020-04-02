import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    SLACK_NOTIFICATION_TYPE,
    SLACK_WATER_FEED_FORMAT,
)
from lib.notification import post_slack_by_type
from service.feed_pump import feed_pump

"""
python3 feed_pump.py {pin} {water_feed_time}
"""

if __name__ == '__main__':

    args = sys.argv
    pin = int(args[1])
    water_feed_time = int(args[2])
    # todo pin check

    feed_pump(pin, water_feed_time)

    post_slack_by_type(
        text = SLACK_WATER_FEED_FORMAT.format(
            device_id = 100,
            name = 'test',
            water_feed_time = water_feed_time,
        ),
        type = SLACK_NOTIFICATION_TYPE['NOTIFICATION'],
    )
