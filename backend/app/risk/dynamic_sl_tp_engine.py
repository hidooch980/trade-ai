class DynamicSLTPEngine:

    def calculate(
        self,
        side,
        entry,
        atr,
        risk_reward=3,
        symbol=None
    ):

        if atr <= 0:
            if symbol in ["XAUUSD"]:
                atr = entry * 0.005
            elif symbol in ["BTCUSD"]:
                atr = entry * 0.01
            else:
                atr = entry * 0.001

        if side == "BUY":

            stop_loss = entry - (atr * 2)
            take_profit = entry + (atr * risk_reward)

        elif side == "SELL":

            stop_loss = entry + (atr * 2)
            take_profit = entry - (atr * risk_reward)

        else:
            return {
                "approved": False,
                "reason": "INVALID_SIDE"
            }

        if stop_loss <= 0 or take_profit <= 0:
            return {
                "approved": False,
                "reason": "INVALID_PRICE_LEVEL"
            }

        return {
            "approved": True,
            "side": side,
            "entry": entry,
            "stop_loss": round(stop_loss, 5),
            "take_profit": round(take_profit, 5),
            "risk_reward": risk_reward,
            "atr": atr
        }


dynamic_sl_tp_engine = DynamicSLTPEngine()
