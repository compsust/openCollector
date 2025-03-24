from datetime import datetime
from common import (
    errors_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
errors_from_sensor_query_string = """--sql 
SELECT *
FROM $1
WHERE sensor_id = $2
ORDER BY timestamp DESC
LIMIT $3, $4
"""


# Query result type.
class ErrorsFromSensorQueryRow(TypedDict):
    collector_id: str
    sensor_id: str
    error_message: str
    timestamp: datetime


async def errors_from_sensor_query(
    connection: Connection, sensor_id: str, page: int, page_size: int
) -> list[ErrorsFromSensorQueryRow]:
    """
    Returns the errors from the sensor.

    Args:
        connection (Connection): The asyncpg connection
        sensor_id (str): The ID of the sensor.
        page (int): The index of the pagination results. Starts at 0.
        page_size (int): The size of the page of results.

    Returns:
        list[ErrorsFromSensorQueryRow]: The database results.
    """
    limit_start = page * page_size
    limit_end = limit_start + page_size
    return await connection.fetch(
        errors_from_sensor_query_string,
        errors_table_name,
        sensor_id,
        limit_start,
        limit_end,
    )
