from app.analytics.performance_service import PerformanceService


trades = [

    {
        "symbol": "XAUUSD",
        "result": "WIN",
        "profit": 50
    },

    {
        "symbol": "XAUUSD",
        "result": "LOSS",
        "profit": -25
    },

    {
        "symbol": "XAUUSD",
        "result": "WIN",
        "profit": 40
    },

    {
        "symbol": "XAUUSD",
        "result": "WIN",
        "profit": 30
    }

]


result = PerformanceService().summarize(
    trades
)


print("DASHBOARD METRICS:")
print(result)
