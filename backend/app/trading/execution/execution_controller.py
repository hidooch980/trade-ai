class ExecutionController:


    def __init__(self, connector, gate):

        self.connector = connector
        self.gate = gate



    async def execute(self, decision):

        validation = self.gate.validate(
            decision
        )


        if not validation["approved"]:

            return {
                "status": "BLOCKED",
                "validation": validation
            }


        result = await self.connector.send_order(
            decision
        )


        return {
            "status": "EXECUTED",
            "order": result
        }
