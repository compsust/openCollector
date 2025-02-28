from decouple import config

# QuestDB connection settings.
QUESTDB_HOST = config('QUESTDB_HOST', cast=str, default="localhost")
QUESTDB_PORT = config('QUESTDB_PORT', cast=int, default=8812)
QUESTDB_USER = config('QUESTDB_USER', cast=str, default="admin")
QUESTDB_PASSWORD = config('QUESTDB_PASSWORD', cast=str, default="password")
QUESTDB_DB_NAME = config('QUESTDB_DB_NAME', cast=str, default="qdb")

# Database schema settings
COLLECTOR_CAPACITY = config('COLLECTOR_CAPACITY', cast=int, default=256)
SENSOR_CAPACITY = config('SENSOR_CAPACITY', cast=int, default=16)