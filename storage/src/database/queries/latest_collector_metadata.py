from datetime import datetime
from asyncpg import Connection
from typing import TypedDict
from common import (
    collector_metadata_table_name,
)

# Query string.
latest_collector_metadata_query_string = f"""--sql
SELECT *
FROM {collector_metadata_table_name}
LATEST ON timestamp PARTITION BY collector_id 
"""


# Query result type.
class LatestCollectorMetadataQueryRow(TypedDict):
    collector_id: str
    collector_name: str
    device_model: str
    polling_interval: int
    timestamp: datetime


async def latest_collector_metadata_query(
    connection: Connection,
) -> list[LatestCollectorMetadataQueryRow]:
    """
    Returns the most recent collector metadata.

    Args:
        connection (Connection): The asyncpg connection

    Returns:
        list[LatestCollectorMetadataQueryRow]: The database results.
    """
    return await connection.fetch(latest_collector_metadata_query_string)
