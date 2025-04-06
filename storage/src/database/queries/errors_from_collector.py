from datetime import datetime
from common import (
    errors_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
errors_from_collector_query_string = f"""--sql 
SELECT *
FROM {errors_table_name}
WHERE collector_id = $1
ORDER BY timestamp DESC
LIMIT $2, $3
"""


# Query result type.
class ErrorsFromCollectorQueryRow(TypedDict):
    collector_id: str
    sensor_id: str | None
    error_message: str
    timestamp: datetime


async def errors_from_collector_query(
    connection: Connection, collector_id: str, page: int, page_size: int
) -> list[ErrorsFromCollectorQueryRow]:
    """
    Returns the errors from the collector and its sensors.

    Args:
        connection: The asyncpg connection
        collector_id: The ID of the collector.
        page: The index of the pagination results. Starts at 0.
        page_size: The size of the page of results.

    Returns:
        The database results.
    """
    limit_start = page * page_size
    limit_end = limit_start + page_size
    return await connection.fetch(
        errors_from_collector_query_string,
        collector_id,
        limit_start,
        limit_end,
    )
