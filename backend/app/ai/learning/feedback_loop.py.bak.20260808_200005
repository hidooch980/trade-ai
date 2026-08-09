from app.ai.journal.trade_journal import trade_journal
from app.ai.memory.strategy_memory import strategy_memory


class FeedbackLoop:


    def analyze(
        self,
        symbol,
        timeframe
    ):

        history = trade_journal.history()


        trades = [
            t for t in history
            if t["symbol"] == symbol
            and t.get("status") == "CLOSED"
        ]


        if not trades:
            return {
                "status":"NO_CLOSED_TRADES"
            }


        wins = [
            t for t in trades
            if t.get("profit",0) > 0
        ]


        losses = [
            t for t in trades
            if t.get("profit",0) <= 0
        ]


        total_profit = sum(
            t.get("profit",0)
            for t in trades
        )


        win_rate = (
            len(wins) / len(trades)
        ) * 100


        strategy = strategy_memory.get(
            symbol,
            timeframe
        )


        return {
            "symbol":symbol,
            "closed_trades":len(trades),
            "wins":len(wins),
            "losses":len(losses),
            "win_rate":round(win_rate,2),
            "profit":total_profit,
            "strategy":strategy,
            "status":"ANALYZED"
        }


feedback_loop = FeedbackLoop()
