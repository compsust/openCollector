from litestar import Controller, get
from litestar.plugins.htmx import HTMXTemplate, HTMXRequest
from litestar.response import Template
from bokeh.plotting import figure
from bokeh.embed import components

from common import RecordID, get_unit_from_record_id, get_record_ids
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
        summary = await repository.get_network_summary()

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
    async def collector_select_options(
        self, repository: Repository, request: HTMXRequest
    ) -> Template:
        print("collector_ids")
        collector_ids = await repository.get_collector_ids()
        print(collector_ids)
        options = [
            {"value": collector["collector_id"], "label": collector["collector_name"]}
            for collector in collector_ids
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
        self, collector_id: str, repository: Repository, request: HTMXRequest
    ) -> Template:
        print("collector id:::")
        print(collector_id)
        sensor_ids = await repository.get_sensor_ids(collector_id)
        options = [
            {"value": sensor["sensor_id"], "label": sensor["sensor_name"]}
            for sensor in sensor_ids
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
        self, sensor_id: str, repository: Repository, request: HTMXRequest
    ) -> Template:
        sensor_code = await repository.get_sensor_code(sensor_id)
        print("sensor code")
        print(sensor_code)
        record_ids = get_record_ids(sensor_code)
        options = [{"value": record_id, "label": record_id} for record_id in record_ids]

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
        self,
        collector_id: str,
        sensor_id: str,
        record_id: str,
        repository: Repository,
        request: HTMXRequest,
    ) -> Template:
        if not collector_id or not sensor_id or not record_id:
            return HTMXTemplate(template_name="snippets/bokeh_failed.html")

        timeline = await repository.get_timeline(
            collector_id=collector_id, sensor_id=sensor_id, record_id=record_id
        )
        sensor_code = await repository.get_sensor_code(sensor_id)
        unit = get_unit_from_record_id(sensor_code=sensor_code, record_id=record_id)

        graph = figure(sizing_mode="stretch_both")
        graph.line(x=timeline.timestamps, y=timeline.values)

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
