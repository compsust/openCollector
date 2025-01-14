import machine
import utime
from machine import I2C, UART, Pin
import dht

# I2C Setup for TSL2561
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))

# UART Setup for PMS5003 and MH-Z19B
uart_pms = UART(0, baudrate=9600, tx=Pin(1), rx=Pin(2))
uart_mhz = UART(1, baudrate=9600, tx=Pin(6), rx=Pin(7))

# Set up the GPIO pin for DHT22
dht_pin = machine.Pin(34, machine.Pin.OUT)

utime.sleep(1)  # Allow the sensor to initialize

# Functions to get Sensor Readings

# Light Sensor Reading
def read_tsl2561():
    # Example: Assuming a library or basic read implementation for TSL2561
    # Replace this with actual TSL2561 read logic
    try:
        light_data = i2c.readfrom(0x39, 2)  # Adjust the I2C address if necessary
        lux = int.from_bytes(light_data, "big")
        return lux
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
            uart_mhz.write(b"\xFF\x01\x86\x00\x00\x00\x00\x00\x79")  # Command to read CO2
            utime.sleep(0.1)
            response = uart_mhz.read(9)  # Read 9-byte response
            if response and len(response) == 9:
                co2 = response[2] * 256 + response[3]
                return co2
        return None
    except Exception as e:
        print("MH-Z19B Error:", e)
        return None

# Temperature & Humidity Sensor Reading
def read_dht22():
    try:
        dht_sensor.measure()  # Trigger the DHT22 to read
        temp = dht_sensor.temperature()  # Get temperature in °C
        hum = dht_sensor.humidity()      # Get humidity in %
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

    dht22_temp, dht22_hum = read_dht22()
    if dht22_temp is not None:
        print(f"DHT22 Temperature: {dht22_temp} °C")
    if dht22_hum is not None:
        print(f"DHT22 Humidity: {dht22_hum} %")

    utime.sleep(2) # Loops every 2 seconds
