import os
import subprocess
import time

from lib.config import get_config_item
from service.reboot import set_init_device_state
from service.sensor import publish_sensor_data

PWD = os.getcwd()
SUBSCRIBER_PATH = '/'.join([PWD, 'subscriber', 'subscriber.py'])

def main() -> None:
    # set initial device state
    set_init_device_state()

    # open subscriber
    network_connection_wait_time = get_config_item('NETWORK_CONNECTION_WAIT_TIME')
    time.sleep(network_connection_wait_time)
    subprocess.Popen(['python3', SUBSCRIBER_PATH])

    # open sensor manager
    while True:
        publish_sensor_data()

if __name__ == '__main__':
    main()
