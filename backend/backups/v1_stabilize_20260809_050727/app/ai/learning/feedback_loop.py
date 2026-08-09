from app.ai.journal.trade_journal import trade_journal
from app.ai.memory.strategy_memory import strategy_memory


class FeedbackLoop:

    def analyze(self, symbol, timeframe):

        history = trade_journal.history(limit=5000)

        trades = [
            t for t in history
            if isinstance(t, dict)
            and t.get("symbol") == symbol
            and t.get("status") == "CLOSED"
        ]

        if not trades:
            return {
                "symbol": symbol,
                "timeframe": timeframe,
                "closed_trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0,
                "profit": 0,
                "strategy": strategy_memory.get(symbol, timeframe),
                "status": "NO_CLOSED_TRADES"
            }

        wins = [
            t for t in trades
            if float(t.get("profit", 0) or 0) > 0
        ]

        losses = [
            t for t in trades
            if float(t.get("profit", 0) or 0) <= 0
        ]

        total_profit = sum(
            float(t.get("profit", 0) or 0)
            for t in trades
        )

        win_rate = (
            len(wins) / len(trades) * 100
        )

        strategy = strategy_memory.get(
            symbol,
            timeframe
        )

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "closed_trades": len(trades),
            "wins": len(wins),
            "losses": len(losses),
            "win_rate": round(win_rate, 2),
            "profit": total_profit,
            "strategy": strategy,
            "status": "ANALYZED"
        }


feedback_loop = FeedbackLoop()
