from typing import NamedTuple

from common.src import RecordID, SensorCodeEnum

type SensorData = dict[RecordID, float | int]
"""Alias for data returned by a sensor. The keys must be RecordIDs and the values are numerical."""


class CollectorRecord(NamedTuple):
    """
    Associates recorded sensor data with a sensor.

    Attributes:
        sensor_id (str): The ID of the associated sensor,
            as contained in the associated SensorConfig.
        data (SensorData): The data returned by the sensor.
        timestamp (float): The Unix timestamp at which the record was recorded.
    """

    sensor_id: str
    data: SensorData
    timestamp: float


class CollectorError(NamedTuple):
    """
    Associates a caught exception with a sensor, or the node itself
    if no sensor was involved.

    Attributes:
        sensor_id (str | None): The ID of the associated sensor,
            as contained in the associated SensorConfig, or None
            if the error wasn't associated with a particular sensor.
        error_message (str): A description of the exception
            raised by the sensor.
        timestamp (float): The Unix timestamp at which the error occurred.
    """

    sensor_id: str | None
    error_message: str
    timestamp: float


class CollectorReport(NamedTuple):
    """
    Packages sensor data to be sent to storage nodes.

    Attributes:
        collector_id (str): The ID of this collector node,
            as contained within the CollectorConfig.
        records (list[CollectorRecord]): The collected sensor data.
        errors (list[CollectorError]): The collected sensor errors.
    """

    collector_id: str
    records: list[CollectorRecord]
    errors: list[CollectorError]


class CollectorMetadata(NamedTuple):
    """
    Packages collector metadata to be sent to storage nodes.

    Attributes are same as in the collector config.
    """

    collector_id: str
    collector_name: str
    device_model: str
    polling_interval: int


class SensorMetadata(NamedTuple):
    """
    Packages sensor metadata to be sent to storage nodes.

    Attributes are same as in the collector config.
    """

    collector_id: str
    sensor_id: str
    sensor_code: SensorCodeEnum
    sensor_name: str
