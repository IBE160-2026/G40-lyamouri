"""load_seed creates the local session secret once and loads the seed data
(Stories 1.1 and 1.7; AD-13, AD-15, DR-4, FR-4, NFR-3).

Every test points SECRET_KEY_FILE and SEED_DIR at a temporary folder, so the
repository's own .secret_key and seed files are never touched, except the one
test that reads the committed files.
"""

import os
import re
import stat
import subprocess
from datetime import timedelta
from io import StringIO
from pathlib import Path
from unittest import mock

import pytest
import seed_files
from django.contrib.sessions.models import Session
from django.core.management import CommandError, call_command
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from forecasting import settings as defaults
from prognose import env
from web.management.commands.load_seed import Command
from web.models import Company, CompanySettings, Product, SalesWeek
from web.seed import read_seed

REPO_ROOT = Path(__file__).resolve().parents[1]

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def secret_file(settings, tmp_path):
    settings.SECRET_KEY_FILE = tmp_path / ".secret_key"
    return settings.SECRET_KEY_FILE


@pytest.fixture(autouse=True)
def seed_dir(settings, tmp_path):
    """Company A with two products and company B with one (seed_files.two_companies)."""
    directory = tmp_path / "seed"
    directory.mkdir()
    seed_files.write_files(directory, seed_files.two_companies())
    settings.SEED_DIR = directory
    return directory


def load_seed(*args):
    output = StringIO()
    call_command("load_seed", *args, stdout=output)
    return output.getvalue()


def typed(monkeypatch, answer):
    """Answer the prompt of --reset with answer, or end the input if it is None.
    Return the list that collects the prompts shown."""
    prompts = []

    def answer_prompt(prompt=""):
        prompts.append(prompt)
        if answer is None:
            raise EOFError
        return answer

    monkeypatch.setattr("builtins.input", answer_prompt)
    return prompts


def counts():
    return (
        Company.objects.count(),
        Product.objects.count(),
        SalesWeek.objects.count(),
        CompanySettings.objects.count(),
    )


def add_session():
    Session.objects.create(
        session_key="en-tilfeldig-nokkel",
        session_data="data",
        expire_date=timezone.now() + timedelta(days=1),
    )


def test_creates_the_missing_secret_for_the_owner_only(secret_file):
    """AD-13, NFR-3: without .secret_key, load_seed creates it from
    secrets.token_urlsafe(50), readable only by the owner on macOS and Linux."""
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
    """AD-13, NFR-3: running load_seed again never replaces the key it made, even
    though the second run stops on the data of the first."""
    load_seed()
    first = secret_file.read_bytes()

    with pytest.raises(CommandError, match="Databasen har allerede data"):
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


def test_creates_the_secret_before_it_stops_on_a_database_with_data(secret_file):
    """AD-13, AD-15, NFR-3: a database that holds data but has no .secret_key, as
    after a reused Docker volume, still gets the key before load_seed stops."""
    load_seed()
    secret_file.unlink()

    with pytest.raises(CommandError, match="Databasen har allerede data"):
        load_seed()

    assert re.fullmatch(r"[A-Za-z0-9_-]{67}", secret_file.read_text(encoding="utf-8"))


def test_loads_both_companies_into_an_empty_database():
    """FR-4, AD-15, DR-4: into an empty database, load_seed loads each company
    with its products and sales weeks and one settings row with the FR-20
    defaults, and says how much it loaded."""
    output = load_seed()

    assert "Lastet 2 bedrifter med 3 produkter og 10 salgsuker." in output
    assert counts() == (2, 3, 10, 2)
    a = Company.objects.get(customer_number="1001")
    assert a.name == "Testbedrift A"
    tape = Product.objects.get(company=a, product_number="10001")
    assert (tape.name, tape.stock_on_hand) == ("Malertape", 4)
    assert [
        (w.position, w.iso_year, w.iso_week, w.units_sold, w.stockout)
        for w in tape.sales_weeks.order_by("position")
    ] == [(1, 2026, 43, 5, False), (2, 2026, 44, 6, True), (3, 2026, 45, 7, False)]
    for company in Company.objects.all():
        row = company.company_settings
        assert (row.method, row.window, row.smoothing_factor) == (
            defaults.DEFAULT_METHOD,
            defaults.WINDOW.default,
            defaults.SMOOTHING_FACTOR.default,
        )
        assert (row.scenario_percentage, row.safety_margin) == (
            defaults.SCENARIO_PERCENTAGE.default,
            defaults.SAFETY_MARGIN.default,
        )
        assert row.unusual_weeks_included is defaults.DEFAULT_UNUSUAL_WEEKS_INCLUDED
        assert row.seasonal_adjustment is defaults.DEFAULT_SEASONAL_ADJUSTMENT


