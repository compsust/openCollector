import time

from config import ConfigManager
from collector.src.sensors.driver import AbstractSensorDriver
from sensors.sensor_codes import get_sensor_driver_from_code
from datastructures import CollectorRecord, CollectorError


class SensorManager:
    """
    Initializes and orchestrates the configured
    sensor drivers.

    Attributes:
        collector_id: The configured collector ID.
        drivers: The driver instances, or an empty list
            if they have yet to be initialized.
    """

    collector_id: str
    drivers: list[AbstractSensorDriver] = []

    def __init__(self, config_manager: ConfigManager):
        """
        Initializes all SensorDrivers.

        Args:
            config_manager: ConfigManager instance
                used to retrieve the sensor configs.
        """
        self.collector_id = config_manager.config.collector_id

        for sensor_config in config_manager.config.sensors:
            # Retrieve the driver class for this sensor.
            DriverClass = get_sensor_driver_from_code(
                sensor_config.sensor_code, config_manager.micropython
            )

            driver = DriverClass(config=sensor_config)
            self.drivers.append(driver)

    def poll(self) -> tuple[list[CollectorRecord], list[CollectorError]]:
        """
        Polls all sensors.

        If the sensor returns data, uses it to construct a CollectorRecord.

        If the sensor raises an exception, uses it to construct a CollectorError.

        Returns:
            All recorded sensor data and caught sensor exceptions.
        """
        records: list[CollectorRecord] = []
        errors: list[CollectorError] = []

        for driver in self.drivers:
            # Timestamp in microseconds.
            timestamp = time.time() * 1000 * 1000
            try:
                data = driver.poll()
                record = CollectorRecord(
                    sensor_id=driver.config.sensor_id, data=data, timestamp=timestamp
                )
                records.append(record)
            except Exception as e:
                error = CollectorError(
                    sensor_id=driver.config.sensor_id,
                    error_message=str(e),
                    timestamp=timestamp,
                )
                errors.append(error)

        return records, errors
