class MultiTimeframe:

    def __init__(self):
        self.frames = {
            "M1": [],
            "M5": [],
            "M15": [],
            "H1": []
        }


    def add(self, candle):

        for tf in self.frames:

            self.frames[tf].append(candle)

            if len(self.frames[tf]) > 200:
                self.frames[tf].pop(0)


        return self.frames


    def get(self, timeframe):

        return self.frames.get(
            timeframe,
            []
        )
