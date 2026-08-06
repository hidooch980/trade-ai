class InstitutionalAI:

    def analyze(self,market):

        liquidity=market.get("liquidity",0)
        volume=market.get("volume",0)
        structure=market.get("structure","UNKNOWN")

        score=50

        if liquidity>0:
            score+=20

        if volume>0:
            score+=15

        if structure=="SHIFT":
            score+=15

        if score>=80:
            decision="STRONG_SETUP"

        elif score>=60:
            decision="VALID_SETUP"

        else:
            decision="NO_SETUP"

        return {
            "score":score,
            "decision":decision,
            "liquidity":liquidity,
            "structure":structure
        }


institutional_ai=InstitutionalAI()
