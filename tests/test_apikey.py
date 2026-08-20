from mcplane.auth.apikey import ApiKeyManager
from mcplane.errors import AuthError


def test_generate_has_prefix():
    m = ApiKeyManager()
    assert m.generate().startswith("mcp_")


def test_verify_roundtrip():
    m = ApiKeyManager()
    key = m.generate()
    assert m.verify(key, m.hash(key))


def test_verify_wrong():
    m = ApiKeyManager()
    assert not m.verify("mcp_wrong", m.hash("mcp_right"))


def test_extract_bearer():
    m = ApiKeyManager()
    assert m.extract("Bearer abc") == "abc"


def test_extract_missing_raises():
    m = ApiKeyManager()
    try:
        m.extract("")
        assert False
    except AuthError:
        pass
