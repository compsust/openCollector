from typing import Any, NamedTuple
from uuid import UUID

from collector.sensors import SensorCodeEnum

class CacheConfig(NamedTuple):
    """
    Configuration object which describes a Memcached target.

    Attributes:
        cache_id (UUID): An ID associated with the target.
        name (str): A descriptive name for the target.
        endpoint (str): The URI through which the cache target node may
            accept requests.
    """

    cache_id: UUID
    name: str
    endpoint: str


class SensorConfig(NamedTuple):
    """
    Configuration object which describes a sensor.

    Attributes:
        sensor_id (UUID): An ID associated with the sensor.
        sensor_code (SensorCodeEnum): Associated with
            a specific implementation of AbstractSensorDriver.
        name (str): A descriptive name for the sensor.
        attributes (dict[str, Any]): Any other attributes
            which are required to use the sensor. For example,
            GPIO pins.
    """

    sensor_id: UUID
    sensor_code: SensorCodeEnum
    name: str
    attributes: dict[str, Any]


class CollectorConfig(NamedTuple):
    """
    Configuration object which describes the collector node device.

    Attributes:
        collector_id (UUID): An ID associated with the node.
        device_name (str): A name associated with the node.
        sensors (list[SensorConfig]): All configured sensors.
        targets (list[TargetConfig]): All configured targets.
    """

    collector_id: UUID
    device_name: str
    sensors: list[SensorConfig]
    targets: list[CacheConfig]
