"""Self-check script: compile, import, and smoke-test mcplane."""

import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    checks = []

    checks.append(("compileall", run([sys.executable, "-m", "compileall", "-q", "mcplane"])))
    checks.append(("version", run([sys.executable, "-m", "mcplane", "version"])))
    checks.append(("doctor", run([sys.executable, "-m", "mcplane", "doctor"])))
    checks.append(("imports", run([
        sys.executable, "-c",
        "from mcplane.gateway import HeaderRouter; "
        "from mcplane.auth import JwtCodec; "
        "from mcplane.tasks import TaskManager; print('ok')",
    ])))

    failed = False
    for name, proc in checks:
        status = "PASS" if proc.returncode == 0 else "FAIL"
        if proc.returncode != 0:
            failed = True
        print("[%s] %s" % (status, name))
        if proc.returncode != 0 and proc.stderr:
            print(proc.stderr[:400])

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
