# MC: 02/21/2025, new file complete implementation

import utime
import machine
from datastructures import SensorData
from config import SensorConfig
from ..driver import AbstractSensorDriver


class MHZ19BSensorDriver(AbstractSensorDriver):
    """
    Implementation of the MHZ19B Sensor Driver.
    """

    def __init__(self, config: SensorConfig):
        """Initialize the sensor driver with an UART instance."""
        baudrate = 9600
        if config.attributes and config.attributes["baudrate"]:
            baudrate = config.attributes["baudrate"]

        self.uart = machine.UART(
            0,
            baudrate=baudrate,
            tx=machine.Pin(config.gpio["TX"]),
            rx=machine.Pin(config.gpio["RX"]),
        )

    def poll(self) -> SensorData:
        """
        collects sensor data from MHZ19C
        Args:
            UART object. Ex: uart_mhz = UART(0, baudrate=9600, tx=Pin(22), rx=Pin(21))
        Returns:
            SensorData: The CO2 data returned by the sensor.
        """
        if self.uart.any():
            self.uart.write(
                bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
            )  # Command to read CO2
            utime.sleep_ms(100)
            response = self.uart.read(9)  # Read 9-byte response
            if (
                response
                and len(response) == 9
                and response[0] == 0xFF
                and response[1] == 0x86
            ):
                co2 = response[2] * 256 + response[3]
                return {"CO2": co2}

        raise Exception("MHZ91B Failed to return data")
