"""Settings for the local run mode (Story 1.1; AD-12, AD-13, AD-14, NFR-1, NFR-3, NFR-6).

The settings tests run src/prognose/settings.py again with a stubbed .env and
without the PROGNOSE_* variables and DATABASE_URL of the machine that runs them,
so the result never depends on that machine.
"""

import importlib.util
import os
import traceback
from pathlib import Path

import pytest
from django.core.exceptions import ImproperlyConfigured

from prognose import env

REPO_ROOT = Path(__file__).resolve().parents[1]
SETTINGS_FILE = REPO_ROOT / "src" / "prognose" / "settings.py"
STUB_SECRET_KEY = "stub-secret-key"
LOCAL_HOSTS = ["127.0.0.1", "localhost"]
FILE_URL = "postgresql://fil@h:5433/fra_fil"
CUSTOM_URL = "postgres://u:p%40ss@h:5433/x"
CUSTOM_DATABASE = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "x",
    "USER": "u",
    "PASSWORD": "p@ss",
    "HOST": "h",
    "PORT": 5433,
}


@pytest.fixture
def load_settings(monkeypatch):
    """Return a function that runs the settings module again and returns it.

    The function takes the stubbed .env values as a dict and the process
    variables as keyword arguments. The stubs also check that the settings read
    .env and .secret_key from the repository root.
    """
    for name in list(os.environ):
        if name.startswith("PROGNOSE_") or name == "DATABASE_URL":
            monkeypatch.delenv(name)

    def load(dotenv=None, **environ):
        def stub_read_dotenv(path):
            assert path == REPO_ROOT / ".env"
            return dict(dotenv or {})

        def stub_load_secret_key(path):
            assert path == REPO_ROOT / ".secret_key"
            return STUB_SECRET_KEY

        monkeypatch.setattr(env, "read_dotenv", stub_read_dotenv)
        monkeypatch.setattr(env, "load_secret_key", stub_load_secret_key)
        for name, value in environ.items():
            monkeypatch.setenv(name, value)
        spec = importlib.util.spec_from_file_location("settings_again", SETTINGS_FILE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    return load


def shown_error(error):
    """The traceback a user would see, with any chained exception."""
    return "".join(traceback.format_exception(error))


def test_defaults_need_no_variables_and_no_env_file(load_settings):
    """AD-13, AD-14, NFR-1, NFR-3: without variables or .env, Prognose uses the
    Compose database without a password, answers only to this computer, keeps
    DEBUG off and speaks Norwegian in Oslo time."""
    settings = load_settings()

    assert settings.BASE_DIR == REPO_ROOT
    assert settings.ALLOWED_HOSTS == LOCAL_HOSTS
    assert settings.DEBUG is False
    assert settings.DATABASES == {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "prognose",
            "USER": "prognose",
            "PASSWORD": "",
            "HOST": "127.0.0.1",
            "PORT": 15432,
        }
    }
    assert settings.LANGUAGE_CODE == "nb"
    assert settings.TIME_ZONE == "Europe/Oslo"
    assert settings.SECRET_KEY_FILE == REPO_ROOT / ".secret_key"
    assert settings.SECRET_KEY == STUB_SECRET_KEY


@pytest.mark.parametrize("source", ["environment", ".env"])
def test_phone_test_adds_the_lan_address_and_keeps_debug_off(load_settings, source):
    """AD-12, AD-13, NFR-6: PROGNOSE_LAN_HOST adds the computer's private address
    for the phone test, and DEBUG stays off even when .env turns it on."""
    if source == "environment":
        settings = load_settings(
            {"PROGNOSE_DEBUG": "1"}, PROGNOSE_LAN_HOST="192.168.1.20"
        )
    else:
        settings = load_settings(
            {"PROGNOSE_DEBUG": "1", "PROGNOSE_LAN_HOST": "192.168.1.20"}
        )

    assert settings.ALLOWED_HOSTS == [*LOCAL_HOSTS, "192.168.1.20"]
    assert settings.DEBUG is False


@pytest.mark.parametrize(
    "host", ["10.0.0.5", "172.16.0.1", "172.20.10.2", "172.31.255.254", "192.168.1.20"]
)
def test_private_network_addresses_are_allowed(host):
    """AD-13, NFR-6: any IPv4 address on a private network (RFC 1918) can be
    used for the phone test."""
    assert env.allowed_hosts(host) == [*LOCAL_HOSTS, host]


@pytest.mark.parametrize(
    "host",
    [
        "*",
        "0.0.0.0",
        "8.8.8.8",
        "172.32.0.1",
        "127.0.0.1",
        "prognose.example.com",
        "minmac.local",
        "192.168.1.20:8000",
        "fd00::1",
    ],
)
def test_unsafe_lan_host_is_refused(host):
    """AD-13, NFR-3: a wildcard, every address, a public or loopback address or
    a host name is refused, so the app is never opened beyond this computer and
    the private network."""
    with pytest.raises(ImproperlyConfigured, match="PROGNOSE_LAN_HOST må være"):
        env.allowed_hosts(host)


