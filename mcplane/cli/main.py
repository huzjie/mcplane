"""mcplane CLI entry point.

Subcommands:
  version   Print version and MCP spec version.
  doctor    Validate config and dependencies.
  serve     Run the stateless gateway (HTTP).
  register  Register an upstream MCP server.
  list      List registered servers.
  call      Call a tool through the gateway (convenience).
  token     Issue a signed JWT for testing.
  cache     Inspect the list-result cache.
"""

import argparse
import json
import sys

from .._version import __version__, __spec_version__


def _cmd_version(args):
    print("mcplane %s (MCP spec %s)" % (__version__, __spec_version__))


def _cmd_doctor(args):
    from ..config import load_config, find_config_path
    cfg_path = args.config or find_config_path()
    if cfg_path:
        print("config file : %s" % cfg_path)
    try:
        cfg = load_config(cfg_path)
    except Exception as exc:
        print("config      : ERROR (%s)" % exc)
        return 1
    print("gateway     : %s:%s" % (cfg["gateway"]["host"], cfg["gateway"]["port"]))
    print("auth        : %s" % ("enabled" if cfg["auth"]["enabled"] else "disabled"))
    print("rate limit  : %s" % ("enabled" if cfg["rate_limit"]["enabled"] else "disabled"))
    print("cache       : %s" % ("enabled" if cfg["cache"]["enabled"] else "disabled"))
    print("doctor      : OK")
    return 0


def _cmd_register(args):
    from ..config import load_config, find_config_path
    from ..registry.server_registry import ServerRegistry, ServerRecord
    from ..storage.sqlite_store import SqliteStore
    cfg = load_config(args.config or find_config_path())
    reg = ServerRegistry()
    reg.register(ServerRecord(
        name=args.name, url=args.url, description=args.description or "",
        weight=args.weight,
    ))
    store = SqliteStore(cfg["storage"]["db_path"])
    rec = reg.get(args.name)
    store.upsert_server(rec.name, rec.url, rec.description, rec.enabled, rec.weight)
    store.close()
    print("registered server '%s' -> %s" % (args.name, args.url))
    return 0


def _cmd_list(args):
    from ..config import load_config, find_config_path
    from ..registry.server_registry import ServerRegistry
    from ..registry.discovery import discover_servers
    cfg = load_config(args.config or find_config_path())
    reg = ServerRegistry()
    discover_servers(reg, cfg["registry"]["discovery_paths"])
    for s in reg.list():
        print("%-24s %-8s %s" % (s.name, s.health, s.url))
    if not reg.list():
        print("(no servers registered)")
    return 0


def _cmd_token(args):
    from ..auth.jwt import JwtCodec
    codec = JwtCodec(args.secret or "dev-secret")
    claims = {"sub": args.subject, "scope": args.scopes}
    print(codec.encode(claims, ttl_s=args.ttl))
    return 0


def _cmd_serve(args):
    from ..config import load_config, find_config_path
    from ..server.app import run_server
    cfg = load_config(args.config or find_config_path())
    run_server(cfg)
    return 0


def _cmd_call(args):
    from ..config import load_config, find_config_path
    from ..sdk.client import McplaneClient
    cfg = load_config(args.config or find_config_path())
    base = args.endpoint or ("http://%s:%s" % (cfg["gateway"]["host"], cfg["gateway"]["port"]))
    client = McplaneClient(base)
    try:
        arguments = json.loads(args.arguments) if args.arguments else {}
    except json.JSONDecodeError:
        print("invalid JSON arguments", file=sys.stderr)
        return 1
    result = client.call_tool(args.server, args.tool, arguments, token=args.token)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def _cmd_cache(args):
    from ..cache.list_cache import ListResultCache
    cache = ListResultCache()
    print("cache entries : %d" % len(cache))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="mcplane", description="Stateless MCP control plane")
    parser.add_argument("--config", help="path to JSON config file")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("version", help="print version")
    p.set_defaults(func=_cmd_version)

    p = sub.add_parser("doctor", help="validate config")
    p.set_defaults(func=_cmd_doctor)

    p = sub.add_parser("serve", help="run the gateway")
    p.set_defaults(func=_cmd_serve)

    p = sub.add_parser("register", help="register an upstream server")
    p.add_argument("--name", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--weight", type=int, default=1)
    p.set_defaults(func=_cmd_register)

    p = sub.add_parser("list", help="list registered servers")
    p.set_defaults(func=_cmd_list)

    p = sub.add_parser("call", help="call a tool through the gateway")
    p.add_argument("--server", required=True)
    p.add_argument("--tool", required=True)
    p.add_argument("--arguments", default="")
    p.add_argument("--token", default="")
    p.add_argument("--endpoint", default="")
    p.set_defaults(func=_cmd_call)

    p = sub.add_parser("token", help="issue a signed JWT")
    p.add_argument("--subject", default="admin")
    p.add_argument("--scopes", default="mcp:read mcp:write")
    p.add_argument("--ttl", type=int, default=3600)
    p.add_argument("--secret", default="")
    p.set_defaults(func=_cmd_token)

    p = sub.add_parser("cache", help="inspect cache")
    p.set_defaults(func=_cmd_cache)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
