class AIBusinessIntelligence:

    def __init__(self):
        self.kpis={}
        self.reports=[]
        self.forecasts=[]
        self.strategies=[]


    def calculate_kpi(self,name,value):

        self.kpis[name]=value


    def add_report(self,report):

        self.reports.append(report)


    def add_forecast(self,item):

        self.forecasts.append(item)


    def analyze_strategy(self,strategy):

        self.strategies.append(strategy)


    def dashboard(self):

        return {
            "kpis":len(self.kpis),
            "reports":len(self.reports),
            "forecasts":len(self.forecasts),
            "strategies":len(self.strategies),
            "business_intelligence":"ONLINE"
        }


bi=AIBusinessIntelligence()
