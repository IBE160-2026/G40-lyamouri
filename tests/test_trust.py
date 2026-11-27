"""The active warnings, the notes and the confidence label (Story 2.5).

FR-7, FR-8, FR-15 to FR-19, R-15, R-16. The expected warnings, labels and weeks since the
latest valid week are read from the reference spreadsheet for every case and rule test
product that states them, so no expected value is copied into the tests (AD-17). They use
no database.
"""

import dataclasses

import answer_key_reader as reader
import pytest

from forecasting import forecast as core
from forecasting import trust
from forecasting.settings import ForecastSettings
from forecasting.weeks import Week

# The cases that state warnings, a label or the weeks since the latest valid week, without
# the Should-have seasonal pattern (FR-36, E30), as the spreadsheet names them (PRD §5.7).
LISTED_EXAMPLES = {
    "E11 a",
    "E11 b",
    "E12 (95)",
    "E12 (96)",
    "E28",
    "E29 a",
    "E29 b",
    "E29 c",
    "E29 d",
    "E29 e",
    "E29 f",
    "E29 g",
}
STATED = ("warnings", "confidence_label", "weeks_since_latest_valid")
CASES = [
    row
    for row in reader.cases()
    if any(column in row for column in STATED)
    and row["seasonal_adjustment"] == "off"
    and "seasonal_pattern" not in row.get("warnings", [])
]


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


def row_of(name):
    return next(row for row in reader.cases() if row["case"] == name)


def history(*units):
    return [Week(unit, False) for unit in units]


def series(length, units=10, stockouts=(), spikes=None):
    """A history of `length` weeks with `units` each, the positions in `stockouts` sold out,
    and the units of the positions in `spikes` set."""
    spikes = spikes or {}
    return [
        Week(spikes.get(position, units), position in stockouts)
        for position in range(1, length + 1)
    ]


def forecast(weeks, settings=None, stock_on_hand=0):
    return core.forecast_product(weeks, stock_on_hand, settings or ForecastSettings())


@pytest.mark.parametrize("row", CASES, ids=lambda row: row["case"])
def test_every_stated_warning_and_label_is_the_one_the_core_finds(row):
    """FR-8, FR-15 to FR-19, R-15, R-16 (E11, E12, E28, E29): the active warnings in R-15
    order, the label and the weeks since the latest valid week equal the spreadsheet's."""
    result = core.forecast_product(
        core_weeks(row["sales"]), row["stock_on_hand"], settings_of(row)
    )

    if "warnings" in row:
        assert list(result.warnings) == row["warnings"], row["case"]
    if "confidence_label" in row:
        assert result.confidence_label == row["confidence_label"], row["case"]
    if "weeks_since_latest_valid" in row:
        assert result.weeks_since_latest_valid == row["weeks_since_latest_valid"]


def test_the_spreadsheet_examples_for_warnings_and_labels_are_all_checked():
    """SM-1: no case that states a warning or a label is left out of the check."""
    assert {row["case"] for row in CASES} == LISTED_EXAMPLES


@pytest.mark.parametrize(
    "product", reader.products(), ids=lambda product: product["product"]
)
def test_the_rule_test_products_get_the_warnings_and_labels_of_the_spreadsheet(product):
    """SM-7, FR-3, FR-8, FR-15 to FR-19: each rule test product with the FR-20 defaults gets
    the warnings and the confidence label that the spreadsheet states for it."""
    result = core.forecast_product(
        core_weeks(product["sales"]), product["stock_on_hand"], ForecastSettings()
    )

    assert list(result.warnings) == product["warnings"]
    assert result.confidence_label == product["confidence_label"]


def test_the_warnings_use_the_names_and_the_order_of_the_spreadsheet():
    """R-15: five warnings in the order of the rule; the seasonal one is Should."""
    assert trust.WARNINGS == reader.WARNINGS[:5]
    assert trust.WARNINGS[-1] == "insufficient_data"
    assert (trust.LAV, trust.MIDDELS, trust.HOY) == reader.LABELS


