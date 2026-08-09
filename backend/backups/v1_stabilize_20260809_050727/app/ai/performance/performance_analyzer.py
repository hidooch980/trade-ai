class PerformanceAnalyzer:

    def analyze(self, trades):

        if not trades:
            return {
                "trades":0,
                "win_rate":0,
                "profit":0,
                "loss":0
            }


        wins = [
            t for t in trades
            if t.get("pnl",0) > 0
        ]

        losses = [
            t for t in trades
            if t.get("pnl",0) < 0
        ]


        total_profit = sum(
            t.get("pnl",0)
            for t in wins
        )

        total_loss = sum(
            t.get("pnl",0)
            for t in losses
        )


        win_rate = (
            len(wins) / len(trades)
        ) * 100


        return {
            "trades": len(trades),
            "wins": len(wins),
            "losses": len(losses),
            "win_rate": round(win_rate,2),
            "profit": round(total_profit,2),
            "loss": round(total_loss,2),
            "net": round(
                total_profit + total_loss,
                2
            )
        }


performance_analyzer = PerformanceAnalyzer()
