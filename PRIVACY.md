# FoodSaver Privacy and Data Overview

This document describes data used by the current FoodSaver codebase. It is a technical project overview, not a claim that the application is ready for public production deployment.

## Information FoodSaver Uses

Based on the Django models and serializers:

| Data | Purpose | Location |
| --- | --- | --- |
| Username and email | Create accounts and identify users | Django `User` model |
| Password | Authenticate users | Django password hash, managed by Django's built-in authentication system |
| First and last name | Optional account profile information | Django `User` model |
| Role (`admin` or `customer`) | Decide who can perform administrative operations | `UserProfile` |
| Notification preference and reminder time | Support expiration reminders | `UserProfile` |
| Reminder delivery date, product count, and time sent | Track delivery of reminders | `ReminderDelivery` |
| Order, order items, quantities, and prices | Maintain purchase history and order records | `Order` and `OrderItem` |
| Product information, including expiration dates and stock | Manage inventory and catalog functionality | `Product` |
| Authentication token | Authenticate API requests | Django REST Framework token model |

The project currently configures SQLite for local data storage. The code also configures optional email delivery for reminders. Do not assume that every field is mandatory or that real users have consented to production data collection.

## Access Controls Found in the Backend

- Registration and login are public endpoints by design.
- Profile retrieval and updates require an authenticated user and access the current user's account.
- Password changes require the current password and validate the replacement password.
- The API restricts order listing and order detail retrieval to the authenticated customer's orders.
- Product edits and discount-rule edits are limited to the backend's `IsAdminUser` role check.

## Privacy and Security Considerations

- Only collect information needed for the application.
- Keep database files, secrets, and environment settings outside Git.
- Never print passwords or authentication tokens in application logs or screenshots.
- Use HTTPS, `DEBUG=False`, and a secure environment-specific `DJANGO_SECRET_KEY` before production deployment.
- The Angular frontend stores the API token and profile in browser `localStorage`; a successful logout clears both. Protect against script injection and review token persistence. The server currently does not revoke the existing API token after a password change.
- Define account deletion, data retention, backup, and incident-response procedures before using real customer data in production.
- Confirm whether all product and inventory fields are intended to be publicly visible through the read-only product API.

## Scope

This overview is based on a static review of selected files in the public FoodSaver GitHub repository on November 23, 2026. It is not a complete privacy audit or legal privacy notice.
