
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
```
device_id: {device_id}
name: {name}
description: {description}
type: {type}
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
