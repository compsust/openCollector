from common import (
    errors_table_name,
)
from asyncpg import Connection
from typing import TypedDict

# Query string.
total_errors_query_string = f"""--sql 
SELECT COUNT FROM {errors_table_name}
"""


# Query result type.
class ErrorsCountQueryRow(TypedDict):
    count: int


async def total_errors_query(connection: Connection) -> list[ErrorsCountQueryRow]:
    """
    Returns the number of errors that have been received.

    Args:
        connection (Connection): The asyncpg connection

    Returns:
        list[ErrorsCountQueryRow]: The database results.
    """
    return await connection.fetch(total_errors_query_string)
