#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Build a Pico-ready directory and zip archive from a collector config."""

import argparse
import json
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", default=Path("dist/pico"), type=Path)
    args = parser.parse_args()

    repository = Path(__file__).resolve().parents[1]
    with args.config.open(encoding="utf-8") as config_file:
        config = json.load(config_file)
    required = {"collector_id", "polling_interval", "device", "upload", "sensors"}
    missing = sorted(required.difference(config))
    if missing:
        raise SystemExit(f"Collector config is missing: {', '.join(missing)}")

    output = args.output.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "config.json")
    shutil.copytree(
        repository / "collector" / "src", output / "collector_app", ignore=ignore
    )
    shutil.copytree(
        repository / "common" / "src" / "common", output / "common", ignore=ignore
    )
    shutil.copy2(args.config, output / "config.json")
    (output / "main.py").write_text(
        "from collector_app.main import main\n\nmain()\n", encoding="utf-8"
    )
    archive = shutil.make_archive(str(output), "zip", root_dir=output)
    print(f"Created {archive}")


if __name__ == "__main__":
    main()
