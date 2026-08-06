class PerformanceEngine:

    def analyze(self, records):

        total = len(records)

        wins = len([
            r for r in records
            if r.get("result") == "WIN"
        ])

        losses = len([
            r for r in records
            if r.get("result") == "LOSS"
        ])

        win_rate = 0

        if total:
            win_rate = round(
                (wins / total) * 100,
                2
            )

        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate
        }
