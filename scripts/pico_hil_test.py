# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""One-cycle smoke test executed on a connected MicroPython device."""

from collector_app.config import ConfigManager
from collector_app.sensors import SensorManager

config_manager = ConfigManager(True)
sensor_manager = SensorManager(config_manager)
records, errors = sensor_manager.poll()
assert config_manager.config.sensors, "HIL config must include at least one sensor"
assert records or errors, (
    "Every configured sensor must return a record or a captured error"
)
print("HIL_OK", len(records), len(errors))
