from app.execution.position_monitor import position_monitor

class MarketMonitor:

    def update_price(self, prices):
        return position_monitor.update(prices)

market_monitor=MarketMonitor()
