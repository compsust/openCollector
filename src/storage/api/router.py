from litestar import Router

from .commands import ApiCommandController
from .queries import ApiQueryController

api_router = Router(
    path="/api", route_handlers=[ApiCommandController, ApiQueryController]
)
