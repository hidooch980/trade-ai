import asyncio

from app.performance import WinRateEngine
from app.backtest import BacktestEngine
from app.trading.gate import TradingGate
from app.broker.bridge import MT5Bridge


async def run_test():

    win = WinRateEngine()

    backtest = BacktestEngine()

    gate = TradingGate()

    bridge = MT5Bridge()


    await bridge.connect()


    performance = win.calculate(
        [
            {"result":"WIN"},
            {"result":"WIN"},
            {"result":"LOSS"}
        ]
    )


    validation = await backtest.run(
        "TEST",
        [
            {"close": 100.0},
            {"close": 110.0},
            {"close": 95.0},
            {"close": 120.0},
        ],
        tp=20,
        sl=10,
    )


    permission = gate.validate({

        "risk_safe": True,

        "backtest_ok":
            validation["count"] >= 0,

        "win_rate":
            performance["win_rate"],

        "news_safe": True,

        "market_ready": True

    })


    print({

        "win_rate":
            performance,

        "backtest":
            validation,

        "trade_permission":
            permission

    })


asyncio.run(run_test())
