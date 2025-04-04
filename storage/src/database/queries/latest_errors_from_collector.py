from datetime import datetime
from common import (
    errors_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
latest_errors_from_collector_query_string = f"""--sql
(
    SELECT *
    FROM {errors_table_name}
    LATEST ON timestamp PARTITION BY collector_id, sensor_id
) WHERE collector_id = $1
"""


# Query result type.
class LatestErrorsFromCollectorQueryRow(TypedDict):
    collector_id: str
    sensor_id: str | None
    error_message: str
    timestamp: datetime


async def latest_errors_from_collector_query(
    connection: Connection, collector_id: str
) -> list[LatestErrorsFromCollectorQueryRow]:
    """
    Returns the most recent errors from a collector (including its sensors).

    Args:
        connection (Connection): The asyncpg connection.
        collector_id (str): The ID of the collector.

    Returns:
        list[LatestErrorsFromCollectorQueryRow]: The database results.
    """
    return await connection.fetch(
        latest_errors_from_collector_query_string, collector_id
    )
