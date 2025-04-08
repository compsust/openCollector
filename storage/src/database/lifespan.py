from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
import asyncpg
from litestar import Litestar
from .tables import records_table_init_command, errors_table_init_command, collector_metadata_table_init_command, sensor_metadata_table_init_command
import config

"""
The keys used to set objects on the Litestar application state.
"""
PG_POOL_STATE_KEY = "pgconn"


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    """
    The database in use is QuestDB. To query from QuestDb, we
    can use a Postgres client.
    Initializes an asynchronous Postgres client from asyncpg.

    Args:
        app: The Litestar application instance.
            Used to attach the created client object to the
            application state which can be accessed in routes.
    """
    client = getattr(app.state, PG_POOL_STATE_KEY, None)
    if client is None:
        connection = await asyncpg.create_pool(
            host=config.QUESTDB_HOST,
            port=config.QUESTDB_PORT,
            user=config.QUESTDB_USER,
            password=config.QUESTDB_PASSWORD,
            database=config.QUESTDB_DB_NAME,
        )
        setattr(app.state, PG_POOL_STATE_KEY, connection)

    await connection.execute(records_table_init_command)
    await connection.execute(errors_table_init_command)
    await connection.execute(collector_metadata_table_init_command)
    await connection.execute(sensor_metadata_table_init_command)

    try:
        yield
    finally:
        await connection.close()
