import os
import sys
import time

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config_item
from lib.gpio import gpio_write, gpio_read
from service.device import publish_device_state

def feed_pump(pin: int) -> bool:
    """
    feed water

    Parameters
    ----------
    pin : int
        target gpio (BCM)
    
    Returns
    -------
    bool
        Auto feeding successful
    """
    is_running = gpio_read(pin)
    if is_running:
        return False
    
    AUTO_FEEDER_RUN_TIME = get_config_item('DEVICE')['AUTO_FEEDER_RUN_TIME']
    
    # auto feeder on
    gpio_write(pin, 1)
    try:
        publish_device_state()
    except:
        gpio_write(pin, 0)
        return False
    
    time.sleep(AUTO_FEEDER_RUN_TIME)
    # pump off
    gpio_write(pin, 0)
    publish_device_state()
    
    return True
