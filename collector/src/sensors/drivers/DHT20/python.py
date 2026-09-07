from ....config import SensorConfig
from ....datastructures import SensorData
from ...driver import AbstractSensorDriver


class DHT20SensorDriverPython(AbstractSensorDriver):
    """
    Implementation of the Dht20 Sensor Driver for python.
    """

    config: SensorConfig

    def __init__(self, config: SensorConfig):
        """
        Initialize the sensor driver.

        Args:
            config: The parsed config object for this sensor.
        """
        self.config = config
        raise NotImplementedError

    def poll(self) -> SensorData:
        """
        Utilizes the underlying device driver to collect sensor data.

        Returns:
            The data returned by the sensor.

        Raises:
            Exception: Raised if the sensor fails to return data.
        """
        raise NotImplementedError
