"""The seed generator and its two test companies (Story 1.6; FR-3, AD-8, AD-15).

No test uses the database. The files in data/seed/ are compared with a fresh
run of data/generate_seed.py, the rule test products with the reference
spreadsheet, and the patterns with the table in data/README.md. A test that
verifies no FR names its NFR, DR or AD (D-10).
"""

import copy
import json
import math
import re
import shutil
import subprocess
import sys
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
from pathlib import Path
from statistics import mean, median

import answer_key
import answer_key_reader as reader
import generate_seed
import openpyxl
import pytest
from django.contrib.auth.hashers import check_password, identify_hasher

REPO_ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = REPO_ROOT / "data/seed"
DATA_README = REPO_ROOT / "data/README.md"
ROOT_README = REPO_ROOT / "README.md"
FILES = ("testbedrift-a.json", "testbedrift-b.json")
RECENT = 12
# UX-DR46: where the rules win over the mockup, the mockup's week-1 forecast of
# Skruer, 21,5, cannot occur with whole units, and the seed gives 21,3.
MOCKUP_FORECAST_DEVIATIONS = {"10004": ("21,5", "21,3")}


def committed(name):
    return json.loads((SEED_DIR / name).read_text(encoding="utf-8"))


def all_products():
    return [p for name in FILES for p in committed(name)["products"]]


def valid_units(product):
    out = set(product["stockout_positions"])
    return [u for i, u in enumerate(product["units_sold"], 1) if i not in out]


def first_monday(product):
    year, week = generate_seed.parse_week(product["first_week"])
    return generate_seed.monday_of(year, week)


def spike_baseline(product, position):
    """The median of the 3 weeks before a position that are not stockout weeks,
    or None where fewer than 3 exist."""
    out = set(product["stockout_positions"])
    before = [product["units_sold"][i - 1] for i in range(1, position) if i not in out][
        -3:
    ]
    return median(before) if len(before) == 3 else None


def baseline_spike(product, position):
    """Whether a week sells more than 2 × its baseline: the shape of an unusual
    week."""
    baseline = spike_baseline(product, position)
    return baseline is not None and product["units_sold"][position - 1] > 2 * baseline


def run(tmp_path, *arguments):
    generate_seed.main(["--output-dir", str(tmp_path), *arguments])
    return {name: (tmp_path / name).read_bytes() for name in FILES}


def test_two_runs_write_identical_files(tmp_path):
    """FR-3, AD-15: the generator run twice writes the same bytes, with LF line
    endings and a final newline."""
    first = run(tmp_path / "first")
    second = run(tmp_path / "second")

    assert first == second
    for content in first.values():
        assert b"\r" not in content
        assert content.endswith(b"}\n")


def test_the_script_runs_as_the_readme_says(tmp_path):
    """FR-3, AD-15: `python data/generate_seed.py` in its own process writes the
    committed files, wherever it is started from."""
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "data/generate_seed.py"), "--output-dir", "."],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 0, result.stderr
    for name in FILES:
        assert (tmp_path / name).read_bytes() == (SEED_DIR / name).read_bytes()


def test_the_committed_files_equal_a_fresh_run(tmp_path):
    """AD-15: the files in data/seed/ are what the generator writes now."""
    fresh = run(tmp_path)

    for name in FILES:
        assert (SEED_DIR / name).read_bytes() == fresh[name], (
            f"{name} differs from a fresh run; run "
            "`uv run python data/generate_seed.py` and commit the files"
        )


