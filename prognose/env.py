"""Helpers that turn the environment into settings (AD-12, AD-13, AD-15).

Each helper takes its inputs as arguments and changes no global state, so the
tests can check both run modes without reloading the settings. None of them
connects to the database, and no error message repeats a secret or a URL.
"""

import secrets
from collections.abc import Mapping
from pathlib import Path
from urllib.parse import unquote, urlsplit

from django.core.exceptions import ImproperlyConfigured

TRUE_VALUES = {"1", "true", "yes", "on"}
POSTGRESQL_SCHEMES = {"postgres", "postgresql"}

# The variables the published version cannot start without, with the fix for each.
REQUIRED_ON_VERCEL = {
    "SECRET_KEY": (
        "Sett SECRET_KEY for Production under Settings → Environment Variables "
        "i Vercel-prosjektet."
    ),
    "DATABASE_URL": (
        "Koble Neon-databasen til Vercel-prosjektet under Storage; "
        "da setter Vercel DATABASE_URL."
    ),
}


def read_dotenv(path: Path) -> dict[str, str]:
    """Return the KEY=VALUE lines of an optional .env file, or {} when it is missing.

    Blank lines and lines starting with # are skipped, and one pair of matching
    quotes around a value is removed.
    """
    try:
        text = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return {}
    values = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key] = value
    return values


def env_flag(value: str | None) -> bool:
    """True for 1, true, yes or on (in any case); anything else, or nothing, is False."""
    return (value or "").strip().lower() in TRUE_VALUES


def database_config(url: str | None, sqlite_path: Path) -> dict:
    """AD-15: the local SQLite file without a URL, PostgreSQL through psycopg with one.

    Every PostgreSQL connection requires SSL, closes after each request and uses
    no server-side cursors, so it also works behind Neon's connection pooler.
    Query parameters in the URL are ignored.
    """
    if not url:
        return {"ENGINE": "django.db.backends.sqlite3", "NAME": sqlite_path}
    parts = urlsplit(url)
    if parts.scheme not in POSTGRESQL_SCHEMES:
        raise ImproperlyConfigured(
            "DATABASE_URL må være en PostgreSQL-adresse som begynner med postgresql://."
        )
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": unquote(parts.path.removeprefix("/")),
        "USER": unquote(parts.username or ""),
        "PASSWORD": unquote(parts.password or ""),
        "HOST": parts.hostname or "",
        "PORT": parts.port or 5432,
        "CONN_MAX_AGE": 0,
        "DISABLE_SERVER_SIDE_CURSORS": True,
        "OPTIONS": {"sslmode": "require"},
    }


def published_settings(environ: Mapping[str, str]) -> dict:
    """AD-13: the settings for the published version on Vercel.

    Stops with ImproperlyConfigured if SECRET_KEY or DATABASE_URL is missing.
    The hosts come from Vercel's system variables, which hold no protocol.
    """
    for name, fix in REQUIRED_ON_VERCEL.items():
        if not environ.get(name):
            raise ImproperlyConfigured(
                f"Miljøvariabelen {name} mangler på Vercel. {fix}"
            )
    hosts = [
        host
        for host in (
            environ.get("VERCEL_PROJECT_PRODUCTION_URL"),
            environ.get("VERCEL_URL"),
        )
        if host
    ]
    return {
        "DEBUG": False,
        "SECRET_KEY": environ["SECRET_KEY"],
        "ALLOWED_HOSTS": hosts,
        "CSRF_TRUSTED_ORIGINS": [f"https://{host}" for host in hosts],
        "SECURE_PROXY_SSL_HEADER": ("HTTP_X_FORWARDED_PROTO", "https"),
        "SESSION_COOKIE_SECURE": True,
        "CSRF_COOKIE_SECURE": True,
    }


def load_secret_key(path: Path) -> str:
    """NFR-3, AD-12: the local secret from the secret file.

    Until load_seed creates the file, each process gets a random key that lives
    only in memory, so nothing is hard-coded and nothing is written here.
    """
    try:
        key = path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        key = ""
    return key or secrets.token_urlsafe(50)
