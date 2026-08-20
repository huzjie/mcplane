"""Rule compilation for access policies."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Rule:
    name: str
    principal: str = "*"
    server: str = "*"
    method: str = "*"
    scopes: List[str] = None
    effect: str = "allow"

    def __post_init__(self):
        if self.scopes is None:
            self.scopes = []

    def to_dict(self):
        return {
            "name": self.name,
            "principal": self.principal,
            "server": self.server,
            "method": self.method,
            "scopes": self.scopes,
            "effect": self.effect,
        }


def compile_rules(raw: List[Dict]) -> List[Rule]:
    rules = []
    for item in raw or []:
        rules.append(Rule(
            name=item.get("name", "rule-%d" % len(rules)),
            principal=item.get("principal", "*"),
            server=item.get("server", "*"),
            method=item.get("method", "*"),
            scopes=list(item.get("scopes") or []),
            effect=item.get("effect", "allow"),
        ))
    return rules
