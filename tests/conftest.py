"""Fixtures shared by the tests that log in (Story 1.8; AD-6, AD-7).

The two companies hold the real hashes of the seed files, so a login checks the
real passwords with Django's default hasher, and their products overlap in
product number but not in name or stock, as two real companies' could.
"""

import json
from io import StringIO
from pathlib import Path
from typing import NamedTuple

import pytest
from django.core.management import call_command

from web.models import Company, Product, SalesWeek

SEED_DIR = Path(__file__).resolve().parents[1] / "data" / "seed"


class Account(NamedTuple):
    company: Company
    password: str
    products: tuple


def seed_hash(file_name):
    return json.loads((SEED_DIR / file_name).read_text(encoding="utf-8"))[
        "password_hash"
    ]


def create_account(
    customer_number, name, file_name, password, products, last_week, weeks=3
):
    """Create a company with the seed file's hash, products and sales weeks that end at last_week."""
    company = Company.objects.create(
        customer_number=customer_number, name=name, password=seed_hash(file_name)
    )
    year, last = last_week
    for number, product_name, stock in products:
        product = Product.objects.create(
            company=company,
            product_number=number,
            name=product_name,
            stock_on_hand=stock,
        )
        SalesWeek.objects.bulk_create(
            SalesWeek(
                product=product,
                position=position,
                iso_year=year,
                iso_week=last - weeks + position,
                units_sold=5,
                stockout=False,
            )
            for position in range(1, weeks + 1)
        )
    return Account(company, password, tuple(products))


@pytest.fixture
def two_companies(db):
    """Test company A, ending in week 45 of 2026, and B, ending in week 44 (FR-2, SM-4).

    Both have a product 10001, with another name and stock.
    """
    a = create_account(
        "1001",
        "Testbedrift A",
        "testbedrift-a.json",
        "testbedrift-a",
        [
            ("10001", "Hammer fra A", 7371),
            ("10002", "Sag fra A", 7372),
            ("10003", "Tang fra A", 7373),
        ],
        (2026, 45),
    )
    b = create_account(
        "1002",
        "Testbedrift B",
        "testbedrift-b.json",
        "testbedrift-b",
        [
            ("10001", "Spade fra B", 8481),
            ("20001", "Rive fra B", 8482),
        ],
        (2026, 44),
    )
    return a, b


@pytest.fixture
def seeded(settings, tmp_path, db):
    """The committed seed files in the database, as load_seed puts them there."""
    settings.SECRET_KEY_FILE = tmp_path / ".secret_key"
    call_command("load_seed", stdout=StringIO())
