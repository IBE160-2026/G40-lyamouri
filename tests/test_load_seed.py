"""load_seed creates the local session secret once (Story 1.1; AD-13, NFR-3).

Every test points SECRET_KEY_FILE at a temporary folder, so the repository's own
.secret_key is never touched.
"""

import os
import re
import stat
from io import StringIO

import pytest
from django.core.management import CommandError, call_command

from prognose import env


@pytest.fixture
def secret_file(settings, tmp_path):
    settings.SECRET_KEY_FILE = tmp_path / ".secret_key"
    return settings.SECRET_KEY_FILE


def load_seed():
    output = StringIO()
    call_command("load_seed", stdout=output)
    return output.getvalue()


@pytest.mark.django_db
def test_creates_the_missing_secret_for_the_owner_only(
    secret_file, django_assert_num_queries
):
    """AD-13, NFR-3: without .secret_key, load_seed creates it from
    secrets.token_urlsafe(50), readable only by the owner on macOS and Linux,
    and loads no data."""
    with django_assert_num_queries(0):
        output = load_seed()

    assert "Lagde .secret_key" in output
    key = secret_file.read_text(encoding="utf-8")
    assert re.fullmatch(r"[A-Za-z0-9_-]{67}", key)
    if os.name == "posix":
        assert stat.S_IMODE(secret_file.stat().st_mode) == 0o600
    assert env.load_secret_key(secret_file) == key


def test_leaves_an_existing_secret_unchanged(secret_file):
    """AD-13, NFR-3: an existing key stays byte for byte, and load_seed says so."""
    secret_file.write_bytes(b"eksisterende-nokkel\r\n")

    output = load_seed()

    assert ".secret_key finnes allerede og er ikke endret." in output
    assert secret_file.read_bytes() == b"eksisterende-nokkel\r\n"


def test_second_run_keeps_the_first_secret(secret_file):
    """AD-13, NFR-3: running load_seed again never replaces the key it made."""
    load_seed()
    first = secret_file.read_bytes()

    load_seed()

    assert secret_file.read_bytes() == first


@pytest.mark.parametrize("content", [b"", b" \n"])
def test_blank_secret_stops_and_stays_unchanged(secret_file, content):
    """AD-13, NFR-3: a blank .secret_key is left as it is, and load_seed stops
    and says to delete it and run again."""
    secret_file.write_bytes(content)

    with pytest.raises(CommandError, match="Slett fila og kjør load_seed på nytt"):
        load_seed()

    assert secret_file.read_bytes() == content
