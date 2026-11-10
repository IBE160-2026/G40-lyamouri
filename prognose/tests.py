"""Settings and architecture tests (Story 1.1; AD-1, AD-12, AD-13, AD-15, NFR-3, DR-10).

The run modes are checked twice: through the helpers in prognose/env.py, and by
starting Django in a fresh process with a chosen environment, as Vercel does.
"""

import ast
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from prognose.env import (
    database_config,
    env_flag,
    load_secret_key,
    published_settings,
    read_dotenv,
)

BASE_DIR = settings.BASE_DIR
SQLITE_PATH = BASE_DIR / "db.sqlite3"
POSTGRESQL_URL = "postgresql://u:p%40ss@h:5432/db"
PUBLISHED_ENV = {
    "VERCEL": "1",
    "SECRET_KEY": "published-test-secret",
    "DATABASE_URL": POSTGRESQL_URL,
    "VERCEL_PROJECT_PRODUCTION_URL": "x.vercel.app",
    "VERCEL_URL": "y.vercel.app",
}


def temp_dir(test_case):
    """A temporary folder that is removed after the test."""
    folder = tempfile.TemporaryDirectory()
    test_case.addCleanup(folder.cleanup)
    return Path(folder.name)


class ReadDotenvTests(SimpleTestCase):
    def test_missing_file_gives_no_values(self):
        self.assertEqual(read_dotenv(temp_dir(self) / ".env"), {})

    def test_reads_values_and_skips_comments_and_blank_lines(self):
        path = temp_dir(self) / ".env"
        path.write_text(
            "# kommentar\n"
            "\n"
            "DEBUG=1\n"
            'PROGNOSE_LLM_URL = "http://127.0.0.1:11434"\n'
            "PROGNOSE_LLM_MODEL=\n"
            "UTEN_LIKHETSTEGN\n",
            encoding="utf-8",
        )
        self.assertEqual(
            read_dotenv(path),
            {
                "DEBUG": "1",
                "PROGNOSE_LLM_URL": "http://127.0.0.1:11434",
                "PROGNOSE_LLM_MODEL": "",
            },
        )


class EnvFlagTests(SimpleTestCase):
    def test_only_clear_yes_values_turn_a_flag_on(self):
        for value in ("1", "true", "True", "yes", "on", " ON "):
            with self.subTest(value=value):
                self.assertTrue(env_flag(value))
        for value in (None, "", "0", "false", "no", "off", "debug"):
            with self.subTest(value=value):
                self.assertFalse(env_flag(value))


class DatabaseConfigTests(SimpleTestCase):
    """AD-15 and FR-4: SQLite locally, PostgreSQL through DATABASE_URL."""

    def test_without_url_uses_the_local_sqlite_file(self):
        for url in (None, ""):
            with self.subTest(url=url):
                self.assertEqual(
                    database_config(url, SQLITE_PATH),
                    {"ENGINE": "django.db.backends.sqlite3", "NAME": SQLITE_PATH},
                )

    def test_postgresql_url(self):
        self.assertEqual(
            database_config(POSTGRESQL_URL, SQLITE_PATH),
            {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "db",
                "USER": "u",
                "PASSWORD": "p@ss",
                "HOST": "h",
                "PORT": 5432,
                "CONN_MAX_AGE": 0,
                "DISABLE_SERVER_SIDE_CURSORS": True,
                "OPTIONS": {"sslmode": "require"},
            },
        )

    def test_ssl_is_required_even_if_the_url_asks_otherwise(self):
        config = database_config("postgres://u:p@h/db?sslmode=disable", SQLITE_PATH)
        self.assertEqual(config["OPTIONS"], {"sslmode": "require"})
        self.assertEqual(config["PORT"], 5432)

    def test_other_databases_are_refused_without_repeating_the_url(self):
        with self.assertRaises(ImproperlyConfigured) as caught:
            database_config("mysql://u:hemmelig@h/db", SQLITE_PATH)
        self.assertNotIn("hemmelig", str(caught.exception))


class PublishedSettingsTests(SimpleTestCase):
    """AD-13 and DR-10: the settings on Vercel."""

    def test_published(self):
        self.assertEqual(
            published_settings(PUBLISHED_ENV),
            {
                "DEBUG": False,
                "SECRET_KEY": "published-test-secret",
                "ALLOWED_HOSTS": ["x.vercel.app", "y.vercel.app"],
                "CSRF_TRUSTED_ORIGINS": [
                    "https://x.vercel.app",
                    "https://y.vercel.app",
                ],
                "SECURE_PROXY_SSL_HEADER": ("HTTP_X_FORWARDED_PROTO", "https"),
                "SESSION_COOKIE_SECURE": True,
                "CSRF_COOKIE_SECURE": True,
            },
        )

    def test_missing_or_empty_variable_stops_with_its_name(self):
        for name in ("SECRET_KEY", "DATABASE_URL"):
            missing = {
                key: value for key, value in PUBLISHED_ENV.items() if key != name
            }
            empty = {**PUBLISHED_ENV, name: ""}
            for environ in (missing, empty):
                with (
                    self.subTest(name=name, empty=name in environ),
                    self.assertRaisesMessage(
                        ImproperlyConfigured, f"Miljøvariabelen {name}"
                    ),
                ):
                    published_settings(environ)


