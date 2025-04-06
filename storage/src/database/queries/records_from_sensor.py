from datetime import datetime
from common import records_table_name, RecordID
from asyncpg import Connection
from typing import TypedDict

# Query string.
records_from_sensor_query_string = """--sql 
SELECT *
FROM {records_table_name}
WHERE sensor_id = $1
ORDER BY timestamp DESC
LIMIT $2, $3
"""


# Query result type.
class RecordsFromSensorQueryRow(TypedDict):
    collector_id: str
    sensor_id: str
    record_id: RecordID
    value: float
    timestamp: datetime


async def records_from_sensor_query(
    connection: Connection, sensor_id: str, page: int, page_size: int
) -> list[RecordsFromSensorQueryRow]:
    """
    Returns the records from the sensor.

    Args:
        connection: The asyncpg connection
        sensor_id: The ID of the sensor.
        page: The index of the pagination results. Starts at 0.
        page_size: The size of the page of results.

    Returns:
        list[RecordsFromSensorQueryRow]: The database results.
    """
    limit_start = page * page_size
    limit_end = limit_start + page_size
    return await connection.fetch(
        records_from_sensor_query_string,
        sensor_id,
        limit_start,
        limit_end,
    )
