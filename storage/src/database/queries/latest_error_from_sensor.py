from datetime import datetime
from common import errors_table_name
from asyncpg import Connection
from typing import TypedDict

# Query string.
latest_error_from_sensor_query_string = f"""--sql
(
    SELECT *
    FROM {errors_table_name}
    LATEST ON timestamp PARTITION BY sensor_id
) WHERE sensor_id = $1
"""


# Query result type.
class LatestErrorFromSensorQueryRow(TypedDict):
    collector_id: str
    sensor_id: str
    error_message: str
    timestamp: datetime


async def latest_error_from_sensor_query(
    connection: Connection, sensor_id: str
) -> list[LatestErrorFromSensorQueryRow]:
    """
    Returns the most recent error from a sensor.

    Args:
        connection: The asyncpg connection.
        sensor_id: The ID of the sensor.

    Returns:
        The database results.
    """
    return await connection.fetch(latest_error_from_sensor_query_string, sensor_id)
