import json
from typing import Any

from .datastructures import CollectorConfig, DeviceConfig, SensorConfig, UploadConfig
from .utils import generate_unique_id

"""
Deals with reading and writing configuration values to the file system.
"""


class ConfigManager:
    # If true, the code is being run on micropython
    micropython: bool = True
    _config: CollectorConfig | None = None

    def __init__(self, micropython: bool):
        self.micropython = micropython
        self.initialize_config()

    def initialize_config(self):
        """
        Initializes config objects for all
        sensors and cache targets specified in
        the configuration file.

        Sets the config on the class.
        """
        # Load config into a dictionary.
        with open("config.json") as f:
            config: dict[str, Any] = json.load(f)

        # Generate an ID for this device if not included
        if "collector_id" not in config or config["collector_id"] is None:
            config["collector_id"] = generate_unique_id(self.micropython)

        # Initialize all configs

        # Device config
        if "device" not in config:
            raise ValueError("Config missing device config.")
        device_config = DeviceConfig(config["device"], self.micropython)

        # Upload config
        if "upload" not in config:
            raise ValueError("Config missing upload config.")
        upload_config = UploadConfig(config["upload"])

        # Sensor configs
        if "sensors" not in config:
            raise ValueError("Config missing sensors config.")

        sensors: list[SensorConfig] = []
        for config, index in config["sensors"]:
            # Generate an ID for this device if not included
            if "sensor_id" not in config or config["sensor_id"] is None:
                config["sensor_id"] = generate_unique_id(self.micropython)

            sensor = SensorConfig(config, index, device_config.allowed_gpio)
            sensors.append(sensor)

        # Collector config
        collector_config = CollectorConfig(
            config, device_config, upload_config, sensors
        )

        self._config = collector_config

    @property
    def config(self) -> CollectorConfig:
        """
        Retrieves the device config.

        Returns:
            CollectorConfig: the current device config.
        """
        if self._config is None:
            self.initialize_config()
            if self._config is None:
                raise Exception("Failed to load device config.")

        return self._config
