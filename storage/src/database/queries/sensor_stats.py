from datetime import datetime
from common import (
    errors_table_name,
    records_table_name,
)
from asyncpg import Connection
from typing import TypedDict

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
),
latest_record AS (
    (
        SELECT *
        FROM {records_table_name}
        LATEST ON timestamp PARTITION BY sensor_id
    ) WHERE sensor_id = $1
),
earliest_record AS (
    SELECT *
    FROM {records_table_name}
    WHERE sensor_id = $1
    ORDER BY timestamp ASC
    LIMIT 1
),
latest_error AS (
    (
        SELECT *
        FROM {errors_table_name}
        LATEST ON timestamp PARTITION BY sensor_id
    ) WHERE sensor_id = $1
)
SELECT 
    total_records.count AS total_records,
    total_errors.count AS total_errors,
    latest_record.timestamp AS latest_record,
    earliest_record.timestamp AS earliest_record,
    latest_error.timestamp AS latest_error
FROM total_records
CROSS JOIN total_errors
CROSS JOIN latest_record
CROSS JOIN earliest_record
CROSS JOIN latest_error
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
        connection (Connection): The asyncpg connection.
        sensor_id (str): The ID of the sensor.

    Returns:
        list[SensorStatsQueryRow]: The database results.
    """
    return await connection.fetch(
        sensor_stats_query_string,
        sensor_id,
    )
