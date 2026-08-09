import os


class ConfigManager:

    def get(
        self,
        key,
        default=None
    ):

        return os.getenv(
            key,
            default
        )


    def trading_config(self):

        return {

            "environment": self.get(
                "ENVIRONMENT",
                "development"
            ),

            "symbol": self.get(
                "DEFAULT_SYMBOL",
                "XAUUSD"
            ),

            "risk_percent": float(
                self.get(
                    "RISK_PERCENT",
                    2
                )
            ),

            "max_drawdown": float(
                self.get(
                    "MAX_DRAWDOWN",
                    10
                )
            )

        }
