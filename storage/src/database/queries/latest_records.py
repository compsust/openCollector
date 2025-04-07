from datetime import datetime
from common import records_table_name
from asyncpg import Connection
from typing import TypedDict

# Query string.
latest_records_query_string = f"""--sql
SELECT *
FROM {records_table_name}
LATEST ON timestamp PARTITION BY sensor_id, record_id
"""


# Query result type.
class LatestRecordsQueryRow(TypedDict):
    collector_id: str
    sensor_id: str
    record_id: str
    value: float
    timestamp: datetime


async def latest_records_query(connection: Connection) -> list[LatestRecordsQueryRow]:
    """
    Returns the most recent records.

    Args:
        connection: The asyncpg connection

    Returns:
        The database results.
    """
    return await connection.fetch(latest_records_query_string)
