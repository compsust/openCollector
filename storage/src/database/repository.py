from datetime import datetime, timedelta
from asyncpg.connection import Connection
from common import CollectorRecord, get_unit_from_record_id
from datastructures import (
    SensorSummary,
    CollectorSummary,
    NetworkSummary,
    CollectorDetails,
    SensorDetails,
    CollectorError,
    CollectorRecord,
    StatusEnum,
)
from . import queries
import config


class RepostioryError(Exception):
    """Base class for query errors."""

    pass


class Repository:
    connection: Connection

    def __init__(self, connection: Connection):
        self.connection = connection

    async def get_network_summary(self) -> NetworkSummary:
        """
        Retrieves the network summary from the database.

        Returns:
            NetworkSummary: A summary of the network, its collectors, and sensors.
        """
        # Retrieve the data from the database.
        latest_collector_metadata = await queries.latest_collector_metadata_query(
            self.connection
        )
        latest_sensor_metadata = await queries.latest_sensor_metadata_query(
            self.connection
        )
        latest_records = await queries.latest_records_query(self.connection)
        latest_errors = await queries.latest_errors_query(self.connection)
        total_collectors = await queries.collector_count_query(self.connection)
        total_sensors = await queries.sensor_count_query(self.connection)
        total_records = await queries.total_records_query(self.connection)
        total_errors = await queries.total_errors_query(self.connection)

        # Initialize the collector summaries.
        collector_summaries: list[CollectorSummary] = []
        for collector in latest_collector_metadata:
            collector_summaries.append(
                CollectorSummary(
                    id=collector["collector_id"],
                    name=collector["collector_name"],
                    status=StatusEnum.UNKNOWN,
                    sensors=[],
                )
            )

        # Populate the sensor summaries.
        for record in latest_records:
            # Retrieve the sensor metadata of the sensor responsible for this record.
            sensor_metadata = next(
                (
                    sensor
                    for sensor in latest_sensor_metadata
                    if sensor["sensor_id"] == record["sensor_id"]
                ),
                None,
            )
            if sensor_metadata is None:
                raise RepostioryError(
                    "Sensor record detected with a sensor ID that isn't found in the sensor metadata."
                )

            # Retrieve the collector summary with this sensor.
            collector_summary = next(
                (
                    collector
                    for collector in collector_summaries
                    if record["collector_id"] == collector.id
                ),
                None,
            )
            if collector_summary is None:
                raise RepostioryError(
                    "Sensor record detected with a collector ID that isn't found in the collector metadata."
                )

            # Retrieve the sensor summary in the collector summary with this sensor.
            # Create it if this is the first sensor time this sensor has been processed.
            sensor_summary = next(
                (
                    sensor
                    for sensor in collector_summary.sensors
                    if sensor.id == record["sensor_id"]
                ),
                None,
            )
            if sensor_summary is None:
                sensor_summary = SensorSummary(
                    id=record["sensor_id"],
                    name=sensor_metadata["sensor_name"],
                    status=StatusEnum.UNKNOWN,
                    last_value={},
                )
                collector_summary.sensors.append(sensor_summary)

            # Add the record value to the sensor data.
            if not sensor_summary.last_value:
                sensor_summary.last_value = {}
            sensor_summary.last_value[record["record_id"]] = record["value"]

        # Populate the status field on the summaries.
        collectors_reporting = 0
        sensors_reporting = 0
        for collector_summary in collector_summaries:
            # Retrieve the collector metadata of the sensor responsible for this record.
            collector_metadata = next(
                (
                    collector
                    for collector in latest_collector_metadata
                    if collector["collector_id"] == collector_summary.id
                ),
                None,
            )
            if collector_metadata is None:
                raise RepostioryError(
                    "Collector detected with a collector ID that isn't found in the collector metadata."
                )

            collector_summary.status = StatusEnum.OPERATIONAL
            for sensor_summary in collector_summary.sensors:
                # Retrieve the latest record returned by this sensor.
                # Note that there may be multiple records per sensor,
                # so we need to grab the latest out of those.
                # The records will probably have the same timestamp,
                # or they will be close enough together that it shouldn't matter,
                # but they are sorted here to be safe.
                latest_record = max(
                    (
                        record
                        for record in latest_records
                        if record["sensor_id"] == sensor_summary.id
                    ),
                    key=lambda r: r["timestamp"],
                    default=None,
                )

                # Retrieve the latest error returned by this sensor.
                latest_error = next(
                    (
                        error
                        for error in latest_errors
                        if error["sensor_id"] == sensor_summary.id
                    ),
                    None,
                )

                # If there are no latest records and no latest errors the status is UNKNOWN.
                if not latest_record and not latest_error:
                    sensor_summary.status = StatusEnum.UNKNOWN
                    collector_summary.status = StatusEnum.UNKNOWN
                    continue

                # If the latest record or error is long ago enough, determined
                # by active_device_polling_threshold, is is considered DROPPED.
                latest_timestamp = max(
                    (
                        item["timestamp"]
                        for item in (latest_record, latest_error)
                        if item is not None
                    )
                )
                active_threshold = timedelta(
                    milliseconds=(
                        collector_metadata["polling_interval"]
                        * config.ACTIVE_DEVICE_POLLING_THRESHOLD
                    )
                )
                if latest_timestamp < (datetime.now() - active_threshold):
                    sensor_summary.status = StatusEnum.DROPPED
                    collector_summary.status = StatusEnum.DROPPED
                    continue

                # If the error is more recent than the record, the status is ERROR.
                if (latest_error and not latest_record) or (
                    latest_error
                    and latest_record
                    and latest_error["timestamp"] > latest_record["timestamp"]
                ):
                    sensor_summary.status = StatusEnum.ERROR
                    collector_summary.status = StatusEnum.ERROR
                    sensors_reporting += 1
                    continue

                # Otherwise, it is OPERATIONAL.
                sensor_summary.status = StatusEnum.OPERATIONAL
                sensors_reporting += 1

            if (
                collector_summary.status == StatusEnum.ERROR
                or collector_summary.status == StatusEnum.OPERATIONAL
            ):
                collectors_reporting += 1

        # Create and return the node summary
        return NetworkSummary(
            total_collectors=total_collectors[0]["count_distinct"],
            collectors_reporting=collectors_reporting,
            total_sensors=total_sensors[0]["count_distinct"],
            sensors_reporting=sensors_reporting,
            records_reported=total_records[0]["count"],
            errors_reported=total_errors[0]["count"],
            collectors=collector_summaries,
        )

    async def get_collector_details(
        self, collector_id: str, errors_page: int, errors_page_size: int
    ) -> CollectorDetails:
        """
        Retrieves the collector summary from the database

        Args:
            collector_id (str): The ID of the collector.
            errors_page (int): The index of the pagination result. Starts at 0.
            errors_page_size (int): The size of the page of results.

        Returns:
            CollectorDetails: The details for a collector.
        """
        # Retrieve the data from the database.
        latest_collector_metadata = await queries.latest_collector_metadata_query(
            self.connection
        )
        latest_sensor_metadata = await queries.latest_sensor_metadata_query(
            self.connection
        )
        collector_stats = await queries.collector_stats_query(
            self.connection, collector_id
        )
        latest_records = await queries.latest_records_from_collector_query(
            self.connection, collector_id
        )
        latest_errors = await queries.latest_errors_from_collector_query(
            self.connection, collector_id
        )
        collector_errors = await queries.errors_from_collector_query(
            self.connection, collector_id, errors_page, errors_page_size
        )

        # Retrieve the collector metadata of this ID.
        collector_metadata = next(
            (
                collector
                for collector in latest_collector_metadata
                if collector["collector_id"] == collector_id
            ),
            None,
        )
        if collector_metadata is None:
            raise RepostioryError(
                "Collector detected with a collector ID that isn't found in the collector metadata."
            )

        # Populate the sensor summaries
        sensor_summaries: list[SensorSummary] = []
        for record in latest_records:
            # Retrieve the sensor metadata of the sensor responsible for this record.
            sensor_metadata = next(
                (
                    sensor
                    for sensor in latest_sensor_metadata
                    if sensor["sensor_id"] == record["sensor_id"]
                ),
                None,
            )
            if sensor_metadata is None:
                raise RepostioryError(
                    "Sensor record detected with a sensor ID that isn't found in the sensor metadata."
                )

            # Retrieve the sensor summary in the collector summary with this sensor.
            # Create it if this is the first sensor time this sensor has been processed.
            sensor_summary = next(
                (
                    sensor
                    for sensor in sensor_summaries
                    if sensor.id == record["sensor_id"]
                ),
                None,
            )
            if sensor_summary is None:
                sensor_summary = SensorSummary(
                    id=record["sensor_id"],
                    name=sensor_metadata["sensor_name"],
                    status=StatusEnum.UNKNOWN,
                    last_value={},
                )
                sensor_summaries.append(sensor_summary)

            # Add the record value to the sensor data.
            if not sensor_summary.last_value:
                sensor_summary.last_value = {}
            sensor_summary.last_value[record["record_id"]] = record["value"]

        # Populate the status field on the summaries.
        status = StatusEnum.OPERATIONAL
        for sensor_summary in sensor_summaries:
            # Retrieve the latest record returned by this sensor.
            # Note that there may be multiple records per sensor,
            # so we need to grab the latest out of those.
            # The records will probably have the same timestamp,
            # or they will be close enough together that it shouldn't matter,
            # but they are sorted here to be safe.
            latest_record = max(
                (
                    record
                    for record in latest_records
                    if record["sensor_id"] == sensor_summary.id
                ),
                key=lambda r: r["timestamp"],
                default=None,
            )

            # Retrieve the latest error returned by this sensor.
            latest_error = next(
                (
                    error
                    for error in latest_errors
                    if error["sensor_id"] == sensor_summary.id
                ),
                None,
            )

            # If there are no latest records and no latest errors the status is UNKNOWN.
            if not latest_record and not latest_error:
                sensor_summary.status = StatusEnum.UNKNOWN
                status = StatusEnum.UNKNOWN
                continue

            # If the latest record or error is long ago enough, determined
            # by active_device_polling_threshold, is is considered DROPPED.
            latest_timestamp = max(
                (
                    item["timestamp"]
                    for item in (latest_record, latest_error)
                    if item is not None
                )
            )
            active_threshold = timedelta(
                milliseconds=(
                    collector_metadata["polling_interval"]
                    * config.ACTIVE_DEVICE_POLLING_THRESHOLD
                )
            )
            if latest_timestamp < (datetime.now() - active_threshold):
                sensor_summary.status = StatusEnum.DROPPED
                status = StatusEnum.DROPPED
                continue

            # If the error is more recent than the record, the status is ERROR.
            if (latest_error and not latest_record) or (
                latest_error
                and latest_record
                and latest_error["timestamp"] > latest_record["timestamp"]
            ):
                sensor_summary.status = StatusEnum.ERROR
                status = StatusEnum.ERROR
                continue

            # Otherwise, it is OPERATIONAL.
            sensor_summary.status = StatusEnum.OPERATIONAL

        # Construct the errors.
        errors: list[CollectorError] = []
        for error in collector_errors:
            if error["sensor_id"] is None:
                error_source = collector_metadata["collector_name"]
            else:
                sensor_metadata = next(
                    (
                        sensor
                        for sensor in latest_sensor_metadata
                        if sensor["sensor_id"] == record["sensor_id"]
                    ),
                    None,
                )
                if sensor_metadata is None:
                    raise RepostioryError(
                        "Sensor record detected with a sensor ID that isn't found in the sensor metadata."
                    )
                error_source = sensor_metadata["sensor_name"]

            errors.append(
                CollectorError(
                    source=error_source,
                    message=error["error_message"],
                    timestamp=error["timestamp"],
                )
            )

        return CollectorDetails(
            id=collector_metadata["collector_id"],
            name=collector_metadata["collector_name"],
            device_model=collector_metadata["device_model"],
            polling_interval=collector_metadata["polling_interval"],
            status=status,
            total_sensors=collector_stats[0]["total_sensors"],
            latest_record=collector_stats[0]["latest_record"],
            earliest_record=collector_stats[0]["earliest_record"],
            total_records=collector_stats[0]["total_records"],
            latest_error=collector_stats[0]["latest_error"],
            total_errors=collector_stats[0]["total_errors"],
            sensors=sensor_summaries,
            errors=errors,
        )

    async def get_sensor_details(
        self,
        sensor_id: str,
        records_page: int,
        records_page_size: int,
        errors_page: int,
        errors_page_size: int,
    ) -> SensorDetails:
        """
        Retrieves the sensor summary from the database

        Args:
            sensor_id (str): The ID of the sensor.
            records_page (int): The index of the pagination result. Starts at 0.
            records_page_size (int): The size of the page of results.
            errors_page (int): The index of the pagination result. Starts at 0.
            errors_page_size (int): The size of the page of results.

        Returns:
            SensorDetails: The details for a sensor.
        """
        # Retrieve the data from the database.
        latest_collector_metadata = await queries.latest_collector_metadata_query(
            self.connection
        )
        # Retrieve the data from the database.
        latest_sensor_metadata = await queries.latest_sensor_metadata_query(
            self.connection
        )
        sensor_stats = await queries.sensor_stats_query(self.connection, sensor_id)
        latest_record = await queries.latest_record_from_sensor_query(
            self.connection, sensor_id
        )
        latest_error = await queries.latest_error_from_sensor_query(
            self.connection, sensor_id
        )
        sensor_records = await queries.records_from_sensor_query(
            self.connection, sensor_id, records_page, records_page_size
        )
        sensor_errors = await queries.errors_from_sensor_query(
            self.connection, sensor_id, errors_page, errors_page_size
        )

        # Retrieve the sensor metadata of the sensor responsible for this record.
        sensor_metadata = next(
            (
                sensor
                for sensor in latest_sensor_metadata
                if sensor["sensor_id"] == sensor_id
            ),
            None,
        )
        if sensor_metadata is None:
            raise RepostioryError(
                "Sensor record detected with a sensor ID that isn't found in the sensor metadata."
            )

        # Retrieve the collector metadata of the collector responsible for this record.
        collector_metadata = next(
            (
                collector
                for collector in latest_collector_metadata
                if collector["collector_id"] == sensor_metadata["collector_id"]
            ),
            None,
        )
        if collector_metadata is None:
            raise RepostioryError(
                "Collector detected with a collector ID that isn't found in the collector metadata."
            )

        status = StatusEnum.UNKNOWN
        # If there are no latest records and no latest errors the status is UNKNOWN.
        if not latest_record and not latest_error:
            status = StatusEnum.UNKNOWN

        elif latest_record and latest_error:
            # If the latest record or error is long ago enough, determined
            # by active_device_polling_threshold, is is considered DROPPED.
            latest_timestamp = max(
                (
                    item["timestamp"]
                    for item in (latest_record[0], latest_error[0])
                    if item is not None
                )
            )
            active_threshold = timedelta(
                milliseconds=(
                    collector_metadata["polling_interval"]
                    * config.ACTIVE_DEVICE_POLLING_THRESHOLD
                )
            )
            if latest_timestamp < (datetime.now() - active_threshold):
                status = StatusEnum.DROPPED

        else:
            # If the error is more recent than the record, the status is ERROR.
            if (latest_error and not latest_record) or (
                latest_error
                and latest_record
                and latest_error[0]["timestamp"] > latest_record[0]["timestamp"]
            ):
                status = StatusEnum.ERROR

        # Otherwise, it is OPERATIONAL.
        status = StatusEnum.OPERATIONAL

        records: list[CollectorRecord] = [
            CollectorRecord(
                sensor_id=record["sensor_id"],
                record_id=record["record_id"],
                unit=get_unit_from_record_id(
                    sensor_code=sensor_metadata["sensor_code"],
                    record_id=record["record_id"],
                ),
                value=record["value"],
                timestamp=record["timestamp"],
            )
            for record in sensor_records
        ]
        errors: list[CollectorError] = [
            CollectorError(
                message=error["error_message"],
                timestamp=error["timestamp"],
                source=sensor_metadata["sensor_name"],
            )
            for error in sensor_errors
        ]

        return SensorDetails(
            id=sensor_metadata["sensor_id"],
            name=sensor_metadata["sensor_name"],
            status=status,
            code=sensor_metadata["sensor_code"],
            latest_record=sensor_stats[0]["latest_record"],
            earliest_record=sensor_stats[0]["earliest_record"],
            total_records=sensor_stats[0]["total_records"],
            latest_error=sensor_stats[0]["latest_error"],
            total_errors=sensor_stats[0]["total_errors"],
            records=records,
            errors=errors,
        )