def test_the_rule_test_products_come_from_the_workbook():
    """FR-3, AD-15: each product of the workbook is in the company the workbook
    names, with its series and stock on hand, and no other product has them
    without being in the workbook."""
    rows = {row["product"]: row for row in reader.products()}
    placed = {}
    for company in generate_seed.COMPANIES:
        data = committed(company["file"])
        by_number = {p["product_number"]: p for p in data["products"]}
        for key, (number, name) in company["from_workbook"].items():
            placed[key] = company["company"]
            product = by_number[number]
            weeks = rows[key]["sales"]
            assert product["name"] == name
            assert product["units_sold"] == [w.units_sold for w in weeks], key
            assert product["stockout_positions"] == [
                i for i, w in enumerate(weeks, 1) if w.stockout
            ], key
            assert product["stock_on_hand"] == rows[key]["stock_on_hand"], key

    assert placed == {key: row["company"] for key, row in rows.items()}


def test_a_changed_workbook_changes_a_rule_test_product(tmp_path):
    """AD-15: the series and stock of a rule test product are read from the
    workbook, not from the generator's own code."""
    changed = tmp_path / "workbook.xlsx"
    workbook = openpyxl.load_workbook(reader.WORKBOOK)
    sheet = workbook["products"]
    header = [cell.value for cell in sheet[1]]
    for row in sheet.iter_rows(min_row=2):
        if row[header.index("product")].value == "E1":
            row[header.index("stock_on_hand")].value = 6
            row[header.index("sales")].value = "12, 15, 13, 16, 12, 15, 14, 99"
    workbook.save(changed)

    companies = {c["file"]: c["data"] for c in generate_seed.build_companies(changed)}

    product = next(
        p
        for p in companies["testbedrift-b.json"]["products"]
        if p["product_number"] == "20001"
    )
    assert product["stock_on_hand"] == 6
    assert product["units_sold"][-1] == 99
    assert companies["testbedrift-b.json"] != committed("testbedrift-b.json")


def test_a_missing_rule_test_product_stops_the_generator(tmp_path):
    """AD-15: without the workbook's row for E1, nothing is written, and the
    message names the product."""
    without = tmp_path / "workbook.xlsx"
    workbook = openpyxl.load_workbook(reader.WORKBOOK)
    sheet = workbook["products"]
    for row in sheet.iter_rows(min_row=2):
        if row[0].value == "E1":
            for cell in row:
                cell.value = None
    workbook.save(without)
    out = tmp_path / "out"

    with pytest.raises(SystemExit) as stopped:
        generate_seed.main(["--workbook", str(without), "--output-dir", str(out)])

    assert "E1" in str(stopped.value)
    assert not out.exists()


def broken(change):
    companies = copy.deepcopy(generate_seed.build_companies())
    change(companies)
    return companies


def test_broken_seed_data_is_refused_before_writing():
    """AD-8, AD-15: a history that ends early, a number that is not 5 digits,
    a number used in both companies, a negative stock, a bad series, a repeated
    name or customer number, a different latest week and a company with too few
    products stop the generator."""

    def ends_early(companies):
        companies[0]["data"]["products"][0]["units_sold"].pop()

    def short_number(companies):
        companies[0]["data"]["products"][0]["product_number"] = "1234"

    def shared_number(companies):
        number = companies[0]["data"]["products"][0]["product_number"]
        companies[1]["data"]["products"][0]["product_number"] = number

    def negative_stock(companies):
        companies[0]["data"]["products"][0]["stock_on_hand"] = -1

    def unsorted_stockouts(companies):
        companies[0]["data"]["products"][0]["stockout_positions"] = [3, 2]

    def stockout_out_of_range(companies):
        companies[0]["data"]["products"][0]["stockout_positions"] = [999]

    def negative_sales(companies):
        companies[0]["data"]["products"][0]["units_sold"][0] = -1

    def empty_series(companies):
        companies[0]["data"]["products"][0]["units_sold"] = []

    def repeated_name(companies):
        products = companies[0]["data"]["products"]
        products[1]["name"] = products[0]["name"]

    def shared_customer(companies):
        companies[1]["data"]["customer_number"] = companies[0]["data"][
            "customer_number"
        ]

    def wrong_latest_week(companies):
        companies[0]["latest_week"] = "2026-W44"

    def few_products(companies):
        companies[0]["data"]["products"] = companies[0]["data"]["products"][:9]

    for change, message in (
        (ends_early, "end at"),
        (short_number, "5 digits"),
        (shared_number, "used twice"),
        (few_products, "not 10–50"),
        (negative_stock, "negative stock"),
        (unsorted_stockouts, "a bad series"),
        (stockout_out_of_range, "out of range"),
        (negative_sales, "negative sales"),
        (empty_series, "no weeks"),
        (repeated_name, "empty or used twice"),
        (shared_customer, "customer number .* used twice"),
        (wrong_latest_week, "not at 2026-W44"),
    ):
        with pytest.raises(ValueError, match=message):
            generate_seed.validate(broken(change))


