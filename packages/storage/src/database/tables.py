import config
from common.src import (
    records_table_name,
    errors_table_name,
    collector_metadata_table_name,
    sensor_metadata_table_name,
)

"""
This file contains the SQL commands to create the database
tables which store all the records and errors from the sensors.

See the QuestDB docs on this for more info: https://questdb.com/docs/reference/sql/create-table/

Some information on what the parts of the commands do:
- CREATE TABLE IF NOT EXISTS {table_name} just makes the
    database aware of the table and its structure
- timestamp TIMESTAMP creates a column on the table that
    stores the timestamp, and TIMESTAMP(timestamp) designates
    that column as the one which stores the timestamp,
    so that QuestDB can know which one to populate when generating timestamps.
- {column_name} SYMBOL CAPACITY {column_capacity} creates a column
    with the SYMBOL type. The SYMBOL type maps strings to integers,
    making the storage much more efficient. So for example, for collector IDs,
    which are long strings, it is more efficient to map each ID that inserts
    into the database to an integer value, which is only a few bytes,
    than it is to store the entire string, which is one byte per character.
    This works because we have less unique collector IDs than possible integer
    values in the supported range. The CAPACITY part sets the ceiling for the
    maximum number of possible integer values and thus unique symbols. For
    collector and sensor IDs, this is configurable, but for sensor types it
    is assumed that we won't support more than 256 unique sensors.
"""

"""
The SQL command to create the records table.

Each record contains everything needed for context to be
identified, with information about the sensor being contained
in the sensor_metadata table.
"""
records_table_init_command = (
    f"CREATE TABLE IF NOT EXISTS {records_table_name}("
    "timestamp TIMESTAMP, "
    f"collector_id SYMBOL CAPACITY {config.COLLECTOR_CAPACITY}, "
    f"sensor_id SYMBOL CAPACITY {config.TOTAL_SENSOR_CAPACITY}, "
    "record_id SYMBOL CAPACITY 256, "
    "value DOUBLE"
    ") TIMESTAMP(timestamp)"
)

"""
The SQL command to create the error table.

Each error contains everything needed for context to be
identified, with information about the sensor being contained
in the sensor_metadata table.
"""
errors_table_init_command = (
    f"CREATE TABLE IF NOT EXISTS {errors_table_name}("
    "timestamp TIMESTAMP, "
    f"collector_id SYMBOL CAPACITY {config.COLLECTOR_CAPACITY}, "
    f"sensor_id SYMBOL CAPACITY {config.TOTAL_SENSOR_CAPACITY}, "
    "error_message VARCHAR"
    ") TIMESTAMP(timestamp)"
)

"""
The SQL command to create the collector metadata table.

The metadata table maps a collector ID to its metadata attributes so
we don't have to send them in each record. The metadata table is
updated by the collector each time it starts up.
"""
collector_metadata_table_init_command = (
    f"CREATE TABLE IF NOT EXISTS {collector_metadata_table_name}("
    "timestamp TIMESTAMP, "
    f"collector_id SYMBOL CAPACITY {config.COLLECTOR_CAPACITY}, "
    "collector_name VARCHAR, "
    "device_model VARCHAR, "
    "polling_interval INT, "
    ") TIMESTAMP(timestamp)"
)

"""
The SQL command to create the sensor metadata table.

The metadata table maps a sensor ID to its metadata attributes so
we don't have to send them in each record. The metadata table is
updated by the collector each time it starts up.
"""
sensor_metadata_table_init_command = (
    f"CREATE TABLE IF NOT EXISTS {sensor_metadata_table_name}("
    "timestamp TIMESTAMP, "
    f"collector_id SYMBOL CAPACITY {config.COLLECTOR_CAPACITY}, "
    f"sensor_id SYMBOL CAPACITY {config.TOTAL_SENSOR_CAPACITY}, "
    "sensor_code INT, "
    "sensor_name VARCHAR, "
    ") TIMESTAMP(timestamp)"
)
