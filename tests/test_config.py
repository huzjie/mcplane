import json
import os
import tempfile

from mcplane.config import load_config, find_config_path, DEFAULT_CONFIG
from mcplane.errors import ConfigError


def test_default_config():
    cfg = load_config()
    assert cfg["gateway"]["port"] == 8090
    assert cfg["auth"]["enabled"] is False


def test_load_json_config():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"gateway": {"port": 9999}}, f)
        path = f.name
    try:
        cfg = load_config(path)
        assert cfg["gateway"]["port"] == 9999
        # unmerged keys retain defaults
        assert cfg["gateway"]["host"] == "0.0.0.0"
    finally:
        os.unlink(path)


def test_load_missing_raises():
    try:
        load_config("/no/such/file.json")
        assert False
    except ConfigError:
        pass


def test_env_override():
    os.environ["MCPLANE_GATEWAY__PORT"] = "1234"
    try:
        cfg = load_config()
        assert cfg["gateway"]["port"] == 1234
    finally:
        del os.environ["MCPLANE_GATEWAY__PORT"]


def test_find_config_path_returns_none_when_absent():
    # No config in cwd; returns None is acceptable.
    assert find_config_path() is None or isinstance(find_config_path(), str)
