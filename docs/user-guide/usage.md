# Usage

This page explains how to monitor an openCollector deployment through the browser and REST interfaces.

## Data Display

### Data Types

openCollector stores two categories of information from a collector:

1. **Records** are numerical readings measured by a sensor. A single sensor can produce several record types, such as temperature and humidity.
2. **Errors** describe exceptions raised while initializing or reading a sensor, or while the collector performs other work.

### Node Status

Status gives a quick indication of a collector or sensor's recent activity:

1. White — `UNKNOWN`: no records or errors have been received.
2. Yellow — `DROPPED`: no recent records or errors have arrived. The timeout is the collector's `polling_interval` multiplied by the storage node's `ACTIVE_DEVICE_POLLING_THRESHOLD`.
3. Red — `ERROR`: the most recent event is an error rather than a numerical record.
4. Green — `OPERATIONAL`: numerical data has arrived more recently than an error.

A collector's status is derived from its own errors and the status of its sensors. Use the status as a prompt to investigate, not as proof that every reading is accurate. See [Storage Config](./storage/config.md#data-display) to change the dropped-device threshold.

### Errors

Sensor errors occur while reading a sensor. The current collector provides best-effort, at-most-once delivery: each report is submitted once during its polling cycle. If an upload fails, the exception is printed locally and polling continues. The failed report is neither buffered nor retried, so measurements produced during a communication failure are permanently absent from QuestDB. Sensor polling errors can be stored when communication is available, but communication failures themselves are not persisted remotely.

Durable offline buffering and bounded retry are future work. Do not rely on this research prototype as the only copy of safety-critical data.

## Web Interface

Start the storage service, then open its address in a browser (for a local default deployment, `http://localhost:8000`). The navigation bar links to the home page, dashboard, authentication information, and project information.

### Authentication

Browser and REST routes use HTTP Basic authentication when `AUTH_ENABLED=true`, which is the default. Enter `INTERFACE_USER` and `INTERFACE_PASSWORD` when prompted. Basic authentication does not encrypt traffic, so production deployments must use HTTPS. The production Compose configuration includes Caddy for TLS termination.

### Dashboard

Open `/dashboard` to see the deployment overview. The summary reports total collectors, sensors, records, and errors. The collector list shows each sensor's current status and latest values.

To graph a measurement:

1. Select a collector.
2. Select one of its sensors.
3. Select the record type to plot.
4. Use the refresh button to pause or resume automatic graph updates. Pause updates before zooming or inspecting the graph so a refresh does not replace the current view.

The page refresh interval is controlled by `INTERFACE_REFRESH_SECONDS` in the storage configuration. An empty selector usually means metadata for that collector or sensor has not reached the database yet.

### Collector Page

Select a collector name on the dashboard, or open `/collectors/{collector_id}`, to view device metadata, totals, latest sensor values, sensor status, and recent errors. Select a sensor card to open its detail page.

### Sensor Page

Open `/collectors/{collector_id}/sensors/{sensor_id}` to view the sensor type, current status, recent records, and recent errors. The page displays the first 100 records and 50 errors returned by the detail query.

## REST API

The storage service exposes a read-only JSON API under `/api/query`. The generated OpenAPI schema is also included in this documentation under [OpenAPI](./storage/openapi.md).

### Authentication

The REST API uses the same HTTP Basic credentials as the browser. Always use HTTPS outside a trusted local network.

### Endpoints

- `GET /api/query/summary` returns totals and status information for the deployment.
- `GET /api/query/collectors/{collector_id}` returns collector details. Supply `errors_page` and `errors_page_size` query parameters.
- `GET /api/query/collectors/sensors/{sensor_id}` returns sensor records and errors. Supply `records_page`, `records_page_size`, `errors_page`, and `errors_page_size` query parameters.

For example:

```bash
curl --user "admin:YOUR_PASSWORD" "http://localhost:8000/api/query/summary"
```

```bash
curl --user "admin:YOUR_PASSWORD" "http://localhost:8000/api/query/collectors/COLLECTOR_ID?errors_page=1&errors_page_size=25"
```

Use IDs from the collector configuration or a previous API response. Pagination values must be positive integers. API routes under `/api/command` are reserved for future functionality and currently expose no operations.
