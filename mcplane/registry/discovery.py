"""Server discovery from config files (mcp.json / servers.json)."""

import json
from pathlib import Path
from typing import List

from .server_registry import ServerRecord, ServerRegistry
from ..errors import RegistryError


def discover_servers(registry: ServerRegistry, paths: List[str]) -> int:
    """Load server records from discovery files into ``registry``.

    Returns the number of servers registered. Each file may be a JSON object
    mapping ``name -> {url, description, weight}`` or a JSON array of objects
    with a ``name`` and ``url`` field.
    """
    count = 0
    for raw_path in paths:
        p = Path(raw_path).expanduser()
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise RegistryError("invalid JSON in %s: %s" % (p, exc))
        records = _parse(data)
        for rec in records:
            registry.register(rec)
            count += 1
    return count


def _parse(data) -> List[ServerRecord]:
    records = []
    if isinstance(data, list):
        for item in data:
            records.append(_from_item(item))
    elif isinstance(data, dict):
        for name, item in data.items():
            if isinstance(item, dict) and "url" in item:
                records.append(_from_item({"name": name, **item}))
    return records


def _from_item(item: dict) -> ServerRecord:
    return ServerRecord(
        name=str(item.get("name", "")),
        url=str(item.get("url", "")),
        description=str(item.get("description", "")),
        enabled=bool(item.get("enabled", True)),
        weight=int(item.get("weight", 1)),
        metadata={str(k): str(v) for k, v in (item.get("metadata") or {}).items()},
    )
