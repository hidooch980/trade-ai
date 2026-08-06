from app.monitoring.realtime_monitor import RealTimeMonitor
from app.analytics.performance_service import PerformanceService
from app.dashboard.dashboard_service import DashboardService
from app.api_gateway.gateway import APIGateway


monitor = RealTimeMonitor()


monitor.record(
    "TRADE_OPEN",
    {
        "symbol": "XAUUSD",
        "side": "BUY"
    }
)


dashboard = DashboardService(
    PerformanceService()
)


gateway = APIGateway(
    monitor,
    dashboard
)


trades = [

    {
        "symbol": "XAUUSD",
        "result": "WIN",
        "profit": 50
    },

    {
        "symbol": "XAUUSD",
        "result": "LOSS",
        "profit": -20
    }

]


print("HEALTH:")
print(gateway.health())

print()

print("SYSTEM STATUS:")
print(gateway.system_status())

print()

print("DASHBOARD:")
print(gateway.dashboard_data(trades))
