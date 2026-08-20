"""Configuration loading for mcplane.

mcplane uses JSON as its primary config format (zero YAML dependency) plus
environment variable overrides prefixed with ``MCPLANE_``. A default config is
embedded so the tool runs out-of-the-box with no config file at all.
"""

import json
import os
from copy import deepcopy
from pathlib import Path

from .errors import ConfigError

DEFAULT_CONFIG = {
    "gateway": {
        "host": "0.0.0.0",
        "port": 8090,
        "upstream_timeout_s": 60,
        "max_round_trips": 8,
        "load_balance": "round-robin",
    },
    "registry": {
        "servers": [],
        "discovery_paths": ["mcp.json", "servers.json"],
    },
    "auth": {
        "enabled": False,
        "mode": "ema",
        "issuer": None,
        "audience": None,
        "jwks_url": None,
        "require_issuer_validation": True,
    },
    "rate_limit": {
        "enabled": False,
        "requests_per_second": 100,
        "burst": 200,
    },
    "cache": {
        "enabled": True,
        "default_ttl_ms": 60000,
        "max_entries": 4096,
    },
    "storage": {
        "db_path": "mcplane.db",
    },
    "observability": {
        "enabled": True,
        "metrics_endpoint": "/metrics",
    },
    "logging": {
        "level": "INFO",
    },
}


def _deep_merge(base, override):
    """Recursively merge ``override`` into ``base`` (dicts only)."""
    out = deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def _env_override(config):
    """Apply MCPLANE_* environment variable overrides (dotted keys)."""
    prefix = "MCPLANE_"
    for key, value in os.environ.items():
        if not key.startswith(prefix) or len(key) <= len(prefix):
            continue
        path = key[len(prefix):].lower().split("__")
        node = config
        for part in path[:-1]:
            node = node.setdefault(part, {})
        leaf = path[-1]
        raw = value
        if raw.lower() in ("true", "false"):
            node[leaf] = raw.lower() == "true"
        elif raw.isdigit():
            node[leaf] = int(raw)
        else:
            try:
                node[leaf] = float(raw)
            except ValueError:
                node[leaf] = raw
    return config


def load_config(path=None):
    """Load config from ``path`` (JSON), merging over embedded defaults.

    Returns a plain dict. Raises ConfigError on malformed JSON.
    """
    config = deepcopy(DEFAULT_CONFIG)
    if path:
        p = Path(path)
        if not p.exists():
            raise ConfigError("config file not found: %s" % p)
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ConfigError("invalid JSON in %s: %s" % (p, exc))
        config = _deep_merge(config, data)
    return _env_override(config)


def find_config_path():
    """Return first existing config file from standard locations, else None."""
    candidates = ["mcplane.json", "config/mcplane.json", "~/.mcplane/config.json"]
    for cand in candidates:
        p = Path(cand).expanduser()
        if p.exists():
            return str(p)
    return None
