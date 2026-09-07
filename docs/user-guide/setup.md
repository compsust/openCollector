# Setup

This guide explains how to assemble a small openCollector deployment. openCollector is currently a research prototype, so validate the complete system before using it for unattended monitoring.

## Before You Begin

You will need:

- A computer capable of running QuestDB and the Python storage service.
- One or more collector devices, such as a Raspberry Pi Pico W, and supported sensors.
- Network connectivity from every collector to QuestDB's HTTP endpoint and from the storage service to QuestDB's PostgreSQL endpoint.
- [Git](https://git-scm.com/), [Python](https://www.python.org/) 3.13 or later, and the [uv package manager](https://docs.astral.sh/uv/getting-started/installation/) for a manual installation.
- Docker and an editor with Development Containers support if you use the repository's development container.

## Identify Devices

First decide which devices will host each service.

- **Collector** nodes may be deployed on any device capable of reading the sensors and reaching the database. The collector is designed to support MicroPython devices such as the Raspberry Pi Pico W.
- The **storage** node may run on any computer capable of hosting a Python web server. It may share a computer with QuestDB.
- **QuestDB** may run beside the storage node or on another host. Size that host for the required data retention, collector count, and sampling frequency.

See [Supported Sensors](./collector/sensors.md) before selecting hardware.

### Network Considerations

Collectors send data to QuestDB over HTTP, normally on port `9000`. The storage service reads QuestDB using the PostgreSQL wire protocol, normally on port `8812`, and serves the browser interface over HTTP, normally on port `8000`. If the components are on separate devices, use the database host's LAN address rather than `localhost` and allow only the required ports through the host firewall.

The browser and REST interfaces enforce HTTP Basic authentication by default, but Basic credentials are safe only when transported over HTTPS. Use the production Caddy configuration or another HTTPS reverse proxy before exposing the interface outside a trusted network. Keep QuestDB's ingestion port limited to intended collector networks.

## Deploy QuestDB and the Storage Node

The storage service creates the openCollector tables when it first starts and successfully connects to QuestDB. Start QuestDB before starting the storage service.

### Development Container (Recommended for Evaluation)

The repository includes a development Compose configuration that starts QuestDB and a Python development container together. It is intended for local development, not production deployment.

1. Clone `https://github.com/compsust/openCollector`.
2. Open the repository in an editor that supports [Development Containers](https://containers.dev/), then choose **Reopen in Container**. Docker starts both the `open-collector` and `database` services, and `uv sync` installs the Python dependencies.
3. Copy `storage/.env.example` to `storage/.env` and set `QUESTDB_HOST=database`, `QUESTDB_USER=pguser`, and `QUESTDB_PASSWORD=quest` to match `.devcontainer/docker-compose.yml`.
4. In the development-container terminal, start the storage service:

    ```bash
    cd /workspace/storage/src
    uv run litestar run --app app:app --host 0.0.0.0 --port 8000
    ```

5. Forward port `8000` in your editor and open `http://localhost:8000/dashboard`.

QuestDB's web console is available on port `9000`. Stop the Compose project when it is no longer needed. Database data is retained under `.devcontainer/data/`.

### Manual Installation on One Host

1. Install and start QuestDB using its [installation guide](https://questdb.com/docs/quick-start/). Configure an HTTP user for collectors and a PostgreSQL user for the storage service.
2. Clone the repository and install the storage dependencies:

    ```bash
    git clone https://github.com/compsust/openCollector.git
    cd openCollector/storage
    uv sync --active
    cp .env.example .env
    ```

3. Edit `.env`. For a database on the same host, use `QUESTDB_HOST=localhost`; set the PostgreSQL username and password to the values configured in QuestDB. See [Storage Config](./storage/config.md) for every setting.
4. Start the service from the source directory:

    ```bash
    cd src
    uv run litestar run --app app:app --host 0.0.0.0 --port 8000
    ```

5. Open `http://localhost:8000/dashboard`. On first startup, check the terminal for database connection or table-creation errors.

### Production Compose Deployment

The `deploy/compose.yaml` stack runs a pinned QuestDB release, the openCollector storage image, and Caddy as an HTTPS reverse proxy. It includes persistent volumes, health checks, restart policies, an unprivileged read-only storage container, and required credentials.

1. Point a DNS name at the server and allow inbound ports `80` and `443`. Keep port `9000` bound to loopback unless collectors must reach it; if they do, set `QUESTDB_BIND_ADDRESS` to the appropriate host address and restrict the port with a firewall.
2. Copy `deploy/.env.example` to `deploy/.env` and replace every example credential with a different long, randomly generated value. Set `DOMAIN` to the public DNS name.
3. Build and start the stack from the repository root:

    ```bash
    docker compose --env-file deploy/.env -f deploy/compose.yaml up -d --build
    docker compose --env-file deploy/.env -f deploy/compose.yaml ps
    ```

4. Open `https://YOUR_DOMAIN/dashboard` and enter `INTERFACE_USER` and `INTERFACE_PASSWORD`.
5. Back up the `questdb-data` Docker volume and the deployment `.env` through secure, access-controlled processes.

For a non-container storage deployment, `deploy/opencollector-storage.service` is a hardened systemd starting point. Adjust its paths and create `/etc/opencollector/storage.env` with permissions readable only by the service account.

### Separate Database and Storage Hosts

Install QuestDB on the database host and the storage service on the application host using the manual steps above. In `storage/.env`, set `QUESTDB_HOST` to the database host name or IP address. In each collector's `config.json`, set `upload.host` to that same reachable address and `upload.port` to QuestDB's HTTP port. Confirm connectivity to ports `8812` and `9000` before troubleshooting the application.

## Assemble Collectors

The wiring and physical placement depend on the deployment. The repository includes an optional PCB for connecting multiple sensors to a Raspberry Pi Pico W and a matching enclosure. See [PCB and Enclosure](./collector/pcb.md) and verify every connection against the sensor documentation before applying power.

## Configure Collectors

Copy `collector/src/config.example.json` to `collector/src/config.json`, assign unique collector and sensor UUIDs, enter the Wi-Fi and QuestDB connection details, and describe each attached sensor. See [Collector Config](./collector/config.md) for all properties and [Supported Sensors](./collector/sensors.md) for sensor-specific pins and attributes.

Do not commit `config.json`: it can contain Wi-Fi and database credentials.

## Deploy Collectors

Collector deployment uses the packaging and flashing scripts in `scripts/`.

1. Install a current MicroPython build on the target board using the board vendor's instructions.
2. Install the host tool with `python -m pip install mpremote`.
3. Connect one Pico W over USB and run `./scripts/flash_pico.sh collector/src/config.json`. Pass an `mpremote` device identifier as the second argument if auto-detection is ambiguous.
4. The script validates the configuration, creates `dist/pico.zip`, copies the collector and common packages plus a boot `main.py`, and resets the board.
5. Connect the sensors while the board is unpowered, then power the collector and monitor its serial output.
6. Confirm that the collector and sensors appear on the dashboard and become `OPERATIONAL`. See [Troubleshooting](./troubleshooting.md) if they do not.

The **Pico W package** workflow creates a downloadable package on changes to the collector. The manually dispatched **Pico W hardware-in-the-loop** workflow flashes a physically attached board and runs one sensor polling cycle. The HIL workflow requires a suitably labelled, secured self-hosted runner; it cannot run on GitHub-hosted hardware.