def test_edits_that_miss_the_history_are_refused():
    """AD-15: a tail longer than the history, or a patch beyond its first week,
    raises instead of landing on the wrong week."""
    monday = generate_seed.monday_of(2026, 45)
    too_long = generate_seed.made("10099", "x", 0, generate_seed.flat(5), 2, "1, 2, 3")
    too_far = generate_seed.made(
        "10099", "x", 0, generate_seed.flat(5), 3, patches={5: "S"}
    )

    with pytest.raises(ValueError, match="longer than the history"):
        generate_seed.series_of(too_long, monday, reader.parse_sales)
    with pytest.raises(ValueError, match="no week 5 from the end"):
        generate_seed.series_of(too_far, monday, reader.parse_sales)


@pytest.mark.parametrize(
    ("renamed", "message"),
    [("E99", "placed in no company"), ("E1", "listed twice")],
)
def test_a_workbook_product_that_no_company_places_is_refused(
    tmp_path, renamed, message
):
    """AD-15: a row added to the workbook's products that the generator does not
    place, or a product listed twice, stops the generator instead of being
    dropped or overwritten."""
    changed = tmp_path / "workbook.xlsx"
    workbook = openpyxl.load_workbook(reader.WORKBOOK)
    sheet = workbook["products"]
    header = [cell.value for cell in sheet[1]]
    source = next(
        [cell.value for cell in row]
        for row in sheet.iter_rows(min_row=2)
        if row[header.index("product")].value == "E1"
    )
    source[header.index("product")] = renamed
    sheet.append(source)
    workbook.save(changed)

    with pytest.raises(ValueError, match=message):
        generate_seed.build_companies(changed)


def test_the_seed_files_have_the_documented_schema():
    """AD-15: schema version 1 with exactly the documented fields, which
    data/README.md lists."""
    for name in FILES:
        data = committed(name)
        assert list(data) == [
            "schema_version",
            "customer_number",
            "name",
            "password_hash",
            "products",
        ]
        assert data["schema_version"] == 1
        for product in data["products"]:
            assert list(product) == [
                "product_number",
                "name",
                "first_week",
                "units_sold",
                "stockout_positions",
                "stock_on_hand",
            ]


def readme_logins():
    """The customer numbers and passwords that the root README gives."""
    text = ROOT_README.read_text(encoding="utf-8")
    return {
        company: (number, password)
        for company, number, password in re.findall(
            r"\| Testbedrift ([AB]) \| (\d+) \| `([^`]+)` \|", text
        )
    }


