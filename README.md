# GCMS Dera Ismail Khan

A Django-based website built for Government College of Management Sciences (GCMS), Dera Ismail Khan. It handles the college's public-facing content — admissions, faculty, announcements, events, gallery — along with an admin panel to manage all of it without touching code.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python version" />
  <img src="https://img.shields.io/badge/Django-5.2.1-092E20?logo=django&logoColor=white" alt="Django version" />
  <img src="https://img.shields.io/badge/Tailwind%20CSS-latest-38B2AC?logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License" />
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Project status" />
</p>

<img width="1890" height="908" alt="image" src="https://github.com/user-attachments/assets/c0da62cd-fe61-4817-99b6-ccc47f7b176c" />


 The preview image above is a placeholder — swap it out with an actual screenshot before publishing the repo.



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

<img width="1892" height="886" alt="image" src="https://github.com/user-attachments/assets/e11e7ddd-7b26-4ab2-ada2-127edadac2d3" />
<img width="752" height="521" alt="image" src="https://github.com/user-attachments/assets/2a77997c-2598-48fc-b7d7-137bef47b975" />

<img width="853" height="772" alt="image" src="https://github.com/user-attachments/assets/60f9bd8f-5803-42f0-89cd-a1c3da39de63" />
<img width="860" height="857" alt="image" src="https://github.com/user-attachments/assets/efc20ec6-faa3-445b-a764-910e1bc0b325" />

<img width="761" height="630" alt="image" src="https://github.com/user-attachments/assets/26de1fa6-62f2-4847-9d29-7ec229f0603c" />
<img width="892" height="806" alt="image" src="https://github.com/user-attachments/assets/0a5af8ec-3c30-420b-b999-6620d544fb00" />
<img width="787" height="592" alt="image" src="https://github.com/user-attachments/assets/8846d8c4-e48f-4c26-8d9e-7c27e3c8d544" />
<img width="812" height="896" alt="image" src="https://github.com/user-attachments/assets/fcca31a4-d0aa-4925-abe7-07df2736410b" />
<img width="791" height="693" alt="image" src="https://github.com/user-attachments/assets/8f179ffc-07bb-409c-8059-1e7120d67764" />
<img width="620" height="880" alt="image" src="https://github.com/user-attachments/assets/1c52283a-6308-44f3-b0b2-ecb4ba11cc36" />

<img width="535" height="683" alt="image" src="https://github.com/user-attachments/assets/22b0d52b-3a3f-4e41-86f0-10358a3ec70c" />
<img width="1917" height="767" alt="image" src="https://github.com/user-attachments/assets/ce169fa3-ed99-4073-99fa-3eda6743ada3" />


<img width="488" height="883" alt="image" src="https://github.com/user-attachments/assets/f6dbd797-ff66-4d63-a4a4-fb1cb7412438" />
<img width="431" height="737" alt="image" src="https://github.com/user-attachments/assets/7573d2bd-c7fd-42bc-9c47-620c23075a29" />
<img width="892" height="256" alt="image" src="https://github.com/user-attachments/assets/0390b13a-96d5-4644-8a10-7119b69ed1c4" />
<img width="362" height="897" alt="image" src="https://github.com/user-attachments/assets/f84a2143-51bd-45d8-ba26-98e5a09fa4c9" />
<img width="365" height="817" alt="image" src="https://github.com/user-attachments/assets/e304da71-721e-4c69-92dd-5fb607f138a4" />
<img width="1877" height="788" alt="image" src="https://github.com/user-attachments/assets/39d8216f-38a2-4806-8557-64a027d8f613" />

<img width="841" height="513" alt="image" src="https://github.com/user-attachments/assets/dc10955f-dca1-4803-a71e-5e436f9f282b" />


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

## Contact


- Email:mrabidullah37@gmail.com

- Institution: Government College of Management Sciences, Dera Ismail Khan


---

Built with Django and Tailwind CSS for GCMS Dera Ismail Khan.
