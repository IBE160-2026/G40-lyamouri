"""Every Must reference example and every rule test product runs through the core (Story 2.6).

SM-1, NFR-2, FR-3, DR-3, AD-17, PRD §10 question 4. The cases and the products are read
from the reference spreadsheet, and the rule test products are run from the committed seed
files with the FR-20 defaults, as the loader will, so no expected value is copied into the
tests. They use no database. The tests of Stories 2.1 to 2.5 check the same values for one
rule at a time; this sweep checks that nothing a Must case states is left out.
"""

import json
import re
from pathlib import Path

import answer_key_reader as reader
import generate_seed
import pytest

from forecasting import display
from forecasting import forecast as core
from forecasting.overview import build_overview
from forecasting.settings import ForecastSettings
from forecasting.weeks import Week

SEED_DIR = Path(__file__).resolve().parents[1] / "data" / "seed"
# SM-1: the Must examples E1 to E13, E15 to E21, E23, E24, E28 and E29 (E11, E18 and E29
# have the parts a, b, and so on in the spreadsheet).
MUST_EXAMPLES = {*range(1, 14), *range(15, 22), 23, 24, 28, 29}
MUST_CASES = [row for row in reader.cases() if row["priority"] == "Must"]
# What a case can state and the core does not give: the Should-have seasonal pattern and
# adjustment (FR-9, FR-36, Epic 5), and the order quantities of the optimistic and
# pessimistic scenarios, which only E22 (Should, FR-13) states. The overstock note (FR-34,
# Should) is checked as absent, which is what E23 states.
NOT_IN_THE_CORE = {
    "week_number_means",
    "mean_of_means",
    "seasonal_indices",
    "adjusted_sales_used",
    "seasonal_adjustment_used",
    "seasonal_pattern",
    "optimistic_order_unrounded",
    "optimistic_order_quantity",
    "pessimistic_order_unrounded",
    "pessimistic_order_quantity",
}
# What the sweep leaves to its own test: the position is a place among the cases of an example.
IN_OTHER_TESTS = {"overview_position"}


def example_number(example):
    return int(re.match(r"E(\d+)", example)[1])


def core_weeks(sales):
    return [Week(week.units_sold, week.stockout) for week in sales]


def settings_of(row):
    return ForecastSettings(
        method=row["method"],
        window=row["window"],
        smoothing_factor=row["smoothing_factor"],
        unusual_weeks_included=row["unusual_weeks_setting"] == "included",
        scenario_percentage=row["scenario_percentage"],
        safety_margin=row["safety_margin"],
    )


def same_number(found, expected):
    if expected is None or found is None:
        return found is expected
    return abs(found - expected) < reader.TOLERANCE


def same_numbers(found, expected):
    if found is None or expected is None:
        return found is expected
    return len(found) == len(expected) and all(
        same_number(a, b) for a, b in zip(found, expected, strict=True)
    )


def week_1(result):
    return result.scenarios[0] if result.scenarios else None


def checks(result):
    """The result's value for every column the core gives, as a test of the stated value."""
    forecast = result.week_forecasts
    scenario = week_1(result)
    return {
        # The spreadsheet states the number of valid and calculation weeks.
        "valid_weeks": lambda e: len(result.valid_weeks) == e,
        "unusual_weeks": lambda e: list(result.unusual_weeks) == e,
        "level_shift_weeks": lambda e: list(result.level_shift_weeks) == e,
        "calculation_weeks": lambda e: len(result.calculation_weeks) == e,
        "levels": lambda e: same_numbers(result.levels, e),
        "base_forecast": lambda e: same_number(result.base_forecast, e),
        "base_forecast_shown": lambda e: display.one_decimal(result.base_forecast) == e,
        "week_forecasts": lambda e: same_numbers(forecast, e),
        "normal": lambda e: same_number(scenario and scenario.normal, e),
        "optimistic": lambda e: same_number(scenario and scenario.optimistic, e),
        "pessimistic": lambda e: same_number(scenario and scenario.pessimistic, e),
        "order_unrounded": lambda e: same_number(result.order_unrounded, e),
        "order_unrounded_shown": lambda e: (
            display.two_decimals(result.order_unrounded) == e
        ),
        "suggested_order_quantity": lambda e: result.suggested_order_quantity == e,
        "weeks_of_cover": lambda e: same_number(result.weeks_of_cover, e),
        "weeks_of_cover_shown": lambda e: (
            (
                "–"
                if result.weeks_of_cover is None
                else display.one_decimal(result.weeks_of_cover)
            )
            == e
        ),
        "order_soon": lambda e: result.order_soon is e,
        # FR-34 is Should: until it is built, no product has an overstock note.
        "overstock_note": lambda e: (
            e is False and not any("overstock" in note for note in result.notes)
        ),
        "weeks_since_latest_valid": lambda e: result.weeks_since_latest_valid == e,
        "warnings": lambda e: list(result.warnings) == e,
        "confidence_label": lambda e: result.confidence_label == e,
    }


