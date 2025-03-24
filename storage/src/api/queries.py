from litestar import Controller, get

from database.repository import Repository
from datastructures import CollectorDetails, NetworkSummary, SensorDetails


class ApiQueryController(Controller):
    path = "/query"

    @get(
        path="summary",
        description="Returns the summary for all data contained in this storage node.",
    )
    async def get_network_summary(self, repository: Repository) -> NetworkSummary:
        return await repository.get_network_summary()

    @get(
        path="collectors/{collector_id:str}",
        description="Returns the details for all data contained in a collector node.",
    )
    async def get_collector_details(
        self,
        collector_id: str,
        errors_page: int,
        errors_page_size: int,
        repository: Repository,
    ) -> CollectorDetails:
        return await repository.get_collector_details(
            collector_id=collector_id,
            errors_page=errors_page,
            errors_page_size=errors_page_size,
        )

    @get(
        path="collectors/sensors/{sensor_id:str}",
        description="Returns the details for all data contained in a sensor.",
    )
    async def get_sensor_details(
        self,
        sensor_id: str,
        records_page: int,
        records_page_size: int,
        errors_page: int,
        errors_page_size: int,
        repository: Repository,
    ) -> SensorDetails:
        return await repository.get_sensor_details(
            sensor_id=sensor_id,
            records_page=records_page,
            records_page_size=records_page_size,
            errors_page=errors_page,
            errors_page_size=errors_page_size,
        )
