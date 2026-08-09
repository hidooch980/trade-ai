#!/usr/bin/env python3

import inspect
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path("/opt/trade-ai/backend")
LOG = ROOT / "logs" / "auto_repair"
BACKUP = LOG / "backups"

LOG.mkdir(parents=True, exist_ok=True)
BACKUP.mkdir(parents=True, exist_ok=True)

MAX_ROUNDS = 5


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
    return run([
        sys.executable,
        "-m",
        "compileall",
        "-q",
        "app",
    ])


def pytest():
    return run([
        sys.executable,
        "-m",
        "pytest",
        "-q",
    ])


def patch_async_backtest():
    path = ROOT / "app/backtest/backtest_engine.py"

    if not path.exists():
        return False

    text = path.read_text(encoding="utf-8")

    old_signature = """    def run(
        self,
        symbol,
        candles,
        tp=20,
        sl=10
    ):
"""

    new_signature = """    async def run(
        self,
        symbol,
        candles,
        tp=20,
        sl=10
    ):
"""

    old_call = """                signal = self.pipeline.generate(
                symbol,
                price
            )
"""

    new_call = """                signal = await self.pipeline.generate(
                symbol,
                price
            )
"""

    if "async def run(" in text and "await self.pipeline.generate(" in text:
        print("[INFO] BacktestEngine async patch already present")
        return False

    if old_signature not in text:
        print("[SAFE STOP] BacktestEngine.run signature not recognized")
        return False

    if "self.pipeline.generate(" not in text:
        print("[SAFE STOP] SignalPipeline.generate call not found")
        return False

    backup = backup_file(path)

    text = text.replace(old_signature, new_signature, 1)

    text = re.sub(
        r"signal = self\.pipeline\.generate\(",
        "signal = await self.pipeline.generate(",
        text,
        count=1,
    )

    path.write_text(text, encoding="utf-8")

    print("[PATCH]", path)
    print("[BACKUP]", backup)

    compile_result = compile_app()

    if compile_result.returncode != 0:
        restore_file(path, backup)
        print("[ROLLBACK] compile failed")
        print(compile_result.stdout[-5000:])
        return False

    test_result = pytest()

    if test_result.returncode == 0:
        print("[KEEP] async backtest patch passed all tests")
        return True

    restore_file(path, backup)

    print("[ROLLBACK] tests failed")
    print(test_result.stdout[-7000:])

    return False


def main():
    print("=" * 72)
    print("TRADE-AI AUTO REPAIR ENGINE v4")
    print("ASYNC CONTRACT REPAIR")
    print("PATCH -> COMPILE -> TEST -> KEEP/ROLLBACK")
    print("=" * 72)

    for round_no in range(1, MAX_ROUNDS + 1):
        print(f"\n--- ROUND {round_no}/{MAX_ROUNDS} ---")

        result = pytest()

        if result.returncode == 0:
            print("\nAUTO REPAIR: ALL TESTS PASS")
            return 0

        output = result.stdout

        async_error = (
            "coroutine" in output
            and "object is not subscriptable" in output
            and "SignalPipeline.generate" in output
        )

        if async_error:
            print("[DETECTED] ASYNC_CONTRACT_MISMATCH")

            if patch_async_backtest():
                continue

        print("\n[AUTO REPAIR STOPPED]")
        print(output[-7000:])
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
