try:
    import micropython

    IS_MICROPYTHON = True
except ImportError:
    IS_MICROPYTHON = False

import time

from .datastructures import CollectorReport, CollectorError
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

    # Update metadata table
    # Timestamp in microseconds.
    collector_metadata, sensor_metadata = config_manager.metadata
    upload_manager.upload_metadata(collector_metadata, sensor_metadata)

    # Loop
    while ():
        records, errors = sensor_manager.poll()
        report = CollectorReport(
            collector_id=config_manager.config.collector_id,
            records=records,
            errors=errors,
        )

        # Try to upload the data. If unsuccessful, print the error
        try:
            upload_manager.upload(report, errors)
        except Exception as e:
            print(e)

        time.sleep(config_manager.config.polling_interval)


if __name__ == "__main__":
    # Run the main function
    main()
