from typing import Any

from common import SensorCodeEnum


def get_attribute_or_error(
    config: dict[str, Any], attribute: str, config_name: str
) -> Any:
    """
    Retrieves the attribute from the config, or
    raises an error if it does not exist.

    Args:
        config (dict[str, Any]): The config to retrieve from.
        attribute (str): The name of the attribute.
        config_name (str): The name of the config.

    Raises:
        ValueError: Raised if the attribute does not
            exist within the config.

    Returns:
        Any: The config attribute.
    """
    try:
        attribute = config["attribute"]
    except KeyError:
        raise ValueError(
            f"Config '{config_name}' missing required parameter '{attribute}'."
        )

    if attribute is None:
        raise ValueError(
            f"Config '{config_name}' missing required parameter '{attribute}'."
        )

    return attribute


class DeviceConfig:
    """
    Configuration object which describes a type of device
    that the collector node runs on.
    Attributes:
        model (str): A string representing the type of device,
            for example "Raspberry Pi 3."
        allowed_gpio (list[int]): A list of GPIO pins on the
            device that the collector node is able to access.
            Used to validate sensor configuration, ie., that the
            sensor is configured to a valid GPIO pin.
        requires_micropython (bool): If true, the program will
            not enable a start unless it is being run in a
            micropython environment.
    """

    model: str
    allowed_gpio: list[int]
    requires_micropython: bool

    def __init__(self, config: dict[str, Any], micropython: bool):
        """
        Initializes the config and ensures the required attributes are present.

        Args:
            config (dict[str, Any]): The device config object, ie. the
                dictionary contained within the "device" key in the config file.
            micropython (bool): Whether the current environment is micropython
        """
        self.model = get_attribute_or_error(config, "model", "device")
        self.allowed_gpio = get_attribute_or_error(config, "allowed_gpio", "device")
        self.requires_micropython = get_attribute_or_error(
            config, "requires_micropython", "device"
        )

        if self.requires_micropython and not micropython:
            raise ValueError(
                f"The current device {self.model} requires micropython but the environment is not micropython."
            )


class CacheConfig:
    """
    Configuration object which describes a Memcached target.
    Attributes:
        name (str): A descriptive name for the target.
        endpoint (str): The URI through which the cache target node may
            accept requests.
    """

    name: str
    endpoint: str

    def __init__(self, config: dict[str, Any], index: int):
        """
        Initializes the config and ensures the required attributes are present.

        Args:
            config (dict[str, Any]): The cache config object, ie. a
                dictionary contained within the "caches" array in the config file.
            index (int): The index of the cache config within the "caches" array.
        """
        self.name = get_attribute_or_error(config, "name", f"cache[{index}]")
        self.endpoint = get_attribute_or_error(config, "endpoint", f"cache[{index}]")


class SensorConfig:
    """
    Configuration object which describes a sensor.
    Attributes:
        sensor_id (str): An ID associated with the sensor.
        sensor_code (SensorCodeEnum): Associated with
            a specific implementation of AbstractSensorDriver.
        name (str): A descriptive name for the sensor.
        gpio (dict[str, int]): A dictionary where the values are
            GPIO pins which the sensor requires use of, and
            the keys are string identifiers. Used to validate
            that the configured GPIO pins match the allowed_gpio
            attribute of the device config.
        attributes (dict[str, Any]): Any other attributes
            which are required to use the sensor.
    """

    sensor_id: str
    sensor_code: SensorCodeEnum
    name: str
    gpio: dict[str, int]
    attributes: dict[str, Any]

    def __init__(
        self,
        config: dict[str, Any],
        index: int,
        allowed_gpio: list[int],
    ):
        """
        Initializes the config and ensures the required attributes are present.
        Also, validates that the configured GPIO pins match those specified in the
        device config.

        Args:
            config (dict[str, Any]): The sensor config object, ie. a
                dictionary contained within the "sensors" array in the config file.
            index (int): The index of the sensor config within the "sensors" array.
            allowed_gpio (list[int]): The allowed GPIO pins as configured in the device config.
        """
        self.sensor_id = get_attribute_or_error(config, "sensor_id", f"sensor[{index}]")
        self.sensor_code = get_attribute_or_error(
            config, "sensor_code", f"sensor[{index}]"
        )
        self.name = get_attribute_or_error(config, "name", f"sensor[{index}]")
        self.gpio = get_attribute_or_error(config, "gpio", f"sensor[{index}]")
        self.attributes = get_attribute_or_error(
            config, "attributes", f"sensor[{index}]"
        )

        # Validate that the configured GPIO pins are allowed on this device.
        for pin in self.gpio:
            if self.gpio[pin] not in allowed_gpio:
                raise ValueError(
                    f"Error when configuring sensor ID {self.sensor_id} with name {self.name}: gpio pin {self.gpio}, {self.gpio[pin]} not included in allowed gpio pins: {allowed_gpio}"
                )


class CollectorConfig:
    """
    Configuration object which describes the collector node device.
    Attributes:
        collector_id (str): An ID associated with the node.
        node_name (str): A name associated with the node.
        polling_interval (int): The number of miliseconds to wait
            between sensor polls. Must not be negative.
        device (DeviceConfig): The device config.
        sensors (list[SensorConfig]): All configured sensors.
        caches (list[TargetConfig]): All configured caches.
    """

    collector_id: str
    node_name: str
    polling_interval: int
    device: DeviceConfig
    sensors: list[SensorConfig]
    caches: list[CacheConfig]

    def __init__(
        self,
        config: dict[str, Any],
        device: DeviceConfig,
        sensors: list[SensorConfig],
        caches: list[CacheConfig],
    ):
        """
        Initializes the config and ensures the required attributes are present.

        Args:
            config (dict[str, Any]): The config object, ie. the
                dictionary pulled from the config file.
        """
        self.collector_id = get_attribute_or_error(config, "collector_id", "config")
        self.node_name = get_attribute_or_error(config, "node_name", "config")
        self.polling_interval = get_attribute_or_error(
            config, "polling_interval", "config"
        )
        self.device = device
        self.sensors = sensors
        self.caches = caches

        # Validate that polling_interval is not negative
        if self.polling_interval < 0:
            raise ValueError("Cannot set a negative polling interval.")
