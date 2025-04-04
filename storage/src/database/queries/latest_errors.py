from datetime import datetime
from common import (
    errors_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
latest_errors_query_string = f"""--sql
SELECT *
FROM {errors_table_name}
LATEST ON timestamp PARTITION BY collector_id, sensor_id
"""


# Query result type.
class LatestErrorsQueryRow(TypedDict):
    collector_id: str
    sensor_id: str | None
    error_message: str
    timestamp: datetime


async def latest_errors_query(connection: Connection) -> list[LatestErrorsQueryRow]:
    """
    Returns the most recent errors

    Args:
        connection (Connection): The asyncpg connection

    Returns:
        list[LatestErrorsQueryRow]: The database results.
    """
    return await connection.fetch(latest_errors_query_string)
