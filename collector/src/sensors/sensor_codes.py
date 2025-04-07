from common import SensorCodeEnum

from .driver import AbstractSensorDriver
from . import drivers


sensor_drivers = {
    SensorCodeEnum.MOCK: {
        "python": drivers.MockSensorDriver,
        "micropython": drivers.MockSensorDriver,
    },
    SensorCodeEnum.DHT20: {
        "python": drivers.DHT20SensorDriverPython,
        "micropython": drivers.DHT20SensorDriverMicropython,
    },
    SensorCodeEnum.MHZ19B: {
        "python": drivers.MHZ19BSensorDriverPython,
        "micropython": drivers.MHZ19BSensorDriverMicropython,
    },
    SensorCodeEnum.PMS5003: {
        "python": drivers.PMS5003SensorDriverPython,
        "micropython": drivers.PMS5003SensorDriverMicropython,
    },
    SensorCodeEnum.TSL2561: {
        "python": drivers.TSL2561SensorDriverPython,
        "micropython": drivers.TSL2561SensorDriverMicropython,
    },
}
"""Maps all sensor types to an implementation."""


def get_sensor_driver_from_code(
    sensor_code: SensorCodeEnum, micropython: bool
) -> type[AbstractSensorDriver]:
    """
    Given a sensor code, returns the associated driver class.

    Arguments:
        sensor_code: The code of the driver to retrieve.
        micropython: If true, the micropython driver will be retrieved.

    Raises:
        ValueError: Raised if there exists no driver implementation
            for the given sensor_code.

    Returns:
        The class implementation.
    """
    if sensor_code not in sensor_drivers or sensor_drivers[sensor_code] is None:
        raise ValueError(
            f"Sensor code: {sensor_code} not contained within the list of implemented sensor drivers."
        )
    if micropython:
        return sensor_drivers[sensor_code]["micropython"]
    else:
        return sensor_drivers[sensor_code]["python"]
