import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_gpio_config
from lib.gpio import gpio_write
from lib.util import get_now_device_should_be_on_by_timer
from commons.consts import DEVICE_RUN_TYPE

def set_init_device_state() -> None:
    devices = get_gpio_config()

    for device in devices:

        # no device
        if device['device'] == {}:
            continue
        
        # device run type is not daily
        if device['device']['run_type'] != DEVICE_RUN_TYPE['DAILY']:
            continue
        
        timer = device['device']['options']['timer']
        ideal_device_state = get_now_device_should_be_on_by_timer(
            on_hour = timer['on_hour'],
            on_minute = timer['on_minute'],
            off_hour = timer['off_hour'],
            off_minute = timer['off_minute'],
        )
        gpio_write(
            pin = device['BCM'],
            value = int(ideal_device_state)
        )




