import datetime
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.errors import (
    FormatInvalid,
)
from lib.config import get_gpio_config, set_gpio_config, get_config_item

def backup_file_now_date_generator() -> str:
    return datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S')

def backup_file_name(type_: str, ext: str) -> str:
    """
    Parameters
    ----------
    type_ : str
        backup type (device|sensor)
    ext : str
        backup file extention (json| ...)
    
    Returns
    ----------
    str
        backup_file_name
        e.g.
        device_20191010_10_00_00.json
    """
    return '{type}_{date}.{ext}'.format(
        type = type_,
        date = backup_file_now_date_generator(),
        ext = ext,
    )

def get_device_backup_file() -> str:
    return get_gpio_config()

def import_device_back_file(backup_file: list) -> None:
    MAX_DEVICE_NUMBER = get_config_item('MAX_DEVICE_NUMBER')

    if len(backup_file) != MAX_DEVICE_NUMBER:
        raise FormatInvalid('Device number invalid')

    # TODO Validation

    set_gpio_config(backup_file)
    return
