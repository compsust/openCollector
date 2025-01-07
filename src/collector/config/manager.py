import json

from common.datastructures.config import CollectorConfig

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
        with open("config.json") as f:
            config = json.load(f)
            # Load config into typed config somehow

        # Generate an ID for this device if not included
        if not config.collector_id:
            if self.micropython:
                from machine import unique_id

                config.collector_id = unique_id().hex()
            else:
                from uuid import uuid4

                config.collector_id = uuid4()

        self._config = config

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
            raise Exception("Failed to load device config..")
        return self._config
