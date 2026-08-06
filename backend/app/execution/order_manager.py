from app.execution.position_store import position_store

class OrderManager:
    def open(self,order):
        if any(p["symbol"]==order["symbol"] and p["side"]==order["side"] for p in position_store.get_all()):
            return {"opened":False,"reason":"DUPLICATE_POSITION"}
        position_store.add(order)
        return {"opened":True,"order":order}

    def close(self,ticket):
        position_store.remove(ticket)
        return {"closed":True,"ticket":ticket}

order_manager=OrderManager()
