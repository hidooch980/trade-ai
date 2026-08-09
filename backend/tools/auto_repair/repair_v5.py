#!/usr/bin/env python3

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


def run(args):
    return subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def backup(path):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = BACKUP / f"{path.name}.{ts}.bak"
    shutil.copy2(path, target)
    return target


def restore(path, target):
    shutil.copy2(target, path)


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


def patch_engine():
    path = ROOT / "app/backtest/backtest_engine.py"
    text = path.read_text(encoding="utf-8")

    if "async def run(" in text and "await self.pipeline.generate(" in text:
        print("[INFO] BacktestEngine already async")
        return False

    old = """    def run(
        self,
        symbol,
        candles,
        tp=20,
        sl=10
    ):
"""

    new = """    async def run(
        self,
        symbol,
        candles,
        tp=20,
        sl=10
    ):
"""

    if old not in text:
        print("[SAFE STOP] BacktestEngine.run signature not recognized")
        return False

    if "self.pipeline.generate(" not in text:
        print("[SAFE STOP] SignalPipeline.generate call not found")
        return False

    b = backup(path)

    text = text.replace(old, new, 1)

    text = text.replace(
        "signal = self.pipeline.generate(",
        "signal = await self.pipeline.generate(",
        1,
    )

    path.write_text(text, encoding="utf-8")

    print("[PATCH]", path)
    print("[BACKUP]", b)

    result = compile_app()

    if result.returncode != 0:
        restore(path, b)
        print("[ROLLBACK] compile failed")
        print(result.stdout[-5000:])
        return False

    return True


def patch_integration_test():
    path = ROOT / "tests/integration/test_trading_pipeline.py"

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

    new = """validation = await backtest.run(
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
        print("[SAFE STOP] Integration test pattern not recognized")
        return False

    b = backup(path)

    text = text.replace(old, new, 1)

    path.write_text(text, encoding="utf-8")

    print("[PATCH]", path)
    print("[BACKUP]", b)

    result = compile_app()

    if result.returncode != 0:
        restore(path, b)
        print("[ROLLBACK] integration compile failed")
        print(result.stdout[-5000:])
        return False

    return True


def main():
    print("=" * 72)
    print("TRADE-AI AUTO REPAIR ENGINE v5")
    print("BACKTEST ASYNC CONTRACT REPAIR")
    print("PATCH -> COMPILE -> TEST -> KEEP / ROLLBACK")
    print("=" * 72)

    print("\n[STEP 1] PATCH BACKTEST ENGINE")

    if not patch_engine():
        return 1

    print("\n[STEP 2] PATCH INTEGRATION TEST")

    if not patch_integration_test():
        print("[ROLLBACK] Integration test was not patched")
        return 1

    print("\n[STEP 3] FULL TEST SUITE")

    result = pytest()

    if result.returncode == 0:
        print("\n" + "=" * 72)
        print("AUTO REPAIR v5: PASS")
        print("ALL TESTS PASSED")
        print("=" * 72)
        return 0

    print("\n[TEST FAILURE]")
    print(result.stdout[-10000:])

    print("\n[AUTO REPAIR v5: ROLLBACK REQUIRED]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
