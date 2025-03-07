try:
    import micropython

    IS_MICROPYTHON = True
except ImportError:
    IS_MICROPYTHON = False

import time

from common.src import SensorReport

from .upload import UploadManager
from .config import ConfigManager
from .sensors import SensorManager


def main():
    """
    Main function where the program execution begins.
    """

    # Initialize manager classes
    config_manager = ConfigManager(IS_MICROPYTHON)
    sensor_manager = SensorManager(config_manager)
    upload_manager = UploadManager(config_manager)

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
        upload_manager.upload(report)
        time.sleep(config_manager.config.polling_interval)


if __name__ == "__main__":
    # Run the main function
    main()
