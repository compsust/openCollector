from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Datastructures for data returned by the API


class StatusEnum(Enum):
    # No data has been received from the node or sensor since the server process has begun.
    UNKNOWN = "Unknown"

    # Data has been received from the node or sensor recently.
    OPERATIONAL = "Operational"

    # Data has been received from the node or sensor since the server process has begun but not recently.
    DROPPED = "Dropped"

    # An error has been received from the node or sensor.
    ERROR = "Error"


@dataclass
class SensorSummary:
    id: str
    name: str
    status: StatusEnum
    last_value: float


@dataclass
class CollectorSummary:
    id: str
    name: str
    status: StatusEnum
    sensors: list[SensorSummary]


@dataclass
class CollectorRecord:
    sensor_id: str
    data: float
    timestamp: datetime


@dataclass
class CollectorError:
    sensor_id: str
    message: str
    timestamp: str
    source: str


@dataclass
class NodeSummary:
    total_collectors: int
    collectors_reporting: int
    total_sensors: int
    sensors_reporting: int
    errors_reported: int
    collectors: list[CollectorSummary]


@dataclass
class CollectorDetails:
    id: str
    name: str
    status: StatusEnum
    total_sensors: int
    latest_report: datetime
    earliest_report: datetime
    total_reports: int
    latest_error: datetime
    total_errors: int
    sensors: list[SensorSummary]
    errors: list[CollectorError]


@dataclass
class SensorDetails:
    id: str
    name: str
    status: StatusEnum
    type: str
    latest_report: datetime
    earliest_report: datetime
    total_reports: int
    latest_error: datetime
    total_errors: int
    records: list[CollectorRecord]
    errors: list[CollectorError]
