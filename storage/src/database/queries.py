from common import (
    records_table_name,
    errors_table_name,
    collector_metadata_table_name,
    sensor_metadata_table_name,
)

collector_count_query = (
    f"SELECT COUNT(DISTINCT collector_id) FROM {collector_metadata_table_name}"
)
"""Returns the number of collector nodes that have reported."""

sensor_count_query = (
    f"SELECT COUNT(DISTINCT sensor_id) FROM {sensor_metadata_table_name}"
)
"""Returns the number of sensors that have reported."""

latest_data_query = f"""
WITH 
latest_sensor_metadata AS (
    -- Get the latest metadata for each sensor
    SELECT 
        sensor_id,
        collector_id,
        sensor_name,
        MAX(timestamp) AS metadata_timestamp
    FROM {sensor_metadata_table_name}
    GROUP BY sensor_id, collector_id, sensor_name
),
latest_records AS (
    -- Get the latest record for each sensor and record_id combination
    SELECT 
        sensor_id,
        collector_id,
        record_id,
        value,
        timestamp AS record_timestamp,
        RANK() OVER (PARTITION BY sensor_id, collector_id, record_id ORDER BY timestamp DESC) AS rank
    FROM {records_table_name}
),
latest_errors AS (
    -- Get the latest error for each sensor
    SELECT 
        sensor_id,
        collector_id,
        error_message,
        timestamp AS error_timestamp,
        RANK() OVER (PARTITION BY sensor_id, collector_id ORDER BY timestamp DESC) AS rank
    FROM {errors_table_name}
),
collector_polling_info AS (
    -- Get polling interval for each collector
    SELECT
        collector_id,
        polling_interval,
        MAX(timestamp) AS metadata_timestamp
    FROM {collector_metadata_table_name}
    GROUP BY collector_id, polling_interval
)
-- Final query returning raw data needed for status determination in Python
SELECT
    sm.sensor_id,
    sm.collector_id,
    sm.sensor_name,
    lr.record_id,
    lr.value,
    lr.record_timestamp,
    le.error_message,
    le.error_timestamp,
    cp.polling_interval
FROM latest_sensor_metadata sm
JOIN collector_polling_info cp ON sm.collector_id = cp.collector_id
LEFT JOIN latest_records lr ON sm.sensor_id = lr.sensor_id AND sm.collector_id = lr.collector_id AND lr.rank = 1
LEFT JOIN latest_errors le ON sm.sensor_id = le.sensor_id AND sm.collector_id = le.collector_id AND le.rank = 1
WHERE lr.record_id IS NOT NULL
ORDER BY sm.collector_id, sm.sensor_id, lr.record_id;
"""

total_records_query = "SELECT COUNT FROM records"
total_errors_query = "SELECT COUNT FROM errors"
