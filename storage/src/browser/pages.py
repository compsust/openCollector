from litestar import Controller, get, Request
from litestar.plugins.htmx import HTMXTemplate, HTMXRequest
from litestar.response import Template
import config


class BrowserPagesController(Controller):
    @get(
        path="/",
        operation_id="index",
        tags=["frontend:index"],
        status_code=200,
        include_in_schema=False,
    )
    async def index(self, request: Request) -> Template:
        context = {"request": request, "node_name": config.NODE_NAME}
        return Template(template_name="index.html", context=context)

    @get(
        path="/about",
        operation_id="about",
        tags=["frontend:about"],
        status_code=200,
        include_in_schema=False,
    )
    async def about(self, request: Request) -> Template:
        context = {"request": request}
        return Template(template_name="about.html", context=context)

    @get(
        path="/login",
        operation_id="login",
        tags=["frontend:login"],
        status_code=200,
        include_in_schema=False,
    )
    async def login(self, request: Request) -> Template:
        context = {"request": request}
        return Template(template_name="login.html", context=context)

    @get(
        path="/dashboard",
        operation_id="dashboard",
        tags=["frontend:dashboard"],
        status_code=200,
        include_in_schema=False,
    )
    async def dashboard(self, request: HTMXRequest) -> Template:
        context = {
            "request": request,
            "refresh_s": config.INTERFACE_REFRESH_SECONDS,
        }
        return HTMXTemplate(template_name="dashboard.html", context=context)

    @get(
        path="/collectors/{collector_id:str}",
        operation_id="collector",
        tags=["frontend:collector"],
        status_code=200,
        include_in_schema=False,
    )
    async def collector(self, collector_id: str, request: Request) -> Template:
        context = {
            "request": request,
            collector_id: collector_id,
        }
        return Template(template_name="collector.html", context=context)

    @get(
        path="/collectors/{collector_id:str}/sensors/{sensor_id:str}",
        operation_id="sensor",
        tags=["frontend:sensor"],
        status_code=200,
        include_in_schema=False,
    )
    async def sensor(
        self, collector_id: str, sensor_id: str, request: Request
    ) -> Template:
        context = {"request": request, collector_id: collector_id, sensor_id: sensor_id}
        return Template(template_name="sensor.html", context=context)
