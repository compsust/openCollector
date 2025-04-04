from common import (
    sensor_metadata_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
sensor_count_query_string = f"""--sql 
SELECT COUNT(DISTINCT sensor_id) FROM {sensor_metadata_table_name}
"""


# Query result type.
class SensorCountQueryRow(TypedDict):
    count_distinct: int


async def sensor_count_query(connection: Connection) -> list[SensorCountQueryRow]:
    """
    Returns the number of sensors that have reported.

    Args:
        connection (Connection): The asyncpg connection.

    Returns:
        list[SensorCountQueryRow]: The database results.
    """
    return await connection.fetch(sensor_count_query_string)
