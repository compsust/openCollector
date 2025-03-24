# 2025/01/31 - Michael Chen: Update DHT22 to DHT20, add all sensors
# 2025/02/21 - MC: Update Tsl2561 to two channels
# 2025/03/07 - MC: Change TSL2561 back to single channel

from enum import Enum
from typing import TypedDict, Literal


class SensorCodeEnum(Enum):
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
    MHZ19B = "MH-Z19B"


class SensorValueMetadata(TypedDict):
    """
    Describes a type of information returned by a sensor.
    Used by the storage node for data display.

    Attributes:
        name (str): The name of the value, for example: "Temperature"
        record_id (str): The name of the value when it is present
            in the SensorData record returned by a sensor.
        unit (str): The unit system of the value, for example "°C"
    """

    name: str
    record_id: str
    unit: str


class SensorMetadata(TypedDict):
    """
    Describes a type of sensor.

    Attributes:
        name (str): The name of the sensor
        values (list[SensorValueMetadata]): A list of the
            quantities returned by the sensor.
    """

    name: str
    values: list[SensorValueMetadata]


"""
Stores metadata for each type of sensor code.

Attributes:
    name: The name of the sensor.
    values: A list containing the values that the sensor will output. For example,
        a temperature and humidity sensor will have two value entries.
    values[i].name: The name of the value.
    values[i].record_id: The key used to store the value in a dictionary.
    values[i].unit: The unit of measurement.

Note that when adding new sensors, the RecordID type below must be
updated for valid type inference.
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
                "name": "Particulate_Matter_Concentration_1.0",
                "record_id": "PM1.0",
                "unit": "PM1.0",
            },
            {
                "name": "Particulate_Matter_Concentration_2.5",
                "record_id": "PM2.5",
                "unit": "PM2.5",
            },
            {
                "name": "Particulate_Matter_Concentration_10",
                "record_id": "PM10",
                "unit": "PM10",
            },
        ],
    },
    SensorCodeEnum.MHZ19B: {
        "name": "MHZ19B",
        "values": [
            {
                "name": "CO2_Concentration",
                "record_id": "CO2",
                "unit": "PPM",
            },
        ],
    },
}

"""
Types the record_ids we expect to see for type safety.    
"""
RecordID = Literal[
    "CO2",
    "humidity",
    "lux0",
    "lux1",
    "PM1.0",
    "PM10",
    "PM2.5",
    "temperature",
]


def get_unit_from_record_id(sensor_code: SensorCodeEnum, record_id: RecordID) -> str:
    """
    Retrieves the unit string for a record_id.

    Args:
        sensor_code (SensorCodeEnum): The type of sensor.
        record_id (RecordID): The record ID of the value type.

    Returns:
        str: The unit describing the record_id.
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

    return value_metadata["unit"]
