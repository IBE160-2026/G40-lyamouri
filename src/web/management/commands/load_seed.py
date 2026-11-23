"""uv run python src/manage.py load_seed [--reset] (AD-13, AD-15, DR-4, NFR-3).

It creates the local session secret when it is missing, reads and checks the seed
files, and loads them into an empty database. With --reset and a typed
confirmation it first deletes every company with its data and every session,
in the same transaction.
"""

import os
import secrets
from pathlib import Path

from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from prognose.env import read_secret_key
from web.models import Company, CompanySettings, Product, SalesWeek
from web.seed import SeedError, read_seed

CONFIRMATION = "nullstill"


class Command(BaseCommand):
    help = (
        "Lager den hemmelige nøkkelen for øktene i .secret_key hvis fila mangler, "
        "og laster testbedriftene inn i en tom database. Med --reset slettes først "
        "alle data, og du må skrive en bekreftelse."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help=(
                "Slett alle bedrifter med produkter, salgsuker og innstillinger og alle "
                "økter, og last testdataene på nytt. Du må skrive en bekreftelse."
            ),
        )

    def handle(self, *args, **options):
        self.ensure_secret_key()
        try:
            companies = read_seed(settings.SEED_DIR)
        except SeedError as error:
            raise CommandError(f"{error} Ingen data er lastet eller slettet.") from None

        if options["reset"]:
            self.confirm_reset()
            with transaction.atomic():
                Company.objects.all().delete()
                Session.objects.all().delete()
                summary = self.load(companies)
        else:
            if Company.objects.exists():
                raise CommandError(
                    "Databasen har allerede data, og ingen data er endret. "
                    "Kjør load_seed --reset for å slette alle data, også innstillinger "
                    "og justerte mengder, og laste testdataene på nytt."
                )
            with transaction.atomic():
                summary = self.load(companies)
        # After the commit, so a failed commit never follows a success line.
        self.stdout.write(self.style.SUCCESS(summary))

    def ensure_secret_key(self):
        path = Path(settings.SECRET_KEY_FILE)
        try:
            # O_EXCL: create the file only if it does not exist, so an existing
            # key is never rewritten. On macOS and Linux only the owner may read
            # or write it; on Windows the mode sets only the read-only flag, and
            # the folder's access rules apply.
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            if not read_secret_key(path):
                raise CommandError(
                    f"{path.name} er tom. Slett fila og kjør load_seed på nytt."
                ) from None
            self.stdout.write(f"{path.name} finnes allerede og er ikke endret.")
            return
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            file.write(secrets.token_urlsafe(50))
        self.stdout.write(
            self.style.SUCCESS(f"Lagde {path.name} med en ny hemmelig nøkkel.")
        )

    def confirm_reset(self):
        """Stop unless the user types the confirmation; nothing is deleted before."""
        try:
            answer = input(
                "Dette sletter alle bedrifter med produkter, salgsuker og innstillinger "
                "og alle økter, så justerte mengder også nullstilles, og laster "
                "testdataene på nytt.\n"
                f"Skriv «{CONFIRMATION}» for å fortsette: "
            )
        except EOFError:
            answer = ""
        if answer.strip() != CONFIRMATION:
            raise CommandError(
                "Bekreftelsen mangler. Ingen data er slettet eller endret."
            )

    def load(self, companies):
        """Create the companies, their settings, products and sales weeks (AD-15).

        Return the summary line, which the caller prints after the commit.
        """
        counts = {"products": 0, "sales_weeks": 0}
        for seed in companies:
            # The hash goes in as it is: set_password would hash it again, and a
            # hash made with another salt would make Django rewrite it at login.
            company = Company.objects.create(
                customer_number=seed.customer_number,
                name=seed.name,
                password=seed.password_hash,
            )
            CompanySettings.objects.create(company=company)
            products = Product.objects.bulk_create(
                Product(
                    company=company,
                    product_number=product.product_number,
                    name=product.name,
                    stock_on_hand=product.stock_on_hand,
                )
                for product in seed.products
            )
            sales_weeks = [
                SalesWeek(
                    product=row,
                    position=position,
                    iso_year=year,
                    iso_week=week,
                    units_sold=units,
                    stockout=stockout,
                )
                for row, product in zip(products, seed.products, strict=True)
                for position, year, week, units, stockout in product.weeks()
            ]
            SalesWeek.objects.bulk_create(sales_weeks, batch_size=2000)
            counts["products"] += len(products)
            counts["sales_weeks"] += len(sales_weeks)
        return (
            f"Lastet {len(companies)} bedrifter med {counts['products']} produkter "
            f"og {counts['sales_weeks']} salgsuker."
        )
