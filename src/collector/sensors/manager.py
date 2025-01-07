import time

from collector.config.manager import ConfigManager
from collector.sensors.driver_interface import AbstractSensorDriver
from collector.sensors.sensor_codes import get_sensor_driver_from_code
from common.datastructures import SensorError, SensorRecord, SensorReport


def generate_unique_id(device_id: str, micropython: bool) -> str:
    if micropython:
        from urandom import getrandbits

        bits = getrandbits(16)
        return f"{device_id}-{bits:04x}"
    else:
        from uuid import uuid4

        return str(uuid4())


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

            # Generate a sensor ID if one doesn't already exist
            if not sensor_config.sensor_id:
                sensor_config.sensor_id = generate_unique_id(
                    config_manager.config.collector_id, config_manager.micropython
                )

            driver = DriverClass(config=sensor_config)
            self.drivers.append(driver)

    def poll(self) -> SensorReport:
        """
        Polls all sensors.

        Returns:
            SensorReport: An object containing all recorded sensor
                data and caught sensor exceptions.
        """
        report = SensorReport(collector_id=self.collector_id, records=[], errors=[])
        timestamp = time.time()

        for driver in self.drivers:
            try:
                data = driver.poll()
                record = SensorRecord(
                    sensor_id=driver.sensor_id, data=data, timestamp=timestamp
                )
                report.records.append(record)
            except Exception as e:
                error = SensorError(
                    sensor_id=driver.sensor_id,
                    error_message=str(e),
                    timestamp=timestamp,
                )
                report.errors.append(error)

        return report
