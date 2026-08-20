from mcplane.gateway.proxy import StatelessProxy
from mcplane.errors import UpstreamError, TimeoutError


def test_forward_unreachable():
    proxy = StatelessProxy(timeout_s=1)
    try:
        proxy.forward("http://127.0.0.1:1/mcp", "tools/list", {})
        assert False
    except (UpstreamError, TimeoutError):
        pass
