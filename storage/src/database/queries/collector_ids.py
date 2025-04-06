from common import (
    collector_metadata_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
collector_ids_query_string = f"""--sql
SELECT DISTINCT collector_id, collector_name
FROM {collector_metadata_table_name}
"""


# Query result type.
class CollectorIdQueryRow(TypedDict):
    collector_id: str
    collector_name: str


async def collector_ids_query(connection: Connection) -> list[CollectorIdQueryRow]:
    """
    Returns the the collector IDs and associated names.

    Args:
        connection: The asyncpg connection.

    Returns:
        The database results.
    """
    return await connection.fetch(collector_ids_query_string)
