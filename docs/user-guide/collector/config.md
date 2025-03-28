# Collector Config

Collector nodes are configured through a JSON file located in the collector project repository. After cloning the repostitory, the config file can be found at the `config.json` file in `collector/src` directory of the repository. Note that `json` is used instead of `yaml` due to increased compatibility with *micropython*.

Within the `config.json` file are several sections:

- A root-level section for properties relating to the collector node itself.
- A device section for properties relating to the device the collector is being run on.
- An upload section for properties relating to how the collector will establish a connection to the database.
-  A sensor section which contains a list of objects each representing a sensor that is connected to the node.

On startup, the config file is parsed by the collector and used for initialization. If any errors are detected in the configuration, such as missing values or 

## A Note on IDs

In order for collectors and sensors to be indentified as unique nodes by the interface, they need to have unique IDs. Since communication between the collector and storage nodes is one-way, collector nodes have no way of verifying that their IDs are unique or of being assigned unique IDs. To get around this, UUIDs are used as collector and sensor IDs to prevent collision between different sensors.

Due to the lack of support for Python's `uuid` module in micropython, UUIDs must be generated and placed into the configuration files manually. An [online generator](https://www.uuidgenerator.net/version4) may be used to do this. In the future, a Python script which scans the `config.json` file and adds UUIDs automatically before deployment may be created to automate this task.

## Properties

The following are the properties set in `config.json`

### Root Properties

The following are the properties set at the root of the `JSON` object.

| Key | Type | Example | Required | Description |
| -------- | ------- | -------- | -------- | ------- |
| `collector_id` | `string` | See [here](https://www.uuidgenerator.net/version4) for generating UUIDs | True | The ID used to identify the collector node within the database. Must be unique amongst all collector and sensor IDs in the database. |
| `node_name` | `string` | `"Greenhouse Collector 1"` | True | A human-readable descriptive name for the collector node. It doesn't have to be unique, but it should be to prevent confusion with other nodes. |
| `polling_interval` | `integer` | `1000` | True | The number of miliseconds between attempts by the collector node to read and upload data from its sensors. |
| `ssid_name` | `string` | `"network_name"` | False | The name of the SSID the node should connect to. If defined, the node will attempt to open a LAN connection to this SSID using the `network` module. If the runtime environment isn't micropython, meaning the network configuration is likely defined elsewhere, this should not be included. |
| `ssid_password` | `string` | `"network_password"` | False | The password of the SSID the node should connect to. If `ssid_name` is defined but this property isn't, an error will be thrown. |

### Device Properties

The following are the properties set on the `device` object in the `config.json` file.

| Key | Type | Example | Required | Description |
| -------- | ------- | -------- | -------- | ------- |
| `model` | `string` | `"Raspberry Pi Pico W"` | True | A human-readable identifying name for the type of device the collector node is being run on. |
| `allowed_gpio` | `integer[]` | `[2, 4, 25]` | True | A list of usable values of GPIO pins for this device. This list is used to validate configured sensors. For example, if a sensor specifies that it requires the use of GPIO pin `3`, but `3` is not a value that is contained within this list, an error will be thrown. |
| `requires_micropython` | `boolean` | `false` | True | If true, the collector will validate that it is being run within a micropython runtime environment, and will throw an error if not. |

### Upload Properties

The following are the properties set on the `upload` object in the `config.json` file. See the [QuestDB REST](https://questdb.com/docs/reference/api/rest/) documentation for more information on the HTTP interface used by the collector node. 

| Key | Type | Example | Required | Description |
| -------- | ------- | -------- | -------- | ------- |
| `host` | `string` | `"localhost"` | True | The URI at which the QuestDB instance in use is exposing itself. Note that this should not include `http://` as that is added by the collector node as it parses its configuration. |
| `port` | `integer` | `9000` | True | The port at which the HTTP interface is exposed. Note that this is a different port than QuestDB uses for other interfaces. By default it is `9000`. |
| `user` | `string` | `"node_user"` | True | The username configured in QuestDB for [HTTP Basic authentication](https://questdb.com/docs/reference/api/rest/#authentication-in-questdb-open-source). |
| `password` | `string` | `"node_password"` | True | The password configured in QuestDB for [HTTP Basic authentication](https://questdb.com/docs/reference/api/rest/#authentication-in-questdb-open-source). |

### Sensor Properties

The sensor properties is an array of `JSON` objects set on the `sensors` key in the `config.json` file. For each object in this array, the collector node will initialize an object representing a sensor of the configured type, and will attempt to pull data from it. Thus, to add a sensor that is supported by the software, a new object must be added to this array.

A list of supported sensors is contained within the [Sensors](./sensors.md) page.

To accomodate configuration that is unique to a sensor and can't be generalized to a common configuration object, the `attributes` key in the sensor configuration is a flexible type which can accept different values depending on the type of sensor. The individual sensor pages within the [Sensors](./sensors.md) page outline the structures of these objects.

| Key | Type | Example | Required | Description |
| -------- | ------- | -------- | -------- | ------- |
| `sensor_id` | `string` | See [here](https://www.uuidgenerator.net/version4) for generating UUIDs | True | The ID used to identify the collector node within the database. Must be unique amongst all collector and sensor IDs in the database, not unique amongst the sensors of this node. |
| `sensor_code` | `"enumerated string"` | `"DHT20"` | True | A string used to identify the type of sensor configured by this sensor config. It is important that the sensor code matches that of one of the supported sensors. Refer to the [Sensors](./sensors.md) page for a list of supported sensors and their associated values of `sensor_code`. |
| `name` | `string` | `"Greenhouse Temperature 1"` | True | A human-readable descriptive name for the sensor. It doesn't have to be unique, but it should be to prevent confusion with other sensors. |
| `gpio` | `object with string keys and integer values` | `{"uart_tx": 21, "uart_rx": 22}` | True | An object where the keys are names of pin functions used by the sensor and the values are GPIO numbers to assign that function to. This is used to match the collector node's config with how the sensor is physically wired up. It is important that the keys in this object match the keys expected by the sensor's configuration as detailed in the [Sensors](./sensors.md) page. It is also important that the values of the GPIO pins be included in the list of allowed pins, `allowed_gpio` as contained within the `device` section of the config. Finally, the values of the GPIO pins must be correct given which functions are supported on which pins as dictated by the model of device the collector is running on. |
| `attributes` | `object with string keys and values of any type` | `{"baudrate": 9600}` | False | An object where the keys are names of configuration parameters and the values are the values of those parameters. This is a custom section of the configuration which will be different for every sensor. See the [Sensors](./sensors.md) page for configuring this section for each sensor. |

## Example Config

Below is an example of the configuration files with all values included. It is also included in the `collector/src` directory of the repository under the filename `config.example.json`, which is the expected location, so it may be copied, renamed `config.json`, and modified to suit the needs of a deployment. 

*Note: [you should generate your own UUIDs!](https://www.uuidgenerator.net/version4)*

```json
{% include "../../../collector/src/config.example.json" %}
```