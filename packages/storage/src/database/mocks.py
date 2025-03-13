from datetime import datetime, timedelta
import uuid
from packages.common.src.sensor_codes import SensorCodeEnum
from questdb.ingress import Sender
import config
import random
from common.src import sensor_metadata

num_nodes = 3
sensors_per_node=3
records_per_sensor = 100
errors_per_sensor = 5

conf = f"http::addr=localhost:9000;username={config.QUESTDB_USER};password={config.QUESTDB_PASSWORD};"

def generate_collectors(num_collectors=num_nodes):
    return [
        {
            "collector_id": str(uuid.uuid4()),
            "collector_name": f"Collector_{i}",
            "device_model": f"Model_{random.choice(['Raspi4', 'Pi Pico'])}",
            "polling_interval": random.randint(500, 3000),
        }
        for i in range(num_collectors)
    ]

def generate_sensors(collectors, sensors_per_node=sensors_per_node):
    sensors = []
    for collector_idx in range(len(collectors)):
        collector = collectors[collector_idx]
        for i in range(sensors_per_node):
            sensors.append({
                "collector_id": collector["collector_id"],
                "sensor_id": str(uuid.uuid4()),
                "sensor_code": random.choice(list(SensorCodeEnum)),
                "sensor_name": f"Sensor_{collector_idx}.{i}",
            })
    return sensors

def generate_records(collectors, sensors, records_per_sensor=records_per_sensor):
    records = []
    for sensor_idx in sensors:
        sensor = sensors[sensor_idx]
        for i in range(records_per_sensor):
            # Timestamps between a month of time.
            timestamp = datetime(year=2025, month=1, day=1) + timedelta(seconds=random.randint(0, 3110400))
            record_id = random.choice(sensor_metadata[sensor["sensor_code"]])
            records.append(
                {
                    timestamp: timestamp,
                    collector_id: sensor["collector_id"]
                    sensor_id: sensor["sensor_id"]
                    record_id: 
                }
            )
    return [
        {
            "timestamp": datetime.utcnow().isoformat(),
            "collector_id": sensor["collector_id"],
            "sensor_id": sensor["sensor_id"],
            "record_id": str(uuid.uuid4()),
            "value": round(random.uniform(10.0, 100.0), 2),
        }
        for _ in range(num_records)
        for sensor in random.sample(sensors, min(5, len(sensors)))  # Limit records per sensor
    ]

def generate_mock_data():
    collector_ids = [str(uuid.uuid4()) for _ in range(num_nodes)]
    sensor_ids = [str(uuid.uuid4()) for _ in range(num_nodes * sensors_per_node)]



    with Sender.from_conf(conf) as sender:
        pass

if __name__ == "__main__":
    generate_mock_data()
