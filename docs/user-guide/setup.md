# Setup

This section of the documentation provides instructions for setting up and using the OpenCollector system to collect data.

## Identify Devices

The first step to deploying the OpenCollector stack is to determine which devices will be hosting which services. The following considerations apply.

- **Collector** nodes may be deployed on any device capable of reading from sensors and connecting to the internet. All collector code is compatible with *[micropython](https://micropython.org/)*, meaning the collector program may be run on a compatible microcontroller such as a Raspberry Pi Pico W. 
- **Storage** nodes may be deployed on any device that is capable of hosting a webserver. It may be run on the same device as the collector node, provided that the collector node is not running using *micropython*, as the storage node code is not compatible with *micropython*.
- **QuestDB** may be hosted on the same device as the **Storage** node, however the device must be capable of storing the desired volume of data at the desired intake bandwidth. If a large amount of data is to be stored, or many simultaneous collector streams are required, it may be best to host the database instance on a seperate device or on the cloud.

A list of which sensors are supported by the software is contained within the [Sensors](./collector/sensors.md) page. 

### Network Considerations

The database is required to be reachable over the network by both the collector and storage nodes. The collector nodes use *HTTP* to upload their data, and the storage node uses *HTTP* to display the user interface in the browser. The storage node uses the *PostgreSQL* protocol for reading data from the database, which by default uses *TCP/IP*.

## Deploy QuestDB and Storage Node

QuestDB and the storage node may be deployed together or seperately. The instructions included below support deploying them through *Docker* or through manual installation.

##### Things to mention

*TODO integrate this into the other sections*
The database tables are created upon the storage node fisrt starting and connecting to the database.

### Together

The following instructions are for self-hosting QuestDB together along with the storage node on the same device.

#### Docker

*TODO*

#### Manually

*TODO*

### Seperate

The following instructions are for hosting QuestDB seperately from the storage node.

#### QuestDB

Instructions for installing QuestDB are included in its [documentation](https://questdb.com/docs/quick-start/#install-questdb).

#### Docker

*TODO*

#### Manually

*TODO*

## Assemble Collectors

The wiring used to connect each collector node to its sensors, as well as how each collector node is situated in its environment, does not affect the operating of the system and thus may be achived however the user wishes. However, this project includes both a PCB that may be used to facilitate clean wiring of multiple sensors to a Raspberry Pi Pico W, as well as a 3D printable enclosure. See the [PCB and Enclosure](./collector/pcb.md) page for more information. 

## Configure Collectors

Each collector must be configured with the information required to connect to its sensors and upload its data. See the [Collector Config](./collector/config.md) for information on how to configure a collector.

## Deploy Collectors

*TODO*


