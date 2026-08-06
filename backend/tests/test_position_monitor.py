from app.trading.services.position_monitor import PositionMonitor


position = {
    "symbol": "XAUUSD",
    "side": "BUY",
    "entry_price": 2450,
    "volume": 1.0,
    "stop_loss": 2430,
    "take_profit": 2490,
    "status": "OPEN"
}


monitor = PositionMonitor()


result = monitor.check(
    position,
    current_price=2495
)


print("POSITION MONITOR RESULT:")
print(result)
