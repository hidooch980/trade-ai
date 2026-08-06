from app.market_data.connectors.market_connector import MarketConnector


connector = MarketConnector()


connect = connector.connect()


price = connector.get_price(
    "XAUUSD"
)


print("CONNECT:")
print(connect)

print()

print("MARKET PRICE:")
print(price)
