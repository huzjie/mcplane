"""In-memory server registry backed by SQLite (optional persistence)."""

import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ..errors import RegistryError


@dataclass
class ServerRecord:
    name: str
    url: str
    description: str = ""
    enabled: bool = True
    weight: int = 1
    health: str = "unknown"  # unknown | healthy | unhealthy
    metadata: Dict[str, str] = field(default_factory=dict)

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "enabled": self.enabled,
            "weight": self.weight,
            "health": self.health,
            "metadata": self.metadata,
        }


class ServerRegistry:
    """Thread-safe registry of upstream MCP servers."""

    def __init__(self):
        self._lock = threading.RLock()
        self._servers: Dict[str, ServerRecord] = {}

    def register(self, record: ServerRecord):
        with self._lock:
            if not record.name:
                raise RegistryError("server name is required")
            if not record.url:
                raise RegistryError("server url is required for %s" % record.name)
            self._servers[record.name] = record

    def unregister(self, name: str):
        with self._lock:
            self._servers.pop(name, None)

    def get(self, name: str) -> Optional[ServerRecord]:
        with self._lock:
            return self._servers.get(name)

    def list(self) -> List[ServerRecord]:
        with self._lock:
            return list(self._servers.values())

    def list_enabled(self) -> List[ServerRecord]:
        with self._lock:
            return [s for s in self._servers.values() if s.enabled]

    def set_health(self, name: str, health: str):
        with self._lock:
            rec = self._servers.get(name)
            if rec:
                rec.health = health

    def __len__(self):
        with self._lock:
            return len(self._servers)