class LoadSecretKeyTests(SimpleTestCase):
    """NFR-3 and AD-12: the local session secret."""

    def test_reads_the_secret_file(self):
        path = temp_dir(self) / ".secret_key"
        path.write_text("lagret-nokkel\n", encoding="utf-8")
        self.assertEqual(load_secret_key(path), "lagret-nokkel")

    def test_without_the_file_each_process_gets_a_random_key_in_memory(self):
        path = temp_dir(self) / ".secret_key"
        first, second = load_secret_key(path), load_secret_key(path)
        self.assertGreaterEqual(len(first), 50)
        self.assertNotEqual(first, second)
        self.assertFalse(path.exists())


# Starts Django through Vercel's entry point and prints what the run modes change.
# A wrapper around load_secret_key records which secret file the settings read.
# A stand-in for read_dotenv records the paths it is given and returns the JSON in
# PROBE_DOTENV, so no test depends on the developer's own .env.
SETTINGS_PROBE = """
import json
import logging
import os

import prognose.env

secret_files, secret_keys, dotenv_paths = [], [], []
read_secret_file = prognose.env.load_secret_key


def recording_load_secret_key(path):
    secret_files.append(str(path))
    secret_keys.append(read_secret_file(path))
    return secret_keys[-1]


def probe_read_dotenv(path):
    dotenv_paths.append(str(path))
    return json.loads(os.environ.get("PROBE_DOTENV", "{}"))


prognose.env.load_secret_key = recording_load_secret_key
prognose.env.read_dotenv = probe_read_dotenv

import prognose.wsgi
from django.conf import settings

# LOGGING must send request errors to the console, also with DEBUG off.
logging.getLogger("django.request").error("Probe error for the console log")

database = settings.DATABASES["default"]
print(json.dumps({
    "DEBUG": settings.DEBUG,
    "DOTENV_PATHS": dotenv_paths,
    "SECRET_KEY_FROM_ENV": settings.SECRET_KEY == os.environ.get("SECRET_KEY"),
    "SECRET_FILES_READ": secret_files,
    "SECRET_KEY_FROM_FILE": secret_keys == [settings.SECRET_KEY],
    "ALLOWED_HOSTS": settings.ALLOWED_HOSTS,
    "CSRF_TRUSTED_ORIGINS": settings.CSRF_TRUSTED_ORIGINS,
    "SECURE_PROXY_SSL_HEADER": settings.SECURE_PROXY_SSL_HEADER,
    "SESSION_COOKIE_SECURE": settings.SESSION_COOKIE_SECURE,
    "CSRF_COOKIE_SECURE": settings.CSRF_COOKIE_SECURE,
    "ENGINE": database["ENGINE"],
    "NAME": str(database["NAME"]),
    "HOST": database.get("HOST", ""),
    "LANGUAGE_CODE": settings.LANGUAGE_CODE,
    "TIME_ZONE": settings.TIME_ZONE,
}))
"""

# The variables the tests set themselves; the developer's own values are left out.
RUN_MODE_VARIABLES = {
    "VERCEL",
    "VERCEL_URL",
    "VERCEL_PROJECT_PRODUCTION_URL",
    "SECRET_KEY",
    "DATABASE_URL",
    "DEBUG",
    "PROBE_DOTENV",
}


def start_app(**environ):
    """Run SETTINGS_PROBE in a fresh Python process with the given variables."""
    child_env = {
        key: value for key, value in os.environ.items() if key not in RUN_MODE_VARIABLES
    }
    child_env.update(
        environ, DJANGO_SETTINGS_MODULE="prognose.settings", PYTHONIOENCODING="utf-8"
    )
    return subprocess.run(
        [sys.executable, "-c", SETTINGS_PROBE],
        cwd=BASE_DIR,
        env=child_env,
        capture_output=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )


