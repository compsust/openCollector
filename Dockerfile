# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

FROM ghcr.io/astral-sh/uv:0.8.22 AS uv

FROM python:3.13-slim AS builder
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /app
COPY common ./common
COPY storage/pyproject.toml storage/uv.lock ./storage/
WORKDIR /app/storage
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.13-slim AS runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/app/storage/.venv/bin:$PATH
RUN useradd --create-home --uid 10001 opencollector
WORKDIR /app
COPY --from=builder /app/storage/.venv ./storage/.venv
COPY common ./common
COPY storage/src ./storage/src
WORKDIR /app/storage/src
USER opencollector
EXPOSE 8000
CMD ["litestar", "run", "--app", "app:app", "--host", "0.0.0.0", "--port", "8000"]
