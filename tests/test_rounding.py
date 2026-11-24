"""Rounding (Story 2.3; R-8, R-9, AD-3, E5, E20, E21).

The expected order quantities and display values are read from the reference
spreadsheet for every case that states them, so no expected value is copied into the
tests (AD-17). They use no database.
"""

import math
from decimal import Decimal

import answer_key_reader as reader
import pytest

from forecasting import display, rounding
from forecasting.forecast import forecast_product
from forecasting.settings import ForecastSettings
from forecasting.weeks import Week

# The examples whose rounding the spreadsheet states, as it names them (PRD §5.7).
ORDER_EXAMPLES = {"E4", "E5", "E6", "E21", "E23", "E24 (A)", "E24 (B)", "FR-21 d"}
SHOWN_EXAMPLES = {"E1", "E2", "E13 (E4)", "E13 (E6)", "E20", "E21", "E27"}
# The columns that state a value as it is shown, and the number that each one shows.
SHOWN_COLUMNS = {
    "base_forecast_shown": ("base_forecast", display.one_decimal),
    "weeks_of_cover_shown": ("weeks_of_cover", display.one_decimal),
    "order_unrounded_shown": ("order_unrounded", display.two_decimals),
}
# Case E23 shows «–» for a missing value, which comes with Story 2.4.
DASH = "–"

ORDER_CASES = [
    row
    for row in reader.cases()
    if "suggested_order_quantity" in row and row["seasonal_adjustment"] == "off"
]
SHOWN_CASES = [
    (row, column)
    for row in reader.cases()
    for column in SHOWN_COLUMNS
    if column in row and row[column] != DASH
]


def unrounded_order(row):
    """The week-1 forecast × (1 + safety margin) − stock on hand, in plain floats, as
    a computer calculates it (Story 2.4 builds the real one), so that E5 gives
    70.00000000000001."""
    settings = ForecastSettings(
        method=row["method"],
        window=row["window"],
        smoothing_factor=row["smoothing_factor"],
        unusual_weeks_included=row["unusual_weeks_setting"] == "included",
    )
    weeks = [Week(week.units_sold, week.stockout) for week in row["sales"]]
    base = forecast_product(weeks, row["stock_on_hand"], settings).base_forecast
    return base * (1 + row["safety_margin"] / 100) - row["stock_on_hand"]


def test_the_spreadsheet_examples_for_rounding_are_all_checked():
    """R-9, E4 to E6, E21, E23, E24, FR-21: the cases that state an order quantity and the cases that
    state a shown value are exactly the ones listed here, so a case that is dropped
    from the spreadsheet or left out of the tests does not go unnoticed."""
    assert {row["case"] for row in ORDER_CASES} == ORDER_EXAMPLES
    assert {row["case"] for row, _ in SHOWN_CASES} == SHOWN_EXAMPLES


@pytest.mark.parametrize("row", ORDER_CASES, ids=lambda row: row["case"])
def test_the_order_quantity_is_rounded_up_once_as_the_spreadsheet_states(row):
    """R-8, R-9, E4 to E6, E21: the larger of 0 and the unrounded order, rounded to 6
    decimals and then up, is the suggested order quantity of the spreadsheet."""
    unrounded = unrounded_order(row)
    if "order_unrounded" in row:
        # The stand-in calculation gives the value the spreadsheet states.
        assert abs(unrounded - row["order_unrounded"]) < reader.TOLERANCE

    assert (
        rounding.round_up_to_units(max(0, unrounded)) == row["suggested_order_quantity"]
    )


def test_e5_gives_70_and_not_71():
    """R-9, E5: 100 × 1.1 − 40 is 70.00000000000001 in floats, which rounds to 70 and
    not up to 71, and plain `math.ceil` shows why the 6 decimals come first."""
    row = next(row for row in ORDER_CASES if row["case"] == "E5")
    unrounded = unrounded_order(row)

    assert unrounded > 70
    assert math.ceil(unrounded) == 71
    assert (
        rounding.round_up_to_units(unrounded) == row["suggested_order_quantity"] == 70
    )


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, 0),
        (0.0, 0),
        (-0.4, 0),
        (0.000001, 1),
        (0.0000004, 0),
        (0.067, 1),
        (69.999999, 70),
        (70.0000004, 70),
        (70.000001, 71),
        (70.5, 71),
        (Decimal("70.0000001"), 70),
        (12, 12),
    ],
)
def test_round_up_to_units_rounds_to_6_decimals_and_then_up(value, expected):
    """R-8, R-9: 6 decimals first, then up; a remainder of a millionth still counts."""
    result = rounding.round_up_to_units(value)

    assert result == expected
    assert type(result) is int


