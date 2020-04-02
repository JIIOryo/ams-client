import os
import sys
import time

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    FEED_PUMP_DEFAULT_TIME,
)
from lib.gpio import gpio_write, gpio_read

def feed_pump(pin, water_feed_time = FEED_PUMP_DEFAULT_TIME):
    """
    feed water

    Parameters
    ----------
    pin : int
        target gpio (BCM)
    water_feed_time : int
        water feeding time
    
    Returns
    -------
    bool
        Was water feeding successful ?
    """
    is_running = gpio_read(pin)
    if is_running:
        return False
    
    gpio_write(pin, 1)
    time.sleep(water_feed_time)
    gpio_write(pin, 0)

    return True
