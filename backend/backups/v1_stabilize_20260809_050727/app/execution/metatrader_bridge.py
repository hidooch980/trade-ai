import json
import os
from datetime import datetime


class MetaTraderBridge:


    def __init__(self):

        self.signal_file = (
            "app/learning/data/"
            "mt5_signal.json"
        )

        self.position_file = (
            "positions.json"
        )


    def send_signal(
        self,
        decision
    ):

        data = {

            "time":
                datetime.utcnow().isoformat(),

            "symbol":
                decision.get("symbol"),

            "action":
                decision.get("action"),

            "confidence":
                decision.get("confidence"),

            "risk":
                decision.get("risk")

        }


        with open(
            self.signal_file,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )


        return data



    def get_positions(self):

        if not os.path.exists(
            self.position_file
        ):

            return []


        with open(
            self.position_file
        ) as f:

            return json.load(f)



metatrader_bridge = MetaTraderBridge()
