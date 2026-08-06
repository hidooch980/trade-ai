from app.core.logging.logger import TradeLogger


logger = TradeLogger()


logger.info(
    "TRADE OPEN XAUUSD BUY 2450"
)


logger.info(
    "RISK APPROVED volume=1.0"
)


logger.error(
    "TEST ERROR EVENT"
)


print("LOGGING TEST COMPLETED")
