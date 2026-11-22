# SQLite Backup and Restore Guide

The backend database is `backend/db.sqlite3`. Git ignores this file, generated backup files, and pre-restore safety copies. Keep backups outside version control and protect them because they may contain account and order data.

## Create a backup

From the `backend` directory:

```powershell
python scripts/sqlite_backup.py backup
```

The command uses SQLite's online backup API and writes a timestamped copy to `backend/backups/`. It runs `PRAGMA integrity_check` against both source and result. To choose another destination:

```powershell
python scripts/sqlite_backup.py backup --output C:\FoodSaverBackups\foodsaver.sqlite3
```

## Restore a backup

Stop Django and other processes using the database. From `backend`, run:

```powershell
python scripts/sqlite_backup.py restore --source backups\foodsaver-YYYYMMDD-HHMMSS.sqlite3
```

The source backup is verified first. The script prepares a verified temporary restore file. If the target database exists, it saves a timestamped `.before-restore-...` copy beside it, then replaces the database. To restore to another path for inspection, supply `--target`:

```powershell
python scripts/sqlite_backup.py restore --source backups\foodsaver-YYYYMMDD-HHMMSS.sqlite3 --target C:\Temp\foodsaver-restore-test.sqlite3
```

Restart Django and run `python manage.py check` and `python manage.py migrate` after restoring the live database. Keep the pre-restore safety copy until the restored application has been checked.

## Verify without replacing the live database

Run the integrity checker against a backup, or restore it to a temporary target first:

```powershell
python scripts/sqlite_backup.py verify --source backups\foodsaver-YYYYMMDD-HHMMSS.sqlite3
python scripts/sqlite_backup.py restore --source backups\foodsaver-YYYYMMDD-HHMMSS.sqlite3 --target C:\Temp\foodsaver-restore-test.sqlite3
```

The restore command integrity-checks the temporary target after copying. The verify command reports database integrity only; it does not print table contents or user data.

Keep a backup on separate or protected storage. The script does not encrypt backups or automate off-device copies.
