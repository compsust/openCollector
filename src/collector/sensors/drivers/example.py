from ..driver_interface import AbstractSensorDriver
from collector.datastructures import SensorData


class ExampleSensorDriver(AbstractSensorDriver):
    """
    Example implementation.

    TODO: Replace with the actual first sensor used.
    """

    def poll() -> SensorData:
        """
        Utilizes the underlying device driver to collect sensor data.

        Returns:
            SensorData: The data returned by the sensor.
        """
        raise NotImplementedError
