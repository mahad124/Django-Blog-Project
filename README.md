# Django Blog (learning project)

This repository is a **beginner-to-intermediate Django learning project** structured as a small blog application with authentication and user profiles. It’s intentionally simple (SQLite, local dev defaults) but includes a few “real app” concerns like password reset email, middleware, and logging.

## Scope / features

- **Blog posts**: list/detail + CRUD via Django class-based views, author ownership enforcement.
- **Auth**: register/login/logout, login-required profile page.
- **Profiles**: `Profile` model with profile image upload + basic image resizing.
- **Password reset**: Django auth password reset flow (requires SMTP config).
- **Admin UX**: [`django-unfold`](https://github.com/unfoldadmin/django-unfold) installed for admin theming.
- **Dev tooling**: Django Debug Toolbar, Django Extensions.
- **Middleware**: IP blacklist middleware in `blog.middleware.ip_blacklist` and an auth/debug middleware in `users.middleware`.

## Tech stack

- **Python**: any modern 3.x (project uses Django 6.0.1)
- **Django**: 6.0.1
- **DB**: SQLite (local file)
- **UI**: Django templates + crispy forms (`crispy-bootstrap5`)

## Project layout

- `myproject/manage.py`: Django entrypoint
- `myproject/myproject/settings.py`: settings (see notes below)
- `myproject/blog/`: blog app (posts)
- `myproject/users/`: users app (registration/profile)
- `myproject/media/`: development media uploads (profile pictures, default avatar)

## Run locally

### 1) Create a virtualenv and install dependencies

From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Apply migrations

```bash
python myproject/manage.py migrate
```

### 3) Create an admin user (required after cloning)

Everyone who clones this repo must create their **own** admin account locally:

```bash
python myproject/manage.py createsuperuser
```

Then open `http://127.0.0.1:8000/admin/` and sign in.

### 4) Start the dev server

```bash
python myproject/manage.py runserver
```

App routes:

- Blog home: `http://127.0.0.1:8000/`
- Register: `http://127.0.0.1:8000/register/`
- Login: `http://127.0.0.1:8000/login/`
- Profile: `http://127.0.0.1:8000/profile/`

## Important configuration notes

### Email / password reset

Password reset endpoints are wired in `myproject/myproject/urls.py`. SMTP is currently configured directly in `myproject/myproject/settings.py`.

- If you want password reset to work, set **valid** values for:
  - `EMAIL_HOST_USER`
  - `EMAIL_HOST_PASSWORD` (Gmail *App Password* if using Gmail)
- If you don’t need email during local dev, you can switch to the console backend:

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

### HTTPS-only cookies during local development

`CSRF_COOKIE_SECURE = True` is enabled in settings. If you’re running plain `http://127.0.0.1:8000/` locally and hit CSRF issues, set it to `False` for local dev (or run behind HTTPS).

## Common dev commands

```bash
# Create migrations (if you change models)
python myproject/manage.py makemigrations

# Apply migrations
python myproject/manage.py migrate
```

## What’s intentionally not covered

- Production deployment configuration (allowed hosts, secure settings, static collection, etc.)
- Environment-based settings split (there is a `config/` folder in the repo, but `manage.py` uses `myproject.settings`)
- CI/CD
