from litestar import Controller, get
from litestar.plugins.htmx import HTMXTemplate, HTMXRequest
from litestar.response import Template
from bokeh.plotting import figure
from bokeh.embed import components

from database.repository import Repository
from datastructures import CollectorSummary, NetworkSummary, SensorSummary


class BrowserSnippetsController(Controller):
    path = "/snippets"

    @get(
        path="/network_summary",
        operation_id="network_summary",
        tags=["frontend:network_summary"],
        status_code=200,
        include_in_schema=False,
    )
    async def network_summary(
        self, repository: Repository, request: HTMXRequest
    ) -> Template:
        print(repository)
        summary = await repository.get_network_summary()
        print(summary)

        context = {"request": request, "network_summary": summary}
        return HTMXTemplate(
            template_name="snippets/network_summary.html", context=context
        )

    @get(
        path="/collector_select_options",
        operation_id="collector_select_options",
        tags=["frontend:collector_select_options"],
        status_code=200,
        include_in_schema=False,
    )
    async def collector_select_options(self, request: HTMXRequest) -> Template:
        options = [
            {"value": "collector1", "label": "Collector 1"},
            {"value": "collector2", "label": "Collector 2"},
            {"value": "collector3", "label": "Collector 3"},
        ]

        context = {"request": request, "options": options}
        return HTMXTemplate(
            template_name="snippets/collector_select_options.html", context=context
        )

    @get(
        path="/sensor_select_options",
        operation_id="sensor_select_options",
        tags=["frontend:sensor_select_options"],
        status_code=200,
        include_in_schema=False,
    )
    async def sensor_select_options(
        self, collector_id: str, request: HTMXRequest
    ) -> Template:
        options = [
            {"value": "sensor1", "label": "Senser 1"},
            {"value": "sensor2", "label": "Sensor 2"},
            {"value": "sensor3", "label": "Sensor 3"},
        ]

        context = {"request": request, "options": options}
        return HTMXTemplate(
            template_name="snippets/sensor_select_options.html", context=context
        )

    @get(
        path="/record_select_options",
        operation_id="record_select_options",
        tags=["frontend:record_select_options"],
        status_code=200,
        include_in_schema=False,
    )
    async def record_select_options(
        self, sensor_id: str, request: HTMXRequest
    ) -> Template:
        options = [
            {"value": "record1", "label": "Record 1"},
            {"value": "record2", "label": "Record 2"},
            {"value": "record3", "label": "Record 3"},
        ]

        context = {"request": request, "options": options}
        return HTMXTemplate(
            template_name="snippets/record_select_options.html", context=context
        )

    @get(
        path="/graph",
        operation_id="graph",
        tags=["frontend:graph"],
        status_code=200,
        include_in_schema=False,
    )
    async def graph(
        self, sensor_id: str, record_id: str, request: HTMXRequest
    ) -> Template:
        x_values = [1, 2, 3, 4, 5]
        y_values = [6, 7, 2, 3, 6]

        graph = figure(sizing_mode="stretch_both")
        graph.line(x=x_values, y=y_values)

        script, div = components(graph)

        context = {"script": script, "div": div}
        return HTMXTemplate(template_name="snippets/bokeh.html", context=context)

    @get(
        path="/collector_summary",
        operation_id="collector_summary",
        tags=["frontend:collector_summary"],
        status_code=200,
        include_in_schema=False,
    )
    async def collector_summary(self, request: HTMXRequest) -> Template:
        summary = NetworkSummary(
            total_collectors=5,
            collectors_reporting=2,
            total_sensors=7,
            sensors_reporting=3,
            records_reported=111,
            errors_reported=12,
            collectors=[
                CollectorSummary(
                    id=f"collector_id{index}",
                    name=f"collector_{index}",
                    status="OPERATIONAL",
                    sensors=[],
                )
                for index in range(50)
            ],
        )

        context = {"request": request, "network_summary": summary}
        return HTMXTemplate(
            template_name="snippets/collector_summary.html", context=context
        )
