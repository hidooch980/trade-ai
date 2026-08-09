from app.monitoring.realtime_monitor import RealTimeMonitor


monitor = RealTimeMonitor()


monitor.record(
    "TRADE_OPEN",
    {
        "symbol": "XAUUSD",
        "side": "BUY",
        "price": 2450
    }
)


monitor.record(
    "SIGNAL_GENERATED",
    {
        "decision": "BUY",
        "confidence": 85
    }
)


monitor.record(
    "RISK_APPROVED",
    {
        "volume": 10
    }
)


status = monitor.status()


print("MONITOR STATUS:")
print(status)
