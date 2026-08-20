import time

from mcplane.auth.jwt import JwtCodec
from mcplane.errors import AuthError


def test_roundtrip():
    codec = JwtCodec("secret")
    token = codec.encode({"sub": "alice"})
    claims = codec.decode(token)
    assert claims["sub"] == "alice"


def test_expiry():
    codec = JwtCodec("secret")
    token = codec.encode({"sub": "bob"}, ttl_s=-1)
    try:
        codec.decode(token)
        assert False
    except AuthError:
        pass


def test_issuer_mismatch():
    codec = JwtCodec("secret")
    token = codec.encode({"sub": "x", "iss": "other"})
    try:
        codec.decode(token, issuer="mine")
        assert False
    except AuthError:
        pass


def test_bad_signature():
    codec = JwtCodec("secret")
    token = codec.encode({"sub": "x"})
    other = JwtCodec("different")
    try:
        other.decode(token)
        assert False
    except AuthError:
        pass
