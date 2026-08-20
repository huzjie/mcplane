"""Stateless upstream proxy using the stdlib HTTP client.

Forwards JSON-RPC requests to upstream MCP servers over HTTP without
maintaining any server-side session. Supports timeout, idempotency key
propagation, and trace-id forwarding.
"""

import json
import urllib.error
import urllib.request
from typing import Dict, Optional

from ..errors import UpstreamError, TimeoutError
from ..spec.headers import HEADER_IDEMPOTENCY_KEY, HEADER_TRACE_ID, HEADER_AUTHORIZATION


class StatelessProxy:
    def __init__(self, timeout_s: int = 60):
        self.timeout_s = timeout_s

    def forward(self, url: str, method: str, payload: Dict,
                headers: Optional[Dict[str, str]] = None) -> Dict:
        """POST ``payload`` to ``url`` and return the parsed JSON body."""
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        for key, value in (headers or {}).items():
            if value:
                req.add_header(key, value)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:500]
            raise UpstreamError(
                "upstream HTTP %s: %s" % (exc.code, detail)
            )
        except (urllib.error.URLError, TimeoutError) as exc:
            raise TimeoutError("upstream unreachable: %s" % exc)
