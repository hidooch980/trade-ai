import os

from app.core.config.config_manager import ConfigManager


os.environ["ENVIRONMENT"] = "production"
os.environ["DEFAULT_SYMBOL"] = "XAUUSD"
os.environ["RISK_PERCENT"] = "1.5"
os.environ["MAX_DRAWDOWN"] = "8"


config = ConfigManager()


result = config.trading_config()


print("TRADING CONFIG:")
print(result)
