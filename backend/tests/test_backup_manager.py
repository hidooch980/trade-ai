from app.backup.backup_manager import BackupManager


manager = BackupManager()


data = {

    "trades": [

        {
            "symbol": "XAUUSD",
            "side": "BUY",
            "profit": 50
        }

    ],

    "signals": [

        {
            "decision": "BUY",
            "confidence": 85
        }

    ]

}


backup = manager.create_backup(
    "trade_ai_test",
    data
)


print("BACKUP CREATED:")
print(backup)


restored = manager.restore(
    backup["file"]
)


print()

print("RESTORED DATA:")
print(restored)
