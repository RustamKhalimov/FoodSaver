# FoodSaver

<<<<<<< HEAD
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
=======
FoodSaver is a web application designed to help stores manage product
inventory, monitor expiration dates, and reduce food waste.

The application helps store employees track products, identify items
approaching their expiration dates, and take timely actions to minimize
unnecessary food waste.

## Project Goals

-   Reduce food waste through better expiration date monitoring.
-   Simplify product inventory management.
-   Help employees identify products approaching expiration.
-   Support timely actions, such as applying discounts before products
    expire.
-   Encourage responsible consumption and production.

## Main Features

-   **Inventory Management:** Manage and monitor store products.
-   **Expiration Date Tracking:** Track product expiration dates.
-   **Expiration Alerts:** Identify products approaching their
    expiration dates.
-   **Product Management:** Store and manage product information.
-   **Discount Management:** Support discounts for products nearing
    expiration.

> **Note:** The listed features describe the project's functionality and
> goals. Their implementation status should be verified against the
> current application version.

## Technologies Used

### Frontend

-   Angular
-   TypeScript
-   HTML
-   CSS

### Backend

-   Python
-   Django 5.2.18
-   Django REST Framework 3.18.3
-   django-cors-headers 4.9.0

### Database

-   SQLite

## Project Structure

``` text
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
└── README.md
```

## Getting Started

Follow these instructions to run FoodSaver locally.

### Prerequisites

Make sure you have installed:

-   Python
-   Node.js
-   npm
-   Git

### 1. Clone the Repository

``` bash
git clone https://github.com/RustamKhalimov/ITPM.git
cd ITPM
```

### 2. Set Up the Backend

Open a terminal and navigate to the backend directory:

``` bash
cd backend
```

Create a Python virtual environment.

**Windows:**

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

``` bash
python -m pip install -r requirements.txt
```

Apply database migrations:

``` bash
python manage.py migrate
```

Start the Django development server:

``` bash
python manage.py runserver
```

The backend will normally be available at:

http://127.0.0.1:8000/

### 3. Set Up the Frontend

Open a second terminal and navigate to the frontend directory:

``` bash
cd frontend
```

Install frontend dependencies:

``` bash
npm install
```

Start the Angular development server:

``` bash
npx ng serve
```

Open the application in your browser:

http://localhost:4200/

## Development

FoodSaver consists of two main parts:

-   **Frontend:** Provides the user interface and user interaction.
-   **Backend:** Handles application logic, data processing, and
    communication with the database.

The frontend and backend work together to provide inventory management
functionality.

## Sustainable Development Goal

FoodSaver supports United Nations Sustainable Development Goal 12:
**Responsible Consumption and Production**.

The project aims to contribute to reducing avoidable food waste by
helping stores monitor expiration dates and manage products more
effectively.

Learn more about SDG 12:

https://sdgs.un.org/goals/goal12
>>>>>>> origin/main
