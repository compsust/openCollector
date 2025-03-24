from datetime import datetime
from common import (
    SensorCodeEnum,
    sensor_metadata_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
latest_sensor_metadata_query_string = f"""--sql
SELECT *
FROM $1
LATEST ON timestamp PARTITION BY sensor_id
"""


# Query result type.
class LatestSensorMetadataQueryRow(TypedDict):
    collector_id: str
    sensor_id: str
    sensor_code: SensorCodeEnum
    sensor_name: str
    timestamp: datetime


async def latest_sensor_metadata_query(
    connection: Connection,
) -> list[LatestSensorMetadataQueryRow]:
    """
    Returns the most recent sensor metadata.

    Args:
        connection (Connection): The asyncpg connection

    Returns:
        list[LatestSensorMetadataQueryRow]: The database results.
    """
    return await connection.fetch(
        latest_sensor_metadata_query_string, sensor_metadata_table_name
    )
