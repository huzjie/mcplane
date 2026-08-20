"""Minimal JWT codec (HS256) using only the standard library.

Supports signing, verification, and expiry/issuer/audience claims validation.
RSA (RS256) verification is delegated to OidcVerifier when a JWKS URL is set.
"""

import base64
import hashlib
import hmac
import json
import time

from ..errors import AuthError


class JwtCodec:
    def __init__(self, secret: str):
        self.secret = secret.encode("utf-8")

    def _b64(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

    def _unb64(self, data: str) -> bytes:
        pad = "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(data + pad)

    def encode(self, claims: dict, ttl_s: int = 3600) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        now = int(time.time())
        payload = {**claims, "iat": now, "exp": now + ttl_s}
        h = self._b64(json.dumps(header, separators=(",", ":")).encode("utf-8"))
        p = self._b64(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
        msg = ("%s.%s" % (h, p)).encode("ascii")
        sig = hmac.new(self.secret, msg, hashlib.sha256).digest()
        return "%s.%s.%s" % (h, p, self._b64(sig))

    def decode(self, token: str, audience: str = None, issuer: str = None) -> dict:
        try:
            h, p, s = token.split(".")
        except ValueError:
            raise AuthError("malformed JWT")
        msg = ("%s.%s" % (h, p)).encode("ascii")
        expected = hmac.new(self.secret, msg, hashlib.sha256).digest()
        if not hmac.compare_digest(self._unb64(s), expected):
            raise AuthError("invalid JWT signature")
        try:
            claims = json.loads(self._unb64(p).decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            raise AuthError("invalid JWT payload")
        if claims.get("exp", 0) < time.time():
            raise AuthError("JWT expired")
        if issuer and claims.get("iss") != issuer:
            raise AuthError("JWT issuer mismatch")
        if audience and claims.get("aud") != audience:
            raise AuthError("JWT audience mismatch")
        return claims
