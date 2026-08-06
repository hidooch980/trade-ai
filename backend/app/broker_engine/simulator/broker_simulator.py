BROKERS={
"Broker_A":{"spread":0.2,"commission":0,"slippage":0.1},
"Broker_B":{"spread":0.3,"commission":1,"slippage":0.05},
"Broker_C":{"spread":0.15,"commission":0.5,"slippage":0.2}
}

def compare_brokers():
    return sorted(BROKERS.items(),key=lambda x:x[1]["spread"])

def execution_cost(broker,volume):
    data=BROKERS.get(broker)
    if not data:
        return None
    return {
        "broker":broker,
        "spread_cost":data["spread"]*volume,
        "commission":data["commission"]*volume,
        "slippage":data["slippage"]
    }
