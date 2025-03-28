# Usage

This page contains all instructions for how to use the system.

## Data Display

This section contains information on how to use the user interface.

### Data Types

There are two categories of data returned from a node:

1. Sensor data is numerical data that has been measured by a sensor. A sensor may output multiple different values at a time.
2. Errors are messages that are caught from exceptions in the sensor code. A node may also upload errors that aren't associated with any sensor.

### Node Status

When data for a collector node or sensor is displayed throughout the interface, it may be associated with a 'status' value. The status is intended to give a brief report on the node or sensor's activity. The status may be one of four values, explained below:

1. White - `UNKNOWN`: If the status is unknown, it means the sensor has not uploaded any data or errors to the database.
2. Yellow - `DROPPED`: If the status is dropped, it means the sensor has not uploaded any data or errors within the last X amount of time, where X is determined by the collector node's value of `polling_interval` and the storage node's value of `ACTIVE_DEVICE_POLLING_THRESHOLD`. For more information, see the [Storage Config](./storage/config.md#data-display) page.
3. Red - `ERROR`: If the status is in error, it means the sensor has uploaded an error more recently than it has numerical data.
4. Green - `OPERATIONAL`: If the status is operational, it means the sensor has successully uploaded numerical data more recently than it has an error. 

A collector node's status is determined by its sensors - a collector is only `OPERATIONAL` if all sensors are operational and it has no errors itself. Any `UNKNOWN` sensor will cause the collector to be `UNKNOWN`, and any `ERROR` sensor will cause the collector to be `ERROR`, in that order. If the collector has any errors that aren't associated with a sensor, its status is `ERROR`.

### Web Interface

This section contains information on how to use the browser interface.

#### Authentication

*TODO*

#### Dashboard

*TODO*

#### Collector Page

*TODO*

#### Sensor Page

*TODO*

### Rest API

This section contains information on how to use the REST HTTP interface.

#### Authentication

*TODO*

#### Interface

*TODO*