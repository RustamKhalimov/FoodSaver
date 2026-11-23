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
│   ├── scripts/
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
├── docs/
│   ├── ACCEPTANCE.md
│   ├── API.md
│   ├── BACKUP_RESTORE.md
│   ├── INSTALLATION.md
│   ├── PROJECT_STATUS.md
│   ├── REMINDERS.md
│   └── TESTING.md
│
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── INSTALLATION.md
├── LICENSE
├── PRIVACY.md
├── SECURITY_REVIEW.md
└── README.md
```

## Installation and Setup

Follow the instructions in [INSTALLATION.md](INSTALLATION.md) to install and run FoodSaver locally.

### Prerequisites

Make sure the following software is installed:

- Python
- Node.js
- npm
- Git

### Clone the Repository

```bash
git clone https://github.com/RustamKhalimov/FoodSaver.git
cd FoodSaver
```

### Running the Application

FoodSaver consists of two main components:

- **Backend:** Django REST API running at `http://127.0.0.1:8000/`
- **Frontend:** Angular application running at `http://localhost:4200/`

Both development servers must be running to use the complete application.

For detailed installation instructions, including virtual environment setup, dependency installation, and database migrations, see [INSTALLATION.md](INSTALLATION.md).

## Project Ownership

FoodSaver is a team-developed project. The development team is responsible for maintaining and improving the application.

## Team Members

FoodSaver is developed collaboratively by a team of four members:

| Member | Name |
|---|---|
| Member 1 | Әзи Айгерім |
| Member 2 | Халимов Рустам |
| Member 3 | Баймырза Нурлыбек |
| Member 4 | Калиев Алпамыс |

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

Contributions and suggestions for improving FoodSaver are welcome.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines, development setup, and pull request instructions.

## Community

We welcome bug reports, documentation improvements, testing feedback, and code contributions.

All contributors are expected to follow the standards described in [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Privacy and Security

FoodSaver uses Django authentication and role-based API permissions.

The project stores account information, inventory data, notification preferences, and order information required for its core functionality.

For more information, see:

- [PRIVACY.md](PRIVACY.md) — technical overview of collected and stored data.
- [SECURITY_REVIEW.md](SECURITY_REVIEW.md) — security review, identified risks, and recommendations.
- [docs/API.md](docs/API.md) — API documentation.
- [docs/TESTING.md](docs/TESTING.md) — testing documentation.
- [docs/BACKUP_RESTORE.md](docs/BACKUP_RESTORE.md) — database backup and restoration instructions.

**Note:** FoodSaver is an ongoing project. The security review documents known limitations and recommendations that should be addressed before production deployment.
