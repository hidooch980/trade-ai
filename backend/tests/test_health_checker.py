from app.health.health_checker import HealthChecker


health = HealthChecker()


health.register(
    "MARKET_DATA",
    True
)

health.register(
    "AI_ENGINE",
    True
)

health.register(
    "RISK_GOVERNOR",
    True
)

health.register(
    "TRADE_MANAGER",
    True
)

health.register(
    "SECURITY",
    True
)

health.register(
    "BACKUP",
    True
)


result = health.check()


print("SYSTEM HEALTH:")
print(result)
