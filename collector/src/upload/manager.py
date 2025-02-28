import requests
from collector.src.config.datastructures import UploadConfig
from config.manager import ConfigManager
from common import SensorReport


class UploadManager:
    config: UploadConfig

    def __init__(self, config_manager: ConfigManager):
        """
        Initializes the manager.
        """
        self.config = config_manager.config.upload

    def upload(self, report: SensorReport):
        raise NotImplementedError
