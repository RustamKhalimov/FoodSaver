# FoodSaver

**FoodSaver** is a web application designed to help stores manage product inventory, monitor expiration dates, and reduce food waste.

The application helps store employees keep track of products, identify items approaching their expiration dates, and take timely actions to minimize unnecessary food waste.

## Project Overview

Food waste is an important environmental and economic problem. Products that expire before being sold or consumed contribute to unnecessary resource consumption.

FoodSaver aims to address this problem by providing stores with a digital tool for inventory and expiration date management.

## Main Objectives

- Reduce avoidable food waste.
- Improve product inventory management.
- Monitor product expiration dates.
- Help employees identify products approaching expiration.
- Support timely actions, such as applying discounts to products before they expire.
- Encourage responsible consumption and production.

## Key Features

- **Inventory Management:** Manage and monitor products stored in the inventory.
- **Expiration Date Tracking:** Keep track of product expiration dates.
- **Expiration Alerts:** Help employees identify products that are approaching their expiration dates.
- **Product Management:** Maintain product information and inventory records.
- **Discount Management:** Support discounts for products nearing expiration.

## Technologies

| Component | Technology |
|---|---|
| Frontend | Angular |
| Programming Language | TypeScript |
| Backend | Python, Django |
| API Framework | Django REST Framework |
| Database | SQLite |
| CORS Configuration | django-cors-headers |

## Project Structure

```text
FoodSaver/
│
├── backend/
│   ├── accounts/
│   ├── products/
│   ├── config/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   └── README.md
│
└── README.md
```

## Installation and Setup

Follow the instructions below to run FoodSaver locally.

### Prerequisites

Make sure the following software is installed:

- Python
- Node.js
- npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/RustamKhalimov/FoodSaver.git
cd FoodSaver
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment.

**Windows:**

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Start the Django development server:

```bash
python manage.py runserver
```

By default, the backend development server is available at:

`http://127.0.0.1:8000/`

### 3. Frontend Setup

Open a separate terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start the Angular development server:

```bash
npx ng serve
```

Open the application in your browser:

`http://localhost:4200/`

## Running the Application

To use FoodSaver locally, both development servers should be running:

- **Django Backend:** `http://127.0.0.1:8000/`
- **Angular Frontend:** `http://localhost:4200/`

The frontend communicates with the backend to access application functionality and data.

## Project Ownership

FoodSaver is a team-developed project. The development team is responsible for maintaining and improving the application.

## Team Members

FoodSaver is developed collaboratively by a team of four members.

## License

FoodSaver is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

This license allows users to use, study, modify, and distribute the software under the terms of GPL-3.0.

See the `LICENSE` file in the root directory for the full license text.

Official license: https://www.gnu.org/licenses/gpl-3.0.en.html

## Sustainable Development Goal

FoodSaver supports **United Nations Sustainable Development Goal 12: Responsible Consumption and Production**.

By helping stores monitor product expiration dates and manage inventory more effectively, FoodSaver aims to reduce avoidable food waste and encourage responsible resource use.

Official SDG information:

https://sdgs.un.org/goals/goal12

## Contributing

Contributions and suggestions for improving FoodSaver are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Community

We welcome bug reports, documentation fixes, testing feedback, and code contributions. Read [CONTRIBUTING.md](CONTRIBUTING.md) for setup and pull request guidelines, and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for our community standards.

## Privacy and Security

FoodSaver uses Django authentication and role-based API permissions. The project stores account, inventory, notification preference, and order information needed for its core features. See [PRIVACY.md](PRIVACY.md) for a technical data overview. Before deploying the application, review the recommendations in [SECURITY_REVIEW.md](SECURITY_REVIEW.md).
