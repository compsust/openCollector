# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import os
import tempfile
import unittest
from pathlib import Path

from src.config import ConfigManager
from src.datastructures import CollectorRecord
from src.upload import UploadManager


class CollectorConfigTests(unittest.TestCase):
    def test_parses_each_sensor_in_the_configuration(self):
        config = {
            "collector_id": "collector-1",
            "node_name": "Test collector",
            "polling_interval": 1000,
            "device": {"model": "test", "requires_micropython": False},
            "upload": {
                "host": "localhost",
                "port": 9000,
                "user": "node",
                "password": "secret",
            },
            "sensors": [
                {
                    "sensor_id": "sensor-1",
                    "sensor_code": "MOCK",
                    "name": "Mock sensor",
                    "gpio": {},
                }
            ],
        }

        original_directory = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "config.json").write_text(json.dumps(config))
            try:
                os.chdir(directory)
                manager = ConfigManager(False)
            finally:
                os.chdir(original_directory)

        self.assertEqual(len(manager.config.sensors), 1)
        self.assertEqual(manager.config.sensors[0].sensor_id, "sensor-1")


class UploadFormattingTests(unittest.TestCase):
    def test_serializes_every_measurement_in_a_record(self):
        manager = UploadManager.__new__(UploadManager)
        manager.collector_id = "collector-1"
        record = CollectorRecord(
            sensor_id="sensor-1",
            data={"temperature": 21.5, "humidity": 45},
            timestamp=123456,
        )

        csv = manager._construct_records([record])["data"][1]

        self.assertIn("123456,collector-1,sensor-1,temperature,21.5", csv)
        self.assertIn("123456,collector-1,sensor-1,humidity,45", csv)


if __name__ == "__main__":
    unittest.main()
