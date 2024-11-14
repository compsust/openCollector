from enum import Enum
from .driver_interface import AbstractSensorDriver
from .drivers.example import ExampleSensorDriver


class SensorCodeEnum(Enum):
    """
    Contains an enumerated value
    for all supported sensor types.

    Each value will be mapped to a
    specific implementation of
    AbstractSensorDriver.
    """

    # TODO: Replace with the first implemented sensor
    FIRST_SENSOR_EXAMPLE = 0


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
