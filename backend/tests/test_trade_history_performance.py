from app.performance.history.trade_history import TradeHistory
from app.performance.win_rate_engine import WinRateEngine


history = TradeHistory()


history.save({
    "symbol": "XAUUSD",
    "side": "BUY",
    "result": "WIN",
    "profit": 40
})


history.save({
    "symbol": "XAUUSD",
    "side": "SELL",
    "result": "LOSS",
    "profit": -20
})


history.save({
    "symbol": "XAUUSD",
    "side": "BUY",
    "result": "WIN",
    "profit": 35
})


trades = history.all()


winrate = WinRateEngine().calculate(
    trades
)


print("TRADE HISTORY:")
print(trades)

print()

print("PERFORMANCE:")
print(winrate)