def test_each_company_ends_at_its_latest_data_week():
    """AD-8: the latest data week is the latest of the stored sales weeks, and
    every product of a company ends there; no model field stores it."""
    load_seed()

    for number, latest in (("1001", (2026, 45)), ("1002", (2026, 44))):
        company = Company.objects.get(customer_number=number)
        ends = {
            max(product.sales_weeks.values_list("iso_year", "iso_week"))
            for product in company.products.all()
        }
        assert ends == {latest}
    stored = {
        field.name
        for model in (Company, Product, SalesWeek, CompanySettings)
        for field in model._meta.get_fields()
    }
    assert not {name for name in stored if "latest" in name or "last_week" in name}


def test_the_committed_files_load_with_their_hashes_unchanged(settings):
    """FR-4, FR-1, NFR-3, AD-15: the real seed files load as they are. The stored
    hash is the file's, and logging in with the README password does not make
    Django rewrite it."""
    settings.SEED_DIR = REPO_ROOT / "data" / "seed"
    files = read_seed(settings.SEED_DIR)

    load_seed()

    assert counts() == (
        2,
        sum(len(c.products) for c in files),
        sum(len(p.units_sold) for c in files for p in c.products),
        2,
    )
    for seed, password in zip(files, ("testbedrift-a", "testbedrift-b"), strict=True):
        company = Company.objects.get(customer_number=seed.customer_number)
        assert company.password == seed.password_hash
        assert company.check_password(password)
        company.refresh_from_db()
        assert company.password == seed.password_hash


def test_the_number_of_queries_does_not_depend_on_the_number_of_products(seed_dir):
    """FR-4, AD-15: loading uses the same number of queries for two products as
    for fifty, because the rows are created in bulk."""
    with CaptureQueriesContext(connection) as small:
        load_seed()
    Company.objects.all().delete()
    for path in seed_dir.glob("*.json"):
        path.unlink()
    many = seed_files.two_companies()
    many[0]["products"] = [
        seed_files.product(f"{10000 + n}", f"Produkt {n}") for n in range(50)
    ]
    seed_files.write_files(seed_dir, many)

    with CaptureQueriesContext(connection) as large:
        load_seed()

    assert Product.objects.count() == 51
    assert len(large) == len(small)


def test_stops_and_changes_nothing_when_the_database_has_data():
    """DR-4, AD-15: without options, a database that holds a company is left as
    it is, and the message names the reset."""
    load_seed()
    CompanySettings.objects.update(window=5)
    before = counts()

    with pytest.raises(CommandError, match=r"Databasen har allerede data.*--reset"):
        load_seed()

    assert counts() == before
    assert set(CompanySettings.objects.values_list("window", flat=True)) == {5}


def test_reset_restores_the_seed_state(monkeypatch, secret_file):
    """DR-4, AD-15, FR-4: with the typed confirmation, --reset deletes the
    companies with their data and every session in one go and loads the seed
    again, so changed settings, a deleted product and an extra company are gone,
    nothing is duplicated, and the secret key is kept."""
    load_seed()
    seeded = counts()
    CompanySettings.objects.update(window=5, scenario_percentage=30)
    Product.objects.filter(product_number="10001").delete()
    Company.objects.create_user("9999", "hemmelig", name="Ekstra bedrift")
    add_session()
    key = secret_file.read_bytes()
    prompts = typed(monkeypatch, "nullstill")

    output = load_seed("--reset")

    (prompt,) = prompts
    assert "sletter alle bedrifter" in prompt
    assert "innstillinger" in prompt
    assert "justerte mengder" in prompt
    assert "Skriv «nullstill»" in prompt
    assert "Lastet 2 bedrifter" in output
    assert counts() == seeded
    assert not Company.objects.filter(customer_number="9999").exists()
    assert Product.objects.filter(product_number="10001").exists()
    assert set(CompanySettings.objects.values_list("window", flat=True)) == {
        defaults.WINDOW.default
    }
    assert set(
        CompanySettings.objects.values_list("scenario_percentage", flat=True)
    ) == {defaults.SCENARIO_PERCENTAGE.default}
    assert Session.objects.count() == 0
    assert secret_file.read_bytes() == key


