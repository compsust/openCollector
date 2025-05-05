# MC: 02/21/2025, new file complete implementation
# MC: 04/04/2025, update implmentation
# MC: 05/04/2025, update poll to use PWM
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

        """self.uart = machine.UART(
            0,
            baudrate=baudrate,
            tx=machine.Pin(config.gpio["TX"]),
            rx=machine.Pin(config.gpio["RX"]),
        )"""
        self.pwm = machine.Pin(2, machine.Pin.IN)

    max_retries = 30

    def poll(self) -> SensorData:
        """
        collects sensor data from MHZ19C
        Args:
            Pin Object
        Returns:
            SensorData: The CO2 data returned by the sensor.
        """
        high_time = machine.time_pulse_us(self.pwm, 1)  # measure HIGH duration in microseconds
        low_time = machine.time_pulse_us(self.pwm, 0)   # measure LOW duration in microseconds

        total_time = high_time + low_time
        if total_time > 0:
            co2 = 5000 * (high_time / 1000 - 2) / ((total_time / 1000) - 4)
            return(co2)

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
