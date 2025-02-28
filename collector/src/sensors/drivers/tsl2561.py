# MC: 02/21/2025, new file complete implementation

import utime
import machine
from common import SensorData
from ..driver_interface import AbstractSensorDriver


class Tsl2561SensorDriver(AbstractSensorDriver):
    """
    Implementation of the Tsl2561 Sensor Driver.
    """

    def power_up_tsl2561(i2c):
        """
        Power up command
        """
        try:
            i2c.writeto(0x39, bytes([0x00, 0x03]))
        except Exception as e:
            print("TSL2561 Power Up Error:", e)

    def poll(self, i2c) -> SensorData:
        """
        collects sensor data from TSL2561
        Args:
            i2c object. Ex: i2c = machine.I2C(0, scl=machine.Pin(27), sda=machine.Pin(26))
        Returns:
            SensorData: The light intensity data returned by the sensor.
        """
        try:
            i2c.writeto(0x39, bytes([0xAC]))
            channel0_data = i2c.readfrom(0x39, 2)
            i2c.writeto(0x39, bytes([0xAE]))
            channel1_data = i2c.readfrom(0x39, 2)

            channel0 = 256 * ((channel0_data[1] << 8) | channel0_data[0])
            channel1 = 256 * ((channel1_data[1] << 8) | channel1_data[0])
            return {"Luminosity Channel0": channel0, "Luminosity Channel1": channel1}

        except Exception as e:
            print("TSL2561 Error:", e)
            return {"Luminosity Channel0": None, "Luminosity Channel1": None}
