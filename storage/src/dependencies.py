from typing import AsyncGenerator
from asyncpg import Connection
from litestar.datastructures import State
from litestar.di import Provide
from database.repository import Repository
from database.lifespan import PG_POOL_STATE_KEY


async def get_connection(state: State) -> AsyncGenerator[Connection]:
    """
    Uses the asyncpg connection pool initialized at app startup
    to create a request-scoped connection.

    Args:
        state: Litestar application state.

    Raises:
        ValueError: Raised if the connection pool doesn't exist.

    Yields:
        The asyncpg connection.
    """
    pool = getattr(state, PG_POOL_STATE_KEY, None)
    if pool is None:
        raise ValueError("Postgres connection pool not set on litestart global state.")

    async with pool.acquire() as connection:
        yield connection


async def get_repository(connection: Connection) -> Repository:
    """
    Uses the request-scoped asyncpg connection to
    create a repository class.

    Args:
        connection: The asyncpg connection.

    Returns:
        The repository
    """
    return Repository(connection)


dependencies = {
    "connection": Provide(get_connection),
    "repository": Provide(get_repository),
}
