# FoodSaver Installation Guide

This guide explains how to install and run FoodSaver locally on a computer.

## 1. Prerequisites

Install the following software before starting:

- **Python 3.12**
- **Node.js** (version 22.22.2 or higher within the supported major version)
- **npm**
- **Git**

Check installed versions:

```bash
python --version
node --version
npm --version
git --version
```

## 2. Clone the Repository

Clone the FoodSaver repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd FoodSaver
```

The project contains two main components:

- `backend` — Django backend and REST API
- `frontend` — Angular frontend application

## 3. Backend Installation

### 3.1 Create a Virtual Environment

From the root directory of the project, run:

```bash
python -m venv backend/venv
```

### 3.2 Activate the Virtual Environment

**Windows (PowerShell):**

```powershell
.\backend\venv\Scripts\Activate.ps1
```

If script execution is blocked, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

**macOS / Linux:**

```bash
source backend/venv/bin/activate
```

### 3.3 Install Dependencies

Install the backend dependencies:

```bash
pip install -r backend/requirements.txt
```

The backend uses Django, Django REST Framework, and django-cors-headers.

### 3.4 Initialize the Database

Apply database migrations:

```bash
python backend/manage.py migrate
```

FoodSaver uses SQLite for local database storage.

### 3.5 Start the Backend Server

Run:

```bash
python backend/manage.py runserver
```

The backend development server will be available at:

http://127.0.0.1:8000/

Keep this terminal open while using the application.

## 4. Frontend Installation

Open a second terminal from the project root.

Navigate to the frontend directory:

```bash
cd frontend
```

Install the dependencies:

```bash
npm ci
```

### Start the Frontend

Run:

```bash
npm start
```

The Angular development server will be available at:

http://localhost:4200/

## 5. Running FoodSaver

To run the complete application:

1. Start the Django backend in the first terminal.
2. Start the Angular frontend in the second terminal.
3. Open http://localhost:4200/ in your web browser.

Both servers must remain running while using FoodSaver.

To stop either server, press `Ctrl + C` in its terminal.

## 6. Database

FoodSaver uses SQLite.

The database is initialized locally by running:

```bash
python backend/manage.py migrate
```

The database is stored locally and does not require a separate database server installation.

## 7. Troubleshooting

### Node.js version incompatibility

If Angular reports that your Node.js version is unsupported, install a compatible Node.js version and check it again:

```bash
node --version
```

### Backend dependencies are missing

Make sure the backend virtual environment is activated and run:

```bash
pip install -r backend/requirements.txt
```

### Frontend dependencies are missing

From the `frontend` directory, run:

```bash
npm ci
```

### Django returns 404 at the root URL

A `404 Not Found` at `http://127.0.0.1:8000/` does not necessarily indicate that the backend is not running. The root URL may not be configured. The backend server can still be operational.

## 8. Platform Independence

FoodSaver uses Python, Django, Angular, Node.js, and SQLite. These technologies support development on Windows, macOS, and Linux.

The installation process relies on standard package managers and development tools rather than platform-specific application dependencies.

The commands in this guide were tested on Windows using PowerShell. Installation on macOS and Linux should follow the corresponding virtual environment activation commands, but those platforms have not been independently tested.