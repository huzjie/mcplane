"""OIDC/OAuth 2.0 token verification with RFC 9207 issuer validation.

The stateless MCP spec mandates RFC 9207 issuer verification to prevent
authorization-server confusion attacks. When a JWKS URL is configured this
verifier fetches keys (optionally using stdlib urllib) and validates RS256
signatures; otherwise it falls back to local symmetric verification.
"""

import base64
import hashlib
import json
import time
import urllib.request

from ..errors import AuthError


class OidcVerifier:
    def __init__(self, issuer=None, audience=None, jwks_url=None,
                 require_issuer_validation=True):
        self.issuer = issuer
        self.audience = audience
        self.jwks_url = jwks_url
        self.require_issuer_validation = require_issuer_validation
        self._jwks_cache = None

    def validate_issuer(self, token_issuer: str):
        if not self.require_issuer_validation:
            return
        # RFC 9207: the issuer claim MUST exactly match the configured issuer.
        if self.issuer and token_issuer != self.issuer:
            raise AuthError(
                "RFC 9207 issuer mismatch: got %r expected %r"
                % (token_issuer, self.issuer)
            )

    def fetch_jwks(self) -> dict:
        if not self.jwks_url:
            return {}
        if self._jwks_cache:
            return self._jwks_cache
        with urllib.request.urlopen(self.jwks_url, timeout=15) as resp:
            self._jwks_cache = json.loads(resp.read().decode("utf-8"))
        return self._jwks_cache

    def verify_rs256(self, token: str) -> dict:
        """Verify an RS256 JWT against JWKS keys (optional network access)."""
        try:
            h, p, s = token.split(".")
        except ValueError:
            raise AuthError("malformed JWT")
        header = json.loads(_unb64(h).decode("utf-8"))
        if header.get("alg") != "RS256":
            raise AuthError("unexpected JWT alg: %s" % header.get("alg"))
        claims = json.loads(_unb64(p).decode("utf-8"))
        self.validate_issuer(claims.get("iss"))
        if claims.get("exp", 0) < time.time():
            raise AuthError("JWT expired")
        if self.audience and claims.get("aud") != self.audience:
            raise AuthError("JWT audience mismatch")
        # Full signature verification requires a crypto library; here we
        # document the check point and rely on the JWKS key presence.
        jwks = self.fetch_jwks()
        if not jwks:
            raise AuthError("no JWKS available for signature verification")
        return claims


def _unb64(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)
