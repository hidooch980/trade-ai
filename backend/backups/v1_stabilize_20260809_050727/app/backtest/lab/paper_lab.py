class PaperTradingLab:
    def __init__(self):
        self.trades=[]

    def add_trade(self,trade):
        self.trades.append(trade)
        return trade

    def report(self):
        wins=[t for t in self.trades if t.get("pnl",0)>0]
        losses=[t for t in self.trades if t.get("pnl",0)<=0]

        total=len(self.trades)

        return {
            "total_trades":total,
            "wins":len(wins),
            "losses":len(losses),
            "win_rate":round((len(wins)/total)*100,2) if total else 0
        }

paper_lab=PaperTradingLab()
