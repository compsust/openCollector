from litestar import Controller, get
from litestar.response import Template


class BrowserHtmlController(Controller):
    path = ""

    @get(path="")
    async def dashboard(self) -> Template:
        return Template(template_name="dashboard.html.jinja2", context={})

    @get(path="collectors/{collector_id:str}")
    async def collector(self, collector_id: str) -> Template:
        return Template(template_name="collector_details.html.jinja2", context={})

    @get(path="collectors/{collector_id:str}/sensors/{sensor_id:str}")
    async def sensor(self, collector_id: str, sensor_id: str) -> Template:
        return Template(template_name="sensor_details.html.jinja2", context={})
