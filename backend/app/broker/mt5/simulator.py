from .mt5_connector import MT5Connector


class MT5Simulator(MT5Connector):

    async def connect(self):

        return {
            "status": "connected",
            "platform": "MT5 Simulator"
        }


    async def get_account(self):

        return {
            "balance": 10000,
            "equity": 10000,
            "margin": 0
        }


    async def get_positions(self):

        return []


    async def send_order(self, order):

        return {
            "status": "accepted",
            "order": order
        }
