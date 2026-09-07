from .DHT20.python import DHT20SensorDriverPython
from .MHZ19B.python import MHZ19BSensorDriverPython
from .mock import MockSensorDriver
from .PMS5003.python import PMS5003SensorDriverPython
from .TSL2561.python import TSL2561SensorDriverPython

try:
    import machine  # noqa: F401
except ImportError:
    DHT20SensorDriverMicropython = None
    MHZ19BSensorDriverMicropython = None
    PMS5003SensorDriverMicropython = None
    TSL2561SensorDriverMicropython = None
else:
    from .DHT20.micropython import DHT20SensorDriverMicropython
    from .MHZ19B.micropython import MHZ19BSensorDriverMicropython
    from .PMS5003.micropython import PMS5003SensorDriverMicropython
    from .TSL2561.micropython import TSL2561SensorDriverMicropython

__all__ = [
    "DHT20SensorDriverPython",
    "DHT20SensorDriverMicropython",
    "MHZ19BSensorDriverPython",
    "MHZ19BSensorDriverMicropython",
    "PMS5003SensorDriverPython",
    "PMS5003SensorDriverMicropython",
    "TSL2561SensorDriverPython",
    "TSL2561SensorDriverMicropython",
    "MockSensorDriver",
]

__all__ = [
    "DHT20SensorDriverPython",
    "DHT20SensorDriverMicropython",
    "MHZ19BSensorDriverPython",
    "MHZ19BSensorDriverMicropython",
    "PMS5003SensorDriverPython",
    "PMS5003SensorDriverMicropython",
    "TSL2561SensorDriverPython",
    "TSL2561SensorDriverMicropython",
    "MockSensorDriver",
]
