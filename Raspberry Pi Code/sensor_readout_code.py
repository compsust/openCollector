# MC: 01/22/2025, change DHT22 to DHT20, update pins as needed, refer to Altium PCB Schematic
# MC: 02/14/2025, fixes to DHT20
# MC: 02/21/2025, adjustments to Mh-z19 and PMS5003

import machine
import utime
from machine import UART, Pin

# I2C Setup for TSL2561 and DH20
i2c = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))

# UART Setup for PMS5003 and MH-Z19B
uart_pms = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
uart_mhz = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

set_pin = Pin(19, mode=Pin.OUT, value=1)
reset_pin = Pin(18, mode=Pin.OUT, value=1)

utime.sleep(1)  # Allow the sensor to initialize

# Functions to get Sensor Readings


# Light Sensor Power Up
def power_up_tsl2561():
    try:
        i2c.writeto(0x39, bytes([0x00, 0x03]))  # Power up command
    except Exception as e:
        print("TSL2561 Power Up Error:", e)


# Light Sensor Reading
def read_tsl2561():
    try:
        i2c.writeto(0x39, bytes([0xAC]))
        channel0_data = i2c.readfrom(0x39, 2)
        i2c.writeto(0x39, bytes([0xAE]))
        channel1_data = i2c.readfrom(0x39, 2)

        channel0 = 256 * ((channel0_data[1] << 8) | channel0_data[0])
        channel1 = 256 * ((channel1_data[1] << 8) | channel1_data[0])
        return channel0, channel1
    except Exception as e:
        print("TSL2561 Error:", e)
        return None


# Particulate Matter Sensor Reading
def read_pms5003():
    try:
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
            return pm1_0, pm2_5, pm10
        return None
    except Exception as e:
        print("PMS5003 Error:", e)
    return None


# Carbon Dioxide Sensor Reading
def read_mhz19b():
    try:
        uart_mhz.write(
            bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
        )  # Command to read CO2
        utime.sleep(1)
        print(uart_mhz.any())
        response = uart_mhz.read(9)  # Read 9-byte response
        print(response)

        co2 = response[2] * 256 + response[3]
        return co2

    except Exception as e:
        print("MH-Z19B Error:", e)
        return None


# Temperature & Humidity Sensor Reading updated
def read_dht20():
    try:
        data = i2c.readfrom(0x38, 1)
        if data[0] != 0x18:
            print("DHT20 Error: Checksum Fail")
            return None, None

        # ask for measurement
        utime.sleep_ms(50)
        i2c.writeto_mem(0x38, 0xAC, bytes([0x33, 0x00]))
        utime.sleep_ms(80)

        # check if measurment is complete
        while True:
            counter = 0
            status = i2c.readfrom(0x38, 1)
            status_bit7 = (status[0] & 0x80) == 0  # Extract Bit [7]
            if status_bit7:  # If Bit [7] == 0, measurement is complete
                break
            elif counter > 10:
                print("DHT20 Error: Measurement Timeout")
                return None, None
            else:
                utime.sleep_ms(80)  # Wait 80ms before checking again
                counter += 1

        # data processing
        data = i2c.readfrom(0x38, 7)  # Read 6 bytes of data
        hum = (data[1] << 12 | data[2] << 4 | data[3] >> 4) / (2**20) * 100
        temp = ((data[3] << 16 | data[4] << 8 | data[5]) & 0xFFFFF) / (2**20) * 200 - 50
        return temp, hum
    except Exception as e:
        print("DHT20 Error:", e)
        return None, None


CMD_RESET = b"\x42\x4d\xe1\xc4"  # Reset command
CMD_SLEEP = b"\x42\x4d\xe2\xc3"  # Sleep command
CMD_WAKEUP = b"\x42\x4d\xe3\xc2"  # Wakeup command
CMD_MODE_PASSIVE = b"\x42\x4d\xe4\xc1"  # Passive mode command
CMD_READ_DATA = b"\x42\x4d\xe5\xc0"  # Read data command
CMD_MODE_ACTIVE = b"\x42\x4d\xe6\xbf"  # Active mode command


def send_command(command):
    uart_pms.write(command)
    utime.sleep(1)


def initialize_sensor():
    print("Initializing PMS5003...")

    # Reset sensor
    send_command(CMD_RESET)
    utime.sleep(5)  # Wait for the reset to complete

    # Set sleep mode and wake up
    send_command(CMD_SLEEP)
    send_command(CMD_WAKEUP)
    utime.sleep(2)

    # Set to passive mode and request data
    send_command(CMD_MODE_ACTIVE)
    # send_command(CMD_READ_DATA)


# initialize_sensor()

# Main loop
while True:
    """tsl2561_lux = read_tsl2561()
    if tsl2561_lux is not None:
        print(f"TSL2561 Lux: {tsl2561_lux} lx")"""

    """pms_data = read_pms5003()
    response = uart_pms.read(32)  # Read 32 bytes (PMS5003 frame size)
    print(response)
    print(uart_pms.any())
    print(f"PMS5003 Data: {pms_data}")"""

    mhz19b_co2 = read_mhz19b()
    print(f"MH-Z19B CO2: {mhz19b_co2} ppm")

    """dht20_temp, dht20_hum = read_dht20()
    if dht20_temp is not None:
        print(f"DHT20 Temperature: {dht20_temp} °C")
    if dht20_hum is not None:
        print(f"DHT20 Humidity: {dht20_hum} %")"""

    utime.sleep(2)  # Loops every 2 seconds
