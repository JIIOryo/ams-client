import os
import subprocess

def gpio_write(pin, value):
    """
    update gpio state

    Parameters
    ----------
    pin : int
        target gpio (BCM)
    value : int
        next state of target gpio
    """
    cmd = 'gpio -g mode {0} out && gpio -g write {0} {1}'.format(pin, value)
    os.system(cmd)
    # todo use subprocess
    # subprocess.Popen(cmd.split(), shell=True)

def gpio_read(pin):
    """
    get gpio state

    Parameters
    ----------
    pin : int
        target gpio (BCM)

    Returns
    -------
    bool
        Is target gpio turned on ?
    """
    cmd = 'gpio -g read {pin}'.format(pin = pin)
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    gpio_state = proc.stdout.readline().decode().rstrip()
    return gpio_state == '1'

