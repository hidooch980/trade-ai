from app.execution.break_even import break_even
from app.execution.trailing_stop import trailing_stop
from app.execution.position_store import position_store
from app.execution.close_manager import close_manager
from app.market.bridge.mt5_bridge import mt5_bridge


class PositionMonitor:

    def check(self, positions, prices):
        actions = []

        for p in positions:

            if p.get("status") != "OPEN":
                continue

            if not isinstance(prices, dict):
                continue

            symbol = p.get("symbol")

            if symbol not in prices:
                continue

            current = prices[symbol]
            entry = p.get("entry_price", 0)
            volume = p.get("volume", 0)

            if p.get("side") == "BUY":

                pnl = (current - entry) * volume

                if (
                    p.get("take_profit") is not None
                    and current >= p["take_profit"]
                ):
                    actions.append({
                        "ticket": p["ticket"],
                        "action": "CLOSE",
                        "reason": "TAKE_PROFIT",
                        "price": current,
                        "pnl": pnl
                    })

                elif (
                    p.get("stop_loss") is not None
                    and current <= p["stop_loss"]
                ):
                    actions.append({
                        "ticket": p["ticket"],
                        "action": "CLOSE",
                        "reason": "STOP_LOSS",
                        "price": current,
                        "pnl": pnl
                    })

            else:

                pnl = (entry - current) * volume

                if (
                    p.get("take_profit") is not None
                    and current <= p["take_profit"]
                ):
                    actions.append({
                        "ticket": p["ticket"],
                        "action": "CLOSE",
                        "reason": "TAKE_PROFIT",
                        "price": current,
                        "pnl": pnl
                    })

                elif (
                    p.get("stop_loss") is not None
                    and current >= p["stop_loss"]
                ):
                    actions.append({
                        "ticket": p["ticket"],
                        "action": "CLOSE",
                        "reason": "STOP_LOSS",
                        "price": current,
                        "pnl": pnl
                    })

        return actions

    async def check_and_execute(self, prices):
        actions = self.check(
            position_store.get_all(),
            prices
        )

        executed = []

        for action in actions:

            if action.get("action") != "CLOSE":
                continue

            result = await close_manager.close(
                mt5_bridge,
                action["ticket"],
                exit_price=action.get("price"),
                reason=action.get(
                    "reason",
                    "EXIT_TRIGGERED"
                )
            )

            item = dict(action)
            item["executed"] = result.get("closed") is True
            item["close_result"] = result

            executed.append(item)

        return executed

    def update(self, prices):
        changed = False

        for p in position_store.get_all():

            if p.get("status") != "OPEN":
                continue

            if isinstance(prices, dict):
                symbol = p.get("symbol")

                if symbol not in prices:
                    continue

                price = prices[symbol]
            else:
                price = prices

            old_price = p.get("current_price")
            old_pnl = p.get("pnl")
            old_sl = p.get("stop_loss")

            p["current_price"] = price

            trailing_stop.update(p)
            break_even.update(p)

            if p.get("side") == "BUY":
                p["pnl"] = (
                    price - p.get("entry_price", 0)
                ) * p.get("volume", 0)
            else:
                p["pnl"] = (
                    p.get("entry_price", 0) - price
                ) * p.get("volume", 0)

            if (
                p.get("current_price") != old_price
                or p.get("pnl") != old_pnl
                or p.get("stop_loss") != old_sl
            ):
                changed = True

        if changed:
            position_store.save()

        return position_store.get_all()


position_monitor = PositionMonitor()
