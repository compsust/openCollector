from litestar import Controller, get
from litestar.plugins.htmx import HTMXTemplate, HTMXRequest
from litestar.response import Template
from datastructures import NetworkSummary


class BrowserSnippetsController(Controller):
    path = "/snippets"

    @get(path="/network_summary", operation_id="network_summary", tags=["frontend:network_summary"], status_code=200, include_in_schema=False)
    async def network_summary(self, request: HTMXRequest) -> Template:
        summary = NetworkSummary(total_collectors=5, collectors_reporting=2, total_sensors=7, sensors_reporting=3, records_reported=111, errors_reported=12, collectors=[])

        context = {
            "request": request,
            "network_summary": summary
        }
        return HTMXTemplate(
            template_name="snippets/network_summary.html", context=context
        )