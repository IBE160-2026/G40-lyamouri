"""Django settings for Prognose's one run mode, the local one (AD-12, AD-13, AD-14).

Every value has a local default, so the basic setup needs neither a .env file
nor a key. A variable in the process environment wins over the same variable in
the optional .env file in the repository root, and a blank value counts as
unset. Reading .env never changes os.environ. The rules live in prognose/env.py.
"""

import os
from pathlib import Path

from prognose import env

# The repository root: this file is src/prognose/settings.py.
BASE_DIR = Path(__file__).resolve().parents[2]

_dotenv = env.read_dotenv(BASE_DIR / ".env")

# NFR-3, AD-13: load_seed creates this git-ignored file and never overwrites it.
SECRET_KEY_FILE = BASE_DIR / ".secret_key"
SECRET_KEY = env.load_secret_key(SECRET_KEY_FILE)

# AD-15: the seed files that load_seed reads, written by data/generate_seed.py.
SEED_DIR = BASE_DIR / "data" / "seed"

# AD-12: only PROGNOSE_DEBUG in .env turns DEBUG on, and never during the phone test.
DEBUG = env.debug_setting(os.environ, _dotenv)

# AD-13, NFR-6: this computer only, unless PROGNOSE_LAN_HOST is set for the phone test.
ALLOWED_HOSTS = env.allowed_hosts(
    env.config_value("PROGNOSE_LAN_HOST", os.environ, _dotenv)
)

# AD-14: the PostgreSQL database from compose.yaml, unless DATABASE_URL names another.
DATABASES = {
    "default": env.database_config(
        env.config_value("DATABASE_URL", os.environ, _dotenv)
        or env.DEFAULT_DATABASE_URL
    )
}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    # Also gives runserver its --insecure option.
    "django.contrib.staticfiles",
    "web",
]

MIDDLEWARE = [
    # AD-12: first, so that it also handles the database errors raised in the others.
    "web.middleware.ErrorPageMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "prognose.urls"
WSGI_APPLICATION = "prognose.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ],
        },
    },
]

# AD-6: the company is the user, and passwords use Django's default PBKDF2 hasher.
AUTH_USER_MODEL = "web.Company"

LANGUAGE_CODE = "nb"
TIME_ZONE = "Europe/Oslo"

STATIC_URL = "static/"

# AD-12: Django prints request and security errors to the console only with DEBUG
# on. These two loggers print them in both run modes, as the message and the
# traceback, never the request body. Configuring the parent logger "django"
# instead would also reset "django.server", which prints runserver's requests.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
