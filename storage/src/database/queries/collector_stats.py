from datetime import datetime
from typing import TypedDict

from asyncpg import Connection

from common import (
    errors_table_name,
    records_table_name,
    sensor_metadata_table_name,
)

# Query string.
collector_stats_query_string = f"""--sql
WITH
total_sensors AS (
    SELECT COUNT(DISTINCT sensor_id) count
    FROM {sensor_metadata_table_name}
    WHERE collector_id = $1
),
total_records AS (
    SELECT COUNT(*) count
    FROM {records_table_name}
    WHERE collector_id = $1
),
total_errors AS (
    SELECT COUNT(*) count
    FROM {errors_table_name}
    WHERE collector_id = $1
)
SELECT
    total_sensors.count AS total_sensors,
    total_records.count AS total_records,
    total_errors.count AS total_errors,
    (SELECT max(timestamp) FROM {records_table_name} WHERE collector_id = $1) AS latest_record,
    (SELECT min(timestamp) FROM {records_table_name} WHERE collector_id = $1) AS earliest_record,
    (SELECT max(timestamp) FROM {errors_table_name} WHERE collector_id = $1) AS latest_error
FROM total_sensors
CROSS JOIN total_records
CROSS JOIN total_errors
"""


# Query result type.
class CollectorStatsQueryRow(TypedDict):
    total_sensors: int
    latest_record: datetime
    earliest_record: datetime
    total_records: int
    latest_error: datetime
    total_errors: int


async def collector_stats_query(
    connection: Connection, collector_id: str
) -> list[CollectorStatsQueryRow]:
    """
    Returns the details / statistics for one collector.

    Args:
        connection: The asyncpg connection.
        collector_id: The ID of the collector.

    Returns:
        The database results.
    """
    return await connection.fetch(
        collector_stats_query_string,
        collector_id,
    )
