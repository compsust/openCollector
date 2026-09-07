from pathlib import Path

import config
from api import api_router
from asyncpg import Connection
from auth import BasicAuthMiddleware
from browser import browser_router
from database import db_connection
from dependencies import dependencies
from litestar import Litestar, get
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.plugins.htmx import HTMXPlugin
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig


@get(path="/health", include_in_schema=False)
async def health(connection: Connection) -> dict[str, str]:
    """Return readiness only when the database connection is usable."""
    await connection.fetchval("SELECT 1")
    return {"status": "ok"}


static_files = create_static_files_router(path="/static", directories=["static"])

app = Litestar(
    route_handlers=[health, api_router, browser_router, static_files],
    middleware=[BasicAuthMiddleware],
    plugins=[HTMXPlugin()],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    lifespan=[db_connection],
    dependencies=dependencies,
    debug=config.DEBUG,
)
