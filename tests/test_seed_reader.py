"""The seed reader of load_seed refuses a bad file before anything is loaded
(Story 1.7; FR-4, AD-8, AD-15, NFR-3).

The reader touches no database, so these tests need none. The committed files are
read as they are, and each refusal is built from a small valid file.
"""

import json
from copy import deepcopy

import pytest
import seed_files
from django.conf import settings

from web.models import Company
from web.seed import SeedError, read_seed


def refused(tmp_path, companies, match):
    seed_files.write_files(tmp_path, companies)
    with pytest.raises(SeedError, match=match) as error:
        read_seed(tmp_path)
    return str(error.value)


def test_the_committed_files_have_the_documented_companies_and_end_weeks():
    """FR-4, AD-8, AD-15: the committed files give two companies whose products
    all end at the company's latest week, 2026-W45 for A and 2026-W44 for B."""
    companies = read_seed(settings.SEED_DIR)

    assert [c.name for c in companies] == ["Testbedrift A", "Testbedrift B"]
    assert [len(c.products) for c in companies] == [30, 32]
    assert [{p.last_week for p in c.products} for c in companies] == [
        {(2026, 45)},
        {(2026, 44)},
    ]
    assert all(c.password_hash.startswith("pbkdf2_sha256$") for c in companies)


def test_weeks_count_from_the_first_week_across_a_year_end(tmp_path):
    """AD-8: a week is its ISO year and week number, with positions from 1 to N.
    2026 has 53 ISO weeks, so the week after 2026-W53 is 2027-W01, and a
    stockout position marks its week."""
    data = seed_files.company(
        products=[
            seed_files.product(first_week="2026-W52", units=(3, 4, 5), stockouts=(2,))
        ]
    )
    seed_files.write_files(tmp_path, [data])

    ((product,),) = [c.products for c in read_seed(tmp_path)]

    assert list(product.weeks()) == [
        (1, 2026, 52, 3, False),
        (2, 2026, 53, 4, True),
        (3, 2027, 1, 5, False),
    ]
    assert product.last_week == (2027, 1)


def test_files_are_read_in_name_order(tmp_path):
    """AD-15: the companies come in the order of the file names, so a load is the
    same every time."""
    seed_files.write_files(tmp_path, seed_files.two_companies())
    (tmp_path / "bedrift-1.json").rename(tmp_path / "z.json")

    assert [c.customer_number for c in read_seed(tmp_path)] == ["1002", "1001"]


def test_a_folder_without_seed_files_is_refused(tmp_path):
    """AD-15: an empty or missing folder is refused, not loaded as nothing."""
    with pytest.raises(SeedError, match="Fant ingen seed-filer"):
        read_seed(tmp_path)
    with pytest.raises(SeedError, match="Fant ingen seed-filer"):
        read_seed(tmp_path / "finnes-ikke")


def test_an_unreadable_file_is_refused_without_its_local_path(tmp_path):
    """NFR-4, AD-15: a file that cannot be read is named, and the message does not
    hold the local path that the operating system's error text carries."""
    (tmp_path / "mappe.json").mkdir()

    with pytest.raises(SeedError, match=r"mappe\.json: filen kan ikke leses") as error:
        read_seed(tmp_path)

    assert str(tmp_path) not in str(error.value)


def test_values_at_the_limits_of_the_columns_are_accepted(tmp_path):
    """FR-4, AD-8: the longest customer number, hash and names that the columns
    hold, and the largest whole number, pass the reader, because it reads its
    limits from the models; one more is refused (see the table of refusals)."""
    limit = Company._meta.get_field
    product = seed_files.product(
        name="p" * limit("name").max_length, units=(2**31 - 1,), stock=2**31 - 1
    )
    data = seed_files.company(
        customer_number="1" * limit("customer_number").max_length,
        name="b" * limit("name").max_length,
        password_hash="pbkdf2_sha256$" + "x" * (limit("password").max_length - 14),
        products=[product],
    )
    seed_files.write_files(tmp_path, [data])

    ((company),) = read_seed(tmp_path)

    assert len(company.password_hash) == limit("password").max_length
    assert company.products[0].units_sold == (2**31 - 1,)