def test_reset_loads_the_seed_into_an_empty_database(monkeypatch):
    """DR-4, AD-15: a confirmed reset on an empty database simply loads the seed."""
    typed(monkeypatch, "nullstill")

    load_seed("--reset")

    assert counts() == (2, 3, 10, 2)


@pytest.mark.parametrize("answer", ["ja", "", "nullstill nå", "Nullstill", None])
def test_reset_without_the_typed_confirmation_changes_nothing(monkeypatch, answer):
    """DR-4, AD-15: any other answer than the confirmation, or no input at all,
    leaves the data, the settings and the sessions as they are."""
    load_seed()
    CompanySettings.objects.update(window=5)
    add_session()
    before = counts()
    typed(monkeypatch, answer)

    with pytest.raises(CommandError, match="Bekreftelsen mangler"):
        load_seed("--reset")

    assert counts() == before
    assert set(CompanySettings.objects.values_list("window", flat=True)) == {5}
    assert Session.objects.count() == 1


def test_a_reset_that_fails_while_loading_keeps_the_old_data(monkeypatch):
    """DR-4, AD-15: the deletion and the load are one transaction, so an error
    after the deletion rolls the deletion back."""
    load_seed()
    CompanySettings.objects.update(window=5)
    add_session()
    before = counts()
    typed(monkeypatch, "nullstill")

    with (
        mock.patch.object(Command, "load", side_effect=RuntimeError("feil")),
        pytest.raises(RuntimeError),
    ):
        load_seed("--reset")

    assert counts() == before
    assert set(CompanySettings.objects.values_list("window", flat=True)) == {5}
    assert Session.objects.count() == 1


@pytest.mark.parametrize("reset", [False, True])
def test_a_broken_file_loads_nothing_and_deletes_nothing(monkeypatch, seed_dir, reset):
    """AD-8, AD-15: a file with a negative number is refused before the database
    is touched, and a reset does not even ask for the confirmation."""
    broken = seed_files.two_companies()
    broken[1]["products"][0]["units_sold"][0] = -1
    for path in seed_dir.glob("*.json"):
        path.unlink()
    seed_files.write_files(seed_dir, broken)
    monkeypatch.setattr(
        "builtins.input", lambda prompt="": pytest.fail("the reset asked anyway")
    )
    args = ["--reset"] if reset else []

    with pytest.raises(CommandError, match="Ingen data er lastet eller slettet"):
        load_seed(*args)

    assert counts() == (0, 0, 0, 0)


def test_a_broken_file_leaves_existing_data_untouched(monkeypatch, seed_dir):
    """AD-8, AD-15: with data in the database, a reset with a broken file keeps it."""
    load_seed()
    before = counts()
    broken = seed_files.two_companies()
    broken[0]["schema_version"] = 2
    seed_files.write_files(seed_dir, broken)
    typed(monkeypatch, "nullstill")

    with pytest.raises(CommandError, match="skjemaversjon 2"):
        load_seed("--reset")

    assert counts() == before


def test_only_the_command_runs_the_reset():
    """DR-4, AD-15: no workflow, compose file, script, setting or other command
    runs --reset. Every file that git tracks is read, except the command itself
    and the documents, which explain the reset, and the tests."""
    tracked = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split("\0")
    documents = ("tests/", "docs/", ".logs/", "_bmad-output/", "_bmad/", ".claude/")
    exempt = {"README.md", "data/README.md", "src/web/management/commands/load_seed.py"}
    named = []
    for name in filter(None, tracked):
        if name in exempt or name.startswith(documents):
            continue
        try:
            text = (REPO_ROOT / name).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "--reset" in text or "reset=True" in text:
            named.append(name)

    assert named == []
