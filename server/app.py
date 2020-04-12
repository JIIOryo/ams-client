import sys

from flask import Flask

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config_item

app = Flask(__name__)

server_config = get_config_item('LOCAL_SERVER')

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=server_config['PORT'])
