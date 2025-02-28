from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
import asyncpg
from asyncpg.connection import Connection


from litestar import Litestar


"""
The keys used to set objects on the Litestar application state.
"""
PG_CONN_STATE_KEY = "asyncpg_client"


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    """
    The database in use is QuestDB. To query from QuestDb, we
    can use a Postgres client.
    Initializes an asynchronous Postgres client from asyncpg.

    Args:
        app (Litestar): The Litestar application instance.
            Used to attach the created client object to the
            application state which can be accessed in routes.
    """
    client = getattr(app.state, PG_CONN_STATE_KEY, None)
    if client is None:
        # TODO: Add these as environment variables.
        connection: Connection = await asyncpg.connect(host="", port=0, user="", password="", database="")
        setattr(app.state, PG_CONN_STATE_KEY, connection)

    try:
        yield
    finally:
        await connection.close()