def test_settings_stop_on_an_unsafe_lan_host(load_settings):
    """AD-13, NFR-3: the settings refuse to load with an unsafe PROGNOSE_LAN_HOST."""
    with pytest.raises(ImproperlyConfigured, match="PROGNOSE_LAN_HOST"):
        load_settings(PROGNOSE_LAN_HOST="*")


@pytest.mark.parametrize(
    ("dotenv", "environ", "debug"),
    [
        ({"PROGNOSE_DEBUG": "1"}, {}, True),
        ({"PROGNOSE_DEBUG": "yes"}, {}, True),
        ({"PROGNOSE_DEBUG": "1"}, {"PROGNOSE_DEBUG": " "}, True),
        ({"PROGNOSE_DEBUG": "0"}, {}, False),
        ({}, {"PROGNOSE_DEBUG": "1"}, False),
        ({"PROGNOSE_DEBUG": "1"}, {"PROGNOSE_DEBUG": "0"}, False),
    ],
)
def test_only_dotenv_turns_debug_on(load_settings, dotenv, environ, debug):
    """AD-12, AD-13: only PROGNOSE_DEBUG in .env turns DEBUG on. The environment
    wins as for every variable, so it can turn DEBUG off but never on, and a
    blank value counts as unset."""
    assert load_settings(dotenv, **environ).DEBUG is debug


@pytest.mark.parametrize(
    ("value", "flag"),
    [
        ("1", True),
        ("true", True),
        ("True", True),
        ("yes", True),
        (" ON ", True),
        (None, False),
        ("", False),
        ("0", False),
        ("false", False),
        ("off", False),
        ("debug", False),
    ],
)
def test_flag_values(value, flag):
    """AD-12: 1, true, yes and on in any case turn a flag on; anything else is off."""
    assert env.env_flag(value) is flag


def test_environment_wins_over_dotenv(load_settings):
    """AD-13: a variable in the environment wins over the same one in .env."""
    settings = load_settings(
        {"DATABASE_URL": FILE_URL}, DATABASE_URL="postgresql://m@h:5433/fra_miljo"
    )

    assert settings.DATABASES["default"]["NAME"] == "fra_miljo"


def test_blank_variable_in_the_environment_does_not_hide_dotenv(load_settings):
    """AD-13: a blank variable in the environment counts as unset."""
    settings = load_settings({"DATABASE_URL": FILE_URL}, DATABASE_URL="  ")

    assert settings.DATABASES["default"]["NAME"] == "fra_fil"


def test_blank_values_give_the_defaults(load_settings):
    """AD-13: blank values in .env and the environment give the default settings."""
    settings = load_settings(
        {"DATABASE_URL": "", "PROGNOSE_LAN_HOST": ""}, PROGNOSE_LAN_HOST=""
    )

    assert settings.DATABASES["default"]["NAME"] == "prognose"
    assert settings.ALLOWED_HOSTS == LOCAL_HOSTS


def test_dotenv_values_never_reach_os_environ(load_settings):
    """AD-13: the settings read .env without changing os.environ."""
    before = dict(os.environ)

    load_settings(
        {"DATABASE_URL": FILE_URL, "PROGNOSE_LAN_HOST": "192.168.1.20"},
    )

    assert dict(os.environ) == before


def test_dotenv_with_byte_order_mark_comments_and_quotes(tmp_path):
    """AD-13: .env may be UTF-8 with a byte order mark and Windows line endings,
    with comments, quoted values and export in front of a name."""
    path = tmp_path / ".env"
    lines = [
        "DATABASE_URL=postgresql://u@h:5433/x",
        "# Lokale innstillinger",
        "",
        "export PROGNOSE_DEBUG=1  # feilsøkingssidene på",
        "PROGNOSE_LAN_HOST=   # fylles ut",
        'NAVN = "Bedrift # A"',
        "KORTNAVN='A'",
        "TOM=",
        "UTEN_LIKHETSTEGN",
    ]
    path.write_bytes(("\ufeff" + "\r\n".join(lines) + "\r\n").encode("utf-8"))

    assert env.read_dotenv(path) == {
        "DATABASE_URL": "postgresql://u@h:5433/x",
        "PROGNOSE_DEBUG": "1",
        "PROGNOSE_LAN_HOST": "",
        "NAVN": "Bedrift # A",
        "KORTNAVN": "A",
        "TOM": "",
    }


def test_missing_dotenv_gives_no_values(tmp_path):
    """AD-13, NFR-1: .env is optional."""
    assert env.read_dotenv(tmp_path / ".env") == {}


