from common import SensorCodeEnum

from .driver_interface import AbstractSensorDriver
from .drivers.dht20 import Dht20SensorDriver

"""Maps all sensor types to an implementation."""
sensor_drivers = {SensorCodeEnum.DHT20: Dht20SensorDriver}


def get_sensor_driver_from_code(
    sensor_code: SensorCodeEnum,
) -> type[AbstractSensorDriver]:
    """
    Given a sensor code, returns the associated driver class.

    Arguments:
        sensor_code (SensorCodeEnum): The code of the driver to retrieve.

    Raises:
        ValueError: Raised if there exists no driver implementation
            for the given sensor_code.

    Returns:
        type[AbstractSensorDriver]: The class implementation.
    """
    if sensor_code not in sensor_drivers or sensor_drivers[sensor_code] is None:
        raise ValueError(
            f"Sensor code: {sensor_code} not contained within the list of implemented sensor drivers."
        )
    return sensor_drivers[sensor_code]
