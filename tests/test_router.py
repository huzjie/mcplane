from mcplane.registry.server_registry import ServerRegistry, ServerRecord
from mcplane.gateway.router import HeaderRouter
from mcplane.errors import NotFoundError


def _registry():
    reg = ServerRegistry()
    reg.register(ServerRecord(name="echo", url="http://a"))
    reg.register(ServerRecord(name="calc", url="http://b"))
    return reg


def test_resolve_by_name():
    router = HeaderRouter(_registry())
    assert router.resolve("echo").url == "http://a"


def test_resolve_unknown_raises():
    router = HeaderRouter(_registry())
    try:
        router.resolve("missing")
        assert False
    except NotFoundError:
        pass


def test_resolve_no_name_returns_first():
    router = HeaderRouter(_registry())
    rec = router.resolve(None)
    assert rec is not None


def test_round_robin():
    router = HeaderRouter(_registry())
    first = router.next_by_round_robin()
    second = router.next_by_round_robin()
    assert first is not None and second is not None
