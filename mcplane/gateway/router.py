"""Header-based routing for the stateless gateway.

Routes each request to an upstream server by the ``Mcp-Name`` header. Falls
back to a method-based router for servers not using name-based routing.
"""

import threading
from typing import Dict, Optional

from ..errors import NotFoundError
from ..registry.server_registry import ServerRegistry, ServerRecord


class HeaderRouter:
    def __init__(self, registry: ServerRegistry):
        self.registry = registry
        self._lock = threading.Lock()
        self._rr_counter = 0

    def resolve(self, server_name: Optional[str]) -> Optional[ServerRecord]:
        if server_name:
            rec = self.registry.get(server_name)
            if rec and rec.enabled:
                return rec
            raise NotFoundError("unknown MCP server: %s" % server_name)
        # No Mcp-Name header: route to the first enabled server (or None).
        enabled = self.registry.list_enabled()
        return enabled[0] if enabled else None

    def resolve_many(self, server_name: Optional[str]):
        if server_name:
            rec = self.registry.get(server_name)
            if not rec:
                raise NotFoundError("unknown MCP server: %s" % server_name)
            return [rec]
        return self.registry.list_enabled()

    def next_by_round_robin(self) -> Optional[ServerRecord]:
        enabled = self.registry.list_enabled()
        if not enabled:
            return None
        with self._lock:
            idx = self._rr_counter % len(enabled)
            self._rr_counter += 1
        return enabled[idx]
