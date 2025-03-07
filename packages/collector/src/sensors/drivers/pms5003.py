# MC: 02/21/2025, new file complete implementation

import utime
from machine import UART, Pin
from common.src import SensorData
from ..driver_interface import AbstractSensorDriver


class PMS5003SensorDriver(AbstractSensorDriver):
    """
    Implementation of the PMS5003 Sensor Driver.
    """

    reset_pin = machine.Pin(24, machine.Pin.OUT)  # Assume reset is connected to GP15

    def reset_pms5003():
        """
        Send a short low pulse to reset device
        """
        reset_pin.value(0)  # Pull RESET pin LOW
        utime.sleep_ms(100)  # Wait for 100ms
        reset_pin.value(1)  # Set RESET pin HIGH (normal operation)
        utime.sleep(1)  # Give the sensor time to restart

    def poll(self, uart_pms) -> SensorData:
        """
        collects sensor data from PMS5003
        Args:
            UART object. Ex: uart_pms = UART(1, baudrate=9600, tx=Pin(6), rx=Pin(7))
        Returns:
            SensorData: The particulate matter data returned by the sensor.
        """
        try:
            if uart_pms.any():
                response = uart_pms.read(32)  # Read 32 bytes (PMS5003 frame size)
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
                return {"PM1.0": None, "PM2.5": None, "PM10": None}

        except Exception as e:
            print("PMS5003 Error:", e)
            return {"PM1.0": None, "PM2.5": None, "PM10": None}
