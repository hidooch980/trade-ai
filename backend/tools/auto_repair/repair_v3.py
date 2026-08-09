#!/usr/bin/env python3
import re
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path("/opt/trade-ai/backend")
LOG = ROOT / "logs" / "auto_repair"
BACKUP = LOG / "backups"
MAX_ROUNDS = 5

LOG.mkdir(parents=True, exist_ok=True)
BACKUP.mkdir(parents=True, exist_ok=True)


def run(args):
    return subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def backup_file(path):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = BACKUP / f"{path.name}.{ts}.bak"
    shutil.copy2(path, target)
    return target


def restore_file(path, backup):
    shutil.copy2(backup, path)


def compile_app():
    return run([sys.executable, "-m", "compileall", "-q", "app"])


def pytest():
    return run([sys.executable, "-m", "pytest", "-q"])


def find_signature_mismatch(output):
    lines = output.splitlines()

    error_index = None
    for i, line in enumerate(lines):
        if "TypeError:" in line and "missing" in line:
            error_index = i
            break

    if error_index is None:
        return None

    context = lines[max(0, error_index - 40):error_index + 1]

    owner = None
    method = None

    preferred = {
        ("backtest", "run"),
        ("executor", "execute"),
        ("gate", "validate"),
        ("win", "calculate"),
    }

    for line in reversed(context):
        for candidate_owner, candidate_method in preferred:
            if f"{candidate_owner}.{candidate_method}(" in line:
                owner = candidate_owner
                method = candidate_method
                break
        if owner:
            break

    missing = re.search(
        r"missing \d+ required positional argument: ['\"]([^'\"]+)['\"]",
        lines[error_index],
    )

    if not missing or owner is None or method is None:
        return None

    file_match = None

    for line in reversed(context):
        match = re.search(r"(tests/[^:]+):(\d+)", line)
        if match:
            file_match = match
            break

    if not file_match:
        return None

    return {
        "file": ROOT / file_match.group(1),
        "line": int(file_match.group(2)),
        "owner": owner,
        "method": method,
        "argument": missing.group(1),
    }


def patch_backtest_test(info):
    path = info["file"]

    if not path.exists():
        return False

    text = path.read_text(encoding="utf-8")

    old = """validation = backtest.run(
        [
            {"profit":100},
            {"profit":-50},
            {"profit":120}
        ]
    )"""

    new = """validation = backtest.run(
        "TEST",
        [
            {"close": 100.0},
            {"close": 110.0},
            {"close": 95.0},
            {"close": 120.0},
        ],
        tp=20,
        sl=10,
    )"""

    if old not in text:
        print("[PATCH] Expected legacy BacktestEngine call not found")
        return False

    backup = backup_file(path)

    text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

    print(f"[PATCH] {path}")
    print(f"[BACKUP] {backup}")

    compile_result = compile_app()

    if compile_result.returncode != 0:
        restore_file(path, backup)
        print("[ROLLBACK] compile failed")
        print(compile_result.stdout[-3000:])
        return False

    test_result = pytest()

    if test_result.returncode == 0:
        print("[KEEP] patch passed all tests")
        return True

    restore_file(path, backup)

    print("[ROLLBACK] tests failed")
    print(test_result.stdout[-5000:])

    return False


def main():
    print("=" * 72)
    print("TRADE-AI AUTO REPAIR ENGINE v3")
    print("PATCH -> COMPILE -> TEST -> KEEP/ROLLBACK")
    print("=" * 72)

    for round_no in range(1, MAX_ROUNDS + 1):
        print(f"\n--- ROUND {round_no}/{MAX_ROUNDS} ---")

        result = pytest()

        if result.returncode == 0:
            print("\nAUTO REPAIR: ALL TESTS PASS")
            return 0

        output = result.stdout
        info = find_signature_mismatch(output)

        if not info:
            print("\n[AUTO REPAIR STOPPED]")
            print("No safe known repair pattern detected.")
            print(output[-7000:])
            return 1

        print("[DETECTED]", info)

        if (
            info["owner"] == "backtest"
            and info["method"] == "run"
            and info["argument"] == "candles"
        ):
            if patch_backtest_test(info):
                continue

        print("\n[AUTO REPAIR STOPPED]")
        print("Detected error is not in the safe repair rule set.")
        print(output[-7000:])
        return 1

    print("\n[AUTO REPAIR STOPPED] Maximum rounds reached")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
