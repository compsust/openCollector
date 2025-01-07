from collector.config.manager import ConfigManager
from common.datastructures import SensorReport


class SensorManager:
    def __init__(self, config_manager: ConfigManager) -> None:
        """
        Initializes all SensorDrivers.
        """
        raise NotImplementedError

    def poll(self) -> SensorReport:
        """
        Polls all sensors.

        Returns:
            SensorReport: An object containing all recorded sensor
                data and caught sensor exceptions.
        """
        raise NotImplementedError
