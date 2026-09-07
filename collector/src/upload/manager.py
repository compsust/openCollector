try:
    import requests
except ImportError:
    import urequests as requests

try:
    import base64
except ImportError:
    import ubinascii as base64

from common import (
    collector_metadata_table_name,
    errors_table_name,
    records_table_name,
    sensor_metadata_table_name,
)

from ..config import ConfigManager, UploadConfig
from ..datastructures import (
    CollectorError,
    CollectorMetadata,
    CollectorRecord,
    CollectorReport,
    SensorMetadata,
)


class UploadManager:
    """
    Handles formatting and upload of the data to the database.

    Attributes:
        collector_id: The ID of the collector set on the config.
        config: The upload config.
        endpoint: The endpoint string at which to reach the
            QuestDB REST API.
    """

    collector_id: str
    config: UploadConfig
    endpoint: str

    def __init__(self, config_manager: ConfigManager):
        """
        Initializes the manager.

        Args:
            config_manager: The config manager used to retrieve
                the upload config.
        """
        self.collector_id = config_manager.config.collector_id
        self.config = config_manager.config.upload

        # URL for QuestDB data POST. See: https://questdb.com/docs/reference/api/rest
        self.endpoint = f"http://{self.config.host}:{self.config.port}/imp"
        credentials = f"{self.config.user}:{self.config.password}".encode()
        encoder = (
            base64.b64encode if hasattr(base64, "b64encode") else base64.b2a_base64
        )
        encoded = encoder(credentials).decode().strip()
        self.headers = {"Authorization": f"Basic {encoded}"}

    def _post_files(self, files: dict[str, tuple[str, str]]):
        """POST one CSV file as multipart data on CPython or MicroPython."""
        _, (filename, csv) = next(iter(files.items()))
        boundary = "----openCollectorBoundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="data"; filename="{filename}"\r\n'
            "Content-Type: text/csv\r\n\r\n"
            f"{csv}\r\n--{boundary}--\r\n"
        ).encode()
        headers = dict(self.headers)
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        response = requests.post(self.endpoint, data=body, headers=headers)
        try:
            if hasattr(response, "raise_for_status"):
                response.raise_for_status()
            elif response.status_code < 200 or response.status_code >= 300:
                raise RuntimeError(
                    f"QuestDB upload failed: HTTP {response.status_code}"
                )
        finally:
            if hasattr(response, "close"):
                response.close()

    def upload(
        self,
        report: CollectorReport,
        additional_errors: list[CollectorError] | None = None,
    ):
        """
        Uploads a collector report.

        Args:
            report: The report to upload.
            additional_errors: Any additional errors to attach.
        """
        # Join any additional errors.
        errors = [*report.errors, *(additional_errors or [])]

        # Construct a CSV version of the errors.
        errors = self._construct_errors(errors)

        # Construct a CSV version of the records.
        records = self._construct_records(report.records)

        # Upload the errors.
        self._post_files(errors)

        # Upload the records.
        self._post_files(records)

    def upload_metadata(
        self,
        collector_metadata: CollectorMetadata,
        sensor_metadata: list[SensorMetadata],
    ):
        """
        Uploads the collector and sensor metadata.

        Args:
            collector_metadata: Collector metadata.
            sensor_metadata: Sensor metadata
        """
        # Construct a CSV of the collector metadata.
        collector = self._construct_collector_metadata(collector_metadata)
        # Construct a CSV of the sensor metadata.
        sensors = self._construct_sensor_metadata(sensor_metadata)

        # Upload the collector metadata.
        self._post_files(collector)

        # Upload the sensor metadata.
        self._post_files(sensors)

    def _construct_records(
        self, records: list[CollectorRecord]
    ) -> dict[str, tuple[str, str]]:
        """
        Given a list of CollectorRecord, constructs a CSV file in the format
        that QuestDB's REST API expects.

        Args:
            records: The collector records to format.

        Returns:
            The data in CSV format.
        """

        records_csv_lines = ["timestamp,collector_id,sensor_id,record_id,value"]
        for record in records:
            for record_id, value in record.data.items():
                records_csv_lines.append(
                    f"{record.timestamp},{self.collector_id},{record.sensor_id},{record_id},{value}"
                )
        csv = "\n".join(records_csv_lines)
        return {"data": (records_table_name, csv)}

    def _construct_errors(
        self, errors: list[CollectorError]
    ) -> dict[str, tuple[str, str]]:
        """
        Given a list of CollectorError, constructs a CSV file in the format
        that QuestDB's REST API expects.

        Args:
            records: The collector errors to format.

        Returns:
            The data in CSV format.
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

        Args:
            records: The collector metadata to format.

        Returns:
            The data in CSV format.
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

        Args:
            records: The sensor_metadata to format.

        Returns:
            The data in CSV format.
        """
        metadata_csv_lines = ["collector_id,sensor_id,sensor_code,sensor_name"]
        for data in metadata:
            metadata_csv_lines.append(
                f"{data.collector_id},{data.sensor_id},{data.sensor_code},{data.sensor_name}"
            )
        csv = "\n".join(metadata_csv_lines)
        return {"data": (sensor_metadata_table_name, csv)}
