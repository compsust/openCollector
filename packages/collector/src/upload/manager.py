import requests
from typing import Any
from collector.src.config.datastructures import UploadConfig
from config.manager import ConfigManager
from common import SensorReport


class UploadManager:
    config: UploadConfig
    endpoint: str

    def __init__(self, config_manager: ConfigManager):
        """
        Initializes the manager.
        """
        self.config = config_manager.config.upload

        # URL for QuestDB data POST. See: https://questdb.com/docs/reference/api/rest
        self.endpoint = "http://" + self.config.host + ":" + self.config.port + "/imp"

    def upload(self, report: SensorReport):
        # Construct a CSV version of the errors.
        errors = {"data": ("errors", "")}

        # Construct a CSV version of the records.
        records = self._construct_records(report)

        # Upload the errors.
        response = requests.post(self.endpoint, files=errors)
        # Raises an exception for any non-successful response.
        response.raise_for_status()

        # Upload the records.
        response = requests.post(self.endpoint, files=records)
        # Raises an exception for any non-successful response.
        response.raise_for_status()

    def _construct_records(self, report: SensorReport) -> dict[str, Any]:
        records = ["collector_id,collector_name,sensor_id,sensor_code,record_id,value"]
        for record in report.records:
            records.append("")
        csv = "\n".join(records)
        return {"data": ("records", csv)}
