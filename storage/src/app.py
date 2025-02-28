from litestar import Litestar
from pathlib import Path
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar.plugins.htmx import HTMXPlugin

from database.lifespan import db_connection
from api import api_router
from browser import browser_router

app = Litestar(
    route_handlers=[api_router, browser_router],
    plugins=[HTMXPlugin()],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    lifespan=[db_connection],
)