def test_a_file_that_is_not_json_is_refused(tmp_path):
    """AD-8: a file that cannot be read gives a message with its name."""
    (tmp_path / "rotete.json").write_text("{ikke json", encoding="utf-8")

    with pytest.raises(SeedError, match=r"rotete\.json: filen kan ikke leses"):
        read_seed(tmp_path)


def change(path, value):
    """A function that sets path, a list of keys and indexes, to value."""

    def apply(data):
        target = data
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value

    return apply


def remove(path):
    def apply(data):
        target = data
        for key in path[:-1]:
            target = target[key]
        del target[path[-1]]

    return apply


PRODUCT = ["products", 0]

REFUSED = [
    ("wrong_version", change(["schema_version"], 2), "skjemaversjon 2 støttes ikke"),
    ("true_as_version", change(["schema_version"], True), "skjemaversjon True"),
    ("float_as_version", change(["schema_version"], 1.0), "skjemaversjon 1.0"),
    ("missing_key", remove(["name"]), "feltene er ikke de samme"),
    ("extra_key", change(["siste_uke"], "2026-W45"), "feltene er ikke de samme"),
    ("blank_customer_number", change(["customer_number"], " "), "customer_number må"),
    (
        "long_customer_number",
        change(["customer_number"], "1" * 21),
        "customer_number har mer enn 20 tegn",
    ),
    (
        "padded_customer_number",
        change(["customer_number"], " 1001"),
        "customer_number må være en tekst uten mellomrom først eller sist",
    ),
    (
        "hash_longer_than_the_column",
        change(["password_hash"], "pbkdf2_sha256$" + "x" * 115),
        "password_hash har mer enn 128 tegn",
    ),
    ("no_products", change(["products"], []), "products må være en liste"),
    (
        "short_product_number",
        change(PRODUCT + ["product_number"], "1234"),
        "varenummeret '1234' må være 5 sifre",
    ),
    (
        "letters_in_product_number",
        change(PRODUCT + ["product_number"], "1000a"),
        "må være 5 sifre",
    ),
    (
        "week_without_w",
        change(PRODUCT + ["first_week"], "2026-45"),
        "ikke en ISO-uke",
    ),
    (
        "week_54",
        change(PRODUCT + ["first_week"], "2026-W54"),
        "ikke en ISO-uke",
    ),
    (
        "week_53_of_a_year_with_52",
        change(PRODUCT + ["first_week"], "2025-W53"),
        "ikke en ISO-uke",
    ),
    (
        "negative_units",
        change(PRODUCT + ["units_sold", 1], -1),
        "uke 2 i units_sold er negativ",
    ),
    (
        "gap_as_null",
        change(PRODUCT + ["units_sold", 1], None),
        "uke 2 i units_sold mangler eller er ikke et helt tall",
    ),
    (
        "fractional_units",
        change(PRODUCT + ["units_sold", 0], 5.5),
        "uke 1 i units_sold mangler eller er ikke et helt tall",
    ),
    (
        "boolean_units",
        change(PRODUCT + ["units_sold", 0], True),
        "uke 1 i units_sold mangler eller er ikke et helt tall",
    ),
    ("no_weeks", change(PRODUCT + ["units_sold"], []), "units_sold må være en liste"),
    (
        "stockout_before_the_first_week",
        change(PRODUCT + ["stockout_positions"], [0]),
        "stockout_positions må være ulike posisjoner fra 1 til 3",
    ),
    (
        "stockout_after_the_last_week",
        change(PRODUCT + ["stockout_positions"], [4]),
        "stockout_positions må være ulike posisjoner fra 1 til 3",
    ),
    (
        "repeated_stockout",
        change(PRODUCT + ["stockout_positions"], [2, 2]),
        "stockout_positions må være ulike posisjoner",
    ),
    (
        "units_above_the_column",
        change(PRODUCT + ["units_sold", 2], 2**31),
        "uke 3 i units_sold er større enn 2147483647",
    ),
    (
        "stock_above_the_column",
        change(PRODUCT + ["stock_on_hand"], 2**31),
        "stock_on_hand må være et helt tall fra 0 til 2147483647",
    ),
    (
        "negative_stock",
        change(PRODUCT + ["stock_on_hand"], -1),
        "stock_on_hand må være et helt tall fra 0 til 2147483647",
    ),
    (
        "fractional_stock",
        change(PRODUCT + ["stock_on_hand"], 2.5),
        "stock_on_hand må være et helt tall",
    ),
    (
        "history_ends_a_week_early",
        change(PRODUCT + ["first_week"], "2026-W42"),
        r"slutter ikke i samme uke \(10001 slutter 2026-W44, 10002 slutter 2026-W45\)",
    ),
]


