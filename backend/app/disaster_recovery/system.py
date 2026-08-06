class AIDisasterRecovery:

    def __init__(self):
        self.backups=[]
        self.recoveries=[]
        self.failovers=[]


    def create_backup(self,name,data):

        backup={
            "name":name,
            "data":data,
            "status":"READY"
        }

        self.backups.append(backup)

        return backup


    def restore(self,backup):

        recovery={
            "backup":backup,
            "status":"RESTORED"
        }

        self.recoveries.append(recovery)

        return recovery


    def failover(self,service):

        item={
            "service":service,
            "status":"MOVED"
        }

        self.failovers.append(item)

        return item


    def status(self):

        return {
            "backups":len(self.backups),
            "recoveries":len(self.recoveries),
            "failovers":len(self.failovers),
            "system":"PROTECTED"
        }


disaster_recovery=AIDisasterRecovery()
