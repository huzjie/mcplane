from mcplane.observability.metrics import Counter, Histogram, Metrics


def test_counter():
    c = Counter()
    c.inc()
    c.inc(2)
    assert c.value() == 3


def test_histogram_summary():
    h = Histogram()
    for v in [1, 2, 3, 4, 5]:
        h.observe(v)
    s = h.summary()
    assert s["count"] == 5
    assert s["avg"] == 3.0


def test_metrics_prometheus():
    m = Metrics()
    m.requests_total.inc()
    text = m.prometheus_text()
    assert "mcplane_requests_total" in text
    assert "mcplane_errors_total" in text
