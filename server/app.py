import sys

from flask import Flask, render_template

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config_item, get_gpio_config
from service.device import get_all_device_state

app = Flask(__name__)
server_config = get_config_item('LOCAL_SERVER')

@app.route('/')
def index():
    devices = get_gpio_config()
    device_state = get_all_device_state()
    return render_template('index.html', devices=devices, device_state=device_state)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=server_config['PORT'])
