"""Enterprise-Managed Authorization (EMA) policy evaluation.

EMA lets an organization centrally manage authorization so end users can reach
every connected MCP server through a single login. This authorizer evaluates
``allow``/``deny`` rules over (principal, server, method) triples.
"""

from typing import Dict, List, Optional

from ..errors import ForbiddenError


class EmaAuthorizer:
    def __init__(self, rules: Optional[List[Dict]] = None):
        self.rules = rules or []

    def authorize(self, principal: str, server_name: str, method: str,
                  scopes: Optional[List[str]] = None) -> bool:
        """Return True if allowed; raise ForbiddenError otherwise."""
        scopes = scopes or []
        for rule in self.rules:
            if not self._match(rule, principal, server_name, method, scopes):
                continue
            if rule.get("effect", "allow") == "deny":
                raise ForbiddenError(
                    "denied by EMA rule: %s" % rule.get("name", "unnamed")
                )
            return True
        # Default deny when no rule grants access (zero-trust posture).
        raise ForbiddenError("no EMA rule grants access to %s.%s" % (server_name, method))

    def _match(self, rule, principal, server_name, method, scopes):
        p = rule.get("principal")
        s = rule.get("server")
        m = rule.get("method")
        if p and p != "*" and p != principal:
            return False
        if s and s != "*" and s != server_name:
            return False
        if m and m != "*" and m != method:
            return False
        required = rule.get("scopes")
        if required:
            if not any(r in scopes for r in required):
                return False
        return True
