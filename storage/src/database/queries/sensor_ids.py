from common import (
    sensor_metadata_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
sensor_ids_query_string = f"""--sql
SELECT DISTINCT sensor_id, sensor_name
FROM {sensor_metadata_table_name}
WHERE collector_id=$1
"""


# Query result type.
class SensorIdQueryRow(TypedDict):
    sensor_id: str
    sensor_name: str


async def sensor_ids_query(
    connection: Connection, collector_id: str
) -> list[SensorIdQueryRow]:
    """
    Returns the the sensor IDs and associated names for all sensors on a given collector.

    Args:
        connection: The asyncpg connection.
        collector_id: The collector ID to return sensors for.

    Returns:
        The database results.
    """
    return await connection.fetch(sensor_ids_query_string, collector_id)
