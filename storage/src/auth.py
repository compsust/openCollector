# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""HTTP Basic authentication for the browser and REST interfaces."""

import base64
import binascii
import hmac

import config
from litestar.types import ASGIApp, Receive, Scope, Send


class BasicAuthMiddleware:
    """Protect HTTP endpoints with credentials configured in the environment."""

    public_paths = {"/health"}

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        path = str(scope.get("path", ""))
        if (
            scope["type"] != "http"
            or not config.AUTH_ENABLED
            or path in self.public_paths
            or path.startswith("/static/")
        ):
            await self.app(scope, receive, send)
            return

        supplied_username, supplied_password = self._credentials(scope)
        valid = hmac.compare_digest(supplied_username, config.INTERFACE_USER)
        valid &= hmac.compare_digest(supplied_password, config.INTERFACE_PASSWORD)
        if valid:
            await self.app(scope, receive, send)
            return

        body = b"Authentication required"
        await send(
            {
                "type": "http.response.start",
                "status": 401,
                "headers": [
                    (b"content-type", b"text/plain; charset=utf-8"),
                    (b"content-length", str(len(body)).encode("ascii")),
                    (
                        b"www-authenticate",
                        b'Basic realm="openCollector", charset="UTF-8"',
                    ),
                    (b"cache-control", b"no-store"),
                ],
            }
        )
        await send({"type": "http.response.body", "body": body})

    @staticmethod
    def _credentials(scope: Scope) -> tuple[str, str]:
        authorization = next(
            (
                value.decode("latin-1")
                for key, value in scope.get("headers", [])
                if key.lower() == b"authorization"
            ),
            "",
        )
        scheme, _, encoded = authorization.partition(" ")
        if scheme.lower() != "basic" or not encoded:
            return "", ""
        try:
            decoded = base64.b64decode(encoded, validate=True).decode("utf-8")
        except (binascii.Error, UnicodeDecodeError):
            return "", ""
        username, separator, password = decoded.partition(":")
        return (username, password) if separator else ("", "")
