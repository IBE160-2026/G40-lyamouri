"""Reads and checks the seed files that load_seed loads (AD-8, AD-15, NFR-3).

The files have schema version 1, written by data/generate_seed.py and described
in data/README.md. Nothing here touches the database, so a refused file stops
load_seed before anything is deleted or written. Each message names the file
and, where it applies, the product.
"""

import json
import re
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from django.contrib.auth.hashers import identify_hasher

from web.models import Company, Product

SCHEMA_VERSION = 1
COMPANY_KEYS = {
    "schema_version",
    "customer_number",
    "name",
    "password_hash",
    "products",
}
PRODUCT_KEYS = {
    "product_number",
    "name",
    "first_week",
    "units_sold",
    "stockout_positions",
    "stock_on_hand",
}
# The longest values the columns keep, read from the models so that a file the
# reader accepts cannot fail in the database after a reset has begun.
CUSTOMER_NUMBER_LENGTH = Company._meta.get_field("customer_number").max_length
COMPANY_NAME_LENGTH = Company._meta.get_field("name").max_length
PASSWORD_HASH_LENGTH = Company._meta.get_field("password").max_length
PRODUCT_NAME_LENGTH = Product._meta.get_field("name").max_length
# The largest value of a PositiveIntegerField column.
INTEGER_MAX = 2_147_483_647


class SeedError(Exception):
    """A seed file that load_seed refuses; the message is in Norwegian."""


@dataclass(frozen=True)
class SeedProduct:
    product_number: str
    name: str
    stock_on_hand: int
    first_monday: date
    units_sold: tuple[int, ...]
    stockout_positions: frozenset[int]

    def weeks(self):
        """Yield (position, iso_year, iso_week, units_sold, stockout), oldest first."""
        for index, units in enumerate(self.units_sold):
            year, week, _ = (self.first_monday + timedelta(weeks=index)).isocalendar()
            yield index + 1, year, week, units, (index + 1) in self.stockout_positions

    @property
    def last_week(self):
        """The ISO year and week of the last registered week (AD-8)."""
        monday = self.first_monday + timedelta(weeks=len(self.units_sold) - 1)
        return monday.isocalendar()[:2]


@dataclass(frozen=True)
class SeedCompany:
    file_name: str
    customer_number: str
    name: str
    password_hash: str
    products: tuple[SeedProduct, ...]


def read_seed(directory):
    """Read every *.json file in directory, in name order, or raise SeedError."""
    directory = Path(directory)
    paths = sorted(directory.glob("*.json")) if directory.is_dir() else []
    if not paths:
        raise SeedError(f"Fant ingen seed-filer (*.json) i {directory.name}/.")
    companies = [_company(path) for path in paths]
    _check_unique(
        ((c.customer_number, c.file_name) for c in companies), "Kundenummeret"
    )
    _check_unique(
        ((p.product_number, c.file_name) for c in companies for p in c.products),
        "Varenummeret",
    )
    return companies


def _check_unique(entries, label):
    """Refuse a value that appears twice, naming the files, from (value, file) pairs."""
    seen = {}
    for value, file_name in entries:
        if value in seen:
            first = seen[value]
            places = (
                f"to ganger i {file_name}"
                if first == file_name
                else f"både i {first} og i {file_name}"
            )
            raise SeedError(
                f"{label} {value} står {places}. Hver verdi kan brukes én gang."
            )
        seen[value] = file_name


