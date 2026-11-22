# FoodSaver

FoodSaver is a university project for managing food inventory and reducing waste. Store administrators manage products, quantities, expiry dates, and discounts. Customers browse available products, place orders, and view their order history.

## Features

- Admin and customer accounts with token authentication and role-based access.
- Product inventory with categories, barcodes, prices, quantities, images, and expiry dates.
- Fresh, expiring soon, urgent, and expired inventory statuses.
- Admin-configurable discounts for products expiring in two days, one day, or today.
- Customer catalog, shopping cart, checkout, and order history.
- Server-side order price calculation, expiry validation, and stock reduction.

Reminder time and enabled/disabled preferences are saved per account. The backend includes a daily expiry-reminder email command; configure SMTP and a host scheduler to deliver messages automatically. See [Reminder Setup](docs/REMINDERS.md).

## Technology and architecture

- **Frontend:** Angular 22, TypeScript, HTML, and CSS.
- **Backend:** Python 3, Django 5.2, Django REST Framework.
- **Database:** SQLite for local development.
- **Communication:** JSON REST API with DRF token authentication.

The Angular single-page app calls the Django API. Django owns account permissions, inventory data, discount calculations, order validation, and stock updates. Product and account code is in `backend/products` and `backend/accounts`; the Angular app is in `frontend/src/app`.

## Requirements

- Python 3.10 or newer.
- Node.js compatible with the version of Angular CLI in `frontend/package-lock.json` and npm.

## Quick start on Windows PowerShell

Open two terminals in the project directory.

### Backend terminal

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000/`. Create an administrator account when needed with `python manage.py createsuperuser`. Django superusers are treated as FoodSaver admins.

### Frontend terminal

```powershell
cd frontend
npm ci
npm start
```

Open `http://localhost:4200/`. The development frontend uses `http://127.0.0.1:8000/api`. Production builds use `/api` and expect the hosting server to proxy that path to Django. See [Installation Guide](docs/INSTALLATION.md) for environment settings and troubleshooting.

## Tests and build

Run backend commands from `backend`:

```powershell
python manage.py check
python manage.py makemigrations --check
python manage.py test
```

Run frontend commands from `frontend`:

```powershell
npm test -- --watch=false
npm run build
```

See [Testing Report](docs/TESTING.md) for the latest recorded results. API routes and authentication are documented in [API Documentation](docs/API.md).

See [Project Status](docs/PROJECT_STATUS.md) for current Sprint 3 status and remaining review work.

## Database backup

Run from `backend` while the app is available:

```powershell
python scripts/sqlite_backup.py backup
```

Backups are written under `backend/backups/`, excluded from Git, and integrity-checked. To restore, stop the Django server, then run:

```powershell
python scripts/sqlite_backup.py restore --source backups/foodsaver-YYYYMMDD-HHMMSS.sqlite3
```

If a database already exists, the script preserves a verified copy beside it before replacing it. Read [Backup and Restore Guide](docs/BACKUP_RESTORE.md) before restoring a real database.

## Project status

FoodSaver is an academic project under active development. Automated checks cover core account, inventory, pricing, and order behavior. Browser-based end-to-end workflows and deployed production configuration still require verification. Do not commit the database, backups, secrets, or user data.
