# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unittest
from contextlib import redirect_stdout
from io import StringIO
from types import SimpleNamespace

from src.main import run


class FakeSensorManager:
    def __init__(self):
        self.poll_count = 0

    def poll(self):
        self.poll_count += 1
        return [], []


class FakeUploadManager:
    def __init__(self, fail_on_upload=None):
        self.fail_on_upload = fail_on_upload
        self.metadata_count = 0
        self.reports = []

    def upload_metadata(self, collector, sensors):
        self.metadata_count += 1

    def upload(self, report):
        self.reports.append(report)
        if len(self.reports) == self.fail_on_upload:
            raise OSError("network unavailable")


class CollectorLoopTests(unittest.TestCase):
    def test_runs_requested_cycles_and_converts_milliseconds(self):
        config = SimpleNamespace(collector_id="collector", polling_interval=250)
        config_manager = SimpleNamespace(config=config, metadata=(object(), []))
        sensor_manager = FakeSensorManager()
        upload_manager = FakeUploadManager()
        sleeps = []

        run(
            config_manager,
            sensor_manager,
            upload_manager,
            max_cycles=3,
            sleep_fn=sleeps.append,
        )

        self.assertEqual(sensor_manager.poll_count, 3)
        self.assertEqual(len(upload_manager.reports), 3)
        self.assertEqual(upload_manager.metadata_count, 1)
        self.assertEqual(sleeps, [0.25, 0.25])

    def test_upload_failure_does_not_stop_later_polling_cycles(self):
        config = SimpleNamespace(collector_id="collector", polling_interval=1000)
        config_manager = SimpleNamespace(config=config, metadata=(object(), []))
        sensor_manager = FakeSensorManager()
        upload_manager = FakeUploadManager(fail_on_upload=1)

        with redirect_stdout(StringIO()):
            run(
                config_manager,
                sensor_manager,
                upload_manager,
                max_cycles=2,
                sleep_fn=lambda _: None,
            )

        self.assertEqual(sensor_manager.poll_count, 2)
        self.assertEqual(len(upload_manager.reports), 2)


if __name__ == "__main__":
    unittest.main()
