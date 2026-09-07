# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unittest
from pathlib import Path
from types import SimpleNamespace

from jinja2 import Environment, FileSystemLoader, StrictUndefined


class TemplateTests(unittest.TestCase):
    def setUp(self):
        templates = Path(__file__).resolve().parents[1] / "src" / "templates"
        self.environment = Environment(
            loader=FileSystemLoader(templates), undefined=StrictUndefined
        )
        self.environment.globals["url_for"] = (
            lambda name, file_path: f"/static/{file_path}"
        )

    def test_all_templates_compile(self):
        for template_name in self.environment.list_templates():
            with self.subTest(template=template_name):
                self.environment.get_template(template_name)

    def test_collector_detail_page_renders(self):
        record = SimpleNamespace(record_name="Temperature", value=21.5, unit="°C")
        sensor = SimpleNamespace(
            id="sensor-1",
            name="Greenhouse sensor",
            status="Operational",
            last_value=[record],
        )
        collector = SimpleNamespace(
            id="collector-1",
            name="Greenhouse collector",
            device_model="Raspberry Pi Pico W",
            polling_interval=1000,
            total_records=1,
            total_errors=0,
            sensors=[sensor],
            errors=[],
        )

        html = self.environment.get_template("collector.html").render(
            collector=collector, title="openCollector"
        )

        self.assertIn("Greenhouse collector", html)
        self.assertIn("Greenhouse sensor", html)

    def test_sensor_detail_page_renders(self):
        record = SimpleNamespace(
            timestamp="2026-09-07 12:00:00",
            record_name="Temperature",
            value=21.5,
            unit="°C",
        )
        sensor = SimpleNamespace(
            name="Greenhouse sensor",
            code="DHT20",
            status="Operational",
            total_records=1,
            total_errors=0,
            records=[record],
            errors=[],
        )

        html = self.environment.get_template("sensor.html").render(
            sensor=sensor, collector_id="collector-1", title="openCollector"
        )

        self.assertIn("Greenhouse sensor", html)
        self.assertIn("21.5", html)


if __name__ == "__main__":
    unittest.main()
