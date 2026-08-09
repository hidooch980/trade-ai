#!/usr/bin/env python3

import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path("/opt/trade-ai/backend")
LOG = ROOT / "logs" / "auto_repair"
LOG.mkdir(parents=True, exist_ok=True)

MAX_ROUNDS = 5


def cmd(args):
    p = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return p.returncode, p.stdout


def save_state():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = LOG / f"before_round_{ts}.patch"

    rc, data = cmd(["git", "diff"])
    out.write_text(data, encoding="utf-8")

    return out


def restore():
    cmd(["git", "restore", "--worktree", "--", "."])
    cmd(["git", "clean", "-fd", "--", "app", "tests"])


def compile_all():
    rc, out = cmd([
        sys.executable,
        "-m",
        "compileall",
        "-q",
        "app",
    ])
    return rc == 0, out


def tests():
    return cmd([
        sys.executable,
        "-m",
        "pytest",
        "-q",
    ])


def dependency_fix(output):
    found = set()

    for module in re.findall(
        r"No module named ['\"]([^'\"]+)['\"]",
        output,
    ):
        module = module.split(".")[0]

        mapping = {
            "pydantic": "pydantic",
            "fastapi": "fastapi",
            "uvicorn": "uvicorn",
            "httpx": "httpx",
            "numpy": "numpy",
            "pandas": "pandas",
            "pytest": "pytest",
            "pytest_asyncio": "pytest-asyncio",
            "sqlalchemy": "sqlalchemy",
            "asyncpg": "asyncpg",
            "redis": "redis",
        }

        if module in mapping:
            found.add(mapping[module])

    if not found:
        return False

    print("[REPAIR] Installing:", ", ".join(sorted(found)))

    rc, out = cmd([
        sys.executable,
        "-m",
        "pip",
        "install",
        *sorted(found),
    ])

    print(out)
    return rc == 0


def detect(output):
    if "ModuleNotFoundError" in output:
        return "DEPENDENCY"

    if "SyntaxError" in output:
        return "SYNTAX"

    if "missing 1 required positional argument" in output:
        return "SIGNATURE_MISMATCH"

    if "unexpected keyword argument" in output:
        return "SIGNATURE_MISMATCH"

    if "AttributeError:" in output:
        return "ATTRIBUTE_ERROR"

    if "TypeError:" in output:
        return "TYPE_ERROR"

    if "AssertionError" in output:
        return "ASSERTION"

    if "FAILED" in output:
        return "TEST_FAILURE"

    return "UNKNOWN"


def safe_signature_report(output):
    pattern = r"([\w.]+)\.([\w]+)\(.*?missing \d+ required positional argument: ['\"]([^'\"]+)['\"]"

    matches = re.findall(pattern, output, re.S)

    for obj, method, arg in matches:
        print(
            f"[SIGNATURE] {obj}.{method} requires missing argument: {arg}"
        )

    # Python traceback may contain "future.result()" above the
    # actual failing call. Prefer the source traceback line.
    source_calls = re.findall(
        r"tests/[^\n]+:\d+:.*?([\w]+)\.([\w]+)\(",
        output,
    )

    if source_calls:
        for method_owner, method in source_calls:
            if method in {"run", "execute", "validate", "calculate"}:
                print(
                    f"[SIGNATURE-SOURCE] {method_owner}.{method}()"
                )

    return bool(matches)


def main():
    print("=" * 72)
    print("TRADE-AI AUTO REPAIR ENGINE v2")
    print("=" * 72)

    for round_no in range(1, MAX_ROUNDS + 1):
        print(f"\n--- ROUND {round_no}/{MAX_ROUNDS} ---")

        snapshot = save_state()
        print("[SNAPSHOT]", snapshot)

        ok, compile_output = compile_all()

        if not ok:
            print("[STOP] Compile/Syntax error")
            print(compile_output)
            return 2

        rc, output = tests()

        if rc == 0:
            print("\n[AUTO-REPAIR] ALL TESTS PASS")
            return 0

        error = detect(output)

        print("[DIAGNOSIS]", error)

        if error == "DEPENDENCY":
            if dependency_fix(output):
                continue

        if error == "SIGNATURE_MISMATCH":
            safe_signature_report(output)

            print(
                "[SAFE MODE] Signature mismatch detected."
                " No automatic source mutation performed."
            )

            print("\n" + output[-6000:])
            return 1

        if error in {
            "ATTRIBUTE_ERROR",
            "TYPE_ERROR",
            "ASSERTION",
            "TEST_FAILURE",
        }:
            print(
                "[SAFE MODE] Semantic failure detected."
                " Automatic mutation blocked."
            )

            print("\n" + output[-6000:])
            return 1

        print("[STOP] Unknown failure.")
        print(output[-6000:])
        return 1

    print("[STOP] Maximum repair rounds reached.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
