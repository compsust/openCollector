from litestar import Litestar
from pathlib import Path
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar.plugins.htmx import HTMXPlugin
from litestar.static_files import create_static_files_router

from database import db_connection
from api import api_router
from browser import browser_router
from dependencies import dependencies

static_files = create_static_files_router(path="/static", directories=["static"])

app = Litestar(
    route_handlers=[api_router, browser_router, static_files],
    plugins=[HTMXPlugin()],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    lifespan=[db_connection],
    dependencies=dependencies,
)