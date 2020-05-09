import os
import sys
import time

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config_item
from lib.gpio import gpio_write, gpio_read
from service.device import publish_device_state

FEED_PUMP_DEFAULT_TIME = get_config_item('DEVICE')['FEED_PUMP_DEFAULT_TIME']

def feed_pump(pin: int, water_supply_time: int=FEED_PUMP_DEFAULT_TIME) -> bool:
    """
    feed water

    Parameters
    ----------
    pin : int
        target gpio (BCM)
    water_supply_time : int
        water feeding time
    
    Returns
    -------
    bool
        Was water feeding successful ?
    """
    is_running = gpio_read(pin)
    if is_running:
        return False
    
    # pump on
    gpio_write(pin, 1)
    try:
        publish_device_state()
    except:
        gpio_write(pin, 0)
        return False
    
    time.sleep(water_supply_time)
    # pump off
    gpio_write(pin, 0)
    publish_device_state()
    
    return True
