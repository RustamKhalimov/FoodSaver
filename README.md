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