def test_old_data_is_more_than_8_weeks_since_the_latest_valid_week():
    """FR-18, R-15 (E12): 9 weeks gives the old-data warning and 8 weeks does not, counted
    by position from the latest data week, and the stockout warning is active in both."""
    nine, eight = row_of("E12 (95)"), row_of("E12 (96)")
    results = [
        core.forecast_product(core_weeks(row["sales"]), 0, settings_of(row))
        for row in (nine, eight)
    ]

    assert [r.weeks_since_latest_valid for r in results] == [9, 8]
    assert trust.OLD_DATA in results[0].warnings
    assert trust.OLD_DATA not in results[1].warnings
    assert all(trust.STOCKOUT_WEEKS in r.warnings for r in results)
    assert trust.OLD_DATA_WEEKS == 8


def test_a_stockout_week_before_the_recent_period_is_not_a_warning():
    """FR-15, R-15: week 92 of 104 is the 13th from the end, so it is no warning, and week
    93, the 12th from the end, is one."""
    before = forecast(series(104, stockouts={92}))
    inside = forecast(series(104, stockouts={93}))

    assert before.warnings == ()
    assert before.recent_stockout_weeks == ()
    assert inside.warnings == (trust.STOCKOUT_WEEKS,)
    assert inside.recent_stockout_weeks == (93,)
    assert trust.RECENT_WEEKS == 12


def test_an_unusual_week_before_the_recent_period_is_not_a_warning():
    """FR-16, R-15: an unusual week 13th from the end is listed by the calculation but is no
    active warning; the 12th from the end is one."""
    before = forecast(series(104, spikes={92: 30}))
    inside = forecast(series(104, spikes={93: 30}))

    assert before.unusual_weeks == (92,)
    assert before.warnings == () and before.recent_unusual_weeks == ()
    assert inside.warnings == (trust.UNUSUAL_WEEKS,)
    assert inside.recent_unusual_weeks == (93,)
    assert inside.recent_unusual_units == (30,)


@pytest.mark.parametrize("included", [True, False])
def test_the_unusual_weeks_setting_neither_adds_nor_removes_the_warning(included):
    """FR-16, R-15 (E8): the same unusual-weeks warning with the setting on and off."""
    row = row_of("E8 (included)")
    settings = dataclasses.replace(settings_of(row), unusual_weeks_included=included)
    result = core.forecast_product(core_weeks(row["sales"]), 0, settings)

    assert result.warnings == (trust.UNUSUAL_WEEKS,)
    assert list(result.recent_unusual_weeks) == row["unusual_weeks"]
    assert result.recent_unusual_units == tuple(
        row["sales"][position - 1].units_sold for position in row["unusual_weeks"]
    )
    assert result.confidence_label == trust.LAV


def test_a_level_shift_in_the_recent_period_is_an_active_warning():
    """FR-17, R-15 (E9): three level-shift weeks are a warning, and a 104-week history with
    nothing else is «middels» because of it."""
    e9 = row_of("E9 (included)")
    short = core.forecast_product(core_weeks(e9["sales"]), 0, settings_of(e9))
    long = forecast(series(104, spikes={102: 50, 103: 52, 104: 51}))

    assert short.warnings == (trust.LEVEL_SHIFT,)
    assert short.recent_level_shift_weeks == (4, 5, 6)
    assert long.level_shift_weeks == (102, 103, 104)
    assert long.warnings == (trust.LEVEL_SHIFT,)
    assert (long.confidence_label, long.confidence_condition) == (
        trust.MIDDELS,
        trust.ACTIVE_WARNING,
    )


