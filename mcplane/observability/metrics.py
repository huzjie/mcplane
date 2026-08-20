"""Prometheus-style metrics (counters + histograms) using stdlib only."""

import threading
import time


class Counter:
    def __init__(self):
        self._value = 0.0
        self._lock = threading.Lock()

    def inc(self, amount: float = 1.0):
        with self._lock:
            self._value += amount

    def value(self) -> float:
        with self._lock:
            return self._value


class Histogram:
    def __init__(self):
        self._values = []
        self._lock = threading.Lock()

    def observe(self, value: float):
        with self._lock:
            self._values.append(value)

    def summary(self):
        with self._lock:
            values = list(self._values)
        if not values:
            return {"count": 0, "sum": 0.0, "avg": 0.0, "p50": 0.0, "p99": 0.0}
        values.sort()
        n = len(values)
        return {
            "count": n,
            "sum": sum(values),
            "avg": sum(values) / n,
            "p50": values[int(n * 0.5)],
            "p99": values[int(n * 0.99)],
        }


class Metrics:
    def __init__(self):
        self.requests_total = Counter()
        self.errors_total = Counter()
        self.latency = Histogram()
        self.upstream_latency = Histogram()
        self.round_trips = Counter()
        self.cache_hits = Counter()
        self.cache_misses = Counter()
        self._started = time.monotonic()

    def prometheus_text(self) -> str:
        """Render the metrics in Prometheus text exposition format."""
        lat = self.latency.summary()
        up = self.upstream_latency.summary()
        lines = [
            "# HELP mcplane_requests_total Total gateway requests.",
            "# TYPE mcplane_requests_total counter",
            "mcplane_requests_total %.0f" % self.requests_total.value(),
            "# HELP mcplane_errors_total Total gateway errors.",
            "# TYPE mcplane_errors_total counter",
            "mcplane_errors_total %.0f" % self.errors_total.value(),
            "# TYPE mcplane_round_trips_total counter",
            "mcplane_round_trips_total %.0f" % self.round_trips.value(),
            "# TYPE mcplane_cache_hits_total counter",
            "mcplane_cache_hits_total %.0f" % self.cache_hits.value(),
            "# TYPE mcplane_cache_misses_total counter",
            "mcplane_cache_misses_total %.0f" % self.cache_misses.value(),
            "# TYPE mcplane_latency_seconds_summary summary",
            "mcplane_latency_seconds_summary{quantile=\"0.99\"} %.4f" % lat["p99"],
            "# TYPE mcplane_upstream_latency_seconds_summary summary",
            "mcplane_upstream_latency_seconds_summary{quantile=\"0.99\"} %.4f" % up["p99"],
        ]
        return "\n".join(lines) + "\n"
