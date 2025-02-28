from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
import asyncpg
from asyncpg.connection import Connection
from litestar import Litestar
from .tables import records_table_init_command, errors_table_init_command
import config

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
        connection: Connection = await asyncpg.connect(
            host=config.QUESTDB_HOST,
            port=config.QUESTDB_PORT,
            user=config.QUESTDB_USER,
            password=config.QUESTDB_PASSWORD,
            database=config.QUESTDB_DB_NAME,
        )
        setattr(app.state, PG_CONN_STATE_KEY, connection)

    await connection.execute(records_table_init_command)
    await connection.execute(errors_table_init_command)

    try:
        yield
    finally:
        await connection.close()