@pytest.mark.parametrize("encoding", ["latin-1", "utf-16"])
def test_dotenv_that_is_not_utf8_is_refused(tmp_path, encoding):
    """AD-13: a .env file in another encoding stops with a Norwegian message."""
    path = tmp_path / ".env"
    path.write_bytes("PROGNOSE_LAN_HOST=192.168.1.20  # på\n".encode(encoding))

    with pytest.raises(ImproperlyConfigured, match="ikke lagret som UTF-8"):
        env.read_dotenv(path)


def test_dotenv_that_is_a_folder_is_refused(tmp_path):
    """AD-13: a .env that is a folder, such as a virtual environment, stops the
    settings with a Norwegian message that names the file and the fix."""
    path = tmp_path / ".env"
    path.mkdir()

    with pytest.raises(
        ImproperlyConfigured, match=r"\.env kan ikke leses som en fil"
    ) as caught:
        env.read_dotenv(path)

    assert str(tmp_path) not in shown_error(caught.value)


def test_custom_database_url(load_settings):
    """AD-14: DATABASE_URL names another PostgreSQL database, with a
    percent-encoded password."""
    settings = load_settings(DATABASE_URL=CUSTOM_URL)

    assert settings.DATABASES["default"] == CUSTOM_DATABASE


def test_database_url_decodes_the_user_and_the_name():
    """AD-14: a percent-encoded user and database name are decoded."""
    config = env.database_config("postgresql://min%40bruker:p%40ss@h:5433/min%20db")

    assert config["USER"] == "min@bruker"
    assert config["NAME"] == "min db"


def test_database_url_without_a_port_uses_5432():
    """AD-14: a URL without a port uses PostgreSQL's default port."""
    config = env.database_config("postgresql://prognose@127.0.0.1/prognose")

    assert config["PORT"] == 5432


@pytest.mark.parametrize(
    ("url", "problem"),
    [
        ("mysql://u:hemmelig@h:5433/x", "må begynne med postgresql://"),
        ("postgresql://u:hemmelig@h:port/x", "ugyldig vert eller port"),
        ("postgresql://u:hemmelig@h:70000/x", "ugyldig vert eller port"),
        ("postgresql://u:hemmelig@h:0/x", "ugyldig port"),
        ("postgresql://u:hemmelig@[::1/x", "ugyldig vert eller port"),
        ("postgresql://u:hemmelig@:5433/x", "mangler vert"),
        ("postgresql://u:hemmelig@h:5433/", "mangler databasenavn"),
        ("postgresql://u:hemmelig@h:5433", "mangler databasenavn"),
        ("postgresql://u:hemmelig/x", "ugyldig vert eller port"),
    ],
)
def test_unusable_database_url_is_refused_without_repeating_it(url, problem):
    """AD-14, NFR-3: another scheme, a bad port, or no host or name stops the
    settings with a Norwegian message that shows neither the URL nor its
    password."""
    with pytest.raises(ImproperlyConfigured, match=problem) as caught:
        env.database_config(url)

    assert "hemmelig" not in shown_error(caught.value)


def test_secret_file_holds_the_session_secret(tmp_path):
    """NFR-3, AD-13: the settings read the session secret from .secret_key."""
    path = tmp_path / ".secret_key"
    path.write_text("lagret-nokkel\n", encoding="utf-8")

    assert env.load_secret_key(path) == "lagret-nokkel"


def test_missing_or_blank_secret_file_gives_a_random_key_per_process(tmp_path):
    """NFR-3, AD-13: until load_seed creates .secret_key, each process gets its
    own random key in memory, so migrate and the tests can run first."""
    missing = tmp_path / "mangler"
    blank = tmp_path / "tom"
    blank.write_text(" \n", encoding="utf-8")

    for path in (missing, blank):
        first, second = env.load_secret_key(path), env.load_secret_key(path)
        assert len(first) >= 50
        assert first != second
    assert not missing.exists()
    assert blank.read_text(encoding="utf-8") == " \n"


def test_secret_file_that_is_not_utf8_is_refused_without_showing_it(tmp_path):
    """NFR-3, AD-13: a damaged secret file stops with a Norwegian message that
    shows none of its bytes."""
    path = tmp_path / ".secret_key"
    path.write_bytes(b"\xffhemmelig")

    with pytest.raises(ImproperlyConfigured, match="Slett fila") as caught:
        env.load_secret_key(path)

    assert "0xff" not in shown_error(caught.value)


def test_secret_file_that_is_a_folder_is_refused(tmp_path):
    """NFR-3, AD-13: a .secret_key that is a folder stops the settings with a
    Norwegian message that names the file and the fix."""
    path = tmp_path / ".secret_key"
    path.mkdir()

    with pytest.raises(
        ImproperlyConfigured, match=r"\.secret_key kan ikke leses som en fil"
    ) as caught:
        env.load_secret_key(path)

    assert str(tmp_path) not in shown_error(caught.value)
