class TradingPipeline:

    def __init__(
        self,
        signal_engine,
        risk_engine,
        trade_manager
    ):

        self.signal_engine = signal_engine
        self.risk_engine = risk_engine
        self.trade_manager = trade_manager


    def execute(
        self,
        market_data
    ):

        signal = self.signal_engine(
            market_data
        )


        if signal.get("decision") == "WAIT":

            return {
                "status": "NO_TRADE",
                "signal": signal
            }


        risk = self.risk_engine(
            signal
        )


        if not risk.get("approved"):

            return {
                "status": "RISK_REJECTED",
                "risk": risk
            }


        trade = self.trade_manager(
            signal
        )


        return {

            "status": "EXECUTED",

            "signal": signal,

            "risk": risk,

            "trade": trade

        }
