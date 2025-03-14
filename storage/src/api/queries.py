from litestar import Controller, get

from datastructures import CollectorDetails, NodeSummary, SensorDetails


class ApiQueryController(Controller):
    path = "/query"

    @get(
        path="summary",
        description="Returns the summary for all data contained in this storage node.",
    )
    async def get_summary(self) -> NodeSummary:
        raise NotImplementedError

    @get(
        path="collectors/{collector_id:str}",
        description="Returns the details for all data contained in a collector node.",
    )
    async def get_collector(self, collector_id: str) -> CollectorDetails:
        raise NotImplementedError

    @get(
        path="collectors/{collector_id:str}/sensors/{sensor_id:str}",
        description="Returns the details for all data contained in a sensor.",
    )
    async def get_sensor(self, collector_id: str, sensor_id: str) -> SensorDetails:
        raise NotImplementedError
