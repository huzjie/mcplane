"""Load balancing strategies for the stateless gateway."""

import random
import threading
from typing import List, Optional

from ..registry.server_registry import ServerRecord


class LoadBalancer:
    """Round-robin / weighted / random selection over healthy servers."""

    def __init__(self, strategy: str = "round-robin", seed: int = 0):
        self.strategy = strategy
        self._rng = random.Random(seed)
        self._lock = threading.Lock()
        self._rr = 0

    def pick(self, servers: List[ServerRecord]) -> Optional[ServerRecord]:
        if not servers:
            return None
        if self.strategy == "random":
            return self._rng.choice(servers)
        if self.strategy == "weighted":
            return self._weighted(servers)
        # default round-robin
        with self._lock:
            idx = self._rr % len(servers)
            self._rr += 1
        return servers[idx]

    def _weighted(self, servers: List[ServerRecord]) -> ServerRecord:
        total = sum(max(s.weight, 1) for s in servers)
        pick = self._rng.uniform(0, total)
        acc = 0.0
        for s in servers:
            acc += max(s.weight, 1)
            if pick <= acc:
                return s
        return servers[-1]
