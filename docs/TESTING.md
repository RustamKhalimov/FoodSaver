# Testing Report

Last updated: 2026-11-23. Results are from commands run against the local FoodSaver checkout. Browser-based workflows and screenshots were not run.

## Automated checks

| Check | Result | Notes |
| --- | --- | --- |
| `python manage.py check` | Passed | No Django system-check issues. |
| `python manage.py makemigrations --check` | Passed | No model changes need migrations. |
| `python manage.py test` | Passed: 17 tests | Covers account roles, reminder preferences and email delivery, product permissions, catalog, discounts, stock/order rules, and user-specific order access. |
| `npm test -- --watch=false` | Passed: 16 tests in 11 files | Includes expiration classification across 20 dates and the today boundary. ZXing emitted package sourcemap warnings. |
| `npm run build` | Passed | Production Angular bundle generated successfully. |
| `python -m unittest scripts.test_sqlite_backup` | Passed: 3 tests | Verified backup, integrity check, same-file safety, and restore preserving the previous target using temporary databases. |
| Real database backup and restore check | Passed | Backed up `backend/db.sqlite3`, checked integrity, restored to a separate copy, and confirmed 166 products and 7 profiles in both. The working database was not overwritten. |

## Changes covered

- The expiring endpoint now includes dates from today through day 3 and excludes earlier dates. Its regression test verifies today, day 3, sorting, and exclusion of expired and later products.
- Inventory status and color use expiration date rather than discount percentage. Today and tomorrow are Urgent, days 2–3 are Expiring soon, later dates are Fresh, and past dates are Expired.
- Date-only status calculations use calendar-day arithmetic to avoid UTC parsing shifting a product date across midnight.
- Reminder time and enabled state are persisted through the account profile API. The scheduled command sends one daily email for products expiring within three days and prevents duplicate delivery for that date. SMTP credentials and a host scheduler are required for deployment delivery.
- SQLite backup and restore use integrity checks; restore keeps a timestamped safety copy of an existing target.

## Not yet verified

- Full browser flows for admin login, product CRUD, customer registration/login, cart, checkout, orders, account editing, password changes, and role navigation.
- Browser console and responsive layouts at desktop, tablet, and mobile sizes.
- Live SMTP delivery was not attempted because this checkout has no SMTP credentials; use the in-memory email tests for code verification.
- Manual screenshot evidence and end-to-end browser checks remain outstanding. The Windows screenshot helper failed to initialize in this session.

## Existing test gaps

Several Angular page specs only check component creation. More UI and API workflow tests are needed for account editing, discount settings, order edge cases, and responsive interactions.
