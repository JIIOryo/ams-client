
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

# SPI PIN (BCM)
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8