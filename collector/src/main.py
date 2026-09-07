try:
    import micropython as _micropython  # noqa: F401

    IS_MICROPYTHON = True
except ImportError:
    IS_MICROPYTHON = False

import time

from .config import ConfigManager
from .datastructures import CollectorReport
from .sensors import SensorManager
from .upload import UploadManager


def connect_wifi(config, timeout_seconds=30):
    """Connect a MicroPython collector to its configured wireless network."""
    if not IS_MICROPYTHON or not config.ssid_name:
        return

    import network

    station = network.WLAN(network.STA_IF)
    station.active(True)
    if station.isconnected():
        return

    station.connect(config.ssid_name, config.ssid_password)
    started = time.time()
    while not station.isconnected():
        if time.time() - started >= timeout_seconds:
            raise RuntimeError("Timed out connecting to Wi-Fi")
        time.sleep(0.25)


def run(
    config_manager, sensor_manager, upload_manager, max_cycles=None, sleep_fn=time.sleep
):
    """Poll and upload repeatedly; ``max_cycles`` allows deterministic tests."""
    collector_metadata, sensor_metadata = config_manager.metadata
    upload_manager.upload_metadata(collector_metadata, sensor_metadata)

    cycles = 0
    while max_cycles is None or cycles < max_cycles:
        records, errors = sensor_manager.poll()
        report = CollectorReport(
            collector_id=config_manager.config.collector_id,
            records=records,
            errors=errors,
        )

        # Delivery is best-effort and at-most-once. Failed reports are logged,
        # not buffered or retried, and the next polling cycle still runs.
        try:
            upload_manager.upload(report)
        except Exception as error:
            print(error)

        cycles += 1
        if max_cycles is None or cycles < max_cycles:
            # polling_interval is configured in milliseconds.
            sleep_fn(config_manager.config.polling_interval / 1000)


def main():
    """
    Main function where the program execution begins.
    """

    # Initialize manager classes
    config_manager = ConfigManager(IS_MICROPYTHON)
    connect_wifi(config_manager.config)
    sensor_manager = SensorManager(config_manager)
    upload_manager = UploadManager(config_manager)
    run(config_manager, sensor_manager, upload_manager)


if __name__ == "__main__":
    # Run the main function
    main()
