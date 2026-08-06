class WinRateEngine:

    def calculate(self, results):

        wins = 0
        losses = 0

        for trade in results:

            decision = trade.get("result")

            if decision == "WIN":
                wins += 1

            elif decision == "LOSS":
                losses += 1

        total = wins + losses

        win_rate = round(
            (wins / total) * 100, 2
        ) if total else 0

        return {
            "win_rate": win_rate,
            "wins": wins,
            "losses": losses,
            "total": total
        }