def _company(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError:
        # Not the error text: it holds the whole local path.
        raise SeedError(f"{path.name}: filen kan ikke leses.") from None
    except ValueError as error:
        raise SeedError(
            f"{path.name}: filen kan ikke leses som JSON ({error})."
        ) from None
    where = path.name
    _keys(data, COMPANY_KEYS, where)
    # type() is int: neither True nor 1.0 counts as version 1.
    if (
        type(data["schema_version"]) is not int
        or data["schema_version"] != SCHEMA_VERSION
    ):
        raise SeedError(
            f"{where}: skjemaversjon {data['schema_version']!r} støttes ikke. "
            f"Bare versjon {SCHEMA_VERSION} kan lastes."
        )
    customer_number = _text(
        data["customer_number"], "customer_number", where, CUSTOMER_NUMBER_LENGTH
    )
    name = _text(data["name"], "name", where, COMPANY_NAME_LENGTH)
    password_hash = _text(
        data["password_hash"], "password_hash", where, PASSWORD_HASH_LENGTH
    )
    try:
        identify_hasher(password_hash)
    except ValueError:
        # Never echo the value: it could be a plain password.
        raise SeedError(
            f"{where}: password_hash er ikke en hash fra Djangos hasher. "
            "Passord skal aldri ligge i seed-filene."
        ) from None
    if not isinstance(data["products"], list) or not data["products"]:
        raise SeedError(f"{where}: products må være en liste med minst ett produkt.")
    products = tuple(_product(item, where) for item in data["products"])
    first_with_end = {}
    for product in products:
        first_with_end.setdefault(product.last_week, product.product_number)
    if len(first_with_end) > 1:
        ends = ", ".join(
            f"{number} slutter {year}-W{week:02d}"
            for (year, week), number in sorted(first_with_end.items())
        )
        raise SeedError(
            f"{where}: produktene slutter ikke i samme uke ({ends}). "
            "Alle produkter i en bedrift må slutte i bedriftens siste datauke."
        )
    return SeedCompany(path.name, customer_number, name, password_hash, products)


def _product(data, file_name):
    _keys(data, PRODUCT_KEYS, file_name)
    number = data["product_number"]
    if not isinstance(number, str) or not re.fullmatch(r"[0-9]{5}", number):
        raise SeedError(f"{file_name}: varenummeret {number!r} må være 5 sifre.")
    where = f"{file_name}, produkt {number}"
    name = _text(data["name"], "name", where, PRODUCT_NAME_LENGTH)
    stock = data["stock_on_hand"]
    if not _whole(stock) or not 0 <= stock <= INTEGER_MAX:
        raise SeedError(
            f"{where}: stock_on_hand må være et helt tall fra 0 til {INTEGER_MAX}."
        )
    units = data["units_sold"]
    if not isinstance(units, list) or not units:
        raise SeedError(f"{where}: units_sold må være en liste med minst én uke.")
    for position, value in enumerate(units, start=1):
        if not _whole(value):
            raise SeedError(
                f"{where}: uke {position} i units_sold mangler eller er ikke et helt tall."
            )
        if value < 0:
            raise SeedError(f"{where}: uke {position} i units_sold er negativ.")
        if value > INTEGER_MAX:
            raise SeedError(
                f"{where}: uke {position} i units_sold er større enn {INTEGER_MAX}."
            )
    positions = data["stockout_positions"]
    if (
        not isinstance(positions, list)
        or not all(_whole(p) and 1 <= p <= len(units) for p in positions)
        or len(set(positions)) != len(positions)
    ):
        raise SeedError(
            f"{where}: stockout_positions må være ulike posisjoner fra 1 til {len(units)}."
        )
    return SeedProduct(
        product_number=number,
        name=name,
        stock_on_hand=stock,
        first_monday=_monday(data["first_week"], where),
        units_sold=tuple(units),
        stockout_positions=frozenset(positions),
    )


def _monday(value, where):
    match = (
        re.fullmatch(r"([0-9]{4})-W([0-9]{2})", value)
        if isinstance(value, str)
        else None
    )
    try:
        if match:
            return date.fromisocalendar(int(match[1]), int(match[2]), 1)
    except ValueError:
        pass
    raise SeedError(f"{where}: first_week {value!r} er ikke en ISO-uke som «2026-W45».")


def _keys(data, expected, where):
    if not isinstance(data, dict) or set(data) != expected:
        raise SeedError(
            f"{where}: feltene er ikke de samme som i skjemaet ({', '.join(sorted(expected))})."
        )


def _text(value, field, where, limit):
    """A text that is not empty, has no space first or last and fits its column."""
    if not isinstance(value, str) or value != value.strip() or not value:
        raise SeedError(
            f"{where}: {field} må være en tekst uten mellomrom først eller sist, og ikke tom."
        )
    if len(value) > limit:
        raise SeedError(f"{where}: {field} har mer enn {limit} tegn.")
    return value


def _whole(value):
    """A whole number; True and False are not."""
    return isinstance(value, int) and not isinstance(value, bool)
