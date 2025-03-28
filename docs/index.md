# OpenCollector - Open Source Data Collection

*TODO: Replace this with a screenshot of the finished dashboard.*
![Alt: a screenshot of the data monitoring dashboard](developer-guide/images/ui-sketches/dashboard.excalidraw.png)

OpenCollector is an open source Raspberry-Pi based data collection platform. Partnered with the [Simon Fraser University Computational Sustainability Lab](https://compsust.fas.sfu.ca/), this project is intended to create the foundation for a user-friendly IoT system that allows individuals and organizations to safely measure the impacts on their environment and monitor them for analysis and forecasting.

This prototype allows users to identify various parameters in their environment (such as temperature, light intensity, carbon dioxide) and tracks and displays the trends over time. This data is then securely stored in a cloud storage database to be able to access at a later date. While this prototype focuses on the use in a greenhouse, this project is intended for various uses.

The project encompasses the following parts:

1. Python code for collecting data from multiple sensors and uploading it to a database.
2. Python code for reading from a database and visually displaying data.
3. A PCB for wiring up a Raspberry Pi Pico W to a temperature, humidity, particulate matter, light, and CO2 sensor.
4. A 3D printable enclosure for securing the PCB.

## Documentation

See below for how to use this documentation:

- User Guide:
    - [Usage Instructions](./user-guide/usage.md): Instructions on how to use the system.
    - [Setup Instructions](./user-guide/setup.md): Instructions on how to set up the system.
- [Developer Guide](./developer-guide/overview.md): Technical details and design. 

## System Architecture

The OpenCollector system contains two main modules:      

1. **Collector Nodes** are the edge devices responsible for collecting data from sensors and uploading it to the database.
2. **Storage Nodes** are the cloud devices responsible for reading data from the database and displaying it in a cloud platform.

Additionally, the following pieces are required for the OpenCollector system to work:

- **[QuestDB](https://questdb.com/)** is used as the open-source timeseries database and is the glue between the collector and storage nodes.

Given a machine that is compatible with hosting a webserver and connecting to sensors, these modules may be run on the same device. If desired, they can be run on seperate devices, with the storage node and database on the same device or different devices, and the collector node run on an edge device connected to sensors.

![Alt: a diagram visualizes that the collector, database, and storage nodes may be run on seperate or the same device.](./images/devices.excalidraw.png)

Nodes may be connected together under the following rules:

1. Collector nodes have a single QuestDB database as a target.
2. An unlimited number of collector nodes may send data to a single QuestDB database.
3. An unlimited number of storage nodes may read data from a single QuestDB database.

This allows for any number of collector nodes to be used with a single database. While multiple storage nodes can be connected to a single database, since their only purpose is to display data, there may not be an advantage to this. Currently, a collector node can only send data to one database at a time.

![Alt: a diagram visualizes that any number of collectors and storages nodes can be connected to a single database](./images/nodes.excalidraw.png).

## Dependencies

This project makes use of the following dependencies:

- [Raspberry Pi](https://www.raspberrypi.com/) is used as the basis for computing, though the system should work with other hardware.
- [Python](https://www.python.org/) is used for all programming.
- [Micropython](https://micropython.org/) is used to write microcontroller compatible code for the collector node.
- [QuestDB](https://questdb.com/) is used as an open-source timeseries database.
- [Litestar](https://litestar.dev/) is used to create the REST API and browser user-interfaces.
- [HTMX](https://htmx.org/) for real-time HTML updates in the browser interface.
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) is used to create this documentation site.