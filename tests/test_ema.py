from mcplane.auth.ema import EmaAuthorizer
from mcplane.errors import ForbiddenError


def test_allow_rule():
    ema = EmaAuthorizer([
        {"name": "r", "principal": "alice", "server": "*", "method": "*", "effect": "allow"},
    ])
    assert ema.authorize("alice", "echo", "tools/list") is True


def test_default_deny():
    ema = EmaAuthorizer([])
    try:
        ema.authorize("bob", "echo", "tools/list")
        assert False
    except ForbiddenError:
        pass


def test_deny_rule():
    ema = EmaAuthorizer([
        {"name": "d", "principal": "*", "server": "*", "method": "tools/call", "effect": "deny"},
    ])
    try:
        ema.authorize("alice", "echo", "tools/call")
        assert False
    except ForbiddenError:
        pass


def test_scope_required():
    ema = EmaAuthorizer([
        {"name": "s", "principal": "*", "server": "*", "method": "*",
         "scopes": ["mcp:write"], "effect": "allow"},
    ])
    assert ema.authorize("x", "echo", "tools/list", scopes=["mcp:write"]) is True
    try:
        ema.authorize("x", "echo", "tools/list", scopes=["mcp:read"])
        assert False
    except ForbiddenError:
        pass
