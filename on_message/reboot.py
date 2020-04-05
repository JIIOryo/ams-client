import subprocess

def reboot():
    subprocess.Popen(['sudo', 'reboot'])