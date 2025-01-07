from common.datastructures.sensors import SensorCodeEnum

from .driver_interface import AbstractSensorDriver
from .drivers.example import ExampleSensorDriver

"""Maps all sensor types to an implementation."""
sensor_drivers = {
    # TODO: Replace with the first implemented sensor
    SensorCodeEnum.FIRST_SENSOR_EXAMPLE: ExampleSensorDriver
}


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
    raise NotImplementedError
