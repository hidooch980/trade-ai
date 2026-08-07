from datetime import datetime
from app.broker.mt5.mt5_connector import MT5Connector
from app.execution.position_store import position_store
from app.execution.ticket_manager import ticket_manager
from app.execution.position_manager import position_manager

class MT5Bridge(MT5Connector):

    def __init__(self):
        self.connected=False
        self.last_price=0

    async def connect(self):
        self.connected=True
        return {"status":"CONNECTED","platform":"MT5","mode":"SIMULATION"}

    async def get_tick(self,symbol):
        if not self.connected:
            await self.connect()
        return {
            "symbol":symbol,
            "price":self.last_price,
            "volume":0,
            "time":datetime.utcnow().isoformat(),
            "source":"MT5_SIMULATION"
        }

    async def get_account(self):
        return {
            "balance":10000,
            "equity":10000,
            "currency":"USD"
        }

    async def get_positions(self):
        return position_store.get_all()


    async def get_positions_with_pnl(self, symbol=None, price=None):
        positions = position_store.get_all()

        result=[]

        for p in positions:
            if symbol and p.get("symbol") != symbol:
                continue

            current = price if price is not None else p.get("current_price", p.get("entry_price",0))

            entry = p.get("entry_price",0)
            volume = p.get("volume",0)

            if p.get("side") == "BUY":
                pnl = (current - entry) * volume
            else:
                pnl = (entry - current) * volume

            item = dict(p)
            item["current_price"] = current
            item["pnl"] = pnl

            result.append(item)

        return result

    async def send_order(self,order):
        self.last_price=order.get("price",0)

        check=position_manager.can_open(
            order["symbol"],
            order["side"],
            position_store.get_all()
        )

        if not check["allowed"]:
            return {
                "sent":False,
                "reason":check["reason"]
            }

        stop_loss = order.get("stop_loss")
        take_profit = order.get("take_profit")

        if stop_loss is None or take_profit is None:
            if order["side"] == "BUY":
                stop_loss = self.last_price - 10
                take_profit = self.last_price + 20
            else:
                stop_loss = self.last_price + 10
                take_profit = self.last_price - 20

        position={
            "ticket":ticket_manager.new(),
            "symbol":order["symbol"],
            "side":order["side"],
            "volume":order["volume"],
            "entry_price":self.last_price,
            "current_price":self.last_price,
            "pnl":0.0,
            "stop_loss":stop_loss,
            "take_profit":take_profit,
            "status":"OPEN"
        }

        position_store.add(position)

        return {
            "sent":True,
            "platform":"MT5",
            "mode":"SIMULATION",
            "ticket":position["ticket"],
            "order":order
        }

mt5_bridge=MT5Bridge()
