import asyncio
from app.market_data.historical.loaders.csv_loader import CSVMarketLoader
from app.market_data.historical.loaders.historical_service import HistoricalDataService
from app.backtest.backtest_adapter import BacktestAdapter
from app.performance.win_rate_engine import WinRateEngine

async def main():

    loader = CSVMarketLoader()

    historical = HistoricalDataService(
        loader
    )

    data = historical.load_and_validate(
        "tests/data/XAUUSD_H1.csv"
    )

    candles = data["valid_candles"]

    backtest = BacktestAdapter()

    result = await backtest.run(
        candles
    )

    simulated_trades = [
        {"result": "WIN"},
        {"result": "WIN"},
        {"result": "LOSS"}
    ]

    winrate = WinRateEngine().calculate(
        simulated_trades
    )

    print("BACKTEST:", result)
    print("WIN RATE:", winrate)

asyncio.run(main())
