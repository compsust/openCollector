# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import base64
import unittest
from unittest.mock import patch

from auth import BasicAuthMiddleware


class BasicAuthTests(unittest.IsolatedAsyncioTestCase):
    async def request(self, authorization=None, path="/dashboard"):
        called = False
        messages = []

        async def application(scope, receive, send):
            nonlocal called
            called = True

        headers = []
        if authorization:
            headers.append((b"authorization", authorization.encode()))
        scope = {"type": "http", "path": path, "headers": headers}

        async def receive():
            return {"type": "http.request"}

        async def send(message):
            messages.append(message)

        with (
            patch("auth.config.AUTH_ENABLED", True),
            patch("auth.config.INTERFACE_USER", "admin"),
            patch("auth.config.INTERFACE_PASSWORD", "correct horse"),
        ):
            await BasicAuthMiddleware(application)(scope, receive, send)
        return called, messages

    async def test_rejects_missing_credentials(self):
        called, messages = await self.request()
        self.assertFalse(called)
        self.assertEqual(messages[0]["status"], 401)

    async def test_rejects_malformed_credentials(self):
        called, messages = await self.request("Basic not-base64")
        self.assertFalse(called)
        self.assertEqual(messages[0]["status"], 401)

    async def test_accepts_valid_credentials(self):
        token = base64.b64encode(b"admin:correct horse").decode()
        called, _ = await self.request(f"Basic {token}")
        self.assertTrue(called)

    async def test_health_is_public(self):
        called, _ = await self.request(path="/health")
        self.assertTrue(called)


if __name__ == "__main__":
    unittest.main()
