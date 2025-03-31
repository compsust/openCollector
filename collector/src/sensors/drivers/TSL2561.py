# MC: 02/21/2025, new file complete implementation
# MC: 03/07/2025, Update to calculate Lux

import utime
import machine
from common.src import SensorData
from ..driver import AbstractSensorDriver


class TSL2561SensorDriver(AbstractSensorDriver):
    """
    Implementation of the Tsl2561 Sensor Driver.
    """

    def __init__(self, i2c):
        """Initialize the sensor driver with an I2C instance."""
        self.i2c = i2c
        self.address = 0x39  # Default I2C address for TSL2561

    def initilize(self):
        """
        Power up command
        """
        try:
            self.i2c.writeto(0x39, bytes([0x00, 0x03]))
        except Exception as e:
            print("TSL2561 Power Up Error:", e)

    def poll(self) -> SensorData:
        """
        collects sensor data from TSL2561
        Args:
            i2c object. Ex: i2c = machine.I2C(0, scl=machine.Pin(27), sda=machine.Pin(26))
        Returns:
            SensorData: The light intensity data returned by the sensor.
        """
        try:
            self.i2c.writeto(0x39, bytes([0xAC]))
            channel0_data = self.i2c.readfrom(0x39, 2)
            self.i2c.writeto(0x39, bytes([0xAE]))
            channel1_data = self.i2c.readfrom(0x39, 2)
            # removed multiplication by 256. no idea why it works now

            ch0 = (channel0_data[1] << 8) | channel0_data[0]  # light + IR
            ch1 = (channel1_data[1] << 8) | channel1_data[0]  # IR

            # follow datasheet page 23 instructions on how to calculate lux
            a = ch1 / ch0
            if 0 < a <= 0.52:
                lux = 0.0315 * ch0 - (0.0593 * ch0 * (ch1 / ch0) ** 1.4)
            elif 0.52 < a <= 0.65:
                lux = 0.0229 * ch0 - 0.0291 * ch1
            elif 0.65 < a <= 0.80:
                lux = 0.0157 * ch0 - 0.0180 * ch1
            elif 0.80 < a <= 1.30:
                lux = 0.00338 * ch0 - 0.00260 * ch1
            else:
                lux = 0
            return {"Luminosity": lux}

        except Exception as e:
            print("TSL2561 Error:", e)
            return {"Luminosity": None}