@pytest.mark.parametrize(
    ("mutate", "match"),
    [pytest.param(m, r, id=i) for i, m, r in REFUSED],
)
def test_a_file_that_breaks_the_schema_is_refused(tmp_path, mutate, match):
    """FR-4, AD-8, AD-15: a wrong schema version, a gap, a negative number, a bad
    week or a history that does not end at the company's latest week is refused
    with a Norwegian message that names the file. Company A's two products both
    end in 2026-W45, and each case changes its first one."""
    companies = seed_files.two_companies()[:1]
    mutate(companies[0])

    message = refused(tmp_path, companies, match)

    assert message.startswith("bedrift-1.json")


def test_a_plain_password_is_refused_and_never_repeated(tmp_path):
    """NFR-3, AD-15: a seed file with a plain password in password_hash is refused,
    and the message does not show the value."""
    data = seed_files.company(password_hash="testbedrift-a")

    message = refused(tmp_path, [data], "password_hash er ikke en hash")

    assert "testbedrift-a" not in message


def test_a_customer_number_in_two_files_is_refused(tmp_path):
    """FR-4, AD-15: two companies cannot share a customer number."""
    companies = [seed_files.company(), seed_files.company(name="Testbedrift B")]
    companies[1]["products"] = [seed_files.product("20001")]

    refused(
        tmp_path,
        companies,
        "Kundenummeret 1001 står både i bedrift-1.json og i bedrift-2.json",
    )


def test_a_product_number_in_two_companies_is_refused(tmp_path):
    """FR-3, AD-15: the two companies have disjoint product numbers."""
    companies = seed_files.two_companies()
    companies[1]["products"][0]["product_number"] = "10001"

    refused(
        tmp_path,
        companies,
        "Varenummeret 10001 står både i bedrift-1.json og i bedrift-2.json",
    )


def test_a_product_number_twice_in_a_company_is_refused(tmp_path):
    """FR-4, AD-15: a company has one product for each product number."""
    companies = seed_files.two_companies()[:1]
    companies[0]["products"][1]["product_number"] = "10001"

    refused(tmp_path, companies, "Varenummeret 10001 står to ganger i bedrift-1.json")


def test_the_message_names_the_product(tmp_path):
    """AD-8: a refused product is named with its number, so the fix is easy to find."""
    data = deepcopy(seed_files.two_companies()[0])
    data["products"][1]["units_sold"][2] = -3

    message = refused(tmp_path, [data], "uke 3 i units_sold er negativ")

    assert "produkt 10002" in message


def test_the_reader_does_not_change_the_files(tmp_path):
    """AD-15: reading never writes; the files are byte for byte the same."""
    paths = seed_files.write_files(tmp_path, seed_files.two_companies())
    before = [path.read_bytes() for path in paths]

    read_seed(tmp_path)

    assert [path.read_bytes() for path in paths] == before
    assert json.loads(before[0])["schema_version"] == 1
