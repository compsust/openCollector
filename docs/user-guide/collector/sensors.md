# Sensors

This page contains information on the types of sensors that are supported and their associated configuration values.

For information on how to add more supported sensors to the software, see the page in the [Developer Docs](../../developer-guide/collector/sensors.md).

## Supported Sensors and Codes

The following table outlines the sensors that are supported by the collector node software. Node that the values in the *Sensor Code* column are the values that are accepted by the `sensor_code` value in the sensor configuration object. 

| Sensor | Type | Sensor Code |
| -------- | ------- | -------- |
| [DHT20](https://www.adafruit.com/product/5183) | Temperature & Humidity | `"DHT20"` |
| [TSL2561](https://cdn-shop.adafruit.com/datasheets/TSL2561.pdf) | Luminosity | `"TSL2561"` |
| [PMS5003](https://www.adafruit.com/product/3686) | Air Quality | `"PMS5003"` |
| [MH-Z19B](https://www.winsen-sensor.com/d/files/infrared-gas-sensor/mh-z19b-co2-ver1_0.pdf) | CO2 | `"MHZ19B"` |

## Configurations

The following sections outline the required structure of the `gpio` and `attributes` section of the sensor config for each sensor type. It also includes the structure of data which is output by the sensor.

### DHT20

The DHT is a compact temperature and humidity sensor which communicates via I2C.

#### GPIO

The following is the structure and allowed keys of the `gpio` object within the sensor config object for this sensor.

| Key | Description |
| -------- | ------- |
| `"SCL"` | The GPIO pin used for SCL. |
| `"SDA"` | The GPIO pin used for SDA. |

#### Extra Attributes

There are no extra attributes used by this sensor.

#### Output Structure

The following is the structure of the data which this sensor will upload to the database.

| Value | Unit | Description |
| -------- | ------- | ------- |
| Temperature | °C | The temperature read by the sensor in celsius. |
| Humidity | % | The humitidy read by the sensor in %. |

### TSL2561

The TSL2561 is a digital light sensor which communicates via I2C.

#### GPIO

The following is the structure and allowed keys of the `gpio` object within the sensor config object for this sensor.

| Key | Description |
| -------- | ------- |
| `"SCL"` | The GPIO pin used for SCL. |
| `"SDA"` | The GPIO pin used for SDA. |

#### Extra Attributes

There are no extra attributes used by this sensor.

#### Output Structure

The following is the structure of the data which this sensor will upload to the database.

| Value | Unit | Description |
| -------- | ------- | ------- |
| Luminosity | Lux | The luminosity read by the sensor in lux. |

### PMS5003

The PMS5003 is a digital air quality sensor which communicates through UART. It reports the concentration of PM1.0, PM2.5, and PM10.

#### GPIO

The following is the structure and allowed keys of the `gpio` object within the sensor config object for this sensor.

| Key | Description |
| -------- | ------- |
| `"TX"` | The GPIO pin used for UART TX. |
| `"RX"` | The GPIO pin used for UART RX. |

#### Extra Attributes

The following is the structure and allowed keys of the `attributes` object within the sensor config object for this sensor.

| Key | Description |
| `"baudrate"` | The baudrate used for configuring UART. |

#### Output Structure

The following is the structure of the data which this sensor will upload to the database.

| Value | Unit | Description |
| -------- | ------- | ------- |
| Particulate Matter Concentration 1.0 | PM1.0 | The PM1.0 read by the sensor. |
| Particulate Matter Concentration 2.5 | PM2.5 | The PM2.5 read by the sensor. |
| Particulate Matter Concentration 10 | PM10 | The PM10 read by the sensor. |

### MH-Z19B

The MH-Z19B is a digital CO2 sensor which communicates through UART.

#### GPIO

The following is the structure and allowed keys of the `gpio` object within the sensor config object for this sensor.

| Key | Description |
| -------- | ------- |
| `"TX"` | The GPIO pin used for UART TX. |
| `"RX"` | The GPIO pin used for UART RX. |

#### Extra Attributes

The following is the structure and allowed keys of the `attributes` object within the sensor config object for this sensor.

| Key | Description |
| `"baudrate"` | The baudrate used for configuring UART. |

#### Output Structure

The following is the structure of the data which this sensor will upload to the database.

| Value | Unit | Description |
| -------- | ------- | ------- |
| CO2 Concentration | PPM | The CO2 concentration read by the sensor in parts per million. |