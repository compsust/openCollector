from decouple import config

# QuestDB connection settings.
QUESTDB_HOST = config("QUESTDB_HOST", cast=str, default="database")
QUESTDB_PORT = config("QUESTDB_PORT", cast=int, default=8812)
QUESTDB_USER = config("QUESTDB_USER", cast=str, default="pguser")
QUESTDB_PASSWORD = config("QUESTDB_PASSWORD", cast=str, default="quest")
QUESTDB_DB_NAME = config("QUESTDB_DB_NAME", cast=str, default="qdb")

# Database schema settings
COLLECTOR_CAPACITY = config("COLLECTOR_CAPACITY", cast=int, default=1024)
SENSOR_CAPACITY = config("SENSOR_CAPACITY", cast=int, default=16)
TOTAL_SENSOR_CAPACITY = COLLECTOR_CAPACITY * SENSOR_CAPACITY

# Node settings
NODE_NAME = config("NODE_NAME", cast=str, default="OpenCollector")

# User settings
INTERFACE_USER = config("INTERFACE_USER", cast=str, default="username")
INTERFACE_PASSWORD = config("INTERFACE_PASSWORD", cast=str, default="password")
INTERFACE_REFRESH_SECONDS = config("INTERFACE_REFRESH_SECONDS", cast=int, default=1)

# Display settings
ACTIVE_DEVICE_POLLING_THRESHOLD = config(
    "ACTIVE_DEVICE_POLLING_THRESHOLD", cast=int, default=3
)
