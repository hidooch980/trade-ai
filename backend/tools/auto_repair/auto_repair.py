#!/usr/bin/env python3

import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "logs" / "auto_repair"
LOG_DIR.mkdir(parents=True, exist_ok=True)

MAX_ROUNDS = 5


def run(cmd):
    print(f"\n>>> {' '.join(cmd)}")
    p = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(p.stdout)
    return p.returncode, p.stdout


def snapshot():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = LOG_DIR / f"snapshot_{ts}.diff"

    p = subprocess.run(
        ["git", "diff"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    path.write_text(p.stdout, encoding="utf-8")
    print(f"[SNAPSHOT] {path}")


def install_missing_dependencies(output):
    packages = set()

    patterns = [
        r"No module named ['\"]([^'\"]+)['\"]",
        r"ModuleNotFoundError: No module named ([^\s]+)",
    ]

    for pattern in patterns:
        for match in re.findall(pattern, output):
            name = match.split(".")[0].strip("'\"")

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

            if name in mapping:
                packages.add(mapping[name])

    if not packages:
        return False

    print("[AUTO-FIX] Missing dependencies:", sorted(packages))

    rc, _ = run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            *sorted(packages),
        ]
    )

    return rc == 0


def compile_check():
    return run(
        [
            sys.executable,
            "-m",
            "compileall",
            "-q",
            "app",
        ]
    )[0] == 0


def run_tests():
    return run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
        ]
    )


def classify(output):
    if "ModuleNotFoundError" in output:
        return "DEPENDENCY"

    if "SyntaxError" in output:
        return "SYNTAX"

    if "ImportError" in output:
        return "IMPORT"

    if "TypeError:" in output:
        return "TYPE_ERROR"

    if "AttributeError:" in output:
        return "ATTRIBUTE_ERROR"

    if "AssertionError" in output:
        return "ASSERTION"

    if "FAILED" in output:
        return "TEST_FAILURE"

    return "UNKNOWN"


def main():
    print("=" * 70)
    print("TRADE-AI AUTO REPAIR ENGINE")
    print("=" * 70)

    snapshot()

    for round_no in range(1, MAX_ROUNDS + 1):
        print(f"\n{'=' * 20} ROUND {round_no}/{MAX_ROUNDS} {'=' * 20}")

        if not compile_check():
            print("[STOP] Compile error detected.")
            print("[ACTION] Automatic semantic repair disabled.")
            return 2

        rc, output = run_tests()

        if rc == 0:
            print("\n" + "=" * 70)
            print("AUTO REPAIR: ALL TESTS PASS")
            print("=" * 70)
            return 0

        error_type = classify(output)
        print(f"\n[DIAGNOSIS] {error_type}")

        if error_type == "DEPENDENCY":
            if install_missing_dependencies(output):
                continue

        print("\n[STOP] Error requires source-level/semantic repair.")
        print("[REASON]", error_type)
        print("\nLast failure:")
        print(output[-5000:])
        return 1

    print("\n[AUTO REPAIR] Maximum repair rounds reached.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
