"""Seed the SQLite registry with a few example servers."""

from mcplane.storage.sqlite_store import SqliteStore


def main():
    store = SqliteStore("mcplane.db")
    store.upsert_server("echo", "http://127.0.0.1:8100/mcp",
                        "Mock echo + calculator MCP server")
    store.upsert_server("git", "http://127.0.0.1:8200/mcp",
                        "Git integration MCP server")
    store.close()
    print("seeded mcplane.db")


if __name__ == "__main__":
    main()
