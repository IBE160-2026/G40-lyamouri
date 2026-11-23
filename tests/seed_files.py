"""Small valid seed files for the tests of the seed reader and load_seed.

They have schema version 1 (data/README.md) and are written to a temporary
folder, so the tests do not depend on the committed seed files. The hash is only
shaped like Django's PBKDF2 hash, so the tests need no slow hashing.
"""

import json

PASSWORD_HASH = (
    "pbkdf2_sha256$1000000$testsaltAAAAAAAAAAAAAAAA$aGFzaGVuYWRkcmVzc2VkYWxsdGVzdA="
)


def product(
    number="10001",
    name="Testprodukt",
    first_week="2026-W43",
    units=(5, 6, 7),
    stockouts=(),
    stock=4,
):
    """A product that ends in week 45 of 2026 by default."""
    return {
        "product_number": number,
        "name": name,
        "first_week": first_week,
        "units_sold": list(units),
        "stockout_positions": list(stockouts),
        "stock_on_hand": stock,
    }


def company(customer_number="1001", name="Testbedrift A", products=None, **changes):
    data = {
        "schema_version": 1,
        "customer_number": customer_number,
        "name": name,
        "password_hash": PASSWORD_HASH,
        "products": [product()] if products is None else products,
    }
    data.update(changes)
    return data


def two_companies():
    """Company A with two products ending in 2026-W45, B with one ending in W44."""
    return [
        company(
            products=[
                product("10001", "Malertape", stockouts=(2,)),
                product("10002", "Skruer", first_week="2026-W42", units=(1, 2, 3, 4)),
            ]
        ),
        company(
            "1002",
            "Testbedrift B",
            products=[product("20001", "Plantejord", first_week="2026-W42")],
        ),
    ]


def write_files(directory, companies):
    """Write one file per company, named by its position, and return the paths."""
    paths = []
    for index, data in enumerate(companies, start=1):
        path = directory / f"bedrift-{index}.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        paths.append(path)
    return paths
