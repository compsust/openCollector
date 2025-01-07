from litestar import Controller, get

from storage.datastructures import CollectorDetails, NodeSummary, SensorDetails


class ApiQueryController(Controller):
    path = "/query"

    @get()
    def get_summary(self) -> NodeSummary:
        raise NotImplementedError

    @get()
    def get_collector(self) -> CollectorDetails:
        raise NotImplementedError

    @get()
    def get_sensor(self) -> SensorDetails:
        raise NotImplementedError
