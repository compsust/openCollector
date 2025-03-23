from common import (
    collector_metadata_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
collector_count_query_string = "--sql SELECT COUNT(DISTINCT collector_id) FROM $1"


# Query result type.
class CollectorCountQueryRow(TypedDict):
    count_distinct: int


async def collector_count_query(connection: Connection) -> list[CollectorCountQueryRow]:
    """
    Returns the number of collector nodes that have reported.

    Args:
        connection (Connection): The asyncpg connection.

    Returns:
        list[CollectorCountQueryRow]: The database results.
    """
    return await connection.fetch(
        collector_count_query_string, collector_metadata_table_name
    )
