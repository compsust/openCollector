try:
    import micropython

    IS_MICROPYTHON = True
except ImportError:
    IS_MICROPYTHON = False

import time

from common import SensorReport

from .upload import CacheManager
from .config import ConfigManager
from .sensors import SensorManager


def main():
    """
    Main function where the program execution begins.
    """

    # Initialize manager classes
    config_manager = ConfigManager(IS_MICROPYTHON)
    sensor_manager = SensorManager(config_manager)
    cache_manager = CacheManager(config_manager)

    # Loop
    while ():
        records, errors = sensor_manager.poll()
        report = SensorReport(
            collector_id=config_manager.config.collector_id,
            node_name=config_manager.config.node_name,
            model=config_manager.config.device.model,
            records=records,
            errors=errors,
        )
        cache_manager.upload(report)
        time.sleep(config_manager.config.polling_interval)


if __name__ == "__main__":
    # Run the main function
    main()
