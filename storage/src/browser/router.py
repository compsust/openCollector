from litestar import Router
from litestar_htmx import HTMXRequest

from .pages import BrowserPagesController
from .snippets import BrowserSnippetsController

browser_router = Router(
    path="",
    route_handlers=[BrowserPagesController, BrowserSnippetsController],
    request_class=HTMXRequest,
)
