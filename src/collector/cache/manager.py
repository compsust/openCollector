from collector.config.manager import ConfigManager
from common.sensors import SensorReport


class CacheManager:
    def __init__(self, config_manager: ConfigManager):
        raise NotImplementedError

    def upload(self, report: SensorReport):
        raise NotImplementedError
