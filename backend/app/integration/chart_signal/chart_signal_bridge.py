class ChartSignalBridge:

    def __init__(
        self,
        signal_engine
    ):
        self.signal_engine = signal_engine


    def enrich(
        self,
        signal,
        smart_money,
        chart_structure
    ):

        signal["smart_money"] = smart_money

        signal["chart_structure"] = chart_structure


        if smart_money.get("decision") == "BUY":

            signal["confidence"] += 10


        return signal
