import os
import subprocess
import time

from lib.config import get_config_item
from service.sensor import publish_sensor_data

PWD = os.getcwd()
# SENSOR_MANAGER_PATH = '/'.join([PWD, ..., ])
SUBSCRIBER_PATH = '/'.join([PWD, 'subscriber', 'subscriber.py'])

def main():
    # check cron to write gpio 

    # open sensor manager

    # open subscriber
    network_connection_wait_time = get_config_item('NETWORK_CONNECTION_WAIT_TIME')
    # time.sleep(network_connection_wait_time)
    subprocess.Popen(['python3', SUBSCRIBER_PATH])

    while True:
        publish_sensor_data()

if __name__ == '__main__':
    main()
