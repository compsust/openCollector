from ...config import SensorConfig
from ...datastructures import SensorData
from ..driver import AbstractSensorDriver


class MockSensorDriver(AbstractSensorDriver):
    """
    An interface used to describe a type of sensor.

    Attributes:
        config: The parsed config object for this sensor.
    """

    config: SensorConfig

    def __init__(self, config: SensorConfig):
        """
        Initialize the sensor driver.

        Args:
            config: The parsed config object for this sensor.
        """
        self.config = config

    def poll(self) -> SensorData:
        """
        Utilizes the underlying device driver to collect sensor data.

        Returns:
            The data returned by the sensor.

        Raises:
            Exception: Raised if the sensor fails to return data.
        """
        return {"temperature": 20, "humidity": 30}
