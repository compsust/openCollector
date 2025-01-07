from litestar import Litestar

from .api import api_router

app = Litestar(route_handlers=[api_router])
