from litestar import Controller, get
from litestar.plugins.htmx import HTMXTemplate, HTMXRequest
from litestar.response import Template
from bokeh.plotting import figure
from bokeh.embed import components

from common import get_record_ids
from database.repository import Repository


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
        """
        Retrieves the network summary HTML snippet

        Args:
            repository: Database interface. Provided through
                Litestar's dependency injection.
            request: HTTP Request instance.

        Returns:
            HTML.
        """
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
        """
        Retrieves the collector select options HTML snippet.

        Args:
            repository: Database interface. Provided through
                Litestar's dependency injection.
            request: HTTP Request instance.

        Returns:
            HTML.
        """
        collector_ids = await repository.get_collector_ids()
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
        """
        Retrieves the sensor select options HTML snippet.

        Args:
            collector_id: The collector to retrieve sensors for.
                Provided through Litestar as a query parameter.
            repository: Database interface. Provided through
                Litestar's dependency injection.
            request: HTTP Request instance.

        Returns:
            HTML.
        """
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
        """
        Retrieves the record select options HTML snippet.

        Args:
            sensor_id: The sensor to retrieve record IDs for.
                Provided through Litestar as a query parameter.
            repository: Database interface. Provided through
                Litestar's dependency injection.
            request: HTTP Request instance.

        Returns:
            HTML.
        """
        sensor_code = await repository.get_sensor_code(sensor_id)
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
        """
        Retrieves the graph HTML snippet.

        Args:
            collector_id: The collector to retrieve the graph for.
                Provided through Litestar as a query parameter.
            sensor_id: The sensor to retrieve the graph for.
                Provided through Litestar as a query parameter.
            record_id: The record ID to retrieve the graph for.
                Provided through Litestar as a query parameter.
            repository: Database interface. Provided through
                Litestar's dependency injection.
            request: HTTP Request instance.

        Returns:
            HTML.
        """
        if not collector_id or not sensor_id or not record_id:
            return HTMXTemplate(template_name="snippets/bokeh_failed.html")

        try:
            timeline = await repository.get_timeline(
                collector_id=collector_id, sensor_id=sensor_id, record_id=record_id
            )
        except:
            return HTMXTemplate(template_name="snippets/bokeh_failed.html")

        graph = figure(
            x_axis_type="datetime",
            y_axis_label=f"{timeline.record_name} ({timeline.unit})",
            sizing_mode="stretch_both",
        )
        graph.line(x=timeline.timestamps, y=timeline.values)

        script, div = components(graph)

        context = {"request": request, "script": script, "div": div}
        return HTMXTemplate(template_name="snippets/bokeh.html", context=context)

    @get(
        path="/collector_summary",
        operation_id="collector_summary",
        tags=["frontend:collector_summary"],
        status_code=200,
        include_in_schema=False,
    )
    async def collector_summary(
        self, repository: Repository, request: HTMXRequest
    ) -> Template:
        """
        Retrieves the collector summary HTML snippet.

        Args:
            repository: Database interface. Provided through
                Litestar's dependency injection.
            request: HTTP Request instance.

        Returns:
            HTML.
        """
        summaries = await repository.get_collector_summaries()

        context = {"request": request, "summaries": summaries}
        return HTMXTemplate(
            template_name="snippets/collector_summary.html", context=context
        )
