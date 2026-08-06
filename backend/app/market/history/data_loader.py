import csv


class HistoricalDataLoader:


    def load_csv(self, path):

        candles = []


        with open(path, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                candles.append({

                    "time": row.get("time"),

                    "open": float(row.get("open",0)),

                    "high": float(row.get("high",0)),

                    "low": float(row.get("low",0)),

                    "close": float(row.get("close",0)),

                    "volume": float(row.get("volume",0))

                })


        return candles



    def validate(self, candles):

        return {

            "valid":
                len(candles) > 0,

            "count":
                len(candles)

        }
