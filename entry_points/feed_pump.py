import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    SLACK_NOTIFICATION_TYPE,
    SLACK_WATER_FEED_FORMAT,
    DEVICE_TYPE,
)
from commons.errors import DeviceNotFound, DeviceOtherError
from lib.notification import post_slack_by_type
from service.device import get_all_device_by_device_id
from service.feed_pump import feed_pump

"""
python3 feed_pump.py {device_id} {water_feed_time}
"""

if __name__ == '__main__':

    args = sys.argv
    device_id = int(args[1])
    water_feed_time = int(args[2])
    # todo device_id check

    device = get_all_device_by_device_id(device_id)

    if device == {}:
        raise DeviceNotFound('Device does not exist.')
    
    if device['device']['type'] != DEVICE_TYPE['FEED_PUMP']:
        raise DeviceOtherError('This is not feed pump.')

    # feeding water
    feed_pump(device['BCM'], water_feed_time)

    post_slack_by_type(
        text = SLACK_WATER_FEED_FORMAT.format(
            device_id = device_id,
            name = device['device']['name'],
            water_feed_time = water_feed_time,
        ),
        type = SLACK_NOTIFICATION_TYPE['NOTIFICATION'],
    )
