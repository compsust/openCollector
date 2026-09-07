# Troubleshooting

Work from the database outward: first confirm QuestDB, then the storage service, network access, collector startup, and finally individual sensors. Record the exact command, timestamp, collector ID, sensor ID, and error message when asking for help.

## Database Problems

- Confirm QuestDB is running. For the production stack, run `docker compose --env-file deploy/.env -f deploy/compose.yaml ps` and inspect `docker compose --env-file deploy/.env -f deploy/compose.yaml logs database`.
- Use `QUESTDB_HOST=database` inside Compose; `localhost` inside the storage container refers to that container, not QuestDB.
- Match the storage service's PostgreSQL credentials and port `8812` to QuestDB's `QDB_PG_USER` and `QDB_PG_PASSWORD`.
- For collector uploads, match `upload.user` and `upload.password` to QuestDB's separate `QDB_HTTP_USER` and `QDB_HTTP_PASSWORD` and confirm port `9000` is reachable only from intended collector networks.

## Wi-Fi Problems

- Recheck `ssid_name` and `ssid_password`, including capitalization and spaces. Do not commit these values.
- Confirm the access point offers a compatible 2.4 GHz network for the Pico W.
- Attach a serial console during boot and look for association, DHCP, DNS, or timeout errors.
- Test near the access point and use the database host's IP address temporarily to distinguish DNS failure from general connectivity failure.

## Sensor Problems

- Disconnect power before changing wiring. Verify voltage, ground, connector orientation, and every GPIO against the exact module datasheet.
- Ensure `sensor_code`, GPIO names, baud rate, and other attributes match the [sensor guide](./collector/sensors.md).
- Test one sensor at a time with a short cable. Check placement, airflow, warm-up time, condensation, sunlight, and calibration against a reference instrument.
- An `ERROR` status means the latest sensor event was an exception. Open its detail page and compare the error timestamp with serial output.

## Status Problems

- `UNKNOWN`: no record or error has reached the database. Check startup, metadata upload, IDs, and database credentials.
- `DROPPED`: the newest event is older than `polling_interval × ACTIVE_DEVICE_POLLING_THRESHOLD`. Check power and networking; increase the threshold only if healthy uploads are occasionally slow.
- `ERROR`: the latest error is newer than the latest record. Fix the reported cause; a newer valid record returns the sensor to `OPERATIONAL`.
- `OPERATIONAL` with implausible data: status indicates recent software activity, not accuracy. Check clock, units, placement, and calibration.

## Authentication and TLS Problems

- A `401 Authentication required` response means the HTTP Basic credentials are missing or incorrect. Use `INTERFACE_USER` and `INTERFACE_PASSWORD`, not QuestDB credentials.
- Browsers cache Basic credentials. Close every window for the site or use a private window after changing a password.
- A `502` from Caddy usually means the storage container is unhealthy. Check `/health` and the storage logs.
- Certificate issuance requires `DOMAIN` to resolve to the server and inbound ports `80` and `443` to reach Caddy.

## Pico Packaging and Hardware Tests

- Install `mpremote`, connect one Pico W, and run `./scripts/flash_pico.sh path/to/config.json`.
- If the device is not found, run `mpremote connect list` and pass its device identifier as the second argument.
- The HIL workflow needs a physically secured self-hosted runner labelled `self-hosted`, `micropython`, and `pico-w`, plus a `PICO_CONFIG_JSON` repository secret.
