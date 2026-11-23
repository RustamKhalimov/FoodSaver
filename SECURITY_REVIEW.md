# FoodSaver Security Review — Criterion 7

**Review date:** 2026-11-23
**Source baseline:** `3c2673e`
**Scope:** Django configuration, authentication, profile and order access, product permissions, browser token storage, and tracked local data.

This review combines source inspection with the existing Django automated tests and deployment checks. It is not a penetration test, a browser end-to-end test, or verification of a deployed production environment.

## 1. Controls observed in the source

| Area | Observation |
| --- | --- |
| Passwords | Registration uses `User.objects.create_user()` and Django password validation. Password changes check the current password and validate the replacement. |
| Authentication | DRF TokenAuthentication and SessionAuthentication are configured. Logout deletes the user's API token. |
| Profile | `ProfileView` requires authentication and returns `request.user`; the profile serializer makes `role` read-only. Registration assigns the customer role. |
| Orders | Order collection and detail endpoints require authentication and filter records by `customer=request.user`. These endpoints live in `backend/products/`, not a separate orders application. |
| Administration | Product writes and discount-rule changes require the custom `IsAdminUser` permission. |
| Browser protections | CSRF, SecurityMiddleware, and X-Frame-Options middleware are enabled. CORS defaults to the two local Angular development origins. |
| Hosts and secrets | `ALLOWED_HOSTS` is read from `DJANGO_ALLOWED_HOSTS`, defaulting to `127.0.0.1,localhost,testserver`. Disabling debug without supplying a secret raises an error. |
| Local data | `.gitignore` excludes environment files, local SQLite databases, and virtual environments. No `.env`, `.env.*`, `.sqlite3`, or `.sqlite3.*` files were found in the tracked file list. This is not a full Git-history secret scan. |

## 2. Checks actually executed

Dependencies were installed from `backend/requirements.txt` into an isolated Python 3.12 environment (Django 5.2.18, DRF 3.18.3). From `backend/`:

```powershell
python manage.py check --deploy
python manage.py test --noinput
```

### Deployment check

`check --deploy` completed with **6 warnings, 0 silenced**, using the repository's default development configuration:

| Warning | Finding | Action before production |
| --- | --- | --- |
| `security.W004` | HSTS duration is not configured | Plan and validate HTTPS coverage before enabling HSTS. |
| `security.W008` | HTTPS redirect is disabled | Configure HTTPS redirection in Django or the trusted reverse proxy. |
| `security.W009` | Development fallback secret is insecure | Supply a unique, long random `DJANGO_SECRET_KEY` outside Git. |
| `security.W012` | Session cookie is not secure-only | Enable `SESSION_COOKIE_SECURE` for HTTPS deployment. |
| `security.W016` | CSRF cookie is not secure-only | Enable `CSRF_COOKIE_SECURE` for HTTPS deployment. |
| `security.W018` | Debug is enabled | Set `DJANGO_DEBUG=False` and verify the deployed configuration. |

These warnings were recorded, not fixed by this documentation change. A successful command exit does not mean the project is production-ready. HTTPS cookie, redirect, and HSTS settings need explicit deployment configuration; this settings file does not currently read environment variables for those options.

### Existing automated tests

**17 tests passed** using Django's temporary test database. The ordinary system check reported no issues. No existing user database was migrated or modified.

Security-relevant coverage includes:

- Registration ignores a submitted administrator role and creates a customer.
- Customer and administrator login return server-assigned roles.
- Django superusers receive administrative permissions.
- Customers cannot create, update, or delete products; administrators can.
- Customers cannot change discount rules; administrators can.
- Order lists contain only the authenticated user's orders; access to another user's order returns 404.

Some permission tests use `force_authenticate`; they verify backend authorization but do not prove the complete browser/token authentication flow. The suite also covers inventory validation, pricing, reminder preferences, and reminder delivery.

## 3. Remaining findings and follow-up

| Priority | Finding | Recommended follow-up |
| --- | --- | --- |
| Before production | Development defaults produce the six warnings above | Supply deployment configuration and rerun `check --deploy` in that environment. Restrict allowed hosts to actual deployment hosts. |
| Medium | Angular stores the token and user profile in `localStorage` | Review XSS defenses and token persistence. Successful logout removes these local entries and deletes the server token; inspect failure handling as well. |
| Medium | Password changes do not revoke the existing API token | Define and implement token revocation/rotation on password change; test old-token rejection. |
| Medium | No DRF throttling is configured for login | Define and test login rate limiting, including any protection provided by the reverse proxy. |
| Medium | Product reads expose inventory data publicly | Confirm public visibility is intended for all serialized fields. |
| Before real customer use | Data lifecycle decisions remain necessary | Define retention, account deletion, backup access, and incident handling. Existing backup guidance is in `docs/BACKUP_RESTORE.md`. |

### Still to verify

- [ ] Unauthenticated requests to profile and order endpoints are rejected in runtime tests.
- [ ] Profile updates cannot promote a customer to administrator in runtime tests.
- [ ] Password-change and logout behavior is verified with real API tokens, including invalidation behavior.
- [ ] Full Angular registration, login, profile, and logout flows are checked in a browser.
- [ ] Production HTTPS, host configuration, and secure cookies are verified on the deployed application.
- [ ] A dependency vulnerability audit and full Git-history secret scan are performed.

## 4. Files inspected

- `backend/config/settings.py`
- `backend/accounts/models.py`
- `backend/accounts/serializers.py`
- `backend/accounts/views.py`
- `backend/accounts/permissions.py`
- `backend/accounts/tests.py`
- `backend/products/models.py`
- `backend/products/views.py`
- `backend/products/tests.py`
- `frontend/src/app/services/auth.ts`
- `.gitignore`

## 5. Presentation summary

> I reviewed FoodSaver's authentication, role-based permissions, user data handling, and Django deployment settings. I ran the existing backend suite: all 17 tests passed, including product permissions and order isolation checks. The deployment check reported six warnings for development defaults, which I documented with recommended production actions. Browser end-to-end testing and production verification remain separate tasks.

Source: https://github.com/RustamKhalimov/FoodSaver
