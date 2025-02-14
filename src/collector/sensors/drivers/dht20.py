from common import SensorData

from ..driver_interface import AbstractSensorDriver


class Dht20SensorDriver(AbstractSensorDriver):
    """
    Implementation of the Dht20 Sensor Driver.
    """

    def poll(self) -> SensorData:
        """
        Utilizes the underlying device driver to collect sensor data.

        Returns:
            SensorData: The data returned by the sensor.
        """

        # Note that SensorData must be a dict with the following structure,
        # as defined within the sensor metadata used by the display node.
        return {"temperature": 10, "humidity": 10}
