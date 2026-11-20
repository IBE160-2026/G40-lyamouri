"""Helpers that turn the environment into Prognose's settings (AD-12, AD-13, AD-14).

Each helper takes its inputs as arguments and changes no global state: none of
them writes to os.environ or connects to the database. Error messages are in
Norwegian and never repeat a database URL or a secret.
"""

import ipaddress
import re
import secrets
from collections.abc import Mapping
from pathlib import Path
from urllib.parse import unquote, urlsplit

from django.core.exceptions import ImproperlyConfigured

# AD-13: the database from compose.yaml, which has no password.
DEFAULT_DATABASE_URL = "postgresql://prognose@127.0.0.1:15432/prognose"
DEFAULT_POSTGRESQL_PORT = 5432
POSTGRESQL_SCHEMES = frozenset({"postgres", "postgresql"})

LOCAL_HOSTS = ("127.0.0.1", "localhost")
# RFC 1918: the IPv4 ranges of private networks, such as a home or office network.
PRIVATE_NETWORKS = tuple(
    ipaddress.IPv4Network(network)
    for network in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")
)

TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
# In an unquoted .env value, a # at the start or after whitespace starts a comment.
INLINE_COMMENT = re.compile(r"(?:^|\s+)#.*$")


def read_dotenv(path: Path) -> dict[str, str]:
    """Return the KEY=VALUE lines of an optional .env file, or {} when it is missing.

    The file must be UTF-8, with or without a byte order mark. Blank lines,
    lines starting with # and lines without = are skipped, and an export in
    front of a name is ignored. A value in matching quotes is taken as it is;
    an unquoted value ends at a # that starts it or follows whitespace.
    """
    try:
        text = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return {}
    except UnicodeDecodeError:
        raise ImproperlyConfigured(
            f"{path.name} er ikke lagret som UTF-8. Lagre fila som UTF-8 og prøv igjen."
        ) from None
    except OSError:
        raise ImproperlyConfigured(
            f"{path.name} kan ikke leses som en fil. Er det en mappe, for eksempel "
            "et virtuelt miljø, gi den et annet navn. Er det en fil, sørg for at du "
            "har lesetilgang til den."
        ) from None
    values = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        values[key.removeprefix("export ").lstrip()] = _dotenv_value(value)
    return values


def _dotenv_value(text: str) -> str:
    if text[:1] in {'"', "'"}:
        closing = text.find(text[0], 1)
        if closing != -1:
            return text[1:closing]
    return INLINE_COMMENT.sub("", text)


def config_value(
    name: str, environ: Mapping[str, str], dotenv: Mapping[str, str]
) -> str | None:
    """Return the variable from the environment, else from .env, else None.

    A blank value counts as unset, so it never hides a value in .env.
    """
    for source in (environ, dotenv):
        value = source.get(name, "").strip()
        if value:
            return value
    return None


def env_flag(value: str | None) -> bool:
    """True for 1, true, yes or on in any case; anything else, or nothing, is False."""
    return (value or "").strip().lower() in TRUE_VALUES


def debug_setting(environ: Mapping[str, str], dotenv: Mapping[str, str]) -> bool:
    """AD-12: DEBUG is on only when .env turns it on and the phone test is off.

    The environment wins over .env here as everywhere, so it can turn DEBUG
    off, but never on.
    """
    return (
        env_flag(dotenv.get("PROGNOSE_DEBUG"))
        and env_flag(config_value("PROGNOSE_DEBUG", environ, dotenv))
        and config_value("PROGNOSE_LAN_HOST", environ, dotenv) is None
    )


def allowed_hosts(lan_host: str | None) -> list[str]:
    """AD-13, NFR-6: this computer's names, plus its private address for the phone test.

    The address must be an IPv4 address on a private network. Anything that
    would open the app to every host or to the internet is refused.
    """
    if not lan_host:
        return list(LOCAL_HOSTS)
    try:
        address = ipaddress.IPv4Address(lan_host)
    except ValueError:
        address = None
    if address is None or not any(address in net for net in PRIVATE_NETWORKS):
        raise ImproperlyConfigured(
            "PROGNOSE_LAN_HOST må være maskinens IPv4-adresse på et privat nettverk "
            "(10.x.x.x, 172.16.x.x til 172.31.x.x eller 192.168.x.x), for eksempel "
            "192.168.1.20. Rett adressen, eller fjern variabelen når du ikke "
            "tester på telefon."
        )
    return [*LOCAL_HOSTS, str(address)]


def database_config(url: str) -> dict:
    """AD-14: Django's settings for the PostgreSQL database that the URL names.

    The user, the password and the database name may be percent-encoded. A URL
    without a port uses PostgreSQL's 5432, and query parameters are ignored.
    """
    try:
        parts = urlsplit(url)
        port = parts.port
    except ValueError:  # a port outside 0-65535 or not a number, or a broken host
        raise _database_url_error("har en ugyldig vert eller port") from None
    if parts.scheme not in POSTGRESQL_SCHEMES:
        raise _database_url_error("må begynne med postgresql://")
    if port == 0:
        raise _database_url_error("har en ugyldig port")
    if not parts.hostname:
        raise _database_url_error("mangler vert")
    name = unquote(parts.path.removeprefix("/"))
    if not name:
        raise _database_url_error("mangler databasenavn")
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": name,
        "USER": unquote(parts.username or ""),
        "PASSWORD": unquote(parts.password or ""),
        "HOST": parts.hostname,
        "PORT": port or DEFAULT_POSTGRESQL_PORT,
    }


def _database_url_error(problem: str) -> ImproperlyConfigured:
    # The message never repeats the URL, which may hold a password.
    return ImproperlyConfigured(
        f"DATABASE_URL {problem}. Bruk formen postgresql://bruker@vert:port/database, "
        "med spesialtegn i brukernavnet, passordet og databasenavnet prosentkodet, "
        "for eksempel @ som %40 og # som %23. Du kan også fjerne DATABASE_URL for å "
        "bruke databasen fra compose.yaml."
    )


def read_secret_key(path: Path) -> str:
    """Return the key in the secret file, or "" when the file is missing or blank."""
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""
    except UnicodeDecodeError:
        raise ImproperlyConfigured(
            f"{path.name} er ikke en gyldig nøkkelfil. "
            "Slett fila og kjør load_seed på nytt."
        ) from None
    except OSError:
        raise ImproperlyConfigured(
            f"{path.name} kan ikke leses som en fil. Er det en mappe, slett den og "
            "kjør load_seed på nytt. Er det en fil, sørg for at du har lesetilgang "
            "til den."
        ) from None


def load_secret_key(path: Path) -> str:
    """NFR-3, AD-13: the session secret from the secret file.

    Until load_seed creates the file, and while it is blank, each process gets
    a random key that lives only in memory, so migrate and the tests can run
    before load_seed. Nothing is written here.
    """
    return read_secret_key(path) or secrets.token_urlsafe(50)
