# GCMS Dera Ismail Khan

A Django-based website built for Government College of Management Sciences (GCMS), Dera Ismail Khan. It handles the college's public-facing content — admissions, faculty, announcements, events, gallery — along with an admin panel to manage all of it without touching code.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python version" />
  <img src="https://img.shields.io/badge/Django-5.2.1-092E20?logo=django&logoColor=white" alt="Django version" />
  <img src="https://img.shields.io/badge/Tailwind%20CSS-latest-38B2AC?logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License" />
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Project status" />
</p>

<p align="center">
  <img src="docs/images/project-preview.svg" alt="GCMS Project Preview" width="1200" />
</p>

> The preview image above is a placeholder — swap it out with an actual screenshot before publishing the repo.

**Live demo:** [gcms-example.com](#) *(replace with your actual deployed URL, or remove this line if not yet deployed)*

## What this is

GCMS is a full website for a college, not just a template. It's built on Django, styled with Tailwind, and split into focused apps so each part of the site (departments, faculty, admissions, etc.) can be maintained independently. Content editors work through the Django admin, so updating a news post or adding a faculty member doesn't require a developer.

## Features

- Homepage with a hero section and quick navigation links
- Department listings with individual detail pages
- Faculty profile management
- Online admissions form with application status tracking
- News and announcements
- Event listings, including upcoming events
- Photo gallery / media library
- Download center for forms, prospectuses, and other institutional files
- Contact page with campus details
- Custom admin dashboard for content management
- Tailwind CSS for the frontend

## Built With

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Django 5.2.1 | Web framework |
| SQLite | Local development database |
| Tailwind CSS | Styling |
| WhiteNoise | Serving static files |
| Pillow | Image handling |
| python-dotenv | Environment variable management |

## Project Layout

```text
GCMS/
├── accounts/
├── admissions/
├── announcements/
├── assets/
├── contact/
├── core/
├── dashboard/
├── departments/
├── docs/
├── downloads/
├── events/
├── faculty/
├── gallery/
├── gcms_project/
├── homepage/
├── media/
├── news/
├── seo/
├── static/
├── staticfiles/
├── templates/
├── .env.example
├── db.sqlite3
├── manage.py
├── manage_gcms.py
├── package.json
├── requirements.txt
└── README.md
```

## Before You Start

You'll need these installed:

- Python
- pip
- Node.js and npm
- Git

## Setting It Up Locally

**1. Clone the repo**

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

**3. Install Python dependencies**

```bash
pip install -r requirements.txt
```

**4. Install frontend dependencies**

```bash
npm install
```

**5. Set up environment variables**

```bash
copy .env.example .env
```

Open `.env` and fill in your own secret key and config values.

**6. Build Tailwind CSS**

```bash
npm run build:css
```

For live rebuilds while developing:

```bash
npm run dev:css
```

**7. Run migrations**

```bash
python manage.py migrate
```

**8. Create a superuser**

```bash
python manage.py createsuperuser
```

**9. Start the dev server**

```bash
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/` in your browser.

## Environment Variables

Config is handled through environment variables — see `.env.example` for the full template. The key ones:

- `DEBUG`
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `EMAIL_BACKEND`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`

## Handy Commands

```bash
python manage.py check              # Run Django's system checks
python manage.py migrate            # Apply database migrations
python manage.py startapp app_name  # Scaffold a new app
python manage.py collectstatic      # Collect static files for production
```

## Going to Production

Don't deploy with the dev defaults. Before going live:

- Set `DEBUG=False`
- Use a strong, unique `SECRET_KEY`
- Set real values for `ALLOWED_HOSTS`
- Enable HTTPS and secure cookies
- Switch to a production-grade database (Postgres, MySQL, etc.)
- Run `collectstatic` and make sure static files are served correctly

## Screenshots

A placeholder lives at `docs/images/project-preview.svg`. Replace it with an actual screenshot of the running site once you're ready to share the repo publicly.

## Troubleshooting

A few issues that tend to come up during setup:

- **Tailwind styles not updating** — make sure `npm run dev:css` is running in a separate terminal while you develop. A one-off `npm run build:css` won't watch for changes.
- **`ModuleNotFoundError` after install** — double check your virtual environment is activated before running `pip install -r requirements.txt` or `manage.py` commands.
- **Static files missing in production** — run `python manage.py collectstatic` and confirm `STATIC_ROOT` is set correctly in your settings.
- **Migration errors after pulling new changes** — run `python manage.py migrate` again; if models changed significantly, you may need `makemigrations` first.
- **Emails not sending** — verify `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `.env`; most providers require an app-specific password rather than your regular account password.

## Contributing

Contributions are welcome. If you'd like to help:

1. Fork the repo and create a new branch for your change
2. Keep commits focused and write clear commit messages
3. Test your changes locally before opening a pull request
4. Open a PR describing what you changed and why

For larger changes, open an issue first to discuss the approach.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details. In short: you're free to use, modify, and distribute this code, including commercially, as long as the original license and copyright notice are kept.

*(If MIT isn't the license you actually want, swap this section and the `LICENSE` file for the correct one — e.g. GPL-3.0 or All Rights Reserved.)*

## Contact

Maintained by **[Your Name / GCMS Dev Team]**.

- Email: your-email@example.com
- GitHub: [@your-username](https://github.com/your-username)
- Institution: Government College of Management Sciences, Dera Ismail Khan

Questions, bug reports, and feature requests are best filed as [GitHub Issues](../../issues).

---

Built with Django and Tailwind CSS for GCMS Dera Ismail Khan.
