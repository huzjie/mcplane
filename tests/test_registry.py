from mcplane.registry.server_registry import ServerRegistry, ServerRecord
from mcplane.errors import RegistryError


def test_register_and_get():
    reg = ServerRegistry()
    reg.register(ServerRecord(name="echo", url="http://x/mcp"))
    assert reg.get("echo").url == "http://x/mcp"
    assert len(reg) == 1


def test_register_missing_name():
    reg = ServerRegistry()
    try:
        reg.register(ServerRecord(name="", url="http://x"))
        assert False
    except RegistryError:
        pass


def test_unregister():
    reg = ServerRegistry()
    reg.register(ServerRecord(name="a", url="http://x"))
    reg.unregister("a")
    assert len(reg) == 0


def test_list_enabled():
    reg = ServerRegistry()
    reg.register(ServerRecord(name="a", url="http://x", enabled=True))
    reg.register(ServerRecord(name="b", url="http://y", enabled=False))
    assert len(reg.list_enabled()) == 1