def test_a_level_shift_before_the_recent_period_is_not_a_warning():
    """FR-17, R-15: level-shift weeks 13 to 15 from the end are not recent, so there is no
    warning; the shift is still found by the classification."""
    result = forecast(series(104, spikes={90: 50, 91: 52, 92: 51}))

    assert result.level_shift_weeks == (90, 91, 92)
    assert result.warnings == () and result.recent_level_shift_weeks == ()


def test_the_recent_period_of_a_short_history_is_the_whole_history():
    """R-15: a history shorter than 12 weeks has all its weeks in the recent period."""
    result = forecast(series(5, stockouts={2}))

    assert result.recent_stockout_weeks == (2,)
    assert result.warnings == (trust.STOCKOUT_WEEKS,)
    assert list(trust.recent_positions(0)) == []
    assert list(trust.recent_positions(5)) == [1, 2, 3, 4, 5]
    assert list(trust.recent_positions(12)) == list(range(1, 13))
    assert list(trust.recent_positions(13)) == list(range(2, 14))
    assert result.history_length == 5


def test_no_forecast_is_the_insufficient_data_warning_for_both_reasons():
    """FR-8, R-15 (E11 a and b): fewer than 3 valid weeks and fewer calculation weeks than
    the window both give insufficient data, and the product is «lav»."""
    few = forecast(history(5, 6))
    window = forecast(history(10, 11, 12, 13), ForecastSettings(window=12))

    assert few.no_forecast_reason == core.TOO_FEW_VALID_WEEKS
    assert window.no_forecast_reason == core.TOO_FEW_CALCULATION_WEEKS
    for result in (few, window):
        assert result.warnings == (trust.INSUFFICIENT_DATA,)
        assert result.confidence_label == trust.LAV
    assert few.confidence_condition == core.TOO_FEW_VALID_WEEKS
    assert window.confidence_condition == core.TOO_FEW_CALCULATION_WEEKS


def test_an_empty_history_has_no_old_data_warning():
    """FR-8, FR-18: a product with no weeks, or only stockout weeks, has no latest valid
    week, so only insufficient data is active, and the label is «lav»."""
    empty = forecast([])
    sold_out = forecast(series(20, stockouts=set(range(1, 21))))

    assert empty.warnings == (trust.INSUFFICIENT_DATA,)
    assert empty.weeks_since_latest_valid is None
    assert empty.confidence_label == trust.LAV
    assert sold_out.weeks_since_latest_valid is None
    assert sold_out.warnings == (trust.STOCKOUT_WEEKS, trust.INSUFFICIENT_DATA)


def test_a_product_without_a_forecast_can_also_have_old_data():
    """FR-8, FR-18: 2 valid weeks and then 20 stockout weeks have no forecast, and the old
    latest valid week is an active warning too, in R-15 order."""
    weeks = series(22, stockouts=set(range(3, 23)))
    result = forecast(weeks)

    assert result.warnings == (
        trust.STOCKOUT_WEEKS,
        trust.OLD_DATA,
        trust.INSUFFICIENT_DATA,
    )
    assert result.weeks_since_latest_valid == 20


@pytest.mark.parametrize(
    ("length", "stockouts", "label", "condition"),
    [
        (11, set(), trust.LAV, trust.FEWER_THAN_12_VALID_WEEKS),
        (12, set(), trust.MIDDELS, trust.SHORT_HISTORY),
        (103, set(), trust.MIDDELS, trust.SHORT_HISTORY),
        (104, set(), trust.HOY, trust.ALL_CLEAR),
        (104, {1, 2, 3, 4}, trust.HOY, trust.ALL_CLEAR),
        (104, {1, 2, 3, 4, 5}, trust.MIDDELS, trust.FEWER_THAN_100_VALID_WEEKS),
        (105, {1, 2, 3, 4, 5}, trust.HOY, trust.ALL_CLEAR),
    ],
)
def test_the_label_thresholds_are_12_valid_weeks_104_weeks_and_100_valid_weeks(
    length, stockouts, label, condition
):
    """R-16 (E29 b, c, f, g): 11 valid weeks is «lav» and 12 is «middels»; 103 weeks is
    «middels» and 104 is «høy»; 100 valid weeks is «høy» and 99 is «middels», and the
    sales history counts the stockout weeks (105 weeks with 100 valid weeks)."""
    result = forecast(series(length, stockouts=stockouts))

    assert (result.confidence_label, result.confidence_condition) == (label, condition)
    assert (trust.LOW_VALID_WEEKS, trust.HIGH_HISTORY_WEEKS) == (12, 104)
    assert trust.HIGH_VALID_WEEKS == 100


