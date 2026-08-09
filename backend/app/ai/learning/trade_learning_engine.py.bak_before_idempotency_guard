import json
from pathlib import Path
from datetime import datetime


FILE = Path("app/learning/data/trade_learning.json")


class TradeLearningEngine:

    def __init__(self):
        if not FILE.exists():
            FILE.write_text("[]")


    def record_trade(self, trade):

        data = json.loads(FILE.read_text())

        data.append({
            "time": datetime.utcnow().isoformat(),
            "trade": trade
        })

        FILE.write_text(
            json.dumps(
                data,
                indent=2
            )
        )

        return True


    def analyze(self):

        data = json.loads(FILE.read_text())

        wins = 0
        losses = 0

        for item in data:

            pnl = item.get("trade",{}).get("pnl",0)

            if pnl > 0:
                wins += 1

            elif pnl < 0:
                losses += 1


        total = wins + losses

        win_rate = (
            wins / total * 100
            if total
            else 0
        )


        return {
            "trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate,2)
        }


trade_learning_engine = TradeLearningEngine()
