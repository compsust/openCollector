# MC: 02/21/2025, new file complete implementation
# MC: 04/04/2025, update implmentation

import utime
import machine
from datastructures import SensorData
from config import SensorConfig
from ...driver import AbstractSensorDriver


class MHZ19BSensorDriverMicropython(AbstractSensorDriver):
    """
    Implementation of the MHZ19B Sensor Driver.
    """

    calibration_pin = machine.Pin(1, mode=machine.Pin.OUT, value=1)

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

    max_retries = 30

    def poll(self) -> SensorData:
        """
        collects sensor data from MHZ19C
        Args:
            UART object. Ex: uart_mhz = UART(0, baudrate=9600, tx=Pin(22), rx=Pin(21))
        Returns:
            SensorData: The CO2 data returned by the sensor.
        """
        # Flush any leftover junk
        for attempt in range(max_retries):
            while self.uart.any():
                self.uart.read()

            self.uart.write(
                bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
            )  # Command to read CO2
            timeout = 100
            start = utime.ticks_ms()
            while (
                self.uart.any() < 9
                and utime.ticks_diff(utime.ticks_ms(), start) < timeout
            ):
                utime.sleep_ms(5)
            raw = self.uart.read(9)
            # print(raw)
            if raw and raw[0] == 0xFF:
                co2 = raw[3] * 256 + raw[4]
                return co2

        raise Exception("MHZ91B Failed to return data")

    def calibrate(self):
        """
        Manually calibrate sensor
        Args:
            None
        Returns:
            None
        """
        self.calibration_pin.value(0)
        utime.sleep(8)  # hold low for 7+ seconds
        self.calibration_pin.value(1)
