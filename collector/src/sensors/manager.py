import time

from config import ConfigManager
from sensors.driver_interface import AbstractSensorDriver
from sensors.sensor_codes import get_sensor_driver_from_code
from common.src import CollectorError, CollectorRecord, CollectorReport


class SensorManager:
    collector_id: str
    drivers: list[AbstractSensorDriver] = []

    def __init__(self, config_manager: ConfigManager):
        """
        Initializes all SensorDrivers.
        """
        self.collector_id = config_manager.config.collector_id

        for sensor_config in config_manager.config.sensors:
            # Retrieve the driver class for this sensor.
            DriverClass = get_sensor_driver_from_code(sensor_config.sensor_code)

            driver = DriverClass(config=sensor_config)
            self.drivers.append(driver)

    def poll(self) -> tuple[list[CollectorRecord], list[CollectorError]]:
        """
        Polls all sensors.

        Returns:
            tuple[list[CollectorRecord], list[CollectorError]]:
                all recorded sensor data and caught sensor exceptions.
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
