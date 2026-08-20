from mcplane.spec.protocol import (
    JsonRpcRequest, JsonRpcResponse, JsonRpcErrorObject,
    make_response, make_error, MCP_ERROR_CODES,
)


def test_request_roundtrip():
    req = JsonRpcRequest.from_dict({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    assert req.method == "tools/list"
    assert req.id == 1
    assert req.to_dict()["method"] == "tools/list"


def test_request_missing_method():
    try:
        JsonRpcRequest.from_dict({"jsonrpc": "2.0"})
        assert False
    except ValueError:
        pass


def test_response_result():
    req = JsonRpcRequest(method="ping", id=2)
    resp = make_response(req, {"ok": True})
    d = resp.to_dict()
    assert d["result"] == {"ok": True}
    assert "error" not in d


def test_response_error():
    req = JsonRpcRequest(method="x", id=3)
    resp = make_error(req, -32601, "nope")
    assert resp.error.code == -32601
    assert resp.error.message == "nope"


def test_error_codes_map():
    assert MCP_ERROR_CODES["METHOD_NOT_FOUND"] == -32601
