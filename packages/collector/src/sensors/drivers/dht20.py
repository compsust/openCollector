# MC: 02/21/2025, Complete implmentation

import utime
import machine
from common.src import SensorData
from ..driver_interface import AbstractSensorDriver


class Dht20SensorDriver(AbstractSensorDriver):
    """
    Implementation of the Dht20 Sensor Driver.
    """

    def poll(self, i2c) -> SensorData:
        """
        collects sensor data from DHT20
        Args:
            i2c object. Ex: i2c = machine.I2C(0, scl=machine.Pin(27), sda=machine.Pin(26))
        Returns:
            SensorData: The temperature and humidity data returned by the sensor.
        """

        try:
            status = i2c.readfrom(0x38, 1)
            if status[0] != 0x18:
                print("DHT20 Error: Checksum Fail")
                return {"temperature": None, "humidity": None}

            # ask for measurement
            utime.sleep_ms(50)
            i2c.writeto_mem(0x38, 0xAC, bytes([0x33, 0x00]))
            utime.sleep_ms(80)

            # check if measurment is complete
            counter = 0
            while True:
                status = i2c.readfrom(0x38, 1)
                status_bit7 = (status[0] & 0x80) == 0  # Extract Bit [7]
                if status_bit7:  # If Bit [7] == 0, measurement is complete
                    break
                elif counter > 10:
                    print("DHT20 Error: Measurement Timeout")
                    return {"temperature": None, "humidity": None}
                else:
                    utime.sleep_ms(80)  # Wait 80ms before checking again
                    counter += 1

            # data processing
            data = i2c.readfrom(0x38, 7)  # Read 6 bytes of data
            hum = (data[1] << 12 | data[2] << 4 | data[3] >> 4) / (2**20) * 100
            temp = ((data[3] << 16 | data[4] << 8 | data[5]) & 0xFFFFF) / (
                2**20
            ) * 200 - 50
            return {"temperature": temp, "humidity": hum}

        except Exception as e:
            print("DHT20 Error:", e)
            return {"temperature": None, "humidity": None}