def test_git_keeps_the_seed_files_with_lf_endings():
    """AD-15: a Windows checkout with core.autocrlf would otherwise turn the
    committed files into CRLF, and they would differ from a fresh run. Git
    itself reports the attribute for each file."""
    if shutil.which("git") is None or not (REPO_ROOT / ".git").exists():
        pytest.skip("needs git and a clone")
    for name in FILES:
        result = subprocess.run(
            ["git", "check-attr", "eol", "--", f"data/seed/{name}"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

        assert result.stdout.strip().endswith("eol: lf"), result.stdout


def test_the_files_hold_hashes_that_accept_the_readme_passwords():
    """FR-1, NFR-3: each file holds a PBKDF2 hash that Django accepts for the
    README's password and refuses for another, and no login rewrites it."""
    logins = readme_logins()
    assert set(logins) == {"A", "B"}
    for name, company in zip(FILES, "AB", strict=True):
        data = committed(name)
        number, password = logins[company]
        hashed = data["password_hash"]

        assert data["customer_number"] == number
        assert hashed.startswith("pbkdf2_sha256$")
        assert check_password(password, hashed)
        assert not check_password(password + "x", hashed)
        assert not identify_hasher(hashed).must_update(hashed)


def test_no_plain_text_password_in_the_seed_files():
    """NFR-3: a seed file holds neither of the README's passwords."""
    passwords = [password for _, password in readme_logins().values()]
    assert passwords
    for name in FILES:
        text = (SEED_DIR / name).read_text(encoding="utf-8")
        for password in passwords:
            assert password not in text, name


def test_no_local_path_or_personal_data_in_the_seed_files():
    """NFR-4: no home folder, drive path, e-mail address or telephone number."""
    pattern = re.compile(
        r"/Users/|/home/|[A-Za-z]:\\|[\w.+-]+@[\w-]+\.[\w.]+|\+47|\b\d{8}\b"
    )
    for name in FILES:
        text = (SEED_DIR / name).read_text(encoding="utf-8")
        # The hash is base64, so a digit run or «+47» in it is chance.
        text = text.replace(committed(name)["password_hash"], "")
        assert pattern.search(text) is None, name


def test_the_companies_have_the_documented_size_and_numbers():
    """FR-3, UX-DR46: 10 to 50 products each, about 30 in Testbedrift A, disjoint
    5-digit numbers, most products with 104 weeks, and product names without
    duplicates."""
    numbers = []
    for name in FILES:
        products = committed(name)["products"]
        numbers.append({p["product_number"] for p in products})
        assert 10 <= len(products) <= 50
        assert len(numbers[-1]) == len(products)
        assert len({p["name"] for p in products}) == len(products)
        assert all(re.fullmatch(r"\d{5}", n) for n in numbers[-1])
        assert sum(len(p["units_sold"]) == 104 for p in products) > len(products) / 2
    assert len(committed(FILES[0])["products"]) == 30
    assert numbers[0].isdisjoint(numbers[1])


def test_each_history_ends_at_the_latest_data_week():
    """AD-8, UX-DR46: a run of ISO weeks without a gap per product, ending at one
    week per company: week 45 of 2026 in Testbedrift A and week 44 in B."""
    latest = {FILES[0]: "2026-W45", FILES[1]: "2026-W44"}
    for name in FILES:
        ends = set()
        for product in committed(name)["products"]:
            assert re.fullmatch(r"\d{4}-W\d{2}", product["first_week"])
            count = len(product["units_sold"])
            ends.add(generate_seed.end_week(product))
            assert all(isinstance(u, int) and u >= 0 for u in product["units_sold"])
            assert product["stockout_positions"] == sorted(
                set(product["stockout_positions"])
            )
            assert all(1 <= p <= count for p in product["stockout_positions"])
            assert isinstance(product["stock_on_hand"], int)
        assert ends == {latest[name]}


def test_the_histories_cover_the_ranges_of_valid_weeks():
    """FR-3: in each company at least one product has fewer than 3 valid weeks,
    one 3 to 11 and one 12 to 103."""
    for name in FILES:
        counts = [len(valid_units(p)) for p in committed(name)["products"]]
        assert any(c < 3 for c in counts), name
        assert any(3 <= c <= 11 for c in counts), name
        assert any(12 <= c <= 103 for c in counts), name


def pattern_table():
    text = (
        DATA_README.read_text(encoding="utf-8")
        .split("## Mønstrene")[1]
        .split("\n## ")[0]
    )
    table = {}
    for line in text.splitlines():
        match = re.fullmatch(r"\| ([^|]+) \| ([\d, ]+) \|", line)
        if match:
            table[match[1]] = [n.strip() for n in match[2].split(",")]
    return table


def is_trend(product):
    units = product["units_sold"]
    return mean(units[-52:]) >= 1.5 * mean(units[:52])


def is_seasonal_without_trend(product):
    units = product["units_sold"]
    start = first_monday(product)
    by_week = {}
    for i, u in enumerate(units):
        week = (start + timedelta(weeks=i)).isocalendar().week
        by_week.setdefault(week, []).append(u)
    means = [mean(v) for v in by_week.values()]
    indices = [m / mean(means) for m in means]
    flat = abs(mean(units[-52:]) - mean(units[:52])) <= 0.1 * mean(units)
    return max(indices) >= 1.3 and min(indices) <= 0.7 and flat


def recent_positions(product):
    count = len(product["units_sold"])
    return range(max(1, count - RECENT + 1), count + 1)


def has_level_shift(product):
    """Whether three weeks in a row in the recent period each sell more than
    2 × the baseline before the first of them: the shape of a new level."""
    count = len(product["units_sold"])
    for first in recent_positions(product):
        baseline = spike_baseline(product, first)
        if baseline is not None and first + 2 <= count:
            weeks = product["units_sold"][first - 1 : first + 2]
            if all(u > 2 * baseline for u in weeks):
                return True
    return False


PATTERNS = {
    "Kjent trend": is_trend,
    "Sesongmønster uten trend": is_seasonal_without_trend,
    "Utsolgte uker": lambda p: (
        any(s in recent_positions(p) for s in p["stockout_positions"])
        and bool(p["stockout_positions"])
    ),
    "Uvanlige uker": lambda p: any(baseline_spike(p, i) for i in recent_positions(p)),
    "Nytt nivå": has_level_shift,
    "Lang rekke utsolgte uker på slutten": lambda p: (
        set(range(len(p["units_sold"]) - 8, len(p["units_sold"]) + 1))
        <= set(p["stockout_positions"])
    ),
    "Lager som dekker neste uke": lambda p: (
        len(valid_units(p)) >= 3
        and p["stock_on_hand"] >= Decimal("1.1") * Decimal(sum(valid_units(p)[-3:])) / 3
    ),
    "Historikk for «høy»": lambda p: (
        len(p["units_sold"]) == 104
        and len(valid_units(p)) >= 100
        and not set(p["stockout_positions"]) & set(recent_positions(p))
        and not any(baseline_spike(p, i) for i in range(4, 105))
    ),
    "Færre enn 3 gyldige uker": lambda p: len(valid_units(p)) < 3,
    "3 til 11 gyldige uker": lambda p: 3 <= len(valid_units(p)) <= 11,
    "12 til 103 gyldige uker": lambda p: 12 <= len(valid_units(p)) <= 103,
}


def test_every_pattern_has_a_product_that_shows_it():
    """FR-3, SM-7: data/README.md names a product for each pattern, and each
    named product has the shape of the pattern."""
    table = pattern_table()
    products = {p["product_number"]: p for p in all_products()}

    assert set(table) == set(PATTERNS)
    for pattern, numbers in table.items():
        for number in numbers:
            assert PATTERNS[pattern](products[number]), f"{number}: {pattern}"


def test_the_demo_products_of_testbedrift_a_follow_the_mockup():
    """UX-DR46: each product that the mockup's overview shows has its number,
    stock on hand and week-1 forecast, from the last three valid weeks; the
    forecast of Skruer is the one deviation, where the rules win."""
    products = {p["product_number"]: p for p in committed(FILES[0])["products"]}
    mockup = answer_key.mockup_products()

    assert len(mockup) == 8
    for name, shown in mockup.items():
        product = products[shown["number"]]
        assert product["name"] == name
        assert product["stock_on_hand"] == shown["stock"], name
        units = valid_units(product)
        if shown["forecast"] is None:
            assert len(units) < 3, name
            continue
        forecast = (Decimal(sum(units[-3:])) / 3).quantize(
            Decimal("0.1"), rounding=ROUND_HALF_UP
        )
        text = str(forecast).replace(".", ",")
        expected = shown["forecast"]
        if shown["number"] in MOCKUP_FORECAST_DEVIATIONS:
            mockup_text, ours = MOCKUP_FORECAST_DEVIATIONS[shown["number"]]
            assert expected == mockup_text
            expected = ours
        assert text == expected, name


def week_1_forecast(product):
    """The moving average of the last three valid weeks (R-3 with the FR-20
    default window), or None for fewer than 3 valid weeks (R-6)."""
    units = valid_units(product)
    return Fraction(sum(units[-3:]), 3) if len(units) >= 3 else None


def suggested_quantity(product):
    """R-8 with the FR-20 default safety margin, read from the PRD. A stand-in
    for the core, which story 2.8 uses to check the same figures."""
    margin = answer_key.prd_defaults()["safety_margin"]
    need = week_1_forecast(product) * Fraction(100 + margin, 100)
    return max(0, math.ceil(need - product["stock_on_hand"]))


def warning_shapes(product):
    """The R-15 warnings by their shapes in the data: a stockout, an unusual
    week or a new level in the last 12 weeks, old data, no forecast."""
    count = len(product["units_sold"])
    valid_positions = set(range(1, count + 1)) - set(product["stockout_positions"])
    return {
        "stockout_weeks": bool(
            set(product["stockout_positions"]) & set(recent_positions(product))
        ),
        "unusual_weeks": any(
            baseline_spike(product, i) for i in recent_positions(product)
        ),
        "level_shift": has_level_shift(product),
        "old_data": count - max(valid_positions, default=0) > 8,
        "insufficient_data": week_1_forecast(product) is None,
    }


def test_denne_uken_for_testbedrift_a_matches_the_mockup_and_the_ux_flow():
    """UX-DR46: the products to order soon, their suggested quantities and the
    total, the product without a forecast and the four products with warnings
    follow the mockup and Flow 1, and the other products need no order and
    show no warning."""
    products = {p["product_number"]: p for p in committed(FILES[0])["products"]}
    mockup = answer_key.mockup_products()
    overview = answer_key.mockup_overview()
    e8 = generate_seed.COMPANIES[0]["from_workbook"]["E8"][0]
    with_warning = {
        mockup["Strøsand 25 kg"]["number"],
        mockup["Skruer 4×40 mm, 200 stk."]["number"],
        mockup["Snøskuffe aluminium"]["number"],
        e8,
    }

    assert len(products) == overview["products"]
    quantities = {
        number: suggested_quantity(p)
        for number, p in products.items()
        if week_1_forecast(p) is not None
    }
    to_order = {number: q for number, q in quantities.items() if q > 0}
    assert len(to_order) == overview["order_soon"]
    assert sum(to_order.values()) == overview["units"]
    for shown in mockup.values():
        if shown["quantity"] != "–":
            assert quantities[shown["number"]] == int(shown["quantity"]), shown
    assert [n for n in products if week_1_forecast(products[n]) is None] == [
        mockup["Snøskuffe aluminium"]["number"]
    ]
    assert overview["without_forecast"] == 1
    warned = {n for n, p in products.items() if any(warning_shapes(p).values())}
    assert warned == with_warning
    shown_numbers = {shown["number"] for shown in mockup.values()}
    for number in set(products) - shown_numbers - {e8}:
        assert not products[number]["stockout_positions"], number
        assert not any(baseline_spike(products[number], i) for i in range(4, 105)), (
            number
        )


def test_the_seed_dates_are_iso_weeks_that_exist():
    """AD-8: every first week is a real ISO week, so the calendar arithmetic
    that labels the weeks gives a week that round-trips."""
    for product in all_products():
        year, week = generate_seed.parse_week(product["first_week"])
        monday = date.fromisocalendar(year, week, 1)
        assert generate_seed.week_label(monday) == product["first_week"]
