# 2025/01/31 - Michael Chen: Update DHT22 to DHT20, add all sensors
# 2025/02/21 - MC: Update Tsl2561 to two channels
# 2025/03/07 - MC: Change TSL2561 back to single channel

from enum import StrEnum
from typing import TypedDict, Literal


class SensorCodeEnum(StrEnum):
    """
    Contains an enumerated value
    for all supported sensor types.

    Each value will be mapped to a
    specific implementation of
    AbstractSensorDriver.
    """

    DHT20 = "DHT20"
    TSL2561 = "TSL2561"
    PMS5003 = "PMS5003"
    MHZ19B = "MHZ19B"


class SensorValueMetadata(TypedDict):
    """
    Describes a type of information returned by a sensor.
    Used by the storage node for data display.

    Attributes:
        name: The name of the value, for example: "Temperature"
        record_id: The name of the value when it is present
            in the SensorData record returned by a sensor.
        unit: The unit system of the value, for example "°C"
    """

    name: str
    record_id: str
    unit: str


class SensorMetadata(TypedDict):
    """
    Describes a type of sensor.

    Attributes:
        name: The name of the sensor
        values: A list of the
            quantities returned by the sensor.
    """

    name: str
    values: list[SensorValueMetadata]


"""
Stores metadata for each type of sensor code.
"""
sensor_metadata: dict[SensorCodeEnum, SensorMetadata] = {
    SensorCodeEnum.DHT20: {
        "name": "DHT20",
        "values": [
            {"name": "Temperature", "record_id": "temperature", "unit": "°C"},
            {"name": "Humiditiy", "record_id": "humidity", "unit": "%"},
        ],
    },
    SensorCodeEnum.TSL2561: {
        "name": "TSL2561",
        "values": [{"name": "Luminosity", "record_id": "lux0", "unit": "Lux"}],
    },
    SensorCodeEnum.PMS5003: {
        "name": "PMS5003",
        "values": [
            {
                "name": "Particulate Matter Concentration 1.0",
                "record_id": "PM1.0",
                "unit": "PM1.0",
            },
            {
                "name": "Particulate Matter Concentration 2.5",
                "record_id": "PM2.5",
                "unit": "PM2.5",
            },
            {
                "name": "Particulate Matter Concentration 10",
                "record_id": "PM10",
                "unit": "PM10",
            },
        ],
    },
    SensorCodeEnum.MHZ19B: {
        "name": "MHZ19B",
        "values": [
            {
                "name": "CO2 Concentration",
                "record_id": "CO2",
                "unit": "PPM",
            },
        ],
    },
}


def get_unit_from_record_id(
    sensor_code: SensorCodeEnum, record_id: str
) -> tuple[str, str]:
    """
    Retrieves the unit strings for a record_id.

    Args:
        sensor_code: The type of sensor.
        record_id: The record ID of the value type.

    Returns:
        A tuple where the first value is the name of the value type
            and the second value is the name of the unit.
    """
    value_metadata = next(
        (
            value
            for value in sensor_metadata[sensor_code]["values"]
            if value["record_id"] == record_id
        ),
        None,
    )
    if value_metadata is None:
        raise ValueError(
            f"Combination of sensor code {sensor_code} and record_id {record_id} does not exist in the sensor metadata."
        )

    return value_metadata["name"], value_metadata["unit"]


def get_record_ids(sensor_code: SensorCodeEnum) -> list[str]:
    """
    Retrieves a list of the record IDs that are valid for a sensor type.

    Args:
        sensor_code: The sensor code to search.

    Returns:
        list[str]: The record IDs that are valid for this sensor code.
    """
    return [value["record_id"] for value in sensor_metadata[sensor_code]["values"]]
