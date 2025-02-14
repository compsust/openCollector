# 2025/01/31 - Michael Chen: Update DHT22 to DHT20, add all sensors

from enum import Enum
from typing import TypedDict


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


sensor_metadata: dict[SensorCodeEnum, SensorMetadata] = {
    SensorCodeEnum.DHT20: {
        "name": "DHT20",
        "values": [
            {"name": "Temperature", "record_id": "temperature", "unit": "°C"},
            {"name": "Humiditiy", "record_id": "humiditiy", "unit": "%"},
        ],
    },
    SensorCodeEnum.TSL2561: {
        "name": "TSL2561",
        "values": [
            {"name": "Luminosity", "record_id": "luminosity", "unit": "Lux"},
        ],
    },
    SensorCodeEnum.PMS5003: {
        "name": "PMS5003",
        "values": [
            {
                "name": "Particulate_Matter_Concentration",
                "record_id": "particulate_matter_concentration",
                "unit": "PM2.5",
            },
        ],
    },
    SensorCodeEnum.MHZ19B: {
        "name": "MHZ19B",
        "values": [
            {
                "name": "CO2_Concentration",
                "record_id": "CO2_concentration",
                "unit": "PPM",
            },
        ],
    },
}
