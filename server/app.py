import json
import os
import sys

from flask import Flask, render_template, request, send_from_directory

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config_item, get_gpio_config, get_config, set_config
from on_message.device_control import device_control
from on_message.device_update import device_update
from on_message.reboot import reboot
from service.device import get_all_device_state

app = Flask(__name__)
server_config = get_config_item('LOCAL_SERVER')

empty_response = json.dumps({})

@app.route('/')
def index():
    with open('index.html') as f:
        html = f.read()
    return html

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/setting', methods=['GET'])
def get_setting():
    config = get_config()
    return json.dumps(config)

@app.route('/setting', methods=['POST'])
def set_setting():
    print(request.json)
    set_config(request.json)
    return empty_response

@app.route('/devices')
def get_devices():
    devices = get_gpio_config()
    return json.dumps(devices)

@app.route('/devices/state')
def get_all_device_state_():
    devices = get_all_device_state()
    return json.dumps(devices)

@app.route('/device/update', methods=['POST'])
def device_update_():
    print(request.json)
    device_update(message = request.data)
    return empty_response

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
