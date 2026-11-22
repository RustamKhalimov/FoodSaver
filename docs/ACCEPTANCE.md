# Sprint 3 Acceptance Evidence

Date: 2026-11-23  
Checkout: local FoodSaver workspace  
Database: SQLite project database

## Automated results

| Area | Acceptance evidence | Result |
| --- | --- | --- |
| Expiry status | `npm test -- --watch=false`; 20-date status boundary spec | Passed: 16 Angular tests across 11 files |
| Backend workflows | `python manage.py test` | Passed: 17 tests, including registration/roles, catalog, product permissions, order rules, reminder preferences, and reminder email idempotency |
| Reminder delivery | In-memory email backend test; verifies recipient, expiring product details, one email per day, dry-run, and empty catalog | Passed |
| Frontend build | `npm run build` | Passed: production bundle generated |
| Backup utility | `python -m unittest scripts.test_sqlite_backup` | Passed: 3 tests |
| Project database | `python scripts/sqlite_backup.py backup`, `verify`, and `restore` to a separate target | Passed: integrity check `ok`; source and restored copy each contain 166 products and 7 user profiles |

## Release scenarios covered

- Expiry dates map to five distinct visual states: fresh, expiring soon, urgent,
  expired, and no expiry date. Expired products have a separate red card style.
- Account preferences store whether email reminders are enabled and the local
  time to send them.
- The scheduled reminder command selects enabled profiles for the current local
  minute, includes in-stock items expiring within three days, and records at most
  one successful delivery per user per local day.
- Backup and restore use SQLite integrity checks. The real database backup was
  restored to a separate verification copy; the active database was not replaced.

## Not completed in this environment

- Live SMTP delivery was not attempted because no SMTP host or credentials are
  configured. Configure SMTP and schedule the command using
  [Reminder Setup](REMINDERS.md).
- Browser screenshots and full manual end-to-end flows were not captured. The
  Windows screenshot helper failed to initialize (`failed to write kernel
  assets`, OS error 3), and there is no installed browser automation package in
  the frontend dependencies.
- Visual inspection at desktop, tablet, and mobile widths remains to be done in
  the user's browser.
