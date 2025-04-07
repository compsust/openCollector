from common import (
    records_table_name,
)
from asyncpg import Connection
from typing import TypedDict
from datetime import datetime

# Query string.
sensor_timeline_query_string = f"""--sql
SELECT timestamp, value
FROM {records_table_name}
WHERE collector_id=$1
AND sensor_id = $2
AND record_id = $3
"""


# Query result type.
class SensorTimelineQueryRow(TypedDict):
    timestamp: datetime
    value: float | int


async def sensor_timeline_query(
    connection: Connection, collector_id: str, sensor_id: str, record_id: str
) -> list[SensorTimelineQueryRow]:
    """
    Returns a timeline of sensor data for a sensor.

    Args:
        connection: The asyncpg connection
        collector_id: The ID of the collector.
        sensor_id: The ID of the sensor.
        record_id: The ID of the record.

    Returns:
        The database results.
    """
    return await connection.fetch(
        sensor_timeline_query_string, collector_id, sensor_id, record_id
    )
