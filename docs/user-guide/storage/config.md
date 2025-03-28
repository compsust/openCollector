# Storage Config

Storage nodes are configured through an environment variable located in the `storage` folder in the root of the repository.

## Properties

The following are the properties set in `.env`

### QuestDB Connection

The following configuration values relate to connecting the storage node to the QuestDB instance.

| Value | Type | Default | Description |
| -------- | ------- | -------- | ------- |
| `QUESTDB_HOST` | `string` | `localhost` | The hostname the QuestDB instance may be accessed at. This should include the `http://` or `https://` prefix. |
| `QUESTDB_PORT` | `integer` | `8812` | The port the QuestDB database's PostgreSQL may be accessed at. Note that this is the Postgres Wire Protocol port and is different from QuestDB's REST API port. |
| `QUESTDB_USER` | `string` | `pguser` | The username used to access the database. |
| `QUESTDB_PASSWORD` | `string` | `quest` | The password used to access the database. |
| `QUESTDB_DB_NAME` | `string` | `qdb` | The name of the QuestDB database to access using Postgres. |


### QuestDB Schema

The following configuration values relate to how QuestDB's schema is structured.

| Value | Type | Default | Description |
| -------- | ------- | -------- | ------- |
| `COLLECTOR_CAPACITY` | `integer` | `1024` | The total number of unique collector nodes to support on this database. For storing collector IDs, QuestDB's `SYMBOL` type is used, which maps string values to a range of integers, increasing storage efficiency. This parameter sets the maximum number of symbols which are supported in the column which stores collector IDs, and cannot be changed. See [here](https://questdb.com/docs/reference/sql/create-table/#symbols). |
| `SENSOR_CAPACITY` | `integer` | `16` | The total number of unique sensors per collector node to support on this database. For storing collector IDs, QuestDB's `SYMBOL` type is used, which maps string values to a range of integers, increasing storage efficiency. This parameter, multiplied by `COLLECTOR_CAPACITY`, sets the maximum number of symbols which are supported in the column which stores collector IDs, and cannot be changed. See [here](https://questdb.com/docs/reference/sql/create-table/#symbols). |

### Data Display

| Value | Type | Default | Description |
| -------- | ------- | -------- | ------- |
| `ACTIVE_DEVICE_POLLING_THRESHOLD` | `number` | `3` | For each collector, defines an interval equal to the `polling_interval` configuration value of the node times `ACTIVE_DEVICE_POLLING_THRESHOLD` past which, if there are no recent records or errors in the database, the collector node or sensor will be considered 'dropped', ie. not currently sending data. For example, given an `ACTIVE_DEVICE_POLLING_THRESHOLD` of 4, if a collector node has a `polling_interval` of 3000ms, and a sensor on that node has not uploaded any sensor data or errors for the past 3000ms * 4 = 12 seconds, that sensor will be considered 'dropped'. See the [Usage](../usage.md) page for more information on status. |

## Example Config

Below is an example of the configuration files with all values included. It is also included in the `storage` directory of the repository under the filename `.env.example`, which is the expected location, so it may be copied, renamed `.env`, and modified to suit the needs of a deployment. 

```ini
{% include "../../../storage/.env.example" %}
```