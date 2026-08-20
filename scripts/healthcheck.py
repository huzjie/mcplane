"""HTTP health check for the gateway (used by load balancers)."""

import sys
import urllib.request


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8090/healthz"
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            sys.exit(0 if resp.status == 200 else 1)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
