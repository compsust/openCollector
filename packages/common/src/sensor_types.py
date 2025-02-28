from typing import Any, NamedTuple

from .sensor_codes import SensorCodeEnum

type SensorData = dict[str, Any]
"""Alias for data returned by a sensor."""


class SensorRecord(NamedTuple):
    """
    Associates recorded sensor data with a sensor.

    Attributes:
        sensor_id (str): The ID of the associated sensor,
            as contained in the associated SensorConfig.
        sensor_code (SensorCodeEnum): The code of the associated sensor,
            as contained in the associated SensorConfig.
        data (SensorData): The data returned by the sensor.
        timestamp (float): The Unix timestamp at which the data was
            collected.
    """

    sensor_id: str
    sensor_code: SensorCodeEnum
    data: SensorData
    timestamp: float


class SensorError(NamedTuple):
    """
    Associates a caught sensor exception with a sensor.

    Attributes:
        sensor_id (str | None): The ID of the associated sensor,
            as contained in the associated SensorConfig, or None
            if the error wasn't associated with a particular sensor.
        sensor_code (SensorCodeEnum | None): The code of the associated sensor,
            as contained in the associated SensorConfig, or None
            if the error wasn't associated with a particular sensor.
        error_message (str): A description of the exception
            raised by the sensor.
        timestamp (float): The Unix timestamp at which the error occurred.
    """

    sensor_id: str | None
    sensor_code: SensorCodeEnum | None
    error_message: str
    timestamp: float


class SensorReport(NamedTuple):
    """
    Packages sensor data to be sent to storage nodes.

    Attributes:
        collector_id (str): The ID of this collector node,
            as contained within the CollectorConfig.
        node_name (str): The name of this collector node,
            as contained within the CollectorConfig.
        model (str): The name of the collector node device type,
            as contained within the DeviceConfig.
        records (list[SensorRecord]): The collected sensor data.
        errors (list[SensorError]): The collected sensor errors.
    """

    collector_id: str
    node_name: str
    model: str
    records: list[SensorRecord]
    errors: list[SensorError]
