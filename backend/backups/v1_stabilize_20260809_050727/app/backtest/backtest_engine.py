from datetime import datetime

from app.trading.pipeline.signal_pipeline import SignalPipeline
from app.backtest.trade_record import TradeRecord
from app.backtest.performance import performance


class BacktestEngine:

    def __init__(self):
        self.pipeline = SignalPipeline()
        self.trades = []


    def run(
        self,
        symbol,
        candles,
        tp=20,
        sl=10
    ):

        self.trades = []

        position = None


        for candle in candles:

            price = candle["close"]

            signal = self.pipeline.generate(
                symbol,
                price
            )

            decision = signal["decision"]["decision"]


            if decision == "BUY" and position is None:

                position = {
                    "entry_price": price
                }


            if position:

                profit = price - position["entry_price"]


                if profit >= tp or profit <= -sl:

                    trade = TradeRecord(
                        symbol,
                        "BUY",
                        position["entry_price"],
                        price,
                        1,
                        profit,
                        datetime.utcnow()
                    )

                    self.trades.append(trade)

                    position = None


        report = performance.analyze(
            self.trades
        )

        return {
            "performance": report,
            "trades":[
                t.to_dict()
                for t in self.trades
            ],
            "count":len(self.trades),
            "profit":sum(
                t.profit
                for t in self.trades
            )
        }


backtest_engine = BacktestEngine()
