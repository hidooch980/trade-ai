class PerformanceService:

    def summarize(
        self,
        trades
    ):

        total = len(trades)

        wins = len([
            t for t in trades
            if t.get("result") == "WIN"
        ])

        losses = len([
            t for t in trades
            if t.get("result") == "LOSS"
        ])


        win_rate = 0

        if total:

            win_rate = round(
                (wins / total) * 100,
                2
            )


        profit = sum(
            t.get("profit", 0)
            for t in trades
        )


        return {

            "total_trades": total,

            "wins": wins,

            "losses": losses,

            "win_rate": win_rate,

            "net_profit": profit

        }
