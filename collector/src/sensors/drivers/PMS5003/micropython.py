# MC: 02/21/2025, new file complete implementation
# MC: 04/04/2025, update implementation

import machine
import utime

from ....config import SensorConfig
from ....datastructures import SensorData
from ...driver import AbstractSensorDriver


class PMS5003SensorDriverMicropython(AbstractSensorDriver):
    """
    Implementation of the PMS5003 Sensor Driver for micropython.
    """

    # Command values
    PMS5003_SOF = bytearray([0x42, 0x4D])
    PMS5003_CMD_MODE_PASSIVE = bytearray([0xE1, 0x00, 0x00])
    PMS5003_CMD_MODE_ACTIVE = bytearray([0xE1, 0x00, 0x01])
    PMS5003_CMD_READ = bytearray([0xE2, 0x00, 0x00])
    PMS5003_CMD_SLEEP = bytearray([0xE4, 0x00, 0x00])
    PMS5003_CMD_WAKEUP = bytearray([0xE4, 0x00, 0x01])

    set_pin = machine.Pin(19, mode=machine.Pin.OUT, value=1)
    reset_pin = machine.Pin(18, mode=machine.Pin.OUT, value=1)

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
            self.uart.write(self.pms5003_build_frame(self.PMS5003_CMD_READ))
            utime.sleep(0.5)
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

    def pms5003_build_frame(self, cmd_bytes):
        """
        Build command byte array
        Args:
            Command
        Returns:
            Functional byte array
        """
        if len(cmd_bytes) != 3:
            raise RuntimeError("Malformed command frame")
        cmd_frame = bytearray()
        cmd_frame.extend(self.PMS5003_SOF)
        cmd_frame.extend(cmd_bytes)

        cmd_frame.extend(sum(cmd_frame).to_bytes(2, "big"))
        cmd_frame = " ".join(f"0x{b:02X}" for b in cmd_frame)
        print(cmd_frame)
        return cmd_frame

    def reset(self):
        self.reset_pin.value(0)
        utime.sleep(1)
        self.reset_pin.value(1)

    def send_cmd(self, cmd):
        self.uart.write(self.pms5003_build_frame(cmd))
