# Sensors

For documentation on which sensors are currently supported and how to configure them, see the [User Guide](../../user-guide/collector/sensors.md) sensors page.

See the [Sensor Reference](./reference/sensor.md) for documentation on the sensor-related source code.

## Datastructure

Each sensor returns data of the type `SensorData`, which can be found in the file `common/src/common/datastructure.py`. This is a dictionary with values of numerical type and keys of type `RecordID` which is a union of all values of `record_id` found in the sensor metadata. See [Update the Sensor Metadata](#update-the-sensor-metadata) for more information.

## Adding Sensor Support

The following is a list of instructions for adding support for a new sensor. Before starting, first verify the following:

1. The existing sensor interface contained withing the [Sensor Reference](./reference/sensor.md) and the capacities for sensor configuration outlined in the [Config](../../user-guide/collector/config.md) will be able to support the sensor. If the sensor requires any dynamic runtime configuration that can't happen within a single Python module, it may not be able to work.
2. The code for reading from the sensor that you plan to use is compatible with Micropython.

### Update the Sensor Metadata

The first step is to add the sensors to the list of recognized sensors. In the common module, the file `common/src/common/sensors.py` stores this metadata, and it is split into three parts:

1. The `SensorCodeEnum` is an enumerated string where each supported sensor gets its own code. It is used to identify the type of sensor when data is uploaded to the database.
2. The `sensor_metadata` dictionary maps values of `SensorCodeEnum` to a typed dictionary of the type `SensorMetadata`. The `SensorMetadata` dictionary has the following attributes:
    - `name`: A human-readable string name for the sensor, used in the display of the sensor type in the interface. Usually, this will be identical to the value of `SensorCodeEnum`, but in case the sensor code is not what is desired to have displayed as the name of the sensor type, the `name` attribute allows changing that.
    - `values`: A list of `SensorValueMetadata` typed dictionaries, which specify the structure of numerical data returned by the sensor and have the following attributes:
        - `name`: A human readable name of the sensor value. Used for display of the sensor data in the interface. For example, "Temperature" or "CO2 Concentration".
        - `record_id`: The string key under which this sensor value will be stored in the `SensorData` dictionary returned by this sensor. For example, if a sensor has two `SensorValueMetadata`, one with a `record_id` of `"temperature"` and the other with a `record_id` of `"humidity"` we can expect the `SensorData` dictionary returned by the sensor to have the structure `{"temperature": 20, "humidity": 80}`. It is important that `record_id`s be **unique amongst the other `SensorValueMetadata` for a particular sensor type** as a dictionary can only have one value per key.
        - `unit`: A string representing the unit system that the measured value is in. Used in the interface to display the data with the proper unit.
3. The `RecordID` type is a union of strings which contains all values of `record_id` found in the `sensor_metadata` dictionary. It is used for type hinting that a value is one of the keys expected within `SensorData`. Currently, this is defined as a union of literal strings with the `Literal` type, but in the future it would be best if this were derived directly from the `sensor_metadata` dictionary.

With this in mind, adding a new sensor to this metadata requires the following:

1. Add a new, unique code to `SensorCodeEnum`.
2. Add a new entry to the `sensor_metadata` dictionary, ensuring that the full structure of `SensorData` the sensor will return is accounted for with correct values of `SensorValueMetadata`.
3. If any `record_id`s were added to the metadata that weren't in there before, add them to the `RecordID` type.

### Implement the `SensorDriver`

The concrete implementations of the `AbstractSensorDriver` interface.

### Update the Documentation.


Explain all the steps for supporting a new sensor:
1. Add a new value to SensorCodeEnum
2. Add a new entry to sensor_metadata
3. Create a new SensorDriver in the src/collector/sensors/drivers folder
4. Add this SensorDriver to the sensor_drivers dict in sensor_codes.py
5. Add the sensor config to config.json
