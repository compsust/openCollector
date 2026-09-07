import config
from database.repository import Repository
from litestar import Controller, Request, get
from litestar.plugins.htmx import HTMXRequest, HTMXTemplate
from litestar.response import Template


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
    async def collector(
        self, collector_id: str, repository: Repository, request: Request
    ) -> Template:
        details = await repository.get_collector_details(
            collector_id=collector_id, errors_page=0, errors_page_size=50
        )
        context = {
            "request": request,
            "collector": details,
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
        self,
        collector_id: str,
        sensor_id: str,
        repository: Repository,
        request: Request,
    ) -> Template:
        details = await repository.get_sensor_details(
            sensor_id=sensor_id,
            records_page=0,
            records_page_size=100,
            errors_page=0,
            errors_page_size=50,
        )
        context = {
            "request": request,
            "collector_id": collector_id,
            "sensor": details,
        }
        return Template(template_name="sensor.html", context=context)
