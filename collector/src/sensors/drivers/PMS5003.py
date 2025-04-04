# MC: 02/21/2025, new file complete implementation

import utime
import machine
from datastructures import SensorData
from config import SensorConfig
from ..driver import AbstractSensorDriver


class PMS5003SensorDriver(AbstractSensorDriver):
    """
    Implementation of the PMS5003 Sensor Driver.
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
        collects sensor data from PMS5003
        Args:
            UART object. Ex: uart_pms = UART(1, baudrate=9600, tx=Pin(6), rx=Pin(7))
        Returns:
            SensorData: The particulate matter data returned by the sensor.
        """
        if self.uart.any():
            response = self.uart.read(32)  # Read 32 bytes (PMS5003 frame size)
            if (
                response
                and len(response) == 32
                and response[0] == 0x42
                and response[1] == 0x4D
            ):
                # sum together high and low byte for each
                pm1_0 = (response[5] << 8) | response[6]  # PM1.0 concentration
                pm2_5 = (response[7] << 8) | response[8]  # PM2.5 concentration
                pm10 = (response[9] << 8) | response[10]  # PM10 concentration
                return {"PM1.0": pm1_0, "PM2.5": pm2_5, "PM10": pm10}

        raise Exception("PMS5003 Failed to return data")
