from tap import Tap
from dataclasses import dataclass
from datetime import datetime, timedelta
import uuid
from common.src.sensor_codes import SensorCodeEnum
from questdb.ingress import Sender
import config
import random
from common.src import (
    sensor_metadata,
    records_table_name,
    errors_table_name,
    collector_metadata_table_name,
    sensor_metadata_table_name,
)

# The first available time for data to be generated at.
default_base_timestamp = datetime(year=2025, month=1, day=1)
conf = f"http::addr=localhost:9000;username={config.QUESTDB_USER};password={config.QUESTDB_PASSWORD};"


class CliArguments(Tap):
    nodes = 3  # The number of collector nodes to generate.
    sensors = random.randint(2, 5)  # The number of sensors per node to generate.
    records = random.randint(80, 120)  # The number of records per sensor to generate.
    sensor_errors = random.randint(2, 5)  # The number of errors per sensor to generate.
    collector_errors = random.randint(
        1, 3
    )  # The number of errors per collector (ie, errors not caused by a sensor) to generate.
    sign_ons = random.randint(
        2, 5
    )  # The number of times each node will be powered on and upload its configuration to the metadata tables.
    span_seconds = (
        60 * 60 * 24 * 30
    )  # The default number of seconds over which to generate data.


@dataclass
class MockCollector:
    """
    Represents a collector's attributes.
    """

    collector_id: str
    collector_name: str
    device_model: str
    polling_interval: int


@dataclass
class MockSensor:
    """
    Represents a sensor's attributes.
    """

    collector_id: str
    sensor_id: str
    sensor_code: SensorCodeEnum
    sensor_name: str


@dataclass
class MockCollectorMetadata:
    """
    Represents a collector's attributes as inserted into the DB table.
    """

    timestamp: datetime
    collector_id: str
    collector_name: str
    device_model: str
    polling_interval: int


@dataclass
class MockSensorMetadata:
    """
    Represents a sensor's attributes as inserted into the DB table.
    """

    timestamp: datetime
    collector_id: str
    sensor_id: str
    sensor_code: SensorCodeEnum
    sensor_name: str


@dataclass
class MockRecord:
    """
    Represents a record's attributes as inserted into the DB table.
    """

    timestamp: datetime
    collector_id: str
    sensor_id: str
    record_id: str
    value: float


@dataclass
class MockError:
    """
    Represents an error's attributes as inserted into the DB table.
    """

    timestamp: datetime
    collector_id: str
    sensor_id: str | None
    error_message: str


def generate_timestamp(generation_span_seconds: int) -> datetime:
    """
    Generates a timestamp in the configured range.
    """
    return default_base_timestamp + timedelta(
        seconds=random.randint(0, generation_span_seconds)
    )


def generate_collectors(num_nodes: int) -> list[MockCollector]:
    """
    Generates a list of mock collector objects for generating data.
    """
    return [
        MockCollector(
            collector_id=str(uuid.uuid4()),
            collector_name=f"Collector_{i}",
            device_model=f"Model_{random.choice(['Raspi4', 'Pi Pico'])}",
            polling_interval=random.randint(500, 3000),
        )
        for i in range(num_nodes)
    ]


def generate_sensors(
    collectors: list[MockCollector], sensors_per_node: int
) -> list[MockSensor]:
    """
    Generates a list of mock sensor objects for generating data.
    """
    sensors = []
    for index, collector in enumerate(collectors):
        sensors.append(
            [
                MockSensor(
                    collector_id=collector.collector_id,
                    sensor_id=str(uuid.uuid4()),
                    sensor_code=random.choice(list(SensorCodeEnum)),
                    sensor_name=f"Sensor_{index}.{i}",
                )
                for i in range(sensors_per_node)
            ]
        )
    return sensors


def generate_records(
    sensors: list[MockSensor], records_per_sensor: int, generation_span_seconds: int
):
    """
    Generates a list of records.
    """
    records = []
    for sensor in sensors:
        for _ in range(records_per_sensor):
            # Timestamps between the beginning of 2025 and the set timespan.
            timestamp = datetime(year=2025, month=1, day=1) + timedelta(
                seconds=random.randint(0, generation_span_seconds)
            )

            # Get a random record ID for this sensor type.
            metadata = sensor_metadata.get(sensor.sensor_code, {})
            values = metadata.get("values", [])
            record_ids = [value["record_id"] for value in values]
            record_id = random.choice(record_ids)

            records.append(
                MockRecord(
                    timestamp=timestamp,
                    collector_id=sensor.collector_id,
                    sensor_id=sensor.sensor_id,
                    record_id=record_id,
                    value=random.uniform(-10000, 10000),
                )
            )
    return records


