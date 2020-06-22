import datetime
import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )


# from commons.errors import (
#     # SensorNotFound,
# )
from commons.consts import (
    SLACK_NOTIFICATION_TYPE,
)

from lib.config import get_config, get_sensor_config, set_sensor_config
from lib.notification import post_slack_by_type

"""
input
A: [6, 4, 5, 2, 3, 1]
B: [
    {"sensor_id":1, "sensor": {...1} ...},
    {"sensor_id":2, "sensor": {...2} ...},
    {"sensor_id":3, "sensor": {...3} ...},
    {"sensor_id":4, "sensor": {...4} ...},
    {"sensor_id":5, "sensor": {...5} ...},
    {"sensor_id":6, "sensor": {...6} ...}
]

output
X: [
    {"sensor_id":1, "sensor": {...6} ...},
    {"sensor_id":2, "sensor": {...4} ...},
    {"sensor_id":3, "sensor": {...5} ...},
    {"sensor_id":4, "sensor": {...2} ...},
    {"sensor_id":5, "sensor": {...3} ...},
    {"sensor_id":6, "sensor": {...1} ...}
]
"""
def exchanged(A: list, B: list) -> list:
    only_exchanged, result = [dict(B[a-1]) for a in A], []
    for i, o in enumerate(only_exchanged):
        o.update(sensor_id = i+1)
        result.append(o)
    return result

"""
# message 
type: json str
-----
{
    "sensors": [1, 2, 3, 6, 4, 5]
}
"""

def sensor_exchange(message: dict) -> None:
    exchange_sensors = json.loads(message)['sensors']
    sensor_config = get_sensor_config()

    result = exchanged(exchange_sensors, sensor_config)
    
    set_sensor_config(result)

    post_slack_by_type(
        text = 'Sensors are exchanged.',
        type_ = SLACK_NOTIFICATION_TYPE['NOTIFICATION']
    )
