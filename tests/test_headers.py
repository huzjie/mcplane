from mcplane.spec.headers import (
    HEADER_METHOD, HEADER_NAME, HEADER_PROTOCOL_VERSION, HEADER_SESSION_ID,
    StatelessHeaders, DEPRECATED_HEADERS,
)


def test_header_constants():
    assert HEADER_METHOD == "Mcp-Method"
    assert HEADER_NAME == "Mcp-Name"


def test_deprecated_headers():
    assert HEADER_SESSION_ID in DEPRECATED_HEADERS


def test_stateless_headers_to_dict():
    h = StatelessHeaders(method="tools/list", name="echo", trace_id="abc")
    d = h.to_dict()
    assert d["Mcp-Method"] == "tools/list"
    assert d["Mcp-Name"] == "echo"
    assert d["X-Trace-Id"] == "abc"
