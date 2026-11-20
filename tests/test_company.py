"""web.Company, the custom user model (Story 1.1; AD-6, AD-17, FR-1, NFR-3)."""

from importlib import import_module
from io import StringIO

import pytest
from django.contrib.auth import authenticate, get_user_model
from django.core.management import call_command
from django.db import migrations

from web.models import Company


def test_company_is_the_user_model_with_customer_number_as_login():
    """AD-6, FR-1: the company is the user and logs in with its unique customer
    number."""
    assert get_user_model() is Company
    assert Company.USERNAME_FIELD == "customer_number"
    assert Company._meta.get_field("customer_number").unique
    assert Company.REQUIRED_FIELDS == ("name",)


def test_first_migration_creates_company():
    """AD-6: web.0001_initial is the app's first migration and creates Company
    with its login field and name, so the user model exists before the first
    migrate."""
    migration = import_module("web.migrations.0001_initial").Migration

    assert migration.initial is True
    assert migration.dependencies == []
    (operation,) = migration.operations
    assert isinstance(operation, migrations.CreateModel)
    assert operation.name == "Company"
    fields = dict(operation.fields)
    assert fields["customer_number"].unique
    assert {"password", "last_login", "customer_number", "name"} <= fields.keys()


@pytest.mark.django_db
def test_migrations_match_the_models():
    """AD-17: makemigrations --check finds no model change without a migration."""
    output = StringIO()
    try:
        call_command("makemigrations", "--check", "--dry-run", stdout=output)
    except SystemExit:
        pytest.fail(f"A model change has no migration:\n{output.getvalue()}")


@pytest.mark.django_db
def test_password_is_stored_as_a_pbkdf2_hash():
    """FR-1, NFR-3, AD-6: Django's default PBKDF2 hasher stores the password,
    never the plain text, and only the right password logs in."""
    company = Company.objects.create_user(
        "100001", "hemmelig-passord", name="Testbedrift A"
    )
    company.refresh_from_db()

    assert company.password.startswith("pbkdf2_sha256$")
    assert "hemmelig-passord" not in company.password
    assert (
        authenticate(customer_number="100001", password="hemmelig-passord") == company
    )
    assert authenticate(customer_number="100001", password="feil-passord") is None


def test_customer_number_is_required():
    """FR-1, AD-6: a company cannot be created without a customer number."""
    with pytest.raises(ValueError, match="Kundenummer mangler"):
        Company.objects.create_user("", "passord", name="Uten kundenummer")
