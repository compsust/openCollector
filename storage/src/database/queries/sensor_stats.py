from datetime import datetime
from typing import TypedDict

from asyncpg import Connection

from common import (
    errors_table_name,
    records_table_name,
)

# Query string.
sensor_stats_query_string = f"""--sql
WITH
total_records AS (
    SELECT COUNT(*) count
    FROM {records_table_name}
    WHERE sensor_id = $1
),
total_errors AS (
    SELECT COUNT(*) count
    FROM {errors_table_name}
    WHERE sensor_id = $1
)
SELECT
    total_records.count AS total_records,
    total_errors.count AS total_errors,
    (SELECT max(timestamp) FROM {records_table_name} WHERE sensor_id = $1) AS latest_record,
    (SELECT min(timestamp) FROM {records_table_name} WHERE sensor_id = $1) AS earliest_record,
    (SELECT max(timestamp) FROM {errors_table_name} WHERE sensor_id = $1) AS latest_error
FROM total_records
CROSS JOIN total_errors
"""


# Query result type.
class SensorStatsQueryRow(TypedDict):
    latest_record: datetime
    earliest_record: datetime
    total_records: int
    latest_error: datetime
    total_errors: int


async def sensor_stats_query(
    connection: Connection, sensor_id: str
) -> list[SensorStatsQueryRow]:
    """
    Returns the details / statistics for one sensor.

    Args:
        connection: The asyncpg connection.
        sensor_id: The ID of the sensor.

    Returns:
        The database results.
    """
    return await connection.fetch(
        sensor_stats_query_string,
        sensor_id,
    )
