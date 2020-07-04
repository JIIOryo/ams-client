import os
import subprocess
import time
import traceback

from lib.assets import get_boot_ascii_art
from lib.config import get_config_item
from lib.notification import post_slack_by_type
from lib.util import connected_to_internet
from service.logger import (
    logger,
    DEBUG,
    INFO,
    WARN,
    ERROR,
    FATAL,
)
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
    # AMS Start!
    logger(INFO, 'AMS start.')
    logger(DEBUG, 'Welcome to AMS!')
    BOOT_AA = get_boot_ascii_art()
    logger(INFO, BOOT_AA)

    # set initial device state
    logger(INFO, 'set initial device states ...')
    set_init_device_state()
    logger(DEBUG, 'OK.')

    # network connection check
    logger(INFO, 'Network connection check start')
    no_network_connection = True
    while no_network_connection:
        logger(INFO, 'Not connected to the Internet. Please wait ...')
        no_network_connection = not connected_to_internet(
            url = NETWORK_CONNECT_CHECK_URL,
            timeout = NETWORK_CONNECT_CHECK_INTERVAL,
        )
        time.sleep(1)
    logger(DEBUG, 'OK.')

    # open subscriber
    logger(INFO, 'running subscriber ...', True)
    subprocess.Popen(['python3', SUBSCRIBER_PATH])
    logger(DEBUG, 'OK')

    # AMS start successfully
    logger(INFO, 'AMS start successfully!🎉🎉', True)

    # open sensor manager
    logger(INFO, 'running sensor manager ...', True)
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
