import json
import os
from datetime import datetime


class ExecutionEngineV2:


    def __init__(self):

        self.file = "positions.json"


    def load_positions(self):

        if not os.path.exists(
            self.file
        ):
            return []

        with open(
            self.file
        ) as f:

            return json.load(f)



    def save_positions(
        self,
        positions
    ):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                positions,
                f,
                indent=2
            )



    def open_trade(
        self,
        signal
    ):

        positions = self.load_positions()


        for p in positions:

            if (
                p.get("symbol")
                ==
                signal.get("symbol")
                and
                p.get("status")
                ==
                "OPEN"
            ):

                return {
                    "status":
                    "SKIPPED",
                    "reason":
                    "position exists"
                }



        trade = {

            "ticket":
                len(positions)+1,

            "symbol":
                signal.get("symbol"),

            "side":
                signal.get("action"),

            "entry":
                signal.get("price"),

            "risk":
                signal.get("risk"),

            "status":
                "OPEN",

            "time":
                datetime.utcnow().isoformat()

        }


        positions.append(
            trade
        )

        self.save_positions(
            positions
        )


        return {
            "status":
            "OPENED",
            "trade":
            trade
        }



execution_engine_v2 = ExecutionEngineV2()
