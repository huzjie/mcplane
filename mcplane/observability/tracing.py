"""Lightweight trace context propagation (W3C traceparent subset)."""

import secrets


class TraceContext:
    def __init__(self, trace_id: str = None, span_id: str = None):
        self.trace_id = trace_id or _hex(32)
        self.span_id = span_id or _hex(16)

    def child(self) -> "TraceContext":
        return TraceContext(trace_id=self.trace_id)

    @property
    def header_value(self) -> str:
        return "00-%s-%s-01" % (self.trace_id, self.span_id)

    def __str__(self):
        return self.header_value


def _hex(n_bytes: int) -> str:
    return secrets.token_hex(n_bytes // 2)
