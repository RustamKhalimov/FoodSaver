# FoodSaver

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
