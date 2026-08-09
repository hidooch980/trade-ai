from app.trading.services.trade_manager import TradeManager


result = TradeManager().open_trade(
    symbol="XAUUSD",
    decision="BUY",
    price=2450,
    volume=1.0
)


print("TRADE EXECUTION:")
print(result)
