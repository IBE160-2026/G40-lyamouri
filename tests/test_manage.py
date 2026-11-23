"""manage.py, the WSGI entry point and pytest always use Prognose's settings (Story 1.1; AD-13).

A DJANGO_SETTINGS_MODULE exported for another project must not win, or the
README commands and the tests fail with an ImportError. These tests have no
database access.
"""

import importlib
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import django.core.management

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_manage_py_always_uses_prognose_settings(monkeypatch):
    """AD-13: manage.py sets prognose.settings even when another project's
    settings module is exported, and passes the command line on to Django."""
    calls = []
    monkeypatch.setenv("DJANGO_SETTINGS_MODULE", "annet.settings")
    monkeypatch.setattr(
        django.core.management, "execute_from_command_line", calls.append
    )
    spec = importlib.util.spec_from_file_location(
        "manage_under_test", REPO_ROOT / "src" / "manage.py"
    )
    manage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(manage)

    manage.main()

    assert os.environ["DJANGO_SETTINGS_MODULE"] == "prognose.settings"
    assert calls == [sys.argv]


def test_wsgi_always_uses_prognose_settings(monkeypatch):
    """AD-13: the WSGI entry point sets prognose.settings even when another
    project's settings module is exported."""
    monkeypatch.setenv("DJANGO_SETTINGS_MODULE", "annet.settings")

    importlib.reload(importlib.import_module("prognose.wsgi"))

    assert os.environ["DJANGO_SETTINGS_MODULE"] == "prognose.settings"


def test_pytest_uses_prognose_settings_when_another_module_is_exported():
    """AD-13: the --ds option makes pytest use prognose.settings even when
    another project's settings module is exported."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "-p",
            "no:cacheprovider",
            "tests/test_company.py",
        ],
        cwd=REPO_ROOT,
        env={**os.environ, "DJANGO_SETTINGS_MODULE": "annet.settings"},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
