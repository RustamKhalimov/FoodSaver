# Installation Guide

This guide sets up FoodSaver on a new Windows computer. The same Python and npm commands work on other systems after adapting virtual-environment activation.

## 1. Install prerequisites

- Python 3.10 or newer.
- Node.js and npm compatible with the Angular version in `frontend/package-lock.json`.
- Git, if cloning the repository.

## 2. Get the project

```powershell
git clone <repository-url>
cd FoodSaver
```

## 3. Set up Django

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
```

Run the backend:

```powershell
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/`. Create a Django superuser with `python manage.py createsuperuser`; superusers are recognized as FoodSaver admins.

### Backend environment variables

Local development works with defaults. Configure these variables for another environment:

| Variable | Default | Purpose |
| --- | --- | --- |
| `DJANGO_DEBUG` | `True` | Set to `False` in deployment. |
| `DJANGO_SECRET_KEY` | Development-only key | Required when `DJANGO_DEBUG=False`; keep it private. |
| `DJANGO_ALLOWED_HOSTS` | `127.0.0.1,localhost,testserver` | Comma-separated Django host names. |
| `DJANGO_CORS_ALLOWED_ORIGINS` | Local Angular origins | Comma-separated full origins, including scheme. |
| `DJANGO_TIME_ZONE` | `Asia/Qyzylorda` | Django timezone used for expiry date boundaries. |

Do not commit `.env` files or production credentials.

## 4. Set up Angular

Open a second terminal at the repository root:

```powershell
cd frontend
npm ci
npm start
```

Open `http://localhost:4200/`. The development API URL is configured in `frontend/src/environments/environment.ts`.

For production, `npm run build` replaces that file with `environment.production.ts`, which uses `/api`. Configure the web server to proxy `/api` to Django and serve the Angular app over HTTPS.

## 5. Run checks

From `backend`:

```powershell
python manage.py check
python manage.py makemigrations --check
python manage.py test
```

From `frontend`:

```powershell
npm test -- --watch=false
npm run build
```

## Troubleshooting

- If PowerShell blocks virtual-environment activation, use `backend\.venv\Scripts\python.exe` directly.
- If Angular cannot reach Django, check that both servers are running and the development API URL and Django CORS origins match.
- If Django reports a missing secret with debug disabled, set `DJANGO_SECRET_KEY` in the environment.
- If SQLite is locked during restore, stop the Django server and close processes using the database.
