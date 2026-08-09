class AccountRiskMonitor:


    def analyze(self, account):

        balance = account.get(
            "balance",
            0
        )

        equity = account.get(
            "equity",
            0
        )

        if balance <= 0:
            return {
                "status": "BLOCK",
                "reason": "Invalid balance"
            }


        drawdown = (
            (balance - equity)
            /
            balance
        ) * 100


        if drawdown >= 5:

            return {
                "status": "BLOCK",
                "reason": "Maximum drawdown reached",
                "drawdown": round(drawdown,2)
            }


        return {
            "status": "SAFE",
            "drawdown": round(drawdown,2)
        }
