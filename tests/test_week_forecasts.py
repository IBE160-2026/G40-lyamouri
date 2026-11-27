"""The week forecasts, the scenarios and the suggested order quantity (Story 2.4).

FR-7, FR-10, FR-11, FR-12, R-5, R-7, R-8, R-13, AD-2, AD-3. The expected values are read
from the reference spreadsheet for every case that states them, so no expected value is
copied into the tests (AD-17). They use no database.
"""

import dataclasses
from decimal import Decimal

import answer_key_reader as reader
import pytest

from forecasting import forecast as core
from forecasting import settings as defaults
from forecasting.horizon import HORIZON_WEEKS
from forecasting.settings import ForecastSettings
from forecasting.trust import WEEKS_REPEAT_WEEK_1
from forecasting.weeks import Week

# The examples that state a scenario, an unrounded order or a suggested order quantity
# without seasonal adjustment, as the spreadsheet names them (PRD §5.7). The seasonal
# E14 and E25 to E27 are Epic 5.
LISTED_EXAMPLES = {
    "E3",
    "E4",
    "E5",
    "E6",
    "E21",
    "E23",
    "E24 (A)",
    "E24 (B)",
    "FR-21 c",
    "FR-21 d",
}
STATED = (
    "normal",
    "optimistic",
    "pessimistic",
    "order_unrounded",
    "suggested_order_quantity",
)
CASES = [
    row
    for row in reader.cases()
    if any(column in row for column in STATED) and row["seasonal_adjustment"] == "off"
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


def result_of(row):
    return core.forecast_product(
        core_weeks(row["sales"]), row["stock_on_hand"], settings_of(row)
    )


def history(*units):
    return [Week(unit, False) for unit in units]


def forecast(units, settings=None, stock_on_hand=0):
    return core.forecast_product(
        history(*units), stock_on_hand, settings or ForecastSettings()
    )


def close(value, expected):
    return abs(value - expected) < reader.TOLERANCE


@pytest.mark.parametrize("row", CASES, ids=lambda row: row["case"])
def test_every_stated_value_of_a_case_is_the_one_the_core_calculates(row):
    """FR-7, FR-10, FR-11, R-5, R-7, R-8 (E3 to E6, E21, E23, E24, FR-21 c and d): the
    scenarios of every horizon week, the unrounded order and the suggested order quantity
    that a case states are the ones the core calculates from the case's own settings."""
    result = result_of(row)

    for week in result.scenarios:
        for column in ("normal", "optimistic", "pessimistic"):
            if column in row:
                assert close(getattr(week, column), row[column]), column
    if "order_unrounded" in row:
        assert close(result.order_unrounded, row["order_unrounded"])
    if "suggested_order_quantity" in row:
        assert result.suggested_order_quantity == row["suggested_order_quantity"]


def test_the_listed_examples_are_all_checked():
    """DR-3, FR-10, FR-11 (E3 to E6, E21, E23, E24, FR-21): every example of the story
    is among the checked cases, and the only stated values left out are the seasonal ones."""
    assert {row["case"] for row in CASES} == LISTED_EXAMPLES
    left_out = {
        row["case"]
        for row in reader.cases()
        if any(column in row for column in STATED) and row not in CASES
    }
    assert left_out and left_out <= {"E14", "E25", "E26", "E27"}
    assert all(
        row["seasonal_adjustment"] == "on"
        for row in reader.cases()
        if row["case"] in left_out
    )


def row_of(name):
    return next(row for row in reader.cases() if row["case"] == name)


@pytest.mark.parametrize("method", defaults.METHODS)
def test_without_seasonal_adjustment_weeks_1_2_and_3_equal_the_base_forecast(method):
    """FR-7, R-5 (E1): three week forecasts equal to the base forecast for both methods,
    the product is marked for the FR-7 note, and every week has its scenarios; for the
    moving average they are the 14.333 that the spreadsheet states for E1."""
    e1 = row_of("E1")
    settings = dataclasses.replace(settings_of(e1), method=method)
    result = core.forecast_product(core_weeks(e1["sales"]), 0, settings)

    assert len(result.week_forecasts) == len(result.scenarios) == HORIZON_WEEKS == 3
    assert set(result.week_forecasts) == {result.base_forecast}
    assert all(week.normal == result.base_forecast for week in result.scenarios)
    assert result.notes == (WEEKS_REPEAT_WEEK_1,)
    if method == defaults.MOVING_AVERAGE:
        assert all(close(f, e1["base_forecast"]) for f in result.week_forecasts)


def test_e28_the_forecast_lags_behind_a_steady_trend():
    """FR-7, R-5, E28: sales 10 to 20 in steps of 2 give 18.0 in all three weeks, while the
    trend would continue to 22, and nothing marks the lag as an error (a stated limitation)."""
    row = row_of("E28")
    result = result_of(row)
    sales = [week.units_sold for week in row["sales"]]
    next_on_the_trend = sales[-1] + (sales[-1] - sales[-2])

    assert close(result.base_forecast, row["base_forecast"])
    assert result.week_forecasts == (result.base_forecast,) * 3
    assert result.base_forecast < next_on_the_trend == 22
    assert result.no_forecast_reason is None


def test_a_product_without_a_forecast_has_nothing_to_show_or_order():
    """FR-8, FR-11 (E11 a): no week forecasts, no scenarios, no margin amount, no order
    and no FR-7 note; the stock on hand is still held (R-13)."""
    e11a = row_of("E11 a")
    result = core.forecast_product(core_weeks(e11a["sales"]), 7, ForecastSettings())

    assert result.base_forecast is None
    assert result.week_forecasts is None
    assert result.scenarios is None
    assert result.safety_margin_amount is None
    assert result.order_unrounded is None
    assert result.suggested_order_quantity is None
    assert result.notes == ()
    assert result.stock_on_hand == 7


def test_too_few_calculation_weeks_also_leave_nothing_to_show_or_order():
    """FR-8, FR-11 (E11 b): enough valid weeks but fewer calculation weeks than the window
    is the second way to no forecast, and the new fields are None there too."""
    result = forecast((10, 11, 12, 13), ForecastSettings(window=12), stock_on_hand=3)

    assert result.no_forecast_reason == core.TOO_FEW_CALCULATION_WEEKS
    assert result.week_forecasts is result.scenarios is None
    assert result.safety_margin_amount is result.order_unrounded is None
    assert result.suggested_order_quantity is None
    assert result.notes == ()
    assert result.stock_on_hand == 3


def test_the_result_holds_what_the_order_calculation_line_shows():
    """FR-12, R-13 (E4): the week-1 forecast, the safety margin amount, the stock, the
    unrounded result and the quantity, as plain numbers, in a frozen result."""
    row = next(row for row in CASES if row["case"] == "E4")
    result = result_of(row)
    week_1 = result.week_forecasts[0]

    assert result.stock_on_hand == row["stock_on_hand"] == 5
    assert close(result.safety_margin_amount, week_1 * row["safety_margin"] / 100)
    assert close(
        result.order_unrounded,
        week_1 + result.safety_margin_amount - result.stock_on_hand,
    )
    assert isinstance(result.suggested_order_quantity, int)
    assert all(isinstance(f, float) for f in result.week_forecasts)
    assert isinstance(result.order_unrounded, float)
    assert isinstance(result.safety_margin_amount, float)
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.suggested_order_quantity = 0
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.scenarios[0].optimistic = 0


def test_e5_rounds_70_point_00000000000001_to_70_and_not_to_71():
    """FR-11, R-9, E5: the unrounded order is above 70 in floats, and the quantity is 70."""
    row = next(row for row in CASES if row["case"] == "E5")
    result = result_of(row)

    assert result.order_unrounded > 70
    assert result.suggested_order_quantity == row["suggested_order_quantity"] == 70


def test_a_stock_that_covers_the_need_gives_0_and_keeps_the_negative_result():
    """FR-11, R-8, E6: 100 × 1.1 − 150 is −40, the quantity is 0 and never negative, and
    the unrounded result keeps its sign for the calculation line."""
    row = next(row for row in CASES if row["case"] == "E6")
    result = result_of(row)

    assert result.order_unrounded < 0
    assert result.suggested_order_quantity == row["suggested_order_quantity"] == 0


def test_a_real_remainder_is_rounded_up_once():
    """FR-11, R-8, R-9 (E21): 0.067 gives 1, and a hand-made forecast of 100 with stock
    exactly at the need gives 0 and not 1."""
    row = next(row for row in CASES if row["case"] == "E21")
    assert result_of(row).suggested_order_quantity == 1
    assert forecast((100, 100, 100), stock_on_hand=110).suggested_order_quantity == 0
    assert forecast((100, 100, 100), stock_on_hand=109).suggested_order_quantity == 1


def test_a_zero_forecast_has_scenarios_of_0_and_orders_nothing():
    """FR-7, FR-11 (E23): a forecast of 0 has scenarios of 0 and a quantity of 0. That the
    order reads week 1 only cannot be observed before Epic 5, because the three week
    forecasts are equal until seasonal adjustment."""
    result = forecast((0, 0, 0))

    assert set(result.week_forecasts) == {0.0}
    assert result.scenarios[0] == core.WeekScenarios(0.0, 0.0, 0.0)
    assert result.suggested_order_quantity == 0
    assert result.notes == (WEEKS_REPEAT_WEEK_1,)


@pytest.mark.parametrize("percentage", [0, 10, 50])
def test_the_scenarios_follow_the_scenario_percentage(percentage):
    """FR-10, R-7 (E3): optimistic is F × (1 + s) and pessimistic F × (1 − s) for the 14.333
    of E1, also at the two ends of the range; at 0 % all three are equal, and at 50 %
    the pessimistic scenario is 7.167."""
    e1 = row_of("E1")
    settings = dataclasses.replace(settings_of(e1), scenario_percentage=percentage)
    result = core.forecast_product(core_weeks(e1["sales"]), 0, settings)
    share = percentage / 100

    for week in result.scenarios:
        assert close(week.normal, e1["base_forecast"])
        assert close(week.optimistic, e1["base_forecast"] * (1 + share))
        assert close(week.pessimistic, e1["base_forecast"] * (1 - share))
    if percentage == 0:
        assert result.scenarios[0].optimistic == result.scenarios[0].pessimistic
        assert result.scenarios[0].pessimistic == result.base_forecast
    if percentage == 50:
        assert abs(result.scenarios[0].pessimistic - 7.167) < reader.TOLERANCE


def test_the_pessimistic_scenario_is_never_below_0():
    """FR-10, R-7: the function itself keeps the floor, although the range of the setting
    (0 to 50) never reaches it."""
    assert core.scenarios_of(5.0, 150).pessimistic == 0.0
    assert core.scenarios_of(0.0, 50) == core.WeekScenarios(0.0, 0.0, 0.0)


@pytest.mark.parametrize("margin", [0, 100])
def test_the_ends_of_the_safety_margin_are_accepted(margin):
    """FR-20, AD-9: a margin of 0 orders the forecast less the stock, and of 100 doubles it."""
    result = forecast((10, 10, 10), ForecastSettings(safety_margin=margin))
    assert result.suggested_order_quantity == 10 * (100 + margin) // 100


@pytest.mark.parametrize("value", [-1, 51, 10.0, "10", None, True, Decimal(10)])
def test_a_scenario_percentage_outside_its_definition_is_refused(value):
    """FR-20, AD-9: a whole percent from 0 to 50, never a bool, a float or a string."""
    with pytest.raises(ValueError, match="scenario percentage"):
        forecast((10, 11, 12), ForecastSettings(scenario_percentage=value))


@pytest.mark.parametrize("value", [-1, 101, 10.0, "10", None, True, Decimal(10)])
def test_a_safety_margin_outside_its_definition_is_refused(value):
    """FR-20, AD-9: a whole percent from 0 to 100, never a bool, a float or a string."""
    with pytest.raises(ValueError, match="safety margin"):
        forecast((10, 11, 12), ForecastSettings(safety_margin=value))


@pytest.mark.parametrize("stock", [2.5, "5", None, True, False, Decimal(5)])
def test_a_stock_that_is_not_a_whole_number_is_a_type_error(stock):
    """R-13, FR-11: a float, a string, a bool or nothing is not a stock on hand."""
    with pytest.raises(TypeError, match="stock on hand"):
        forecast((10, 11, 12), stock_on_hand=stock)


def test_a_negative_stock_is_a_value_error_also_without_a_forecast():
    """R-13, FR-11: a negative stock would raise the order, so it is refused before
    anything is calculated, also for a product with too little data."""
    with pytest.raises(ValueError, match="stock on hand"):
        forecast((10, 11, 12), stock_on_hand=-1)
    with pytest.raises(ValueError, match="stock on hand"):
        forecast((10,), stock_on_hand=-1)


@pytest.mark.parametrize(
    "settings",
    [ForecastSettings(scenario_percentage=51), ForecastSettings(safety_margin=101)],
)
def test_a_bad_percentage_is_refused_also_for_a_product_without_a_forecast(settings):
    """FR-20, AD-9, FR-8: the settings are checked before the weeks, so a product with
    too little data does not hide a setting the form should have stopped."""
    with pytest.raises(ValueError, match="whole number"):
        forecast((10,), settings)


def test_the_new_settings_start_at_the_fr20_defaults():
    """FR-20, AD-9: the scenario percentage and the margin are read from settings.py."""
    settings = ForecastSettings()
    assert settings.scenario_percentage == defaults.SCENARIO_PERCENTAGE.default
    assert settings.safety_margin == defaults.SAFETY_MARGIN.default
