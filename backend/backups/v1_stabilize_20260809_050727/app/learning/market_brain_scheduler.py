import json
import os
from datetime import datetime

from app.learning.market_universe import market_universe
from app.decision.master_ai_core import master_ai_core


class MarketBrainScheduler:


    def __init__(self):

        self.output = (
            "app/learning/data/"
            "ai_market_signals.json"
        )


    def run(self):

        results = []

        assets = market_universe.get_assets()


        for symbol in assets:

            try:

                result = master_ai_core.decide(
                    symbol
                )

                if result["action"] != "WAIT":

                    results.append(
                        result
                    )

            except Exception:
                continue


        results.sort(
            key=lambda x: x.get(
                "confidence",
                0
            ),
            reverse=True
        )


        os.makedirs(
            os.path.dirname(self.output),
            exist_ok=True
        )


        with open(
            self.output,
            "w"
        ) as f:

            json.dump(
                {
                    "time": datetime.utcnow().isoformat(),
                    "signals": results[:20]
                },
                f,
                indent=2
            )


        return {
            "scanned": len(assets),
            "signals": len(results)
        }



market_brain_scheduler = MarketBrainScheduler()
