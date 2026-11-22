# Expiry email reminders

FoodSaver sends one daily email to each enabled account when at least one
in-stock product expires today or within the next three calendar days. The
reminder time is interpreted in `DJANGO_TIME_ZONE` (defaults to
`Asia/Qyzylorda`). A per-user delivery record prevents duplicate messages on
the same local date.

## Configure email delivery

Set these environment variables on the backend host:

| Variable | Example | Purpose |
| --- | --- | --- |
| `DJANGO_EMAIL_HOST` | `smtp.example.com` | SMTP server; if absent, Django prints messages to the backend console. |
| `DJANGO_EMAIL_PORT` | `587` | SMTP port. |
| `DJANGO_EMAIL_USE_TLS` | `True` | Enable STARTTLS. |
| `DJANGO_EMAIL_HOST_USER` | `foodsaver@example.com` | SMTP account and default sender. |
| `DJANGO_EMAIL_HOST_PASSWORD` | secret from host environment | SMTP credential. |
| `DJANGO_DEFAULT_FROM_EMAIL` | `FoodSaver <foodsaver@example.com>` | Optional sender override. |
| `DJANGO_TIME_ZONE` | `Asia/Qyzylorda` | Local clock used for reminder preferences. |

Do not commit SMTP credentials to the repository. If `DJANGO_EMAIL_HOST` is
empty, `send_expiry_reminders` uses Django's console email backend, which is
useful for local checking but does not deliver mail to the recipient.

## Schedule the command

Run the command every minute. It sends only to profiles whose saved reminder
time matches the current local minute, and the daily delivery record prevents
duplicate mail if the scheduler starts the command more than once.

```powershell
cd backend
.\.venv\Scripts\python.exe manage.py send_expiry_reminders
```

To preview a specific time without sending or recording a message:

```powershell
.\.venv\Scripts\python.exe manage.py send_expiry_reminders --at 09:00 --dry-run
```

For Windows Task Scheduler, run
`backend/scripts/run_expiry_reminders.ps1` every minute. Configure the SMTP
environment variables for the same Windows account that owns the scheduled
task. For a Unix host, an equivalent cron entry is:

```cron
* * * * * cd /path/to/FoodSaver/backend && .venv/bin/python manage.py send_expiry_reminders
```

Automated tests use Django's in-memory email backend. A real delivery still
requires valid SMTP credentials and an active scheduler on the deployment
host.
