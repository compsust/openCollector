from common import (
    records_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
total_records_query_string = "--sql SELECT COUNT FROM $1"


# Query result type.
class RecordsCountQueryRow(TypedDict):
    count: int


async def total_records_query(connection: Connection) -> list[RecordsCountQueryRow]:
    """
    Returns the number of records that have been received.

    Args:
        connection (Connection): The asyncpg connection

    Returns:
        list[RecordsCountQueryRow]: The database results.
    """
    return await connection.fetch(total_records_query_string, records_table_name)
