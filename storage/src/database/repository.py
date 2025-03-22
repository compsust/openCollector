from datetime import datetime, timedelta
from asyncpg.connection import Connection
from storage.src.datastructures import (
    SensorSummary,
    CollectorSummary,
    NodeSummary,
    StatusEnum,
)
from . import queries


active_device_polling_threshold = 3


class Repository:
    connection: Connection

    def __init__(self, connection: Connection):
        self.connection = connection

    async def get_node_summary(self) -> NodeSummary:
        num_collectors_result = await self.connection.execute(
            queries.collector_count_query
        )
        num_sensors_result = await self.connection.execute(queries.sensor_count_query)
        recent_data_result = await self.connection.execute(queries.latest_data_query)

        # Extract counts
        total_collectors = num_collectors_result[0][0] if num_collectors_result else 0
        total_sensors = num_sensors_result[0][0] if num_sensors_result else 0

        # Process the recent data
        sensors_reporting = 0
        records_reported = 0
        errors_reported = 0

        # Group the recent data by collector
        collector_sensors = {}
        collector_errors = {}

        # Accumulate data
        for row in recent_data_result:
            sensor_id = row[0]
            collector_id = row[1]
            sensor_name = row[2]
            record_id = row[3]
            value = row[4]
            record_timestamp = row[5]
            error_message = row[6]
            error_timestamp = row[7]
            polling_interval = row[8]

            # Track collectors and their sensors
            if collector_id not in collector_sensors:
                collector_sensors[collector_id] = set()
                collector_errors[collector_id] = False

            collector_sensors[collector_id].add(sensor_id)

            # Track records and errors
            if record_timestamp is not None:
                records_reported += 1

            if error_message is not None:
                errors_reported += 1
                if error_timestamp and (
                    record_timestamp is None or error_timestamp > record_timestamp
                ):
                    collector_errors[collector_id] = True

        # Process sensors and determine their statuses
        sensor_statuses = {}
        current_time = datetime.now()

        for row in recent_data_result:
            sensor_id = row[0]
            collector_id = row[1]
            sensor_name = row[2]
            record_id = row[3]
            value = row[4]
            record_timestamp = row[5]
            error_message = row[6]
            error_timestamp = row[7]
            polling_interval = row[8]

            # Determine sensor status
            status = StatusEnum.UNKNOWN

            if error_timestamp and (
                record_timestamp is None or error_timestamp > record_timestamp
            ):
                status = StatusEnum.ERROR
            elif record_timestamp:
                # Check if the record is recent
                polling_threshold = timedelta(
                    milliseconds=polling_interval * active_device_polling_threshold
                )
                record_time = datetime.fromtimestamp(record_timestamp.timestamp())

                if current_time - record_time <= polling_threshold:
                    status = StatusEnum.OPERATIONAL
                    sensors_reporting += 1
                else:
                    status = StatusEnum.DROPPED

            # Store the sensor status (using a tuple of collector_id, sensor_id as the key)
            key = (collector_id, sensor_id)
            if key not in sensor_statuses or (
                status == StatusEnum.OPERATIONAL
                and sensor_statuses[key][0] != StatusEnum.ERROR
            ):
                sensor_statuses[key] = (status, sensor_name, value)

        # Build the collector summaries
        collectors = []
        collectors_reporting = 0

        for collector_id, sensor_ids in collector_sensors.items():
            collector_name = f"Collector {collector_id}"  # Default name if not found

            # Get all sensors for this collector
            collector_sensor_summaries = []
            collector_operational = False

            for sensor_id in sensor_ids:
                key = (collector_id, sensor_id)
                if key in sensor_statuses:
                    status, name, value = sensor_statuses[key]
                    sensor_summary = SensorSummary(
                        id=sensor_id, name=name, status=status, last_value=value
                    )
                    collector_sensor_summaries.append(sensor_summary)

                    if status in [StatusEnum.OPERATIONAL, StatusEnum.ERROR]:
                        collector_operational = True

            # Determine collector status based on its sensors
            if collector_errors[collector_id]:
                collector_status = StatusEnum.ERROR
                collectors_reporting += 1
            elif collector_operational:
                collector_status = StatusEnum.OPERATIONAL
                collectors_reporting += 1
            elif collector_sensor_summaries:
                collector_status = StatusEnum.DROPPED
            else:
                collector_status = StatusEnum.UNKNOWN

            collector_summary = CollectorSummary(
                id=collector_id,
                name=collector_name,
                status=collector_status,
                sensors=collector_sensor_summaries,
            )
            collectors.append(collector_summary)

        # Create and return the node summary
        return NodeSummary(
            total_collectors=total_collectors,
            collectors_reporting=collectors_reporting,
            total_sensors=total_sensors,
            sensors_reporting=sensors_reporting,
            records_reported=records_reported,
            errors_reported=errors_reported,
            collectors=collectors,
        )
