# API Documentation

Base URL in local development: `http://127.0.0.1:8000/api/`.

Requests and responses use JSON. Protected endpoints use `Authorization: Token <token>`. Product reads and catalog routes are public. Product mutation and discount-rule updates require the backend admin role. Customers can only read their own orders.

## Accounts

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `POST` | `/accounts/register/` | Public | Create a customer account. Body: `username`, `email`, `password`. Returns token and user. |
| `POST` | `/accounts/login/` | Public | Log in with `email` and `password`; returns token and user. |
| `GET`, `PATCH` | `/accounts/profile/` | Token | Read or update the current user's email, first name, last name, `notifications_enabled`, and `reminder_time` (`HH:MM`). |
| `POST` | `/accounts/change-password/` | Token | Body: `old_password`, `new_password`. |
| `POST` | `/accounts/logout/` | Token | Delete the current token. |

Registration always assigns the customer role; clients cannot self-assign admin access. Reminder preferences are stored per account. The backend can send one daily email for products expiring within three days; SMTP and a once-per-minute host scheduler must be configured for delivery. See [Reminder Setup](REMINDERS.md). Login errors return HTTP 400. Profile and password errors include field or `error` details.

## Products

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `GET` | `/products/` | Public | List products ordered by expiry date; no-expiry products are last. |
| `POST` | `/products/` | Admin | Create a product. |
| `GET`, `PATCH`, `PUT`, `DELETE` | `/products/{id}/` | Read public; mutation admin | Retrieve or manage a product. |
| `GET` | `/products/catalog/` | Public | List in-stock products that have not expired. |
| `GET` | `/products/expiring/` | Public | List products expiring today through three days from today, sorted by date. |

Product responses include `id`, `name`, `barcode`, `image_url`, `category`, `quantity`, `regular_price`, `unit_size`, `expiry_date`, timestamps, `discount_percent`, and `discounted_price`. Product creation requires at least one unit.

## Discount rules

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `GET` | `/discount-rules/` | Public | Read the configured rule set. |
| `PATCH`, `PUT` | `/discount-rules/` | Admin | Update enabled state and discount percentages. |

Percentages are integers from 0 through 100. Discounts are configured for expiry today, in one day, or in two days. The backend recalculates price at order time.

## Orders

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| `GET`, `POST` | `/orders/` | Token | List the current user's orders or place an order. |
| `GET` | `/orders/{id}/` | Token | Retrieve one of the current user's orders. |

Order body:

```json
{
  "items": [
    { "product_id": 12, "quantity": 2 }
  ]
}
```

The server validates stock and expiry, recalculates discounts and totals, reduces stock, and returns HTTP 201 with the order and line items. Invalid quantities, expired products, missing products, or insufficient stock return HTTP 400. An order can contain at most 50 distinct product lines.
