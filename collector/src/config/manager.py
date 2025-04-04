import json
from typing import Any

from common.src import CollectorMetadata, SensorMetadata
from .datastructures import CollectorConfig, DeviceConfig, SensorConfig, UploadConfig

"""
Deals with reading and writing configuration values to the file system.
"""


class ConfigManager:
    """
    Parses and stores all configured paramteres for a collector node.

    Attributes:
        micropython: If true, the program is being run within
            a micropython environment.
        _config: The config, or None if it
            has not been successfully parsed.
    """

    micropython: bool = True
    _config: CollectorConfig | None = None

    def __init__(self, micropython: bool):
        """
        Initialize the config manager.

        Args:
            micropython: If true, the program is being run within
                a micropython environment.
        """
        self.micropython = micropython
        self.initialize_config()

    def initialize_config(self):
        """
        Initializes config objects for all
        configuration parameters contained within the
        configuration file and sets the config on the class.

        Raises:
            ValueError: Raised if any config is missing.
        """
        # Load config into a dictionary.
        with open("config.json") as f:
            config: dict[str, Any] = json.load(f)

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
            The current device config.
        """
        if self._config is None:
            self.initialize_config()
            if self._config is None:
                raise Exception("Failed to load device config.")

        return self._config

    @property
    def metadata(self) -> tuple[CollectorMetadata, list[SensorMetadata]]:
        """
        Packages the configuration into the metadata objects.

        Returns:
            The metadata.
        """
        collector_metadata = CollectorMetadata(
            collector_id=self.config.collector_id,
            collector_name=self.config.node_name,
            device_model=self.config.device.model,
            polling_interval=self.config.polling_interval,
        )
        sensor_metadata = []
        for sensor in self.config.sensors:
            sensor_metadata.append(
                SensorMetadata(
                    collector_id=self.config.collector_id,
                    sensor_id=sensor.sensor_id,
                    sensor_code=sensor.sensor_code,
                    sensor_name=sensor.name,
                )
            )
        return collector_metadata, sensor_metadata
