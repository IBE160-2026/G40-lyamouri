"""accounts.Company, the custom user model (Story 1.1; AD-5, FR-1, NFR-3)."""

from importlib import import_module

from django.contrib.auth import authenticate, get_user_model
from django.db import migrations
from django.test import SimpleTestCase, TestCase

from accounts.models import Company


class CompanyTests(TestCase):
    def test_company_is_the_user_model_with_customer_number_as_login(self):
        self.assertIs(get_user_model(), Company)
        self.assertEqual(Company.USERNAME_FIELD, "customer_number")
        self.assertTrue(Company._meta.get_field("customer_number").unique)

    def test_password_is_hashed_with_pbkdf2(self):
        company = Company.objects.create_user(
            "100001", "hemmelig-passord", name="Testbedrift A"
        )
        company.refresh_from_db()
        self.assertTrue(company.password.startswith("pbkdf2_sha256$"))
        self.assertNotIn("hemmelig-passord", company.password)
        self.assertEqual(
            authenticate(customer_number="100001", password="hemmelig-passord"), company
        )
        self.assertIsNone(
            authenticate(customer_number="100001", password="feil-passord")
        )

    def test_customer_number_is_required(self):
        with self.assertRaises(ValueError):
            Company.objects.create_user("", "passord", name="Uten kundenummer")


class FirstMigrationTests(SimpleTestCase):
    """AD-5: the custom user model is in the very first migration."""

    def test_first_migration_creates_company_with_customer_number_login(self):
        migration = import_module("accounts.migrations.0001_initial").Migration
        self.assertTrue(migration.initial)
        create_company = next(
            operation
            for operation in migration.operations
            if isinstance(operation, migrations.CreateModel)
            and operation.name == "Company"
        )
        fields = dict(create_company.fields)
        self.assertTrue(fields["customer_number"].unique)
        self.assertIn("password", fields)
