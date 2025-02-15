#MC: 01/22/2025, change DHT22 to DHT20, update pins as needed, refer to Altium PCB Schematic

import machine
import utime
from machine import UART, Pin

# I2C Setup for TSL2561 and DH20
i2c = machine.I2C(0, scl=machine.Pin(27), sda=machine.Pin(26))

# UART Setup for PMS5003 and MH-Z19B
uart_pms = UART(0, baudrate=9600, tx=Pin(22), rx=Pin(21))
uart_mhz = UART(1, baudrate=9600, tx=Pin(6), rx=Pin(7))

# Set up the GPIO pin for DHT22
dht_pin = machine.Pin(34, machine.Pin.OUT)

utime.sleep(1)  # Allow the sensor to initialize

# Functions to get Sensor Readings


# Light Sensor Power Up
def power_up_tsl2561():
    try:
        i2c.writeto(0x39, bytes([0x00, 0x03]))  # Power up command
    except Exception as e:
        print("TSL2561 Power Up Error:", e)


# Light Sensor Reading
def read_tsl2561(command):
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
        if uart_pms.any():
            data = uart_pms.read(32)  # Read 32 bytes (PMS5003 frame size)
            # Example parsing; replace with specific PMS5003 protocol
            return data
        return None
    except Exception as e:
        print("PMS5003 Error:", e)
        return None


# Carbon Dioxide Sensor Reading
def read_mhz19b():
    try:
        if uart_mhz.any():
            uart_mhz.write(
                b"\xff\x01\x86\x00\x00\x00\x00\x00\x79"
            )  # Command to read CO2
            utime.sleep(0.1)
            response = uart_mhz.read(9)  # Read 9-byte response
            if response and len(response) == 9:
                co2 = response[2] * 256 + response[3]
                return co2
        return None
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
        
        #ask for measurement
        utime.sleep_ms(10)
        i2c.writeto(0x38, [0x33, 0x00])
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

        #data processing
        data = i2c.readfrom(0x38, 6)  # Read 6 bytes of data
        hum = ((data[1] << 12) | (data[2] << 8) | (data[3] >> 4)) / (2**20) * 100
        temp = (((data[4] & 0x0F) << 12) | (data[5] << 8) | (data[6])) / (2**20) * 200 - 50
        return temp, hum
    except Exception as e:
        print("DHT20 Error:", e)
        return None, None

# Obsolete
# Temperature & Humidity Sensor Reading
def read_dht22():
    try:
        dht_sensor.measure()  # Trigger the DHT22 to read
        temp = dht_sensor.temperature()  # Get temperature in °C
        hum = dht_sensor.humidity()  # Get humidity in %
        return temp, hum
    except Exception as e:
        print("DHT22 Error:", e)
        return None, None


# Main loop
while True:
    tsl2561_lux = read_tsl2561()
    if tsl2561_lux is not None:
        print(f"TSL2561 Lux: {tsl2561_lux} lx")

    pms_data = read_pms5003()
    if pms_data is not None:
        print(f"PMS5003 Data: {pms_data}")

    mhz19b_co2 = read_mhz19b()
    if mhz19b_co2 is not None:
        print(f"MH-Z19B CO2: {mhz19b_co2} ppm")

    dht20_temp, dht20_hum = read_dht20()
    if dht20_temp is not None:
        print(f"DHT20 Temperature: {dht20_temp} °C")
    if dht20_hum is not None:
        print(f"DHT20 Humidity: {dht20_hum} %")

    utime.sleep(2)  # Loops every 2 seconds
