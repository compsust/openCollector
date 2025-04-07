# 2025-03-07 Initial Commit [CSequeira]
# 2025-04-03 Update to correct functions in classes [CSequeira]

# Import Micropython Packages
from machine import I2C
from utime import sleep_ms

# Import User defined Packages
from collector.src.sensors.drivers.DHT20 import micropython
from collector.src.sensors.drivers.TSL2561 import micropython
from collector.src.sensors.drivers.PMS5003 import micropython
from collector.src.sensors.drivers.MHZ19B import micropython

# Initialize I2C Buffer
i2c = I2C(1, scl=Pin(27), sda=Pin(26))  # GPIO pins GP21 and GP20

# Turn on Sensors
dht20 = micropython(i2c)
tsl2561 = micropython(i2c)
pms5003 = micropython(
    UART(1, baudrate=9600, tx=Pin(21), rx=Pin(22))
)  # GPIO pins GP16 and GP17
mhz19b = micropython(
    UART(2, baudrate=9600, tx=Pin(6), rx=Pin(7))
)  # GPIO pins GP4 and GP5

# Initialize Sensors
dht20.initialize()
tsl2561.initialize()
pms5003.initialize()
mhz19b.initialize()

# Read Sensor Data
dht20.poll()
tsl2561.poll()
pms5003.poll()
mhz19b.poll()

# Time delay
time_ms(10)
