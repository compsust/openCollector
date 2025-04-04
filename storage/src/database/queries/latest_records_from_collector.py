from datetime import datetime
from common import records_table_name, RecordID
from asyncpg import Connection
from typing import TypedDict

# Query string.
latest_records_from_collector_query_string = f"""--sql
(
    SELECT *
    FROM {records_table_name}
    LATEST ON timestamp PARTITION BY sensor_id, record_id
) WHERE collector_id = $1
"""


# Query result type.
class LatestRecordsFromCollectorQueryRow(TypedDict):
    collector_id: str
    sensor_id: str
    record_id: RecordID
    value: float
    timestamp: datetime


async def latest_records_from_collector_query(
    connection: Connection, collector_id: str
) -> list[LatestRecordsFromCollectorQueryRow]:
    """
    Returns the most recent records from a collector node.

    Args:
        connection (Connection): The asyncpg connection.
        collector_id (str): The ID of the collector.

    Returns:
        list[LatestRecordsFromCollectorQueryRow]: The database results.
    """
    return await connection.fetch(
        latest_records_from_collector_query_string, collector_id
    )