def swept(row):
    """The columns a case states that the sweep compares, as (column, expected)."""
    stated = {c: row[c] for c in reader.CASE_EXPECTED if c in row}
    return {
        column: expected
        for column, expected in stated.items()
        if column not in NOT_IN_THE_CORE | IN_OTHER_TESTS
        # The levels belong to exponential smoothing; the moving average has none.
        and not (column == "levels" and row["method"] != "exponential_smoothing")
        # A forecast that is None has no shown text to compare.
        and not (
            column in ("base_forecast_shown", "order_unrounded_shown")
            and row.get(column) is None
        )
    }


@pytest.mark.parametrize("row", MUST_CASES, ids=lambda row: row["case"])
def test_every_value_a_must_case_states_is_the_one_the_core_finds(row):
    """SM-1, NFR-2, DR-3: for each Must case of the spreadsheet, the core gives every
    value that the case states and that the core calculates."""
    result = core.forecast_product(
        core_weeks(row["sales"]), row["stock_on_hand"], settings_of(row)
    )
    found = checks(result)
    compared = swept(row)

    assert compared, f"{row['case']} states nothing that the core gives"
    for column, expected in compared.items():
        assert found[column](expected), (row["case"], column, expected)


def test_every_column_a_case_states_is_compared_or_named_as_left_out():
    """SM-1: no column of a Must case is left out without a name in NOT_IN_THE_CORE or
    IN_OTHER_TESTS."""
    stated = {c for row in MUST_CASES for c in reader.CASE_EXPECTED if c in row}
    found = checks(core.forecast_product([Week(1, False)] * 3, 0, ForecastSettings()))

    assert stated <= set(found) | NOT_IN_THE_CORE | IN_OTHER_TESTS


def test_the_sweep_has_every_must_example_of_sm_1():
    """SM-1: E1 to E13, E15 to E21, E23, E24, E28 and E29 are all in the spreadsheet as
    Must cases, and no other E-n example is Must."""
    numbers = {
        example_number(row["example"])
        for row in MUST_CASES
        if row["example"].startswith("E")
    }

    assert numbers == MUST_EXAMPLES


def test_the_overview_positions_of_the_spreadsheet_are_the_overview_order():
    """R-12, E24: a case that states an overview position has that place when the cases of
    its example are built into an overview."""
    rows = [row for row in MUST_CASES if "overview_position" in row]
    results = {
        row["product_number"]: core.forecast_product(
            core_weeks(row["sales"]), row["stock_on_hand"], settings_of(row)
        )
        for row in rows
    }

    overview = build_overview(dict(reversed(results.items())), {})

    assert rows
    assert len(results) == len(rows)
    for row in rows:
        place = overview.order.index(row["product_number"]) + 1
        assert place == row["overview_position"], row["case"]


def seed_product(file_name, number):
    company = json.loads((SEED_DIR / file_name).read_text(encoding="utf-8"))
    return next(p for p in company["products"] if p["product_number"] == number)


RULE_TEST_PRODUCTS = [
    (key, company["file"], number)
    for company in generate_seed.COMPANIES
    for key, (number, _name) in company["from_workbook"].items()
]


@pytest.mark.parametrize(
    ("key", "file_name", "number"), RULE_TEST_PRODUCTS, ids=lambda v: str(v)
)
def test_a_rule_test_product_of_the_seed_data_gets_the_results_of_the_spreadsheet(
    key, file_name, number
):
    """FR-3, DR-3, SM-1, PRD §10 question 4: the base forecast, the suggested order
    quantity, the unusual weeks, the level-shift weeks, the warnings and the confidence label
    of each rule test product in the seed data, with the FR-20 defaults, equal the
    spreadsheet's."""
    expected = next(row for row in reader.products() if row["product"] == key)
    product = seed_product(file_name, number)
    out = set(product["stockout_positions"])
    weeks = [
        Week(units, position in out)
        for position, units in enumerate(product["units_sold"], start=1)
    ]

    result = core.forecast_product(weeks, product["stock_on_hand"], ForecastSettings())
    found = checks(result)

    for column in reader.PRODUCT_EXPECTED:
        assert found[column](expected[column]), (key, column, expected[column])


def test_every_rule_test_product_of_the_spreadsheet_is_in_the_seed_data():
    """FR-3, DR-3: the 11 products of the spreadsheet are all swept, none is left out."""
    assert {key for key, _, _ in RULE_TEST_PRODUCTS} == {
        row["product"] for row in reader.products()
    }
    assert len(RULE_TEST_PRODUCTS) == len(reader.products()) == 11
