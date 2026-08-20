"""Asynchronous mcplane client (asyncio + stdlib http client in executor)."""

import asyncio
import json
import urllib.error
import urllib.request

from ..errors import UpstreamError, TimeoutError
from ..spec.headers import (
    HEADER_METHOD,
    HEADER_NAME,
    HEADER_PROTOCOL_VERSION,
    HEADER_AUTHORIZATION,
)


class AsyncMcplaneClient:
    def __init__(self, base_url: str, token: str = None, timeout_s: int = 60):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout_s = timeout_s

    async def _request(self, server_name: str, method: str, params: dict):
        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        return await asyncio.get_event_loop().run_in_executor(
            None, self._sync_request, server_name, method, payload
        )

    def _sync_request(self, server_name, method, payload):
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.base_url + "/mcp", data=body, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header(HEADER_METHOD, method)
        req.add_header(HEADER_NAME, server_name)
        req.add_header(HEADER_PROTOCOL_VERSION, "2026-07-28")
        if self.token:
            req.add_header(HEADER_AUTHORIZATION, "Bearer " + self.token)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            raise UpstreamError("HTTP %s" % exc.code)
        except (urllib.error.URLError, TimeoutError) as exc:
            raise TimeoutError("request failed: %s" % exc)

    async def list_tools(self, server_name: str):
        return await self._request(server_name, "tools/list", {})

    async def call_tool(self, server_name: str, tool: str, arguments: dict):
        return await self._request(
            server_name, "tools/call", {"name": tool, "arguments": arguments}
        )

    async def ping(self, server_name: str):
        return await self._request(server_name, "ping", {})
