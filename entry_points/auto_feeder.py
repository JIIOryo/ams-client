import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    SLACK_NOTIFICATION_TYPE,
    SLACK_AUTO_FEEDER_FORMAT,
    DEVICE_TYPE,
)
from commons.errors import DeviceNotFound, DeviceOtherError
from lib.notification import post_slack_by_type
from service.device import get_all_device_by_device_id
from service.auto_feeder import auto_feeder

"""
python3 auto_feeder.py {device_id}
"""

if __name__ == '__main__':

    args = sys.argv
    device_id = int(args[1])

    device = get_all_device_by_device_id(device_id)

    if device == {}:
        raise DeviceNotFound('Device does not exist.')
    
    if device['device']['type'] != DEVICE_TYPE['AUTO_FEEDER']:
        raise DeviceOtherError('This is not auto feeder.')

    # auto feeding
    auto_feeder(pin = device['BCM'])

    post_slack_by_type(
        text = SLACK_AUTO_FEEDER_FORMAT.format(
            device_id = device_id,
            name = device['device']['name']
        ),
        type_ = SLACK_NOTIFICATION_TYPE['NOTIFICATION'],
    )
