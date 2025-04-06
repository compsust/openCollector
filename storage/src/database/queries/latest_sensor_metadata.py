from datetime import datetime
from common import (
    SensorCodeEnum,
    sensor_metadata_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query strings.
latest_sensor_metadata_all_query_string = f"""--sql
SELECT *
FROM {sensor_metadata_table_name}
LATEST ON timestamp PARTITION BY sensor_id
"""

latest_sensor_metadata_one_query_string = f"""--sql
SELECT *
FROM {sensor_metadata_table_name}
WHERE sensor_id = $1
LATEST ON timestamp PARTITION BY sensor_id
"""


# Query result type.
class LatestSensorMetadataQueryRow(TypedDict):
    collector_id: str
    sensor_id: str
    sensor_code: str
    sensor_name: str
    timestamp: datetime


async def latest_sensor_metadata_query(
    connection: Connection, sensor_id: str | None = None
) -> list[LatestSensorMetadataQueryRow]:
    """
    Returns the most recent sensor metadata.

    Args:
        connection: The asyncpg connection
        sensor_id: If included, the metadata will be returned for one sensor.

    Returns:
        The database results.
    """
    if sensor_id:
        return await connection.fetch(
            latest_sensor_metadata_one_query_string, sensor_id
        )
    else:
        return await connection.fetch(latest_sensor_metadata_all_query_string)
