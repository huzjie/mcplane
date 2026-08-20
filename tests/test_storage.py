import os
import tempfile

from mcplane.storage.sqlite_store import SqliteStore


def test_upsert_and_list():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        store = SqliteStore(path)
        store.upsert_server("echo", "http://x")
        rows = store.list_servers()
        assert len(rows) == 1
        assert rows[0]["name"] == "echo"
        store.append_audit("echo", "tools/list", "ok", "trace-1")
        audit = store.recent_audit()
        assert len(audit) == 1
        assert audit[0]["server_name"] == "echo"
        store.close()
    finally:
        os.unlink(path)
