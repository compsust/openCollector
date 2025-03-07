try:
    import micropython

    IS_MICROPYTHON = True
except ImportError:
    IS_MICROPYTHON = False

import time

from common.src import CollectorReport, CollectorError

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

    # TODO: Update metadata table
    # upload_manager.upload_metadata()

    # Store errors that don't happen during the sensor polling.
    errors: list[CollectorError] = []

    # Loop
    while ():
        records, errors = sensor_manager.poll()
        report = CollectorReport(
            collector_id=config_manager.config.collector_id,
            records=records,
            errors=errors,
        )

        # Timestamp in microseconds.
        timestamp = time.time() * 1000 * 1000

        # Try to upload the data. If unsuccessful, save the error for upload next loop.
        try:
            upload_manager.upload(report, errors)
            errors = []
        except Exception as e:
            errors.append(
                CollectorError(
                    sensor_id=None, error_message=str(e), timestamp=timestamp
                )
            )

        time.sleep(config_manager.config.polling_interval)


if __name__ == "__main__":
    # Run the main function
    main()