def test_the_first_condition_that_applies_decides_the_label():
    """R-16: no forecast beats an active warning, an active warning beats a short history,
    and a short history beats fewer than 100 valid weeks."""
    window = forecast(
        series(12, spikes={4: 30, 8: 30}),
        ForecastSettings(window=12, unusual_weeks_included=False),
    )
    warned_short = forecast(series(80, stockouts={79}))
    short_and_few = forecast(series(90, stockouts={1, 2, 3, 4, 5, 6}))

    assert (window.confidence_label, window.confidence_condition) == (
        trust.LAV,
        core.TOO_FEW_CALCULATION_WEEKS,
    )
    assert trust.UNUSUAL_WEEKS in window.warnings
    assert (warned_short.confidence_label, warned_short.confidence_condition) == (
        trust.MIDDELS,
        trust.ACTIVE_WARNING,
    )
    assert (short_and_few.confidence_label, short_and_few.confidence_condition) == (
        trust.MIDDELS,
        trust.SHORT_HISTORY,
    )


def test_a_product_with_a_forecast_has_the_note_of_fr_7_and_one_without_has_none():
    """FR-7: weeks 2 and 3 repeat week 1 without seasonal adjustment, so every forecast has
    the note; no forecast, no note."""
    with_forecast = forecast(history(10, 11, 12))
    without = forecast(history(10, 11))

    assert with_forecast.notes == (trust.WEEKS_REPEAT_WEEK_1,)
    assert without.notes == ()


def test_the_warnings_do_not_change_the_forecast_or_the_order():
    """R-15, FR-15 (E7): the warnings only report; a product with stockout weeks gets the
    forecast that the spreadsheet states for E7 and the order of the same history without
    those weeks."""
    e7 = row_of("E7")
    result = core.forecast_product(core_weeks(e7["sales"]), 0, settings_of(e7))
    without = forecast(
        [week for week in core_weeks(e7["sales"]) if not week.stockout],
        settings_of(e7),
    )

    assert result.warnings == (trust.STOCKOUT_WEEKS,)
    assert abs(result.base_forecast - e7["base_forecast"]) < reader.TOLERANCE
    assert result.base_forecast == without.base_forecast
    assert result.suggested_order_quantity == without.suggested_order_quantity


def test_excluded_unusual_weeks_still_count_as_valid_weeks_for_the_label():
    """R-16, FR-16 (E11 b): 12 valid weeks of which 2 are excluded leave 10 calculation
    weeks, but the product is not «lav» for it: R-16 counts valid weeks. A window of 3 still
    gives a forecast, and the unusual weeks are the active warning."""
    result = forecast(
        series(12, spikes={4: 30, 8: 30}),
        ForecastSettings(unusual_weeks_included=False),
    )

    assert len(result.valid_weeks) == 12
    assert len(result.calculation_weeks) == 10
    assert result.base_forecast is not None
    assert (result.confidence_label, result.confidence_condition) == (
        trust.MIDDELS,
        trust.ACTIVE_WARNING,
    )


def test_a_product_whose_latest_week_is_valid_has_0_weeks_since_the_latest_valid_week():
    """FR-18, R-15: no weeks have passed when the latest data week is a valid week."""
    assert forecast(series(20)).weeks_since_latest_valid == 0
    assert forecast(series(20, stockouts={19})).weeks_since_latest_valid == 0
