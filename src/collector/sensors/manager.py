from collector.datastructures import SensorConfig, TargetConfig, SensorReport


class SensorManager:

    def __init__(
        self, sensors: list[SensorConfig], targets: list[TargetConfig]
    ) -> None:
        """
        Initializes all SensorDrivers.
        """
        raise NotImplementedError

    def poll() -> SensorReport:
        """
        Polls all sensors.

        Returns:
            SensorReport: An object containing all recorded sensor
                data and caught sensor exceptions.
        """
        raise NotImplementedError
