from typing import Any

from common import SensorCodeEnum
from .utils import get_attribute


class DeviceConfig:
    """
    Configuration object which describes a type of device
    that the collector node runs on.

    Attributes:
        model: A string representing the type of device,
            for example "Raspberry Pi 3."
        requires_micropython: If true, the program will
            not enable a start unless it is being run in a
            micropython environment.
    """

    model: str
    requires_micropython: bool

    def __init__(self, config: dict[str, Any], micropython: bool):
        """
        Initializes the config and ensures the required attributes are present.

        Args:
            config: The device config object, ie. the
                dictionary contained within the "device" key in the config file.
            micropython: Whether the current environment is micropython
        """
        self.model = get_attribute(config, "model", "device")
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
        host: The database URL.
        port: The database port.
        user: The database username.
        password: The database password.
    """

    host: str
    port: str
    user: str
    password: str

    def __init__(self, config: dict[str, Any]):
        """
        Initializes the config and ensures the required attributes are present.

        Args:
            config: The upload config object, ie. the
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
        sensor_id: An ID associated with the sensor.
        sensor_code: Associated with
            a specific implementation of AbstractSensorDriver.
        name: A descriptive name for the sensor.
        gpio: A dictionary where the values are
            GPIO pins which the sensor requires use of, and
            the keys are string identifiers. Used to validate
            that the configured GPIO pins match the allowed_gpio
            attribute of the device config.
        attributes: Any other attributes
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
    ):
        """
        Initializes the config and ensures the required attributes are present.

        Args:
            config: The sensor config object, ie. a
                dictionary contained within the "sensors" array in the config file.
            index: The index of the sensor config within the "sensors" array.
            allowed_gpio: The allowed GPIO pins as configured in the device config.
        """
        self.sensor_id = get_attribute(config, "sensor_id", f"sensor[{index}]")
        self.sensor_code = SensorCodeEnum[
            get_attribute(config, "sensor_code", f"sensor[{index}]")
        ]
        self.name = get_attribute(config, "name", f"sensor[{index}]")
        self.gpio = get_attribute(config, "gpio", f"sensor[{index}]")
        self.attributes = get_attribute(
            config, "attributes", f"sensor[{index}]", required=False
        )


class CollectorConfig:
    """
    Configuration object which describes the collector node device.

    Attributes:
        collector_id: An ID associated with the node.
        node_name: A name associated with the node.
        ssid_name: If defined, the device will attempt to connect
            to this SSID.
        ssid_password: If defined, the device will attempt to connect
            to this SSID.
        polling_interval: The number of miliseconds to wait
            between sensor polls. Must not be negative.
        device: The device config.
        upload: The configured upload target.
        sensors: All configured sensors.
    """

    collector_id: str
    node_name: str
    polling_interval: int
    ssid_name: str | None
    ssid_password: str | None
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
            config: The config object, ie. the
                dictionary pulled from the config file.
            device: The parsed device config.
            upload: The parsed upload config.
            sensors: The parsed sensor configs.

        Raises:
            ValueError: Raised if the polling interval is a negative number.
        """
        self.collector_id = get_attribute(config, "collector_id", "config")
        self.node_name = get_attribute(config, "node_name", "config")
        self.polling_interval = get_attribute(config, "polling_interval", "config")
        self.ssid_name = get_attribute(config, "ssid_name", "config", required=False)
        self.ssid_password = get_attribute(
            config, "ssid_password", "config", required=False
        )
        self.device = device
        self.upload = upload
        self.sensors = sensors

        # Validate that polling_interval is not negative.
        if self.polling_interval < 0:
            raise ValueError("Cannot set a negative polling interval.")
