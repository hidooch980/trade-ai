class PerformanceAnalyzer:


    def analyze(self, trades, initial_balance=10000):

        total = len(trades)

        if total == 0:
            return {
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0,
                "profit": 0,
                "final_balance": initial_balance,
                "max_drawdown": 0,
                "profit_factor": 0
            }


        wins = [
            t.profit
            for t in trades
            if t.profit > 0
        ]

        losses = [
            t.profit
            for t in trades
            if t.profit <= 0
        ]


        total_profit = sum(wins)

        total_loss = abs(
            sum(losses)
        )


        balance = initial_balance
        peak = balance
        max_drawdown = 0

        equity = []


        for trade in trades:

            balance += trade.profit

            equity.append(balance)


            if balance > peak:
                peak = balance


            drawdown = (
                (peak - balance)
                / peak
            ) * 100


            if drawdown > max_drawdown:
                max_drawdown = drawdown



        profit_factor = (
            total_profit / total_loss
            if total_loss > 0
            else 0
        )


        return {

            "trades": total,

            "wins": len(wins),

            "losses": len(losses),

            "win_rate": round(
                (len(wins)/total)*100,
                2
            ),

            "profit": round(
                sum(
                    t.profit
                    for t in trades
                ),
                2
            ),

            "final_balance": round(
                balance,
                2
            ),

            "max_drawdown": round(
                max_drawdown,
                2
            ),

            "profit_factor": round(
                profit_factor,
                2
            ),

            "equity_curve": equity
        }


performance = PerformanceAnalyzer()
