import requests
from datetime import datetime


class NewsIntelligenceEngine:


    def __init__(self):

        self.sources = [
            "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        ]


    def collect(self):

        news = []

        for url in self.sources:

            try:

                response = requests.get(
                    url,
                    timeout=10
                )

                data = response.json()


                for item in data:

                    news.append(
                        {
                            "time": item.get("date"),
                            "currency": item.get("country"),
                            "title": item.get("title"),
                            "impact": item.get("impact")
                        }
                    )


            except Exception:
                continue


        return news



    def analyze_market_impact(
        self,
        currency
    ):

        news = self.collect()

        impact_score = 0
        events = []


        for item in news:

            if item.get(
                "currency"
            ) == currency:

                events.append(
                    item
                )

                if item.get(
                    "impact"
                ) == "High":

                    impact_score -= 30



        return {

            "currency": currency,

            "news_score": impact_score,

            "events": events

        }



news_intelligence_engine = NewsIntelligenceEngine()
