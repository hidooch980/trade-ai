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


    validation = backtest.run(
        [
            {"profit":100},
            {"profit":-50},
            {"profit":120}
        ]
    )


    permission = gate.validate({

        "risk_safe": True,

        "backtest_ok":
            validation["approved"],

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
