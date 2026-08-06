class TicketManager:
    def __init__(self):
        self.counter=0

    def new(self):
        self.counter+=1
        return f"SIM-{self.counter}"

ticket_manager=TicketManager()
