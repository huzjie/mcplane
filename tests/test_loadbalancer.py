from mcplane.registry.server_registry import ServerRecord
from mcplane.gateway.loadbalancer import LoadBalancer


def _servers():
    return [
        ServerRecord(name="a", url="http://a", weight=1),
        ServerRecord(name="b", url="http://b", weight=3),
    ]


def test_round_robin_cycles():
    lb = LoadBalancer(strategy="round-robin")
    servers = _servers()
    picks = [lb.pick(servers).name for _ in range(4)]
    assert picks == ["a", "b", "a", "b"]


def test_random_returns_one():
    lb = LoadBalancer(strategy="random")
    servers = _servers()
    assert lb.pick(servers).name in ("a", "b")


def test_empty():
    lb = LoadBalancer()
    assert lb.pick([]) is None
