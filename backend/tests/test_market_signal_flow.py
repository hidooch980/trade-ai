from app.market_data.connectors.market_connector import MarketConnector
from app.integration.market.market_signal_bridge import MarketSignalBridge


connector = MarketConnector()

connector.connect()


market_data = connector.get_price(
    "XAUUSD"
)


bridge = MarketSignalBridge(
    None
)


result = bridge.analyze(
    market_data
)


print("MARKET DATA:")
print(market_data)

print()

print("SIGNAL FLOW:")
print(result)
