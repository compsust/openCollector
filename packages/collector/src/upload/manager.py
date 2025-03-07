import requests
from collector.src.config.datastructures import UploadConfig
from config.manager import ConfigManager
from common.src import (
    CollectorReport,
    CollectorError,
    CollectorRecord,
    CollectorMetadata,
    SensorMetadata,
    records_table_name,
    errors_table_name,
    collector_metadata_table_name,
    sensor_metadata_table_name,
)


class UploadManager:
    collector_id: str
    config: UploadConfig
    endpoint: str

    def __init__(self, config_manager: ConfigManager):
        """
        Initializes the manager.
        """
        self.collector_id = config_manager.config.collector_id
        self.config = config_manager.config.upload

        # URL for QuestDB data POST. See: https://questdb.com/docs/reference/api/rest
        self.endpoint = "http://" + self.config.host + ":" + self.config.port + "/imp"

    def upload(
        self, report: CollectorReport, additional_errors: list[CollectorError] = []
    ):
        """
        Uploads a collector report.

        Args:
            report (CollectorReport): The report to upload.
            additional_errors (list[CollectorError]): Any additional errors to attach.
        """
        # Join any additional errors.
        errors = [*report.errors, *additional_errors]

        # Construct a CSV version of the errors.
        errors = self._construct_errors(errors)

        # Construct a CSV version of the records.
        records = self._construct_records(report.records)

        # Upload the errors.
        response = requests.post(self.endpoint, files=errors)
        # Raises an exception for any non-successful response.
        response.raise_for_status()

        # Upload the records.
        response = requests.post(self.endpoint, files=records)
        # Raises an exception for any non-successful response.
        response.raise_for_status()

    def upload_metadata(
        self,
        collector_metadata: CollectorMetadata,
        sensor_metadata: list[SensorMetadata],
    ):
        """
        Uploads the collector metadata.

        Args:
            collector_metadata (CollectorMetadata): Collector metadata.
            sensor_metadata (list[SensorMetadata]): Sensor metadata
        """
        # Construct a CSV of the collector metadata.
        collector = self._construct_collector_metadata(collector_metadata)
        # Construct a CSV of the sensor metadata.
        sensors = self._construct_sensor_metadata(sensor_metadata)

        # Upload the collector metadata.
        response = requests.post(self.endpoint, files=collector)
        # Raises an exception for any non-successful response.
        response.raise_for_status()

        # Upload the sensor metadata.
        response = requests.post(self.endpoint, files=sensors)
        # Raises an exception for any non-successful response.
        response.raise_for_status()

    def _construct_records(
        self, records: list[CollectorRecord]
    ) -> dict[str, tuple[str, str]]:
        """
        Given a list of CollectorRecord, constructs a CSV file in the format
        that QuestDB's REST API expects.
        """

        records_csv_lines = ["timestamp,collector_id,sensor_id,record_id,value"]
        for record in records:
            for record_id, datapoint in record.data:
                records_csv_lines.append(
                    f"{record.timestamp},{self.collector_id},{record.sensor_id},{record_id},{datapoint}"
                )
        csv = "\n".join(records_csv_lines)
        return {"data": (records_table_name, csv)}

    def _construct_errors(
        self, errors: list[CollectorError]
    ) -> dict[str, tuple[str, str]]:
        """
        Given a list of CollectorError, constructs a CSV file in the format
        that QuestDB's REST API expects.
        """

        errors_csv_lines = ["timestamp,collector_id,sensor_id,error_message"]
        for error in errors:
            errors_csv_lines.append(
                f"{error.timestamp},{self.collector_id},{error.sensor_id},{error.error_message}"
            )
        csv = "\n".join(errors_csv_lines)
        return {"data": (errors_table_name, csv)}

    def _construct_collector_metadata(
        self, metadata: CollectorMetadata
    ) -> dict[str, tuple[str, str]]:
        """
        Given a CollectorMetadata, constructs a CSV file in the format
        that QuestDB's REST API expects.
        """
        csv = (
            "collector_id,collector_name,device_model,polling_interval\n"
            f"{metadata.collector_id},{metadata.collector_name},{metadata.device_model},{metadata.polling_interval}"
        )
        return {"data": (collector_metadata_table_name, csv)}

    def _construct_sensor_metadata(
        self, metadata: list[SensorMetadata]
    ) -> dict[str, tuple[str, str]]:
        """
        Given a list of SensorMetadata, constructs a CSV file in the format
        that QuestDB's REST API expects.
        """
        metadata_csv_lines = ["collector_id,sensor_id,sensor_code,sensor_name"]
        for data in metadata:
            metadata_csv_lines.append(
                f"{data.collector_id},{data.sensor_id},{data.sensor_code},{data.sensor_name}"
            )
        csv = "\n".join(metadata_csv_lines)
        return {"data": (sensor_metadata_table_name, csv)}
