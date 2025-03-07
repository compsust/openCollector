# MC: 02/21/2025, new file complete implementation

import utime
from machine import UART, Pin
from common.src import SensorData
from ..driver_interface import AbstractSensorDriver


class MHZ19BSensorDriver(AbstractSensorDriver):
    """
    Implementation of the MHZ19B Sensor Driver.
    """

    def poll(self, uart_mhz) -> SensorData:
        """
        collects sensor data from MHZ19C
        Args:
            UART object. Ex: uart_mhz = UART(0, baudrate=9600, tx=Pin(22), rx=Pin(21))
        Returns:
            SensorData: The CO2 data returned by the sensor.
        """
        try:
            if uart_mhz.any():
                uart_mhz.write(
                    bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
                )  # Command to read CO2
                utime.sleep_ms(100)
                response = uart_mhz.read(9)  # Read 9-byte response
                if (
                    response
                    and len(response) == 9
                    and response[0] == 0xFF
                    and response[1] == 0x86
                ):
                    co2 = response[2] * 256 + response[3]
                    return {"CO2": co2}
            return {"CO2": None}

        except Exception as e:
            print("MH-Z19B Error:", e)
            return {"CO2": None}
