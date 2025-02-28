from litestar import Router

from .html import BrowserHtmlController
from .htmx import BrowserHtmxController

browser_router = Router(
    path="", route_handlers=[BrowserHtmlController, BrowserHtmxController]
)
