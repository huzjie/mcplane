"""Stateless request context.

A StatelessContext bundles everything needed to route and correlate a single
request without any server-side session. It is reconstructed per-request from
headers, making every request independently servable behind a load balancer.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .headers import MCP_DEFAULT_PROTOCOL


@dataclass
class StatelessContext:
    method: Optional[str] = None
    server_name: Optional[str] = None
    protocol_version: str = MCP_DEFAULT_PROTOCOL
    trace_id: Optional[str] = None
    idempotency_key: Optional[str] = None
    auth_token: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    @classmethod
    def from_headers(cls, headers: Dict[str, str]) -> "StatelessContext":
        """Build a context from a case-insensitive header mapping."""
        lookup = {k.lower(): v for k, v in headers.items()}

        def _get(name):
            return lookup.get(name.lower())

        return cls(
            method=_get("Mcp-Method"),
            server_name=_get("Mcp-Name"),
            protocol_version=_get("Mcp-Protocol-Version") or MCP_DEFAULT_PROTOCOL,
            trace_id=_get("X-Trace-Id"),
            idempotency_key=_get("Idempotency-Key"),
            auth_token=_get("Authorization"),
        )
