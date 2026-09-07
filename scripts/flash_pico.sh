#!/usr/bin/env sh
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -eu

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: $0 CONFIG_JSON [MPREMOTE_DEVICE]" >&2
  exit 2
fi

config_path=$1
device=${2:-auto}
repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
package_dir="$repo_dir/dist/pico"

python3 "$repo_dir/scripts/package_pico.py" --config "$config_path" --output "$package_dir"
mpremote connect "$device" fs cp -r "$package_dir"/collector_app :
mpremote connect "$device" fs cp -r "$package_dir"/common :
mpremote connect "$device" fs cp "$package_dir/config.json" :config.json
mpremote connect "$device" fs cp "$package_dir/main.py" :main.py
mpremote connect "$device" reset
echo "Flashed openCollector to $device"
