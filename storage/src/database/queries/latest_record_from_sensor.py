from datetime import datetime
from common import records_table_name, RecordID
from asyncpg import Connection
from typing import TypedDict

# Query string.
latest_record_from_sensor_query_string = f"""--sql
(
    SELECT *
    FROM {records_table_name}
    LATEST ON timestamp PARTITION BY sensor_id
) WHERE sensor_id = $1
"""


# Query result type.
class LatestRecordFromSensorQueryRow(TypedDict):
    collector_id: str
    sensor_id: str
    record_id: RecordID
    value: float
    timestamp: datetime


async def latest_record_from_sensor_query(
    connection: Connection, sensor_id: str
) -> list[LatestRecordFromSensorQueryRow]:
    """
    Returns the most recent record from a sensor.

    Args:
        connection: The asyncpg connection.
        sensor_id: The ID of the sensor.

    Returns:
        The database results.
    """
    return await connection.fetch(latest_record_from_sensor_query_string, sensor_id)
