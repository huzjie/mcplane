"""HTTP header definitions for the stateless MCP transport.

In the 2026-07-28 stateless spec, routing and correlation metadata moved out of
the session into standard HTTP headers. These constants define the canonical
header names used by the gateway for header-based routing and idempotency.
"""

# Request routing (required by stateless spec for streamable HTTP).
HEADER_METHOD = "Mcp-Method"
HEADER_NAME = "Mcp-Name"
HEADER_PROTOCOL_VERSION = "Mcp-Protocol-Version"

# Deprecated in the stateless spec but still accepted for backward compat.
HEADER_SESSION_ID = "Mcp-Session-Id"

# Standard auth / correlation headers.
HEADER_AUTHORIZATION = "Authorization"
HEADER_IDEMPOTENCY_KEY = "Idempotency-Key"
HEADER_TRACE_ID = "X-Trace-Id"

DEPRECATED_HEADERS = frozenset({HEADER_SESSION_ID})


class StatelessHeaders:
    """Convenience wrapper for reading/writing stateless MCP headers."""

    def __init__(self, method=None, name=None, protocol_version=None,
                 authorization=None, idempotency_key=None, trace_id=None):
        self.method = method
        self.name = name
        self.protocol_version = protocol_version or MCP_DEFAULT_PROTOCOL
        self.authorization = authorization
        self.idempotency_key = idempotency_key
        self.trace_id = trace_id

    def to_dict(self):
        out = {HEADER_PROTOCOL_VERSION: self.protocol_version}
        if self.method:
            out[HEADER_METHOD] = self.method
        if self.name:
            out[HEADER_NAME] = self.name
        if self.authorization:
            out[HEADER_AUTHORIZATION] = self.authorization
        if self.idempotency_key:
            out[HEADER_IDEMPOTENCY_KEY] = self.idempotency_key
        if self.trace_id:
            out[HEADER_TRACE_ID] = self.trace_id
        return out


MCP_DEFAULT_PROTOCOL = "2026-07-28"
