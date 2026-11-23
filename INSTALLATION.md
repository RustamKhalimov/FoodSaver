# FoodSaver Installation Guide

This guide explains how to install, configure, and run FoodSaver locally on Windows, macOS, and Linux.

## 1. Prerequisites

Make sure the following software is installed:

- **Python 3.12**
- **Node.js** compatible with Angular 22:
  - Node.js 22.22.3 or later within the 22.x release line;
  - Node.js 24.15.0 or later within the 24.x release line;
  - Node.js 26.x.
- **npm**
- **Git**

Check the installed versions:

```bash
python --version
node --version
npm --version
git --version
```

Official Angular version compatibility: https://angular.dev/reference/versions

## 2. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/RustamKhalimov/FoodSaver.git
cd FoodSaver
```

The project contains two main components:

- `backend/` — Django backend and REST API.
- `frontend/` — Angular frontend application.

## 3. Backend Installation

### 3.1 Create a Virtual Environment

Run this command from the project root directory:

```bash
python -m venv backend/.venv
```

### 3.2 Activate the Virtual Environment

**Windows (PowerShell):**

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

**macOS / Linux:**

```bash
source backend/.venv/bin/activate
```

### 3.3 Install Backend Dependencies

```bash
python -m pip install -r backend/requirements.txt
```

The backend uses Django, Django REST Framework, and django-cors-headers.

### 3.4 Initialize the Database

Run database migrations:

```bash
python backend/manage.py migrate
```

FoodSaver uses SQLite, so a separate database server is not required for local development.

### 3.5 Start the Backend Server

```bash
python backend/manage.py runserver
```

The Django development server will be available at:

`http://127.0.0.1:8000/`

Keep this terminal open while using the application.

## 4. Frontend Installation

Open a second terminal in the project root directory.

Navigate to the frontend folder:

```bash
cd frontend
```

Install the dependencies using the lockfile:

```bash
npm ci
```

### Start the Angular Application

```bash
npm start
```

The Angular development server will be available at:

`http://localhost:4200/`

Keep this terminal open while using the application.

## 5. Running FoodSaver

To run the complete application:

1. Start the Django backend in the first terminal.
2. Start the Angular frontend in the second terminal.
3. Open `http://localhost:4200/` in your browser.

Both development servers must remain running while using FoodSaver.

## 6. Environment Configuration

FoodSaver supports environment-based Django configuration.

The main backend environment variables include:

| Variable | Purpose |
|---|---|
| `DJANGO_DEBUG` | Controls Django debug mode. |
| `DJANGO_SECRET_KEY` | Provides the Django secret key. |
| `DJANGO_ALLOWED_HOSTS` | Defines permitted host names. |
| `DJANGO_CORS_ALLOWED_ORIGINS` | Defines allowed frontend origins. |
| `DJANGO_TIME_ZONE` | Configures the application time zone. |
| `DJANGO_EMAIL_HOST` | Configures the SMTP email server. |
| `DJANGO_EMAIL_HOST_USER` | Defines the SMTP username. |
| `DJANGO_EMAIL_HOST_PASSWORD` | Defines the SMTP password. |

For local development, the project can use its development defaults.

Do not commit production credentials, secret keys, or `.env` files to the repository.

For production deployment, configure secure secrets, HTTPS, allowed hosts, and appropriate security settings.

## 7. Troubleshooting

### Python dependencies are missing

Make sure the virtual environment is activated and run:

```bash
python -m pip install -r backend/requirements.txt
```

### Angular reports an unsupported Node.js version

Check the installed version:

```bash
node --version
```

Install a Node.js version compatible with Angular 22.

### Frontend dependencies are missing

Navigate to the `frontend` directory and run:

```bash
npm ci
```

### PowerShell blocks virtual environment activation

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the virtual environment again.

### Django returns 404 at the root URL

A `404 Not Found` response at `http://127.0.0.1:8000/` does not necessarily mean that the backend is not running. The root URL may not have a configured route.

## 8. Platform Independence

FoodSaver uses Python, Django, Angular, Node.js, npm, and SQLite.

The application has been successfully run on Windows and macOS.

The installation guide includes platform-specific virtual environment activation commands for Windows, macOS, and Linux.

Linux compatibility is expected based on the technologies used, but has not yet been independently verified.

## 9. Additional Documentation

For more information about the project, see:

- [README.md](README.md) — project overview and main features.
- [CONTRIBUTING.md](CONTRIBUTING.md) — contribution guidelines.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — community standards.
- [PRIVACY.md](PRIVACY.md) — technical data overview.
- [SECURITY_REVIEW.md](SECURITY_REVIEW.md) — security review and recommendations.
- [docs/API.md](docs/API.md) — API documentation.
- [docs/TESTING.md](docs/TESTING.md) — testing instructions.
- [docs/BACKUP_RESTORE.md](docs/BACKUP_RESTORE.md) — backup and restoration instructions.
