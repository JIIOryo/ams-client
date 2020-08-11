
class SensorAlreadyExist(Exception):
    pass

class SensorTypeNotExist(Exception):
    pass

class SensorNotFound(Exception):
    pass

class DeviceAlreadyExist(Exception):
    pass

class DeviceNotFound(Exception):
    pass

class DeviceTypeUndefined(Exception):
    pass

class DeviceRunTypeUndefined(Exception):
    pass

class DeviceOtherError(Exception):
    pass

class CameraNotFound(Exception):
    pass

class CameraServerNotRunningError(Exception):
    pass

class AlbumNotFound(Exception):
    pass

class S3UploadFailedError(Exception):
    pass

class MqttNotAuthorisedError(Exception):
    pass

class MqttNoRouteToHostError(Exception):
    pass

class FormatInvalid(Exception):
    pass

class NotificationTypeUndefined(Exception):
    pass

class UnknownError(Exception):
    pass
