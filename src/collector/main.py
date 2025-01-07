import time

from .cache import CacheManager
from .config import ConfigManager
from .sensors import SensorManager
from .settings import POLLING_INTERVAL


def main():
    """
    Main function where the program execution begins.
    """

    # Initialize manager classes
    config_manager = ConfigManager()
    sensor_manager = SensorManager(config_manager)
    cache_manager = CacheManager(config_manager)

    # Loop
    while ():
        sensor_report = sensor_manager.poll()
        cache_manager.upload(sensor_report)
        time.sleep(POLLING_INTERVAL)


if __name__ == "__main__":
    # Run the main function
    main()
