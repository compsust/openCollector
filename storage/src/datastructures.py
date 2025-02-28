from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Datastructures for data returned by the API
# Two main types:
# Summaries provide a quick overview of the information for an entity
# Details provide comprehensive outline of all the data.


class StatusEnum(Enum):
    """
    Describes the knowledge that the storage node
    has about how a collector node or sensor is functioning.

    Statuses are stored in-memory, and thus a restart of the
    server process will result in statuses being reset.

    Options:
        Unknown: No data has been received from the
            node or sensor since the server process has begun.
        Operational: Data has been received from the node or
            sensor recently.
        Dropped: Data has been received from the node or sensor
            since the server process has begun but not recently.
        Error: An error has been received from the node or sensor.
    """

    UNKNOWN = "Unknown"
    OPERATIONAL = "Operational"
    DROPPED = "Dropped"
    ERROR = "Error"


@dataclass
class SensorSummary:
    """
    A summary of a sensor.

    Attributes:
        id (str): The ID of the sensor.
        name (str): The name of the sensor.
        status (StatusEnum): The status of the sensor.
        last_value (float | None): The last value returned
            by the sensor.
    """

    id: str
    name: str
    status: StatusEnum
    last_value: float | None


@dataclass
class CollectorSummary:
    """
    A summary of a collector node.

    Attributes:
        id (str): The ID of the node.
        name (str): The name of the node.
        status (StatusEnum): The status of the node.
        last_value (float | None): The last value returned
            by the sensor.
    """

    id: str
    name: str
    status: StatusEnum
    sensors: list[SensorSummary]


@dataclass
class CollectorRecord:
    """
    A data record returned by a sensor within a collector node.

    Attributes:
        sensor_id (str): ID of the sensor.
        name (str): The name of the value, corresponding to the
            name listed in the sensor_metadata object.
        unit (str): The unit of the value, corresponding to the
            unit listed in the sensor_metadata object.
        data (float): The value of the record.
        timestamp (datetime): The timestamp of the record.
    """

    sensor_id: str
    name: str
    unit: str
    data: float
    timestamp: datetime


@dataclass
class CollectorError:
    """
    An error returned by a collector node
    or a sensor within a collector node.

    Attributes:
        message (str): The error message.
        timestamp (datetime): The timestamp
            of the error.
        source (str): The source of the error.
            If the error originated from a sensor,
            this is equal to the name of the sensor.
            If the error originated from the collector node itself,
            this is equal to the name of the node.
    """

    message: str
    timestamp: datetime
    source: str


@dataclass
class NodeSummary:
    """
    A summary for the entire storage node.

    Attributes:
        total_collectors (int): The total number of collector
            nodes which have sent data to this storage node.
        collectors_reporting (int): The total number of collector
            nodes which currently have the "Operational" or
            "Error" status.
        total_sensors (int): The total number of sensors
            which have sent data to this storage node.
        sensors_reporting (int): The total number of sensors
            which currently have the "Operational" or
            "Error" status.
        errors_reported (int): The number of errors that have
            been reported by all collectors and sensors.
        collectors (list[CollectorSummary]): All collector summaries.
    """

    total_collectors: int
    collectors_reporting: int
    total_sensors: int
    sensors_reporting: int
    errors_reported: int
    collectors: list[CollectorSummary]


@dataclass
class CollectorDetails:
    """
    The details for a collector node.

    Attributes:
        id (str): The ID of the collector node.
        name (str): The name of the collector node.
        status (StatusEnum): The status of the collector node.
        total_sensors (int): The total number of sensors
            connected to this collector node which have returned data.
        latest_record (datetime): The timestamp of the latest sensor record.
        earliest_record (datetime): The timestamp of the earliest sensor record.
        total_records (int): The total number of records that have been received.
        latest_error (datetime): The timestamp of the latest error.
        total_errors (int): The total number of errors that have been received.
        sensors (list[SensorSummary]): The sensor summaries of this collector node.
        errors (list[CollectorError]): The errors reported by the node and sensors.
    """

    id: str
    name: str
    status: StatusEnum
    total_sensors: int
    latest_record: datetime
    earliest_record: datetime
    total_records: int
    latest_error: datetime
    total_errors: int
    sensors: list[SensorSummary]
    errors: list[CollectorError]


@dataclass
class SensorDetails:
    """
    The details for a sensor.

    Attributes:
        id (str): The ID of the sensor.
        name (str): The name of the sensor.
        status (StatusEnum): The status of the sensor.
        type (str): The name of the sensor type. Corresponds
            to the value of "name" in the sensor_metadata object.
        latest_record (datetime): The timestamp of the latest sensor record.
        earliest_record (datetime): The timestamp of the earliest sensor record.
        total_records (int): The total number of records that have been received.
        latest_error (datetime): The timestamp of the latest sensor error.
        total_errors (int): The total number of errors that have been received.
        records (list[CollectorRecord]): The records of this sensor.
        errors (list[CollectorError]): The errors reported by this sensor.
    """

    id: str
    name: str
    status: StatusEnum
    type: str
    latest_record: datetime
    earliest_record: datetime
    total_records: int
    latest_error: datetime
    total_errors: int
    records: list[CollectorRecord]
    errors: list[CollectorError]
