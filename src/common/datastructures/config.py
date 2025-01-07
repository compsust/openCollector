from enum import Enum
from typing import Any, NamedTuple

from .sensors import SensorCodeEnum


class DeviceTypeEnum(Enum):
    """
    Contains an enumerated value
    for all supported devices.
    """

    GENERIC = "generic"
    PI_PICO = "raspi-pico"


class CacheConfig(NamedTuple):
    """
    Configuration object which describes a Memcached target.
    Attributes:
        cache_id (str): An ID associated with the target.
        name (str): A descriptive name for the target.
        endpoint (str): The URI through which the cache target node may
            accept requests.
    """

    cache_id: str
    name: str
    endpoint: str


class SensorConfig(NamedTuple):
    """
    Configuration object which describes a sensor.
    Attributes:
        sensor_id (str): An ID associated with the sensor.
        sensor_code (SensorCodeEnum): Associated with
            a specific implementation of AbstractSensorDriver.
        name (str): A descriptive name for the sensor.
        attributes (dict[str, Any]): Any other attributes
            which are required to use the sensor. For example,
            GPIO pins.
    """

    sensor_id: str
    sensor_code: SensorCodeEnum
    name: str
    attributes: dict[str, Any]


class CollectorConfig(NamedTuple):
    """
    Configuration object which describes the collector node device.
    Attributes:
        collector_id (str): An ID associated with the node.
        device_name (str): A name associated with the node.
        sensors (list[SensorConfig]): All configured sensors.
        targets (list[TargetConfig]): All configured targets.
        polling_interval (int): The number of miliseconds to wait
            between sensor polls.
    """

    collector_id: str
    device_name: str
    device_type: DeviceTypeEnum
    polling_interval: int
    sensors: list[SensorConfig]
    targets: list[CacheConfig]
