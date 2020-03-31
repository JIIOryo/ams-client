
SLACK_NOTIFICATION_TYPE = {
    "ERROR": "error",
    "NOTIFICATION": "notification",
}

SLACK_CREATE_DEVICE_NOTIFICATION_FORMAT = """
New device is created at {now}
device_id: {device_id}
name: {name}
description: {description}
type: {type}
"""

SLACK_UPDATE_DEVICE_NOTIFICATION_FORMAT = \
"""
This device is updated at {now}

`Before`
```
device_id: {device_id}
name: {before_name}
description: {before_description}
type: {before_type}
```

`After`
```
device_id: {device_id}
name: {after_name}
description: {after_description}
type: {after_type}
```
"""

SLACK_DELETE_DEVICE_NOTIFICATION_FORMAT = \
"""
This device is deleted at {now}
```
device_id: {device_id}
name: {name}
description: {description}
type: {type}
```
"""

SLACK_CREATE_SENSOR_NOTIFICATION_FORMAT = \
"""
New sensor is created at {now}
```
device_id: {sensor_id}
name: {name}
description: {description}
type: {type}
```
"""

SLACK_UPDATE_SENSOR_NOTIFICATION_FORMAT = \
"""
This sensor is updated at {now}

`Before`
```
sensor_id: {sensor_id}
name: {before_name}
description: {before_description}
type: {before_type}
```

`After`
```
sensor_id: {sensor_id}
name: {after_name}
description: {after_description}
type: {after_type}
```
"""

SLACK_DELETE_SENSOR_NOTIFICATION_FORMAT = \
"""
This sensor is deleted at {now}
```
sensor_id: {sensor_id}
name: {name}
description: {description}
type: {type}
```
"""

# DEVICE TYPE
DEVICE_TYPE = {
    'MAIN_LIGHT': 'main_light',
    'SUB_LIGHT': 'sub_light',
    'AIR_PUMP': 'air_pump',
    'CO2': 'co2',
    'FEED_PUMP': 'feed_pump',
    'WAVE_PUMP': 'wave_pump',
    'AUTO_FEEDER': 'auto_feeder',
    'PROTEIN_SKIMMER': 'protein_skimmer',
    'FILTER': 'filter',
}

# SENSOR TYPE
SENSOR_TYPE = {
    'WATER_TEMPERATURE': 'water_temperature',
    'ILLUMINANCE': 'illuminance',
    'WATER_LEVEL': 'water_level',
    'SUB_TANK_WATER_LEVEL': 'sub_tank_water_level',
    'ROOM_TEMPERATURE': 'room_temperature',
    'ROOM_HUMIDITY': 'room_humidity',
    'SALINITY': 'salinity',
    'WATER_FLOW_RATE': 'water_flow_rate',
    'PH': 'ph',
}

# SPI PIN (BCM)
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8

# TIMER
CRON_START_TEXT = '# ------ AMS start -------'
CRON_END_TEXT = '# ------ AMS end -------'
CRON_FORMAT = \
"""
# device_id: {device_id}
# device_name: {device_name}
# on
{on_minute} {on_hour} * * * gpio -g mode {BCM} out && gpio -g write {BCM} 1
# off
{off_minute} {off_hour} * * * gpio -g mode {BCM} out && gpio -g write {BCM} 0

"""

# CRONTAB TEMP FILE PATH
CRONTAB_TEMP_FILE_PATH = 'ams_crontab_temp.txt'

# USER (using in command `crontab -u`)
CRONTAB_USER = 'pi'

# LOG TITLE MAX CHAR
LOG_TITLE_MAX_CHAR_NUM = 14

# LOG_TITLE
LOG_TITLE = {
    'SUBSCRIBER': 'subscriber',
    'SENSOR': 'sensor'
}