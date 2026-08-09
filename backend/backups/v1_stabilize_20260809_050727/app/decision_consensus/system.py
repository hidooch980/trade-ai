class DecisionConsensusAI:

    def __init__(self):
        self.decisions=[]
        self.votes=[]


    def add_vote(self,agent,decision,confidence):

        vote={
            "agent":agent,
            "decision":decision,
            "confidence":confidence
        }

        self.votes.append(vote)

        return vote


    def calculate_consensus(self):

        if not self.votes:
            return None

        result={
            "votes":len(self.votes),
            "decision":"CONSENSUS_GENERATED"
        }

        self.decisions.append(result)

        return result


    def final_check(self,decision):

        return {
            "decision":decision,
            "status":"VERIFIED"
        }


    def status(self):

        return {
            "votes":len(self.votes),
            "decisions":len(self.decisions),
            "system":"ONLINE"
        }


decision_consensus=DecisionConsensusAI()