@pytest.mark.parametrize(
    ("value", "decimals", "expected"),
    [
        (10.25, 1, "10.3"),
        (0.285, 2, "0.29"),
        (1.45, 1, "1.5"),
        (2.5, 0, "3"),
        (-0.25, 1, "-0.3"),
        (-2.5, 0, "-3"),
        (10.249999999999998, 1, "10.3"),
        (14.333333333333334, 1, "14.3"),
        (-40, 2, "-40.00"),
        (0, 1, "0.0"),
        (5, 0, "5"),
        (Decimal("0.067"), 2, "0.07"),
        (0.0000004, 6, "0.000000"),
        (Decimal("0.1234565"), 6, "0.123457"),
    ],
)
def test_round_for_display_goes_half_away_from_zero(value, decimals, expected):
    """R-9, E20: half away from zero, after the 6 decimals; `round()` would give 10.2
    for 10.25 and 0.28 for 0.285."""
    result = rounding.round_for_display(value, decimals)

    assert str(result) == expected
    assert isinstance(result, Decimal)


def test_a_value_that_rounds_to_zero_is_a_plain_zero():
    """R-9, NFR-5: −0.04 at one decimal is 0.0, never −0.0."""
    result = rounding.round_for_display(-0.04, 1)

    assert str(result) == "0.0"
    assert not result.is_signed()


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_a_value_that_is_not_a_number_is_refused(value):
    """R-9: NaN and infinity have no rounding, and fail instead of printing."""
    with pytest.raises(ValueError, match="cannot round"):
        rounding.round_up_to_units(value)
    with pytest.raises(ValueError, match="cannot round"):
        rounding.round_for_display(value, 1)


@pytest.mark.parametrize("value", [None, "", "abc", "70", "70,5", True, [1]])
def test_a_value_that_is_not_a_number_type_is_a_type_error(value):
    """R-9, AD-3: `None`, a string or a bool is no number, and fails with a
    `TypeError` instead of being rounded (a string "70" would print unrounded)."""
    with pytest.raises(TypeError, match="cannot round"):
        rounding.round_up_to_units(value)
    with pytest.raises(TypeError, match="cannot round"):
        rounding.round_for_display(value, 1)


@pytest.mark.parametrize("value", [1e22, -1e30, 10**40, Decimal("1E+30")])
def test_a_value_too_large_to_round_is_refused_like_nan(value):
    """R-9: a finite value that `decimal` cannot round to 6 decimals in its 28 digits
    is a `ValueError` like NaN, not an `InvalidOperation`."""
    with pytest.raises(ValueError, match="cannot round"):
        rounding.round_up_to_units(value)
    with pytest.raises(ValueError, match="cannot round"):
        rounding.round_for_display(value, 1)


@pytest.mark.parametrize("decimals", [-1, 7])
def test_display_decimals_outside_0_to_6_are_refused(decimals):
    """R-9: the 6 decimals come first, so a display with more is not defined."""
    with pytest.raises(ValueError, match="0 to 6"):
        rounding.round_for_display(1.5, decimals)


@pytest.mark.parametrize(
    ("row", "column"),
    SHOWN_CASES,
    ids=lambda item: item if isinstance(item, str) else item["case"],
)
def test_every_shown_value_of_the_spreadsheet_is_the_rounded_one(row, column):
    """R-9, NFR-5, E1, E2, E13, E20, E21, E27: the number that a case states is
    shown as the text that it states, with a decimal comma."""
    number_column, show = SHOWN_COLUMNS[column]

    assert show(row[number_column]) == row[column]


@pytest.mark.parametrize(
    "row",
    [row for row in reader.cases() if "base_forecast_shown" in row],
    ids=lambda row: row["case"],
)
def test_the_calculated_base_forecast_is_shown_as_the_spreadsheet_states(row):
    """R-9, E1, E2, E20: the full-precision forecast of the core, not the three
    decimals of the spreadsheet, shows as 14,3, 13,8 and 10,3."""
    weeks = [Week(week.units_sold, week.stockout) for week in row["sales"]]
    settings = ForecastSettings(
        method=row["method"],
        window=row["window"],
        smoothing_factor=row["smoothing_factor"],
        unusual_weeks_included=row["unusual_weeks_setting"] == "included",
    )
    result = forecast_product(weeks, row["stock_on_hand"], settings)

    assert display.one_decimal(result.base_forecast) == row["base_forecast_shown"]


def test_e21_is_shown_with_two_decimals_and_ordered_as_one_unit():
    """R-8, R-9, E21: 27.333 × 1.1 − 30 shows as 0,07 and rounds up to 1."""
    row = next(row for row in ORDER_CASES if row["case"] == "E21")
    unrounded = unrounded_order(row)

    assert display.two_decimals(unrounded) == row["order_unrounded_shown"]
    assert rounding.round_up_to_units(unrounded) == row["suggested_order_quantity"]
