from datetime import datetime


class PaperExecutor:


    def __init__(self):

        self.orders = []



    async def execute(self, order):

        record = {

            "status": "PAPER_FILLED",

            "symbol":
                order.get("symbol"),

            "side":
                order.get("decision"),

            "price":
                order.get("price"),

            "time":
                datetime.utcnow().isoformat()
        }


        self.orders.append(
            record
        )


        return record



    def history(self):

        return self.orders
