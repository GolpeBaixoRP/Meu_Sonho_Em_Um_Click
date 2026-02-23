from services import *


class Container:

    def __init__(self):
        from services.device_service import DeviceService
        self.deviceService = DeviceService()
