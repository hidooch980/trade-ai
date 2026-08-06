class PositionStore:

    def __init__(self):
        self.positions = []

    def add(self, position):
        for p in self.positions:
            if p.get("ticket")==position.get("ticket") and p.get("symbol")==position.get("symbol") and p.get("side")==position.get("side"):
                return p
        self.positions.append(position)
        return position

    def get_all(self):
        return self.positions

    def remove(self, ticket):
        self.positions = [
            p for p in self.positions
            if p.get("ticket") != ticket
        ]


position_store = PositionStore()
