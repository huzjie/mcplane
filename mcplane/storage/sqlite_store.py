"""SQLite persistence for registry, tasks, and audit log (stdlib sqlite3)."""

import json
import sqlite3
import threading
import time
from typing import Any, Dict, List, Optional


class SqliteStore:
    def __init__(self, db_path: str = "mcplane.db"):
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        self._init_schema()

    def _init_schema(self):
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS servers ("
                "name TEXT PRIMARY KEY, url TEXT NOT NULL, description TEXT, "
                "enabled INTEGER DEFAULT 1, weight INTEGER DEFAULT 1, "
                "health TEXT DEFAULT 'unknown')"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS audit_log ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, ts REAL, "
                "server_name TEXT, method TEXT, status TEXT, trace_id TEXT)"
            )
            self._conn.commit()

    def upsert_server(self, name, url, description="", enabled=True, weight=1):
        with self._lock:
            self._conn.execute(
                "INSERT INTO servers(name,url,description,enabled,weight) "
                "VALUES(?,?,?,?,?) "
                "ON CONFLICT(name) DO UPDATE SET url=excluded.url, "
                "description=excluded.description, enabled=excluded.enabled, "
                "weight=excluded.weight",
                (name, url, description, 1 if enabled else 0, weight),
            )
            self._conn.commit()

    def list_servers(self) -> List[Dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM servers ORDER BY name").fetchall()
        return [dict(r) for r in rows]

    def append_audit(self, server_name, method, status, trace_id=None):
        with self._lock:
            self._conn.execute(
                "INSERT INTO audit_log(ts,server_name,method,status,trace_id) "
                "VALUES(?,?,?,?,?)",
                (time.time(), server_name, method, status, trace_id),
            )
            self._conn.commit()

    def recent_audit(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(r) for r in rows]

    def close(self):
        with self._lock:
            self._conn.close()
