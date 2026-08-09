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

        changed = False

        for p in positions:
            if symbol and p.get("symbol") != symbol:
                continue

            # CLOSED positions are immutable historical records.
            # Never recalculate or overwrite their realized PnL/current price.
            if p.get("status") == "CLOSED":
                result.append(dict(p))
                continue

            current = (
                price
                if price is not None
                else p.get(
                    "current_price",
                    p.get("entry_price", 0)
                )
            )

            entry_check = p.get("entry_price", 0)

            if entry_check and current:
                if abs(current - entry_check) > entry_check * 0.05:
                    current = entry_check

            entry = p.get("entry_price", 0)
            volume = p.get("volume", 0)

            if p.get("side") == "BUY":
                pnl = (current - entry) * volume
            else:
                pnl = (entry - current) * volume

            if (
                p.get("current_price") != current
                or p.get("pnl") != pnl
            ):
                p["current_price"] = current
                p["pnl"] = pnl
                changed = True

            result.append(dict(p))

        # Persist only changed OPEN market state.
        if changed:
            position_store.save()

        return result

    async def close_position(self, ticket, price=None):
        positions = position_store.get_all()

        for pos in positions:
            if pos.get("ticket") != ticket:
                continue

            if pos.get("status") != "OPEN":
                return {
                    "closed": False,
                    "reason": "POSITION_NOT_OPEN",
                    "ticket": ticket
                }

            close_price = (
                price
                if price is not None
                else pos.get("current_price", pos.get("entry_price", 0))
            )

            # Calculate final realized PNL before closing.
            entry = pos.get("entry_price", 0)
            volume = pos.get("volume", 0)

            if pos.get("side") == "BUY":
                final_pnl = (close_price - entry) * volume
            else:
                final_pnl = (entry - close_price) * volume

            # Complete the position lifecycle atomically before reporting success.
            pos["current_price"] = close_price
            pos["pnl"] = final_pnl
            pos["status"] = "CLOSED"
            pos["close_price"] = close_price
            pos["closed_at"] = datetime.utcnow().isoformat()
            position_store.save()

            return {
                "closed": True,
                "ticket": ticket,
                "symbol": pos.get("symbol"),
                "price": close_price,
                "platform": "MT5",
                "mode": "SIMULATION"
            }

        return {
            "closed": False,
            "reason": "POSITION_NOT_FOUND",
            "ticket": ticket
        }

    async def send_order(self, order):
        # HARD EXECUTION SAFETY GATE:
        # Never submit an order while the MT5 bridge is disconnected.
        if not self.connected:
            return {
                "sent": False,
                "reason": "BROKER_DISCONNECTED",
                "platform": "MT5",
            }

        if not isinstance(order, dict):
            return {
                "sent": False,
                "reason": "INVALID_ORDER",
                "platform": "MT5",
            }

        required = ("symbol", "side", "volume", "price", "stop_loss", "take_profit")
        if any(order.get(key) is None for key in required):
            return {
                "sent": False,
                "reason": "INCOMPLETE_ORDER",
                "platform": "MT5",
            }

        self.last_price = order.get("price", 0)

        check = position_manager.can_open(
            order["symbol"],
            order["side"],
            position_store.get_all()
        )

        if not check["allowed"]:
            return {
                "sent": False,
                "reason": check["reason"],
                "platform": "MT5",
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

        ticket = ticket_manager.new()

        position = {
            "ticket": ticket,
            "symbol": order["symbol"],
            "side": order["side"],
            "volume": order["volume"],
            "entry_price": order["price"],
            "current_price": order["price"],
            "pnl": 0.0,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "status": "OPEN",
            "opened_at": datetime.utcnow().isoformat(),
            "platform": "MT5",
            "mode": "SIMULATION"
        }

        position_store.add(position)

        return {
            "sent":True,
            "platform":"MT5",
            "mode":"SIMULATION",
            "ticket":ticket,
            "order":order
        }

mt5_bridge=MT5Bridge()
