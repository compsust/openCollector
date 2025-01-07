from common.datastructures.config import CollectorConfig

"""
Deals with reading and writing configuration values to the file system.
"""


class ConfigManager:
    config: CollectorConfig | None

    def __init__(self):
        pass

    def initialize_config(self) -> CollectorConfig:
        """
        Initializes config objects for all
        sensors and cache targets specified in
        the configuration file.

        Sets the config on the class, and returns it.

        Returns:
            CollectorConfig: the initialized config.
        """
        raise NotImplementedError

    def get_config(self) -> CollectorConfig:
        """
        Retrieves the device config.

        Returns:
            CollectorConfig: the current device config.
        """
        if self.config is None:
            return self.initialize_config()
        else:
            return self.config
