"""API key generation, hashing, and verification (stdlib only)."""

import hashlib
import hmac
import secrets

from ..errors import AuthError


class ApiKeyManager:
    PREFIX = "mcp_"

    def generate(self) -> str:
        raw = self.PREFIX + secrets.token_urlsafe(32)
        return raw

    def hash(self, key: str) -> str:
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def verify(self, key: str, stored_hash: str) -> bool:
        if not key or not stored_hash:
            return False
        return hmac.compare_digest(self.hash(key), stored_hash)

    def extract(self, authorization_header: str) -> str:
        if not authorization_header:
            raise AuthError("missing Authorization header")
        parts = authorization_header.split(" ", 1)
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1]
        raise AuthError("unsupported Authorization scheme")
