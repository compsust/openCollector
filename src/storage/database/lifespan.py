from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

import influxdb_client


from litestar import Litestar


"""
The keys used to set objects on the Litestar application state.
"""
INFLUXDB_CLIENT_STATE_KEY = "influxdb_client"
INFLUXDB_QUERY_CLIENT_STATE_KEY = "influxdb_query_client"


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    """
    Initializes the InfluxDB client.

    Args:
        app (Litestar): The Litestar application instance.
            Used to attach the created client object to the
            application state which can be accessed in routes.
    """
    client = getattr(app.state, INFLUXDB_CLIENT_STATE_KEY, None)
    if client is None:
        # TODO: Add these as environment variables.t
        client = influxdb_client.InfluxDBClient(url="", token="", org="")
        query_client = client.query_api()
        setattr(app.state, INFLUXDB_CLIENT_STATE_KEY, client)
        setattr(app.state, INFLUXDB_QUERY_CLIENT_STATE_KEY, query_client)

    try:
        yield
    finally:
        client.close()
