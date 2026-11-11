"""Settings for Prognose, with two run modes (AD-13).

Local (no VERCEL variable): SQLite unless DATABASE_URL is set, the secret from
.secret_key, and the optional .env file, which is the only way to turn DEBUG on.

Published on Vercel (VERCEL is set): every value comes from the environment,
DEBUG is always off, and startup stops if SECRET_KEY or DATABASE_URL is missing.

The logic lives in prognose/env.py. Nothing here connects to the database.
"""

import os
from pathlib import Path

from prognose.env import (
    database_config,
    env_flag,
    load_secret_key,
    published_settings,
    read_dotenv,
)

BASE_DIR = Path(__file__).resolve().parent.parent

ON_VERCEL = bool(os.environ.get("VERCEL"))

# NFR-3, AD-12: load_seed creates this gitignored file. There is none on Vercel.
SECRET_KEY_FILE = BASE_DIR / ".secret_key"

if ON_VERCEL:
    # Sets SECRET_KEY, DEBUG (off), ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS,
    # SECURE_PROXY_SSL_HEADER and the secure cookie flags. .env is never read here.
    globals().update(published_settings(os.environ))
else:
    SECRET_KEY = load_secret_key(SECRET_KEY_FILE)
    # DEBUG stays off unless .env turns it on; the process environment cannot.
    DEBUG = env_flag(read_dotenv(BASE_DIR / ".env").get("DEBUG"))
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# AD-15: PostgreSQL when DATABASE_URL is set (always on Vercel, checked above),
# otherwise the local SQLite file.
DATABASES = {
    "default": database_config(os.environ.get("DATABASE_URL"), BASE_DIR / "db.sqlite3")
}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "accounts",
    "planning",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # AD-5: every view needs a login unless it is marked login_not_required.
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "prognose.urls"
WSGI_APPLICATION = "prognose.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ],
        },
    },
]

# AD-5: the company is the logged-in user, and the start page is the login page.
AUTH_USER_MODEL = "accounts.Company"
LOGIN_URL = "/"

LANGUAGE_CODE = "nb"
TIME_ZONE = "Europe/Oslo"
USE_I18N = True
USE_TZ = True

# Locally, runserver --insecure serves static/. On Vercel, collectstatic fills
# STATIC_ROOT during the build and the CDN serves it at /static/.
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Console logging only, in both run modes, so errors behind the 500 page show up
# in the terminal and in Vercel's logs. Django logs the address and the
# traceback, never passwords, secrets or request bodies.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django": {"handlers": ["console"], "level": "INFO"}},
}
