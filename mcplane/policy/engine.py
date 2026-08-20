"""Policy engine combining EMA authorization and rate limiting."""

from typing import Dict, List, Optional

from ..auth.ema import EmaAuthorizer
from ..errors import ForbiddenError, RateLimitError
from .ratelimit import RateLimiter


class PolicyEngine:
    def __init__(self, ema: Optional[EmaAuthorizer] = None,
                 limiter: Optional[RateLimiter] = None):
        self.ema = ema or EmaAuthorizer([])
        self.limiter = limiter

    def enforce(self, principal: str, server_name: str, method: str,
                scopes: Optional[List[str]] = None,
                rate_key: Optional[str] = None):
        self.ema.authorize(principal, server_name, method, scopes)
        if self.limiter and rate_key:
            self.limiter.guard(rate_key)
