from questdb.ingress import Sender
from datetime import datetime
import time
import uuid
import random
from common import (
    SensorCodeEnum,
    sensor_metadata,
    records_table_name,
    errors_table_name,
    collector_metadata_table_name,
    sensor_metadata_table_name,
)
from ..datastructures import (
    MockCollector,
    MockCollectorMetadata,
    MockSensor,
    MockSensorMetadata,
    MockRecord,
    MockError,
)
from ..generators import get_mock_value

conf = f"http::addr=database:9000;username={'node'};password={'quest'};auto_flush_rows=100;auto_flush_interval=1000;"


rd = random.Random()
rd.seed(0)


def generate_collector() -> MockCollector:
    """
    Generates a mock collector object for generating data.
    """
    return MockCollector(
        collector_id=str(uuid.UUID(int=rd.getrandbits(128), version=4)),
        collector_name=f"MockCollector",
        device_model="Pi Pico",
        polling_interval=1000,
    )


def generate_sensors(
    collector: MockCollector,
) -> list[MockSensor]:
    """
    Generates a list of mock sensor objects for generating data.
    """
    return [
        MockSensor(
            collector_id=collector.collector_id,
            sensor_id=str(uuid.UUID(int=rd.getrandbits(128), version=4)),
            sensor_code=SensorCodeEnum.DHT20,
            sensor_name="DHT20",
        ),
        MockSensor(
            collector_id=collector.collector_id,
            sensor_id=str(uuid.UUID(int=rd.getrandbits(128), version=4)),
            sensor_code=SensorCodeEnum.TSL2561,
            sensor_name="TSL2561",
        ),
        MockSensor(
            collector_id=collector.collector_id,
            sensor_id=str(uuid.UUID(int=rd.getrandbits(128), version=4)),
            sensor_code=SensorCodeEnum.PMS5003,
            sensor_name="PMS5003",
        ),
        MockSensor(
            collector_id=collector.collector_id,
            sensor_id=str(uuid.UUID(int=rd.getrandbits(128), version=4)),
            sensor_code=SensorCodeEnum.MHZ19B,
            sensor_name="MHZ19B",
        ),
    ]


def generate_record(
    sensor: MockSensor,
) -> list[MockRecord]:
    """
    Generates records for a sensor.
    """
    records = []
    metadata = sensor_metadata.get(sensor.sensor_code, {})
    for value in metadata["values"]:
        records.append(
            MockRecord(
                timestamp=datetime.now(),
                collector_id=sensor.collector_id,
                sensor_id=sensor.sensor_id,
                record_id=value["record_id"],
                value=get_mock_value(value["record_id"]),
            )
        )
    return records


def generate_metadata(
    collector: MockCollector,
    sensors: list[MockSensor],
) -> tuple[MockCollectorMetadata, list[MockSensorMetadata]]:
    """
    Generates a metadata entry for a collector and its sensors.
    """
    collector_metadata = MockCollectorMetadata(
        timestamp=datetime.now(),
        collector_id=collector.collector_id,
        collector_name=collector.collector_name,
        device_model=collector.device_model,
        polling_interval=collector.polling_interval,
    )

    sensor_metadata = [
        MockSensorMetadata(
            timestamp=datetime.now(),
            collector_id=sensor.collector_id,
            sensor_id=sensor.sensor_id,
            sensor_code=sensor.sensor_code,
            sensor_name=sensor.sensor_name,
        )
        for sensor in sensors
    ]

    return collector_metadata, sensor_metadata


def main():
    collector = generate_collector()
    sensors = generate_sensors(collector)
    collector_metadata, sensor_metadata = generate_metadata(collector, sensors)

    with Sender.from_conf(conf) as sender:
        sender.row(
            collector_metadata_table_name,
            symbols={"collector_id": collector_metadata.collector_id},
            columns={
                "collector_name": collector_metadata.collector_name,
                "device_model": collector_metadata.device_model,
                "polling_interval": collector_metadata.polling_interval,
            },
            at=collector_metadata.timestamp,
        )

        for metadata in sensor_metadata:
            sender.row(
                sensor_metadata_table_name,
                symbols={
                    "collector_id": metadata.collector_id,
                    "sensor_id": metadata.sensor_id,
                },
                columns={
                    "sensor_code": str(metadata.sensor_code),
                    "sensor_name": metadata.sensor_name,
                },
                at=metadata.timestamp,
            )

        sender.flush()

        while True:
            records = []
            for sensor in sensors:
                records.extend(generate_record(sensor))

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

            sender.flush()

            time.sleep(collector.polling_interval / 1000)


if __name__ == "__main__":
    main()