def generate_collector_errors(
    collectors: list[MockCollector],
    errors_per_collector: int,
    generation_span_seconds: int,
) -> list[MockError]:
    """
    Generates a list of records that do not have to do with a sensor.
    """
    errors = []
    for collector in collectors:
        errors.append(
            [
                MockError(
                    timestamp=generate_timestamp(generation_span_seconds),
                    collector_id=collector.collector_id,
                    sensor_id=None,
                    error_message=random.choice(
                        [
                            "Something terrible has gone wrong on this node.",
                            "A great error has brougt forth havoc to this node.",
                            "This node experienced a technical difficulty.",
                        ]
                    ),
                )
                for _ in range(errors_per_collector)
            ]
        )
    return errors


def generate_sensor_errors(
    sensors: list[MockSensor], errors_per_sensor: int, generation_span_seconds: int
) -> list[MockError]:
    """
    Generates a list of records that are sourced from a sensor.
    """
    errors = []
    for sensor in sensors:
        errors.append(
            [
                MockError(
                    timestamp=generate_timestamp(generation_span_seconds),
                    collector_id=sensor.collector_id,
                    sensor_id=sensor.sensor_id,
                    error_message=random.choice(
                        [
                            "The bits for a sensor reading have been misplaced.",
                            "A dog has chewed on the wire for this sensor.",
                            "This sensor took a nap.",
                        ]
                    ),
                )
                for _ in range(errors_per_sensor)
            ]
        )
    return errors


def generate_metadata(
    collectors: list[MockCollector],
    sensors: list[MockSensor],
    collector_sign_ons: int,
    generation_span_seconds: int,
) -> tuple[list[MockCollectorMetadata], list[MockSensorMetadata]]:
    """
    Generates all the entries that would be inserted into the metadata tables
    by the nodes when they start up.
    """
    collector_metadata = []
    sensor_metadata = []

    collector_ids = [collector.collector_id for collector in collectors]
    for collector in collectors:
        sensors_in_node = [
            sensor for sensor in sensors if sensor.collector_id in collector_ids
        ]

        for sign_on in range(collector_sign_ons):
            timestamp = generate_timestamp(generation_span_seconds)
            collector_metadata.append(
                MockCollectorMetadata(
                    timestamp=timestamp,
                    collector_id=collector.collector_id,
                    collector_name=collector.collector_name,
                    device_model=collector.device_model,
                    polling_interval=collector.polling_interval,
                )
            )
            sensor_metadata.append(
                [
                    MockSensorMetadata(
                        timestamp=timestamp,
                        collector_id=sensor.collector_id,
                        sensor_id=sensor.sensor_id,
                        sensor_code=sensor.sensor_code,
                        sensor_name=sensor.sensor_name,
                    )
                    for sensor in sensors_in_node
                ]
            )

    return collector_metadata, sensor_metadata


def main():
    args = CliArguments().parse_args()

    collectors = generate_collectors(args.nodes)
    sensors = generate_sensors(collectors, args.sensors)
    records = generate_records(sensors, args.records, args.span_seconds)
    collector_errors = generate_collector_errors(
        collectors, args.collector_errors, args.span_seconds
    )
    sensor_errors = generate_sensor_errors(
        sensors, args.sensor_errors, args.span_seconds
    )
    errors = collector_errors + sensor_errors
    collector_metadata, sensor_metadata = generate_metadata(
        collectors, sensors, args.sign_ons, args.span_seconds
    )

    with Sender.from_conf(conf) as sender:
        for record in records:
            sender.row(
                records_table_name,
                symbols={
                    "collector_id": record.collector_id,
                    "sensor_id": record.sensor_id,
                    "record_id": record.record_id,
                },
                columns={"value": record.value},
                at=record.timestamp,
            )

        for error in errors:
            sender.row(
                errors_table_name,
                symbols={
                    "collector_id": error.collector_id,
                    "sensor_id": error.sensor_id,
                },
                columns={"error_message": error.error_message},
                at=error.timestamp,
            )

        for metadata in collector_metadata:
            sender.row(
                collector_metadata_table_name,
                symbols={"collector_id": metadata.collector_id},
                columns={
                    "collector_name": metadata.collector_name,
                    "device_model": metadata.device_model,
                    "polling_interval": metadata.device_model,
                },
                at=metadata.timestamp,
            )

        for metadata in sensor_metadata:
            sender.row(
                sensor_metadata_table_name,
                symbols={
                    "collector_id": metadata.collector_id,
                    "sensor_id": metadata.sensor_id,
                },
                columns={
                    "sensor_code": metadata.sensor_code,
                    "sensor_name": metadata.sensor_name,
                },
                at=metadata.timestamp,
            )

        sender.flush()


if __name__ == "__main__":
    main()
