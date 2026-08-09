from app.backup.backup_manager import BackupManager
from app.recovery.recovery_manager import RecoveryManager


backup_manager = BackupManager()


data = {

    "system": "TRADE_AI",

    "status": "RUNNING",

    "trades": [

        {
            "symbol": "XAUUSD",
            "result": "WIN"
        }

    ]

}


backup = backup_manager.create_backup(
    "recovery_test",
    data
)


print("BACKUP:")
print(backup)


recovery = RecoveryManager()


files = recovery.list_backups()


print()

print("AVAILABLE BACKUPS:")
print(files)


result = recovery.recover(
    backup["file"]
)


print()

print("RECOVERY RESULT:")
print(result)
