from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any

from common import SensorCodeEnum
# Datastructures for data returned by the API
# Two main types:
# Summaries provide a quick overview of the information for an entity
# Details provide comprehensive outline of all the data.


class StatusEnum(StrEnum):
    """
    Describes the knowledge that the storage node
    has about how a sensor is functioning.

    Options:
        Unknown: No data has been received from the
            node or sensor.
        Operational: Data has been received from the node or
            sensor recently.
        Dropped: Data has been received from the node or sensor
            since but it is less recent than a threshold
            determined by a set multiple of the collector's
            polling interval.
        Error: The sensor has an error and it is more recent than
            the most recent data received.
    """

    UNKNOWN = "Unknown"
    OPERATIONAL = "Operational"
    DROPPED = "Dropped"
    ERROR = "Error"


@dataclass
class CollectorRecord:
    """
    Describes the information associated with a record.

    Attributes:
        record_id: The ID of the record.
        record_name: The name of the record
        value: The value of the record.
        unit: The unit of the record.
        timestamp: The timestamp of the record.
    """

    record_id: str
    record_name: str
    value: float | None
    unit: str
    timestamp: datetime


@dataclass
class CollectorError:
    """
    An error returned by a collector node
    or a sensor within a collector node.

    Attributes:
        message: The error message.
        timestamp: The timestamp
            of the error.
        source: The source of the error.
            If the error originated from a sensor,
            this is equal to the name of the sensor.
            If the error originated from the collector node itself,
            this is equal to the name of the node.
    """

    message: str
    timestamp: datetime
    source: str


@dataclass
class SensorSummary:
    """
    A summary of a sensor.

    Attributes:
        id: The ID of the sensor.
        name: The name of the sensor.
        status: The status of the sensor.
            Since the sensor has multiple records for each
            record ID it returns, the status is UNKNOWN by default,
            DROPPED if no sensors or errors have been received within
            the threshold, ERROR if any errors have been reported since
            the last record, and OPERATIONAL otherwise.
        last_value: The last value returned
            by the sensor.
    """

    id: str
    name: str
    status: StatusEnum
    last_value: list[CollectorRecord]


@dataclass
class CollectorSummary:
    """
    A summary of a collector node.

    Attributes:
        id: The ID of the node.
        name: The name of the node.
        status: The status of the node. The status is
            UNKNOWN by if any of the sensor statuses are,
            DROPPED if any of the sensor statuses are,
            ERROR if any of the sensor status are, and
            OPERATIONAL otherwise.
        sensors: The summaries of the
            sensors in this node.
    """

    id: str
    name: str
    sensors: list[SensorSummary]


@dataclass
class NetworkSummary:
    """
    A summary for the entire storage network.

    Attributes:
        total_collectors: The total number of collector
            nodes which have sent data to this storage node.
        total_sensors: The total number of sensors
            which have sent data to this storage node.
        total_records: The number of records that have
            been reported by all and sensors.
        total_errors: The number of errors that have
            been reported by all collectors and sensors.
    """

    total_collectors: int
    total_sensors: int
    total_records: int
    total_errors: int


@dataclass
class CollectorDetails:
    """
    The details for a collector node.

    Attributes:
        id: The ID of the collector node.
        name: The name of the collector node.
        device_model: The node's device model.
        polling_interval: The node's polling interval.
        total_sensors: The total number of sensors
            connected to this collector node which have returned data.
        latest_record: The timestamp of the latest sensor record.
        earliest_record: The timestamp of the earliest sensor record.
        total_records: The total number of records that have been received.
        latest_error: The timestamp of the latest error.
        total_errors: The total number of errors that have been received.
        sensors: The sensor summaries of this collector node.
        errors: The errors reported by the node and sensors.
    """

    id: str
    name: str
    device_model: str
    polling_interval: int
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
        id: The ID of the sensor.
        name: The name of the sensor.
        status: The status of the sensor.
        type: The name of the sensor type. Corresponds
            to the value of "name" in the sensor_metadata object.
        latest_record: The timestamp of the latest sensor record.
        earliest_record: The timestamp of the earliest sensor record.
        total_records: The total number of records that have been received.
        latest_error: The timestamp of the latest sensor error.
        total_errors: The total number of errors that have been received.
        records: The records of this sensor.
        errors: The errors reported by this sensor.
    """

    id: str
    name: str
    status: StatusEnum
    code: SensorCodeEnum
    latest_record: datetime
    earliest_record: datetime
    total_records: int
    latest_error: datetime
    total_errors: int
    records: list[CollectorRecord]
    errors: list[CollectorError]


@dataclass
class SensorTimeline:
    """
    Returns all records for sensor record ID.

    Attributes:
        collector_id: The ID of the collector.
        sensor_id: The ID of the sensor.
        record_id: The ID of the record.
        record_name: The name of the record.
        unit: The string representing the unit of the record.
        timestamps: An ordered list of timestamps of the records.
        values: An ordered list of timestamps of the values.
    """

    collector_id: str
    sensor_id: str
    record_id: str
    record_name: str
    unit: str
    timestamps: list[datetime]
    values: list[float | int]
