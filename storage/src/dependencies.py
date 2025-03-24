from litestar.datastructures import State
from litestar.di import Provide
from database.repository import Repository
from database.lifespan import PG_CONN_STATE_KEY


async def get_repository(state: State) -> Repository:
    connection = getattr(state, PG_CONN_STATE_KEY, None)
    if connection is None:
        raise ValueError("Postgres connection not set on litestart global state.")

    return Repository(connection)


dependencies = {"repository": Provide(get_repository)}
