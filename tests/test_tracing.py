from mcplane.observability.tracing import TraceContext


def test_trace_context():
    tc = TraceContext()
    assert len(tc.trace_id) == 32
    assert len(tc.span_id) == 16


def test_child_shares_trace():
    parent = TraceContext()
    child = parent.child()
    assert child.trace_id == parent.trace_id
    assert child.span_id != parent.span_id


def test_header_value_format():
    tc = TraceContext(trace_id="a" * 32, span_id="b" * 16)
    assert tc.header_value == "00-%s-%s-01" % ("a" * 32, "b" * 16)