class RunModeTests(SimpleTestCase):
    """AD-13 and AD-15: the real settings in each run mode."""

    def test_local_run(self):
        result = start_app(PROBE_DOTENV=json.dumps({"DEBUG": "1"}))
        self.assertEqual(result.returncode, 0, result.stderr)
        values = json.loads(result.stdout)
        # Locally the settings read .env in the project folder, which can turn DEBUG on.
        self.assertEqual(values["DOTENV_PATHS"], [str(BASE_DIR / ".env")])
        self.assertTrue(values["DEBUG"])
        self.assertEqual(values["ENGINE"], "django.db.backends.sqlite3")
        self.assertEqual(values["NAME"], str(SQLITE_PATH))
        self.assertEqual(values["ALLOWED_HOSTS"], ["127.0.0.1", "localhost"])
        # AD-12: the key comes from .secret_key (LoadSecretKeyTests covers the file).
        self.assertEqual(values["SECRET_FILES_READ"], [str(BASE_DIR / ".secret_key")])
        self.assertTrue(values["SECRET_KEY_FROM_FILE"])
        self.assertEqual(values["LANGUAGE_CODE"], "nb")
        self.assertEqual(values["TIME_ZONE"], "Europe/Oslo")

    def test_local_run_ignores_debug_in_the_process_environment(self):
        # Only .env can turn DEBUG on, so DEBUG=1 in the environment does nothing.
        result = start_app(DEBUG="1", PROBE_DOTENV="{}")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["DEBUG"])

    def test_local_run_with_database_url_uses_postgresql(self):
        # README step 5: the owner runs migrate from the PC against Neon.
        result = start_app(DATABASE_URL=POSTGRESQL_URL)
        self.assertEqual(result.returncode, 0, result.stderr)
        values = json.loads(result.stdout)
        self.assertEqual(values["ENGINE"], "django.db.backends.postgresql")
        self.assertEqual(values["HOST"], "h")

    def test_published(self):
        # Host "h" does not exist, so a clean start also shows that neither the
        # settings nor the startup connect to the database.
        result = start_app(
            DEBUG="1", PROBE_DOTENV=json.dumps({"DEBUG": "1"}), **PUBLISHED_ENV
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        values = json.loads(result.stdout)
        # .env is never read on Vercel, so even a .env with DEBUG=1 leaves DEBUG off.
        self.assertEqual(values["DOTENV_PATHS"], [])
        self.assertFalse(values["DEBUG"])
        # LOGGING sends request errors to the console (Vercel's logs) with DEBUG off.
        self.assertIn("Probe error for the console log", result.stderr)
        self.assertTrue(values["SECRET_KEY_FROM_ENV"])
        # AD-12: there is no secret file on Vercel.
        self.assertEqual(values["SECRET_FILES_READ"], [])
        self.assertEqual(values["ALLOWED_HOSTS"], ["x.vercel.app", "y.vercel.app"])
        self.assertEqual(
            values["CSRF_TRUSTED_ORIGINS"],
            ["https://x.vercel.app", "https://y.vercel.app"],
        )
        self.assertEqual(
            values["SECURE_PROXY_SSL_HEADER"], ["HTTP_X_FORWARDED_PROTO", "https"]
        )
        self.assertTrue(values["SESSION_COOKIE_SECURE"])
        self.assertTrue(values["CSRF_COOKIE_SECURE"])
        self.assertEqual(values["ENGINE"], "django.db.backends.postgresql")
        self.assertEqual(values["HOST"], "h")

    def test_published_without_a_required_variable_stops(self):
        for name in ("SECRET_KEY", "DATABASE_URL"):
            with self.subTest(missing=name):
                environ = {
                    key: value for key, value in PUBLISHED_ENV.items() if key != name
                }
                result = start_app(**environ)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("ImproperlyConfigured", result.stderr)
                self.assertIn(f"Miljøvariabelen {name} mangler", result.stderr)
                # The error repeats neither the secret nor the database password.
                self.assertNotIn("published-test-secret", result.stderr)
                self.assertNotIn("p%40ss", result.stderr)


# The shell around the pure core: Django and the project's Django packages.
SHELL_MODULES = frozenset({"django", "accounts", "planning", "prognose"})


class PureCoreTests(SimpleTestCase):
    """AD-1: forecasting/ and explanation/ never import Django or the Django apps."""

    def test_pure_core_imports_no_django(self):
        for package in ("forecasting", "explanation"):
            files = sorted((BASE_DIR / package).rglob("*.py"))
            self.assertTrue(files, f"{package}/ has no Python files")
            for path in files:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        modules = [alias.name for alias in node.names]
                    elif isinstance(node, ast.ImportFrom) and node.level == 0:
                        modules = [node.module]
                    else:
                        continue
                    for module in modules:
                        with self.subTest(file=path.relative_to(BASE_DIR).as_posix()):
                            self.assertNotIn(module.split(".")[0], SHELL_MODULES)
