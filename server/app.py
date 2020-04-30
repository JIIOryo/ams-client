import json
import sys

from flask import Flask, render_template, request

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config_item, get_gpio_config
from on_message.device_control import device_control
from on_message.reboot import reboot
from service.device import get_all_device_state

app = Flask(__name__)
server_config = get_config_item('LOCAL_SERVER')

empty_response = json.dumps({})

@app.route('/')
def index():
    devices = get_gpio_config()
    device_state = get_all_device_state()
    return render_template('index.html', devices=devices, device_state=device_state)

@app.route('/devices')
def get_devices():
    devices = get_gpio_config()
    return json.dumps(devices)

@app.route('/device/control', methods=['POST'])
def device_control_():
    print(request.json)
    device_control(message = request.data)
    return empty_response

@app.route('/reboot')
def reboot_():
    reboot()
    return empty_response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=server_config['PORT'])
