"""Synchronous mcplane client using the stateless MCP transport.

Every method issues an independent HTTP request with routing headers; there is
no persistent session object held by the client beyond the base URL and auth
token.
"""

import json
import urllib.error
import urllib.request

from ..errors import UpstreamError, TimeoutError
from ..spec.headers import (
    HEADER_METHOD,
    HEADER_NAME,
    HEADER_PROTOCOL_VERSION,
    HEADER_AUTHORIZATION,
    HEADER_IDEMPOTENCY_KEY,
)


class McplaneClient:
    def __init__(self, base_url: str, token: str = None, timeout_s: int = 60):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout_s = timeout_s

    def _request(self, server_name: str, method: str, params: dict,
                 idempotency_key: str = None):
        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.base_url + "/mcp", data=body, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        req.add_header(HEADER_METHOD, method)
        req.add_header(HEADER_NAME, server_name)
        req.add_header(HEADER_PROTOCOL_VERSION, "2026-07-28")
        if self.token:
            req.add_header(HEADER_AUTHORIZATION, "Bearer " + self.token)
        if idempotency_key:
            req.add_header(HEADER_IDEMPOTENCY_KEY, idempotency_key)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:500]
            raise UpstreamError("HTTP %s: %s" % (exc.code, detail))
        except (urllib.error.URLError, TimeoutError) as exc:
            raise TimeoutError("request failed: %s" % exc)

    def list_tools(self, server_name: str):
        return self._request(server_name, "tools/list", {})

    def call_tool(self, server_name: str, tool: str, arguments: dict,
                  token: str = None, idempotency_key: str = None):
        if token:
            self.token = token
        return self._request(
            server_name, "tools/call",
            {"name": tool, "arguments": arguments},
            idempotency_key=idempotency_key,
        )

    def list_prompts(self, server_name: str):
        return self._request(server_name, "prompts/list", {})

    def list_resources(self, server_name: str):
        return self._request(server_name, "resources/list", {})

    def ping(self, server_name: str):
        return self._request(server_name, "ping", {})
