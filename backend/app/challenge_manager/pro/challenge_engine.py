CHALLENGES={
"FUNDEDNEXT":{
"profit_target":10,
"daily_loss_limit":5,
"max_drawdown":10,
"min_trading_days":5
},
"GENERIC_FUNDED":{
"profit_target":8,
"daily_loss_limit":5,
"max_drawdown":10,
"min_trading_days":3
}
}

class ChallengeEngine:
    def check(self,challenge,balance,profit,loss):
        rule=CHALLENGES.get(challenge)
        if not rule:
            return {"status":"UNKNOWN"}

        if loss >= balance*(rule["daily_loss_limit"]/100):
            return {"status":"FAILED","reason":"DAILY_LOSS_LIMIT"}

        if profit >= balance*(rule["profit_target"]/100):
            return {"status":"PASSED","reason":"PROFIT_TARGET"}

        return {
            "status":"RUNNING",
            "rules":rule
        }

challenge_engine=ChallengeEngine()
