Will want to create a readthedocs for this as well

Explain all the steps for supporting a new sensor:
1. Add a new value to SensorCodeEnum
2. Add a new entry to sensor_metadata
3. Create a new SensorDriver in the src/collector/sensors/drivers folder
4. Add this SensorDriver to the sensor_drivers dict in sensor_codes.py
5. Add the sensor config to config.json