from typing import Protocol

from collector.config.datastructures import SensorConfig
from common import SensorData


class AbstractSensorDriver(Protocol):
    """
    Interface used to describe a type of sensor.
    """

    config: SensorConfig

    def __init__(self, config: SensorConfig):
        # Note that we may want to do some validation here,
        # as currently the sensor attributes within SensorConfig
        # is just a dict. Though I'm not sure DHT22 needs any extra attributes.
        self.config = config

    def poll(self) -> SensorData:
        """
        Utilizes the underlying device driver to collect sensor data.

        Returns:
            SensorData: The data returned by the sensor.
        """
        ...
