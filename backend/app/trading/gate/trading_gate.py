class TradingGate:


    def validate(self, data):

        checks = {

            "risk":
                data.get("risk_safe", False),

            "backtest":
                data.get("backtest_ok", False),

            "win_rate":
                data.get("win_rate", 0) >= 55,

            "news":
                data.get("news_safe", False),

            "market":
                data.get("market_ready", False)
        }


        approved = all(
            checks.values()
        )


        return {

            "approved": approved,

            "checks": checks,

            "reason":
                "All safety checks passed"
                if approved
                else "Trade blocked by safety layer"
        }
