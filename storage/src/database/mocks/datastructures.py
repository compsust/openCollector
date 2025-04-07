from dataclasses import dataclass
from datetime import datetime

from common import SensorCodeEnum


@dataclass
class MockCollector:
    """
    Represents a collector's attributes.
    """

    collector_id: str
    collector_name: str
    device_model: str
    polling_interval: int


@dataclass
class MockSensor:
    """
    Represents a sensor's attributes.
    """

    collector_id: str
    sensor_id: str
    sensor_code: SensorCodeEnum
    sensor_name: str


@dataclass
class MockCollectorMetadata:
    """
    Represents a collector's attributes as inserted into the DB table.
    """

    timestamp: datetime
    collector_id: str
    collector_name: str
    device_model: str
    polling_interval: int


@dataclass
class MockSensorMetadata:
    """
    Represents a sensor's attributes as inserted into the DB table.
    """

    timestamp: datetime
    collector_id: str
    sensor_id: str
    sensor_code: SensorCodeEnum
    sensor_name: str


@dataclass
class MockRecord:
    """
    Represents a record's attributes as inserted into the DB table.
    """

    timestamp: datetime
    collector_id: str
    sensor_id: str
    record_id: str
    value: float


@dataclass
class MockError:
    """
    Represents an error's attributes as inserted into the DB table.
    """

    timestamp: datetime
    collector_id: str
    sensor_id: str | None
    error_message: str
