from typing import Any

from common.src import SensorCodeEnum


def get_attribute(
    config: dict[str, Any], attribute: str, config_name: str, required: bool = True
) -> Any:
    """
    Retrieves the attribute from the config, or
    raises an error if it does not exist and the attribute is required.

    Args:
        config (dict[str, Any]): The config to retrieve from.
        attribute (str): The name of the attribute.
        config_name (str): The name of the config.
        required (bool): If true, an exception will be raised
            if the attribute doesn't exist.

    Raises:
        ValueError: Raised if the attribute does not
            exist within the config and is required.

    Returns:
        Any: The config attribute, or None if it does not exist and is not required.
    """
    try:
        attribute = config["attribute"]
    except KeyError:
        if required:
            raise ValueError(
                f"Config '{config_name}' missing required parameter '{attribute}'."
            )
        else:
            return None

    if attribute is None and required:
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
        self.model = get_attribute(config, "model", "device")
        self.allowed_gpio = get_attribute(config, "allowed_gpio", "device")
        self.requires_micropython = get_attribute(
            config, "requires_micropython", "device"
        )

        if self.requires_micropython and not micropython:
            raise ValueError(
                f"The current device {self.model} requires micropython but the environment is not micropython."
            )


class UploadConfig:
    """
    Configuration object which describes a QuestDB target.
    Attributes:
        host (str): The database URL.
        port (str): The database port.
        user (str): The database username.
        password (str): The database password.
    """

    host: str
    port: str
    user: str
    password: str

    def __init__(self, config: dict[str, Any]):
        """
        Initializes the config and ensures the required attributes are present.

        Args:
            config (dict[str, Any]): The upload config object, ie. the
                dictionary contained within the "upload" key in the config file.
        """
        self.host = get_attribute(config, "host", "upload")
        self.port = get_attribute(config, "port", "upload")
        self.user = get_attribute(config, "user", "upload")
        self.password = get_attribute(config, "password", "upload")

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
    attributes: dict[str, Any] | None

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
        self.sensor_id = get_attribute(config, "sensor_id", f"sensor[{index}]")
        self.sensor_code = get_attribute(
            config, "sensor_code", f"sensor[{index}]"
        )
        self.name = get_attribute(config, "name", f"sensor[{index}]")
        self.gpio = get_attribute(config, "gpio", f"sensor[{index}]")
        self.attributes = get_attribute(
            config, "attributes", f"sensor[{index}]", required=False
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
        upload (UploadConfig): The configured upload target.
        sensors (list[SensorConfig]): All configured sensors.
    """

    collector_id: str
    node_name: str
    polling_interval: int
    device: DeviceConfig
    upload: UploadConfig
    sensors: list[SensorConfig]

    def __init__(
        self,
        config: dict[str, Any],
        device: DeviceConfig,
        upload: UploadConfig,
        sensors: list[SensorConfig],
    ):
        """
        Initializes the config and ensures the required attributes are present.

        Args:
            config (dict[str, Any]): The config object, ie. the
                dictionary pulled from the config file.
        """
        self.collector_id = get_attribute(config, "collector_id", "config")
        self.node_name = get_attribute(config, "node_name", "config")
        self.polling_interval = get_attribute(
            config, "polling_interval", "config"
        )
        self.device = device
        self.upload = upload
        self.sensors = sensors

        # Validate that polling_interval is not negative
        if self.polling_interval < 0:
            raise ValueError("Cannot set a negative polling interval.")
