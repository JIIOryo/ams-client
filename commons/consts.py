
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

SLACK_UPDATE_DEVICE_NOTIFICATION_FORMAT = """
Your device settings were updated.
"""