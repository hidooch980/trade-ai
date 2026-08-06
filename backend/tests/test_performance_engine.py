from app.performance.performance_engine import PerformanceEngine


records = [
    {
        "symbol": "XAUUSD",
        "decision": "BUY",
        "result": "WIN"
    },
    {
        "symbol": "XAUUSD",
        "decision": "SELL",
        "result": "LOSS"
    },
    {
        "symbol": "XAUUSD",
        "decision": "BUY",
        "result": "WIN"
    },
    {
        "symbol": "BTCUSD",
        "decision": "BUY",
        "result": "WIN"
    },
    {
        "symbol": "EURUSD",
        "decision": "SELL",
        "result": "LOSS"
    }
]


result = PerformanceEngine().analyze(
    records
)


print("PERFORMANCE RESULT:")
print(result)
