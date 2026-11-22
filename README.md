# FoodSaver

FoodSaver is a university project designed to help stores manage food inventory, monitor expiration dates, and reduce food waste.

Store administrators manage products, quantities, expiry dates, and discounts. Customers browse available products, place orders, and view their order history.

## Project Goals

- Reduce food waste through better expiration date monitoring.
- Simplify product inventory management.
- Help employees identify products approaching expiration.
- Support timely actions, such as applying discounts before products expire.
- Encourage responsible consumption and production.

## Main Features

- Admin and customer accounts with token authentication and role-based access.
- Product inventory with categories, barcodes, prices, quantities, images, and expiry dates.
- Fresh, expiring soon, urgent, and expired inventory statuses.
- Admin-configurable discounts for products expiring in two days, one day, or today.
- Customer catalog, shopping cart, checkout, and order history.
- Server-side order price calculation, expiry validation, and stock reduction.

Reminder time and enabled/disabled preferences are saved per account. The backend includes a daily expiry-reminder email command. Configure SMTP and a host scheduler to deliver messages automatically. See [Reminder Setup](docs/REMINDERS.md).

## Technologies Used

### Frontend
- Angular 22
- TypeScript
- HTML
- CSS

### Backend
- Python 3
- Django 5.2
- Django REST Framework

### Database
- SQLite for local development.

### Communication
- JSON REST API with DRF token authentication.

## Project Structure

```text
FoodSaver/
├── backend/
│   ├── accounts/
│   ├── products/
│   ├── config/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
├── docs/
└── README.md
```

## Getting Started

### Requirements

- Python 3.10 or newer.
- Node.js compatible with the Angular version in `frontend/package-lock.json`.
- npm.
- Git.

### Clone the Repository

```bash
git clone https://github.com/RustamKhalimov/ITPM.git
cd ITPM
```

### Backend Setup (Windows PowerShell)

Open a terminal in the project directory:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The backend normally runs at `http://127.0.0.1:8000/`.

Create an administrator account when needed:

```powershell
python manage.py createsuperuser
```

Django superusers are treated as FoodSaver admins.

### Frontend Setup

Open a second terminal in the project directory:

```powershell
cd frontend
npm ci
npm start
```

Open the application at `http://localhost:4200/`.

The development frontend uses `http://127.0.0.1:8000/api` as its API endpoint. Production builds use `/api` and expect the hosting server to proxy that path to Django.

See [Installation Guide](docs/INSTALLATION.md) for environment settings and troubleshooting.

## Development

FoodSaver consists of two main parts:

- **Frontend:** Provides the user interface and user interaction.
- **Backend:** Handles application logic, data processing, account permissions, and database communication.

The Angular single-page application communicates with the Django REST API.

## Sustainable Development Goal

FoodSaver supports United Nations Sustainable Development Goal 12: **Responsible Consumption and Production**.

The project aims to contribute to reducing avoidable food waste by helping stores monitor expiration dates and manage products more effectively.

Learn more: [United Nations SDG 12](https://sdgs.un.org/goals/goal12).

## Tests and Build

Run backend commands from the `backend` directory:

```powershell
python manage.py check
python manage.py makemigrations --check
python manage.py test
```

Run frontend commands from the `frontend` directory:

```powershell
npm test -- --watch=false
npm run build
```

See [Testing Report](docs/TESTING.md) for recorded results. API routes and authentication are documented in [API Documentation](docs/API.md).

See [Project Status](docs/PROJECT_STATUS.md) for current Sprint 3 status and remaining review work.

## Database Backup

Run from `backend` while the application is available:

```powershell
python scripts/sqlite_backup.py backup
```

Backups are written under `backend/backups/`, excluded from Git, and integrity-checked.

To restore a backup, stop the Django server and run:

```powershell
python scripts/sqlite_backup.py restore --source backups/foodsaver-YYYYMMDD-HHMMSS.sqlite3
```

If a database already exists, the script preserves a verified copy beside it before replacing it. Read [Backup and Restore Guide](docs/BACKUP_RESTORE.md) before restoring a real database.

## Project Status

FoodSaver is an academic project under active development. Automated checks cover core account, inventory, pricing, and order behavior. Browser-based end-to-end workflows and deployed production configuration still require verification.

Do not commit the database, backups, secrets, or user data.
