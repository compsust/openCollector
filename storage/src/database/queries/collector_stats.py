from datetime import datetime
from common import (
    collector_metadata_table_name,
    errors_table_name,
    records_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
collector_stats_query_string = """--sql 
WITH 
total_sensors AS (
    SELECT COUNT(DISTINCT sensor_id) count 
    FROM $1 
    WHERE collector_id = $4
),
total_records AS (
    SELECT COUNT(*) count 
    FROM $2 
    WHERE collector_id = $4
),
total_errors AS (
    SELECT COUNT(*) count 
    FROM $3 
    WHERE collector_id = $4
),
latest_record AS (
    (
        SELECT *
        FROM $2
        LATEST ON timestamp PARTITION BY collector_id
    ) WHERE collector_id = $4
),
earliest_record AS (
    SELECT *
    FROM $2
    WHERE collector_id = $4
    ORDER BY timestamp ASC
    LIMIT 1
),
latest_error AS (
    (
        SELECT *
        FROM $3
        LATEST ON timestamp PARTITION BY collector_id
    ) WHERE collector_id = $4
)
SELECT 
    total_sensors.count AS total_sensors,
    total_records.count AS total_records,
    total_errors.count AS total_errors,
    latest_record.timestamp AS latest_record,
    earliest_record.timestamp AS earliest_record,
    latest_error.timestamp AS latest_error
FROM total_sensors
CROSS JOIN total_records
CROSS JOIN total_errors
CROSS JOIN latest_record
CROSS JOIN earliest_record
CROSS JOIN latest_error
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
        connection (Connection): The asyncpg connection.
        collector_id (str): The ID of the collector.

    Returns:
        list[CollectorStatsQueryRow]: The database results.
    """
    return await connection.fetch(
        collector_stats_query_string,
        collector_metadata_table_name,
        records_table_name,
        errors_table_name,
        collector_id,
    )
