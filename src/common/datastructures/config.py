from uuid import UUID
from collector.sensors import SensorCodeEnum
from typing import Any

# TODO: Use Pydantic for config object validation


class TargetConfig:
    """
    Configuration object which describes a storage node target.

    Attributes:
        target_id (UUID): An ID associated with the target.
            Must be consistent with the ID set on the target itself.
        name (str): A descriptive name for the target.
        endpoint (str): The URI through which the target node may
            accept requests.
    """

    target_id: UUID
    name: str
    endpoint: str


class SensorConfig:
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


class CollectorConfig:
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
    targets: list[TargetConfig]
