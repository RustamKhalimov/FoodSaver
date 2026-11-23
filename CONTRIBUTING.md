# Contributing to FoodSaver

Thank you for your interest in improving FoodSaver! The project uses Angular for the frontend and Django REST Framework with SQLite for the backend.

## Ways to Contribute

You can help by:

- Fixing bugs or improving existing features.
- Suggesting enhancements to inventory, expiration-date tracking, or discounts.
- Improving the user interface and accessibility.
- Writing or updating documentation.
- Testing the application and reporting reproducible problems.

## Getting Started

1. Fork the repository on GitHub, or work in an approved team branch if you already have access.
2. Clone your copy of the project:

   ```bash
   git clone https://github.com/<your-username>/FoodSaver.git
   cd FoodSaver
   ```

   Team members with repository access can clone `https://github.com/RustamKhalimov/FoodSaver.git` instead.

3. Create a branch for your change:

   ```bash
   git checkout -b docs/add-contribution-guidelines
   ```

## Backend Setup (Django)

From the project root:

```bash
cd backend
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS / Linux: `source .venv/bin/activate`

Then run:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The local Django server normally runs at `http://127.0.0.1:8000/`.

## Frontend Setup (Angular)

Open a second terminal from the project root:

```bash
cd frontend
npm ci
npx ng serve
```

The Angular application normally runs at `http://localhost:4200/`.

## Before Submitting a Pull Request

- Keep your change focused on one topic.
- Test the feature you modified. For backend changes, run `python manage.py test` from `backend/` (the project may not yet contain comprehensive automated tests).
- Check that the frontend builds and works when you modify Angular components.
- Do not commit passwords, API tokens, `.env` files, personal data, local databases, or virtual environments.
- Update relevant documentation if behavior or setup steps change.
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Submitting Changes

1. Stage only the intended files: `git add <changed-files>`.
2. Commit with a clear message, for example: `docs: add contribution guidelines`.
3. Push the branch to your GitHub account: `git push -u origin <branch-name>`.
4. Open a pull request into the FoodSaver `main` branch.
5. Explain what changed, how you checked it, and any known limitations.
6. Review teammate feedback before merging.

## Reporting Bugs

When opening a GitHub issue, include:

- A short, descriptive title.
- Steps to reproduce the issue.
- Expected and actual results.
- Relevant environment details (Python, Node.js, browser), if known.
- Screenshots or error logs with secrets and personal data removed.

For suspected security issues, do **not** publish vulnerability details in a public issue. Contact a project maintainer privately.

## License

Contributions to this repository are provided under the project's GNU General Public License v3.0 (GPL-3.0). Read the `LICENSE` file before submitting code.
