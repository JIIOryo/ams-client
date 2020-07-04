import json
import os
import sys

from flask import Flask, render_template, request, send_from_directory, jsonify, make_response, current_app

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.errors import (
    FormatInvalid,
)
from lib.config import get_config_item, get_gpio_config, get_config, set_config, get_sensor_config
from on_message.device_control import device_control
from on_message.device_create import device_create
from on_message.device_update import device_update
from on_message.device_delete import device_delete
from on_message.device_exchange import device_exchange
from on_message.sensor_exchange import sensor_exchange
from on_message.sensor_create import sensor_create
from on_message.reboot import reboot
from on_message.device_feed_pump import device_feed_pump
from on_message.device_auto_feeder import device_auto_feeder
from on_message.sensor_update import sensor_update, sensor_calibration_update
from on_message.sensor_delete import sensor_delete
from service.device import get_all_device_state
from service.sensor import get_current_sensor_values
from service.backup import backup_file_name, get_device_backup_file, import_device_back_file, get_sensor_backup_file, import_sensor_back_file
from service.logger import (
    logger,
    DEBUG,
    INFO,
    WARN,
    ERROR,
    FATAL,
)

app = Flask(__name__)
server_config = get_config_item('LOCAL_SERVER')

empty_response = json.dumps({})

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def flask_logger_message(method: str, path: str, data: str, remote_addr: str, user_agent: str) -> str:
    logger_message = f"""
    {method} {path}
    From {remote_addr} {user_agent}
"""
    if len(data) > 0:
        logger_message += f'    Body {data}' 
    return logger_message

def ams_logger(req, log_level: str, notification: bool = False):
    message = flask_logger_message(
        method = req.method,
        path = req.path,
        data = req.data.decode(),
        remote_addr = req.remote_addr,
        user_agent = req.user_agent,
    )
    logger(log_level, message, notification)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def index():
    ams_logger(request, INFO)
    with open('index.html') as f:
        html = f.read()
    return html

@app.route('/ping')
def ping():
    ams_logger(request, DEBUG)
    return empty_response

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/setting', methods=['GET'])
def get_setting():
    ams_logger(request, DEBUG)
    config = get_config()
    return json.dumps(config)

@app.route('/setting', methods=['POST'])
def set_setting():
    ams_logger(request, INFO, True)
    set_config(request.json)
    return empty_response

@app.route('/devices')
def get_devices():
    ams_logger(request, DEBUG)
    devices = get_gpio_config()
    return json.dumps(devices)

@app.route('/devices/state')
def get_all_device_state_():
    ams_logger(request, DEBUG)
    devices = get_all_device_state()
    return json.dumps(devices)

@app.route('/device/create', methods=['POST'])
def device_create_():
    ams_logger(request, INFO, True)
    device_create(message = request.data)
    return empty_response

@app.route('/device/update', methods=['POST'])
def device_update_():
    ams_logger(request, INFO, True)
    device_update(message = request.data)
    return empty_response

@app.route('/device/control', methods=['POST'])
def device_control_():
    ams_logger(request, INFO, True)
    device_control(message = request.data)
    return empty_response

@app.route('/device/delete/<int:device_id>', methods=['DELETE'])
def device_delete_(device_id: int):
    ams_logger(request, INFO, True)
    device_delete(message = json.dumps({
        'device_id': device_id,
    }))
    return empty_response

@app.route('/device/exchange', methods=['POST'])
def device_exchange_():
    ams_logger(request, INFO, True)
    device_exchange(message = request.data)
    return empty_response

@app.route('/device/control/feed_pump/<int:device_id>', methods=['POST'])
def add_water(device_id):
    '''
    request example
    {"warter_supply_time": 120}
    '''
    ams_logger(request, INFO, True)
    water_supply_time = request.json['water_supply_time']
    device_feed_pump(json.dumps({
        "device_id": device_id,
        "water_supply_time": water_supply_time,
    }))
    return empty_response

@app.route('/device/control/auto_feeder/<int:device_id>', methods=['POST'])
def feed(device_id):
    '''
    request example
    {}
    '''
    ams_logger(request, INFO, True)
    device_auto_feeder(json.dumps({
        "device_id": device_id,
    }))
    return empty_response

@app.route('/sensors')
def get_sensors():
    ams_logger(request, DEBUG)
    sensors = get_sensor_config()
    return jsonify(sensors)

@app.route('/sensors/value')
def get_sensor_value():
    ams_logger(request, DEBUG)
    current_sensor_values = get_current_sensor_values()
    return jsonify(current_sensor_values)

@app.route('/sensor/create', methods=['POST'])
def sensor_create_():
    ams_logger(request, INFO, True)
    sensor_create(message = request.data)
    return empty_response

@app.route('/sensor/exchange', methods=['POST'])
def sensor_exchange_():
    ams_logger(request, INFO, True)
    sensor_exchange(message = request.data)
    return empty_response

@app.route('/sensor/update', methods=['POST'])
def sensor_update_():
    ams_logger(request, INFO, True)
    sensor_update(message = request.data)
    return empty_response

@app.route('/sensor/calibration/update/<int:sensor_id>', methods=['POST'])
def sensor_calibration_update_(sensor_id):
    '''
    request example
    {
        "calibration": [[1900, 21], [1910, 21.3], [2010, 23.8]]
    }
    '''
    ams_logger(request, INFO, True)
    sensor_calibration_update(
        sensor_id = sensor_id,
        calibration = request.json['calibration']
    )
    return empty_response

@app.route('/sensor/delete/<int:sensor_id>', methods=['DELETE'])
def sensor_delete_(sensor_id: int):
    ams_logger(request, INFO, True)
    sensor_delete(message = json.dumps({
        'sensor_id': sensor_id,
    }))
    return empty_response

@app.route('/reboot')
def reboot_():
    ams_logger(request, WARN, True)
    reboot()
    return empty_response

@app.route('/device/backup')
def device_backup():
    ams_logger(request, INFO, True)
    downloadFileName = backup_file_name(
        type_ = 'device',
        ext = 'json',
    )
    response = make_response(
        json.dumps(
            get_device_backup_file(),
            ensure_ascii = False,
        )
    )
    response.headers['Content-Disposition'] = 'attachment; filename=' + downloadFileName
    response.mimetype = 'application/json'
    return response

@app.route('/device/backup', methods=['POST'])
def device_backup_post():
    ams_logger(request, WARN, True)
    try:
        import_device_back_file(backup_file = request.json)
    except FormatInvalid as e:
        raise InvalidUsage('format is invalid', status_code=400)

    return empty_response

@app.route('/sensor/backup')
def sensor_backup():
    ams_logger(request, INFO, True)
    downloadFileName = backup_file_name(
        type_ = 'sensor',
        ext = 'json',
    )
    response = make_response(
        json.dumps(
            get_sensor_backup_file(),
            ensure_ascii = False,
        )
    )
    response.headers['Content-Disposition'] = 'attachment; filename=' + downloadFileName
    response.mimetype = 'application/json'
    return response

@app.route('/sensor/backup', methods=['POST'])
def sensor_backup_post():
    ams_logger(request, WARN, True)
    try:
        import_sensor_back_file(backup_file = request.json)
    except FormatInvalid as e:
        raise InvalidUsage('format is invalid', status_code=400)

    return empty_response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=server_config['PORT'])
