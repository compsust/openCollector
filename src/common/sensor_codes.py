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

    DHT22 = "DHT22"
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
    SensorCodeEnum.DHT22: {
        "name": "DHT22",
        "values": [
            {"name": "Temperature", "record_id": "temperature", "unit": "°C"},
            {"name": "Humiditiy", "record_id": "humiditiy", "unit": "%"},
        ],
    }
}
