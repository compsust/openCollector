# Usage

This page explains how to monitor an OpenCollector deployment through the browser and REST interfaces.

## Data Display

### Data Types

OpenCollector stores two categories of information from a collector:

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

Sensor errors occur while reading a sensor. Collector errors occur during initialization, upload, or other collector-level work. When an upload fails, the collector attempts to retain the error for a later successful upload; an active network failure can therefore delay the error appearing in the interface.

Record retry and durable offline buffering are not yet complete. A collector interruption or extended network outage may result in missing readings, so do not rely on the prototype as the only copy of safety-critical data.

## Web Interface

Start the storage service, then open its address in a browser (for a local default deployment, `http://localhost:8000`). The navigation bar links to the home page, dashboard, login placeholder, and project information.

### Authentication

Authentication is not implemented in the current browser interface. The `/login` route is a placeholder, and the `INTERFACE_USER` and `INTERFACE_PASSWORD` configuration values are not enforced. Keep the interface on a trusted network or protect it with an authenticated HTTPS reverse proxy.

### Dashboard

Open `/dashboard` to see the deployment overview. The summary reports total collectors, sensors, records, and errors. The collector list shows each sensor's current status and latest values.

To graph a measurement:

1. Select a collector.
2. Select one of its sensors.
3. Select the record type to plot.
4. Use the refresh button to pause or resume automatic graph updates. Pause updates before zooming or inspecting the graph so a refresh does not replace the current view.

The page refresh interval is controlled by `INTERFACE_REFRESH_SECONDS` in the storage configuration. An empty selector usually means metadata for that collector or sensor has not reached the database yet.

### Collector Page

Collector detail routes use `/collectors/{collector_id}`. The route exists, but its page is not implemented in the current prototype. Use the dashboard or REST API for collector information.

### Sensor Page

Sensor detail routes use `/collectors/{collector_id}/sensors/{sensor_id}`. The route exists, but its page is not implemented in the current prototype. Use the dashboard graph or REST API for sensor information.

## REST API

The storage service exposes a read-only JSON API under `/api/query`. The generated OpenAPI schema is also included in this documentation under [OpenAPI](./storage/openapi.md).

### Authentication

The REST API does not currently enforce authentication. Apply the same network restrictions or reverse-proxy authentication used for the browser interface.

### Endpoints

- `GET /api/query/summary` returns totals and status information for the deployment.
- `GET /api/query/collectors/{collector_id}` returns collector details. Supply `errors_page` and `errors_page_size` query parameters.
- `GET /api/query/collectors/sensors/{sensor_id}` returns sensor records and errors. Supply `records_page`, `records_page_size`, `errors_page`, and `errors_page_size` query parameters.

For example:

```bash
curl "http://localhost:8000/api/query/summary"
```

```bash
curl "http://localhost:8000/api/query/collectors/COLLECTOR_ID?errors_page=1&errors_page_size=25"
```

Use IDs from the collector configuration or a previous API response. Pagination values must be positive integers. API routes under `/api/command` are reserved for future functionality and currently expose no operations.
