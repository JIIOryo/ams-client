import os
import subprocess
import time
import traceback

from lib.config import get_config_item
from lib.notification import post_slack_by_type
from lib.util import connected_to_internet
from service.reboot import set_init_device_state
from service.sensor import publish_sensor_data
from commons.consts import (
    SLACK_NOTIFICATION_TYPE,
    NETWORK_CONNECT_CHECK_INTERVAL,
    NETWORK_CONNECT_CHECK_URL,
)

PWD = os.getcwd()
SUBSCRIBER_PATH = '/'.join([PWD, 'subscriber', 'subscriber.py'])

def main() -> None:
    # set initial device state
    print('set initial device states ...')
    set_init_device_state()
    print('OK.')

    # network connection check
    print('Network connection check start')
    no_network_connection = True
    while no_network_connection:
        print('Not connected to the Internet. Please wait ...')
        no_network_connection = not connected_to_internet(
            url = NETWORK_CONNECT_CHECK_URL,
            timeout = NETWORK_CONNECT_CHECK_INTERVAL,
        )
    print('OK.')

    # open subscriber
    print('running subscriber ...')
    subprocess.Popen(['python3', SUBSCRIBER_PATH])
    print('OK')

    # open sensor manager
    while True:
        try:
            publish_sensor_data()
        except Exception as e:
            error_message = ''.join(traceback.TracebackException.from_exception(e).format())
            post_slack_by_type(
                text = error_message,
                type_ = SLACK_NOTIFICATION_TYPE['ERROR'],
            )
            print(error_message)
            pass

if __name__ == '__main__':
    main()
