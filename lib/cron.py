import subprocess
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    CRONTAB_TEMP_FILE_PATH,
    CRONTAB_USER,
)

def get_crontab():
    """
    get current crontab

    Returns
    -------
    list[str]
        All texts in crontab.
        e.g. ['0 10 * * * command hoge', '', '@reboot command fuga']
    """
    return subprocess.check_output(['crontab', '-l']).decode().split('\n')

def write_to_crontab(new_crontab):
    """
    write new crontab to current crontab

    Parameters
    ----------
    new_crontab : str
        new crontab
        old crontab + new timer setting
    """

    # create temp file
    with open(CRONTAB_TEMP_FILE_PATH, 'w') as f:
        f.write(new_crontab)
    
    # write new timer setting to crontab 
    subprocess.Popen(['crontab', '-u', CRONTAB_USER, CRONTAB_TEMP_FILE_PATH])

    # subprocess.Popen(['rm', CRONTAB_TEMP_FILE_PATH])
