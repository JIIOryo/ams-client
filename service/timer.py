import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    CRON_START_TEXT,
    CRON_END_TEXT,
    CRON_FORMAT,
)

from lib.config import get_gpio_config


def cron_text_generator():
    """
    This text is generated by this function.
    
    # ------ AMS start -------
    # device_id: 1
    # device_name: my_main_light
    # on
    30 10 * * * gpio -g mode 26 out && gpio -g write 26 1
    # off
    30 18 * * * gpio -g mode 26 out && gpio -g write 26 0

    # device_id: 2
    # device_name: my_sub_light
    # on
    30 10 * * * gpio -g mode 19 out && gpio -g write 19 1
    # off
    30 18 * * * gpio -g mode 19 out && gpio -g write 19 0

    ...

    # device_id: 5
    # device_name: my_air_pump
    # on
    30 17 * * * gpio -g mode 19 out && gpio -g write 19 1
    # off
    0 10 * * * gpio -g mode 19 out && gpio -g write 19 0
    # ------ AMS end -------

    """
    gpio_config = get_gpio_config()

    # initial value
    cron_text = CRON_START_TEXT + '\n'

    for device in gpio_config:

        # if device does not exist
        if device['device'] == {}:
            continue
        
        # if the device runs continuously like a wave pump
        if device['device']['options']['continuous']:
            continue
        
        timer = device['device']['options']['timer']

        cron_text += CRON_FORMAT.format(
            device_id = device['device_id'],
            device_name = device['device']['name'],
            BCM = device['BCM'],
            on_minute = timer['on_minute'],
            on_hour = timer['on_hour'],
            off_minute = timer['off_minute'],
            off_hour = timer['off_hour'],
        )
    
    cron_text += CRON_END_TEXT

    return cron_text
