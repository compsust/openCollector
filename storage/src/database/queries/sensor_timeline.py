from common import (
    records_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
sensor_timeline_query_string = f"""--sql
SELECT COUNT FROM {records_table_name}
"""


# Query result type.
class SensorTimelineQueryRow(TypedDict):
    timestamp: datetime
    value: float | int


async def sensor_timeline_query(connection: Connection) -> list[SensorTimelineQueryRow]:
    """
    Returns the number of records that have been received.

    Args:
        connection (Connection): The asyncpg connection

    Returns:
        list[RecordsCountQueryRow]: The database results.
    """
    return await connection.fetch(total_records_query_string)
