from mcplane.errors import (
    McplaneError, ConfigError, AuthError, ForbiddenError, RateLimitError,
    UpstreamError, TimeoutError, JsonRpcError,
)


def test_error_codes():
    assert ConfigError().code == "CONFIG_ERROR"
    assert AuthError().code == "AUTH_ERROR"
    assert ForbiddenError().code == "FORBIDDEN"


def test_jsonrpc_error():
    e = JsonRpcError(-32601, "not found")
    assert e.rpc_code == -32601
    assert e.message == "not found"


def test_hierarchy():
    assert issubclass(ConfigError, McplaneError)
    assert issubclass(ForbiddenError, McplaneError)
