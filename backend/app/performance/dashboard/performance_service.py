class PerformanceService:


    def summarize(self, trades):

        total = len(trades)

        wins = len(
            [
                t for t in trades
                if t.get("result") == "WIN"
            ]
        )

        losses = total - wins


        return {

            "total_trades": total,

            "wins": wins,

            "losses": losses,

            "win_rate":
                round(
                    (wins / total) * 100,
                    2
                )
                if total else 0,

            "status":
                "HEALTHY"
                if total == 0 or wins / total >= 0.55
                else "NEEDS_OPTIMIZATION"
        }
