import time

from collector.config import ConfigManager
from collector.sensors.driver_interface import AbstractSensorDriver
from collector.sensors.sensor_codes import get_sensor_driver_from_code
from common import SensorError, SensorRecord, SensorReport

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

    def poll(self) -> tuple[list[SensorRecord], list[SensorError]]:
        """
        Polls all sensors.

        Returns:
            tuple[list[SensorRecord], list[SensorError]]:
                all recorded sensor data and caught sensor exceptions.
        """
        records: list[SensorRecord] = []
        errors: list[SensorError] = []

        for driver in self.drivers:
            timestamp = time.time()
            try:
                data = driver.poll()
                record = SensorRecord(
                    sensor_id=driver.config.sensor_id, sensor_code=driver.config.sensor_code, data=data, timestamp=timestamp
                )
                records.append(record)
            except Exception as e:
                error = SensorError(
                    sensor_id=driver.config.sensor_id,
                    sensor_code=driver.config.sensor_code,
                    error_message=str(e),
                    timestamp=timestamp,
                )
                errors.append(error)

        return records, errors
