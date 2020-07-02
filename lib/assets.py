import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config_item

AMS_ROOT_PATH = get_config_item('ROOT_PATH')
AMS_BOOT_ASCII_ART_PATH = '/'.join([AMS_ROOT_PATH, 'assets', 'ascii_art', 'ams_boot.txt'])

def get_boot_ascii_art():
    with open(AMS_BOOT_ASCII_ART_PATH) as f:
        return f.read()