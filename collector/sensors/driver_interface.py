from typing import Protocol
from collector.datastructures import SensorData


class AbstractSensorDriver(Protocol):
    """
    Interface used to describe a type of sensor.
    """

    def poll() -> SensorData:
        """
        Utilizes the underlying device driver to collect sensor data.

        Returns:
            SensorData: The data returned by the sensor.
        """
        ...
