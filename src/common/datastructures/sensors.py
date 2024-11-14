from dataclasses import dataclass
from typing import Any
from uuid import UUID
from datetime import datetime

type SensorData = dict[str, Any]
"""Alias for data returned by a sensor."""

@dataclass
class SensorRecord:
    """
    Associates recorded sensor data with a sensor.

    Attributes:
        sensor_id (UUID): The ID of the associated sensor,
            as contained in the associated SensorConfig.
        data (SensorData): The data returned by the sensor.
        timestamp (datetime): The time at which the data was
            collected. 
    """
    sensor_id: UUID
    data: SensorData
    timestamp: datetime 

@dataclass
class SensorError:
    """
    Associates a caught sensor exception with a sensor.

    Attributes:
        sensor_id (UUID): The ID of the associated sensor,
            as contained in the associated SensorConfig.
        error_message (str): A description of the exception 
            raised by the sensor.
        timestamp (datetime): The time at which the error occurred. 
    """
    sensor_id: UUID
    error_message: str
    timestamp: datetime

@dataclass
class SensorReport:
    """
    Packages sensor data to be sent to storage nodes.

    Attributes:
        collector_id (UUID): The ID of this collector node,
            as contained within the CollectorConfig.
        records (list[SensorRecord]): The collected sensor data.
        errors (list[SensorError]): The collected sensor errors.
    """
    collector_id: UUID
    records: list[SensorRecord]
    errors: list[SensorError]