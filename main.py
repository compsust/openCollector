# 2025-03-07 Initial Commit [CSequeira]

# Import Micropython Packages
from machine import I2C
from utime import sleep_ms

# Import User defined Packages
from collector.sensors.drivers.DHT20 import DHT20
from collector.sensors.drivers.TSL2561 import TSL2561
from collector.sensors.drivers.PMS5003 import PMS5003
from collector.sensors.drivers.MZH19B import MZH19B

# Initialize I2C Buffer
i2c = I2C(1, scl=Pin(27), sda=Pin(26))  # GPIO pins GP21 and GP20

# Turn on Sensors
dht20 = DHT20(i2c)
tsl2561 = TSL2561(i2c)
pms5003 = PMS5003(
    UART(1, baudrate=9600, tx=Pin(21), rx=Pin(22))
)  # GPIO pins GP16 and GP17
mzh19b = MZH19B(UART(2, baudrate=9600, tx=Pin(6), rx=Pin(7)))  # GPIO pins GP4 and GP5

# Initialize Sensors
dht20._initialize()
tsl2561._initialize()
pms5003._initialize()
mzh19b._initialize()

# Read Sensor Data
dht20._read_measurements()
tsl2561._read_measurements()
pms5003._read_measurements()
mzh19b._read_measurements()

# Time delay
time_ms(10)
