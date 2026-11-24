"""The base forecast of a product (Story 2.2; FR-5, FR-6, FR-8, FR-16, FR-17, R-2, R-3, R-4, R-6).

The expected calculation weeks, levels and base forecasts are read from the reference
spreadsheet for every case and rule test product that states them, so no expected value
is copied into the tests (AD-17). They use no database.
"""

import dataclasses
from decimal import Decimal

import answer_key_reader as reader
import pytest

from forecasting import forecast as core
from forecasting import settings as defaults
from forecasting.settings import ForecastSettings
from forecasting.weeks import Week

# The examples that Story 2.2 must check, as the spreadsheet names them (PRD §5.7).
# E14 is left out: it has seasonal adjustment on, which is Epic 5.
LISTED_EXAMPLES = {
    "E1",
    "E2",
    "E7",
    "E8",
    "E9",
    "E11 a",
    "E11 b",
    "E15",
    "E16",
    "E17",
    "E18 a",
    "E18 b",
    "E19",
    "E20",
    "E23",
    "E28",
    "FR-21 a",
    "FR-21 b",
}
STATED = ("calculation_weeks", "levels", "base_forecast")
CASES = [
    row
    for row in reader.cases()
    if any(column in row for column in STATED) and row["seasonal_adjustment"] == "off"
]
# The rule test products have no settings of their own, so the FR-20 defaults apply.
PRODUCTS = [row for row in reader.products() if "base_forecast" in row]


def core_weeks(sales):
    return [Week(week.units_sold, week.stockout) for week in sales]


def settings_of(row):
    return ForecastSettings(
        method=row["method"],
        window=row["window"],
        smoothing_factor=row["smoothing_factor"],
        unusual_weeks_included=row["unusual_weeks_setting"] == "included",
    )


DEFAULT_SETTINGS = ForecastSettings()


def forecast(sales, settings=DEFAULT_SETTINGS, stock_on_hand=0):
    return core.forecast_product(core_weeks(sales), stock_on_hand, settings)


def assert_stated_values_match(row, settings):
    """Compare every value that the row states, and only those."""
    result = forecast(row["sales"], settings)
    if "calculation_weeks" in row:
        assert len(result.calculation_weeks) == row["calculation_weeks"]
    if "levels" in row:
        assert len(result.levels) == len(row["levels"])
        for level, expected in zip(result.levels, row["levels"], strict=True):
            assert abs(level - expected) < reader.TOLERANCE
    if "base_forecast" in row:
        if row["base_forecast"] is None:
            assert result.base_forecast is None
            assert result.no_forecast_reason is not None
        else:
            assert abs(result.base_forecast - row["base_forecast"]) < reader.TOLERANCE
            assert result.no_forecast_reason is None


def history(*units):
    """A history of valid weeks, or of stockout weeks for a unit written as «S»."""
    return [
        reader.Week(0, True) if unit == "S" else reader.Week(unit, False)
        for unit in units
    ]


@pytest.mark.parametrize("row", CASES, ids=lambda row: row["case"])
def test_every_case_matches_the_spreadsheet(row):
    """FR-5, FR-6, FR-8 (E1, E2, E7 to E9, E11, E15 to E20, E23, E28 and the FR-21
    variants): the calculation weeks, the levels and the base forecast that a case
    states are the ones the core calculates, with its own method, window, factor and
    setting for unusual weeks."""
    assert_stated_values_match(row, settings_of(row))


@pytest.mark.parametrize("row", PRODUCTS, ids=lambda row: row["product"])
def test_every_rule_test_product_matches_the_spreadsheet(row):
    """FR-3, FR-5: the base forecast of each rule test product, with the FR-20 defaults."""
    assert_stated_values_match(row, ForecastSettings())


def test_the_listed_examples_are_all_checked():
    """DR-3, FR-5 (E1 to E28): every example of the story is among the checked cases,
    the only case with a stated value that is left out is the seasonal E14, and every
    rule test product states a base forecast, so none is left out."""
    checked = {row["case"].split(" (")[0] for row in CASES}
    assert LISTED_EXAMPLES <= checked
    left_out = {
        row["case"]
        for row in reader.cases()
        if any(column in row for column in STATED) and row not in CASES
    }
    assert left_out == {"E14"}
    assert len(PRODUCTS) == len(reader.products())


def test_the_calculation_weeks_follow_the_setting_for_unusual_weeks():
    """FR-16, FR-17, R-2 (E8, E9, E16): an unusual week is a calculation week only when
    the setting includes it, and level-shift weeks always are."""
    e8 = history(20, 22, 21, 50, 52, 21)
    included = forecast(e8)
    excluded = forecast(e8, ForecastSettings(unusual_weeks_included=False))
    assert included.calculation_weeks == (1, 2, 3, 4, 5, 6)
    assert excluded.calculation_weeks == (1, 2, 3, 6)
    assert excluded.unusual_weeks == (4, 5)
    assert excluded.valid_weeks == (1, 2, 3, 4, 5, 6)

    e16 = history(20, 22, 21, "S", "S", 50, "S", 52, 51)
    for unusual_weeks_included in (True, False):
        result = forecast(
            e16, ForecastSettings(unusual_weeks_included=unusual_weeks_included)
        )
        assert result.calculation_weeks == (1, 2, 3, 6, 8, 9)
        assert result.level_shift_weeks == (6, 8, 9)


def test_the_moving_average_takes_the_last_n_calculation_weeks():
    """FR-5, R-3 (E1, E20): the window picks the last N weeks, and a window of 2 and one
    of 12 are the ends of the range (FR-20)."""
    sales = history(*range(10, 10 + 14 * 2, 2))
    assert (
        forecast(sales, ForecastSettings(window=defaults.WINDOW.minimum)).base_forecast
        == (34 + 36) / 2
    )
    assert (
        forecast(sales, ForecastSettings(window=defaults.WINDOW.maximum)).base_forecast
        == sum(range(14, 38, 2)) / 12
    )


def test_the_base_forecast_keeps_full_precision():
    """FR-5, AD-3, R-9 (E1): the core returns 14.3333…, not a rounded number."""
    result = forecast(history(12, 15, 11, 14, 13, 16, 12, 15))
    assert result.base_forecast == (16 + 12 + 15) / 3


def test_exponential_smoothing_skips_weeks_that_are_not_calculation_weeks():
    """FR-6, R-4 (E17): a stockout week is skipped and not counted as 0, and with the
    unusual weeks excluded their weeks are skipped too (as E8)."""
    settings = ForecastSettings(method=defaults.EXPONENTIAL_SMOOTHING)
    e17 = forecast(history(20, 22, "S", "S", 21, 23), settings)
    assert e17.levels == pytest.approx((20, 20.6, 20.72, 21.404))
    assert e17.base_forecast == e17.levels[-1]

    excluded = dataclasses.replace(settings, unusual_weeks_included=False)
    e8 = forecast(history(20, 22, 21, 50, 52, 21), excluded)
    assert e8.calculation_weeks == (1, 2, 3, 6)
    assert e8.levels == pytest.approx((20, 20.6, 20.72, 20.804))


def test_the_smoothing_factor_may_be_a_decimal_as_the_model_stores_it():
    """FR-6, AD-9: a Decimal factor gives the same result as the float of E2."""
    sales = history(12, 15, 11, 14, 13, 16, 12, 15)
    method = defaults.EXPONENTIAL_SMOOTHING
    as_decimal = ForecastSettings(method=method, smoothing_factor=Decimal("0.3"))
    as_float = ForecastSettings(method=method, smoothing_factor=0.3)
    assert forecast(sales, as_decimal) == dataclasses.replace(
        forecast(sales, as_float), settings=as_decimal
    )


def test_fewer_than_three_valid_weeks_gives_no_forecast():
    """FR-8, R-6 (E11 a): 2 valid weeks, whatever the method or the window. The reason
    is checked before the window, so a window of 4 does not change it, and a window of 2
    that the 2 weeks would fill gives no forecast either."""
    for method in defaults.METHODS:
        for window in (2, 3, 4):
            result = forecast(
                history(30, "S", 25), ForecastSettings(method=method, window=window)
            )
            assert result.base_forecast is None
            assert result.levels == ()
            assert result.no_forecast_reason == core.TOO_FEW_VALID_WEEKS
    assert forecast([]).no_forecast_reason == core.TOO_FEW_VALID_WEEKS
    assert forecast(history("S", "S", "S")).valid_weeks == ()


def test_three_valid_weeks_are_enough_for_both_methods():
    """FR-5, FR-6, FR-8, R-6 (E7): exactly 3 valid weeks gives a forecast with the
    moving average, with window 2 or 3, and with exponential smoothing. The moving
    average has no levels."""
    sales = history(10, 20, "S", 30)
    for window, expected in ((2, (20 + 30) / 2), (3, (10 + 20 + 30) / 3)):
        result = forecast(sales, ForecastSettings(window=window))
        assert result.base_forecast == expected
        assert result.no_forecast_reason is None
        assert result.levels == ()
    smoothing = ForecastSettings(method=defaults.EXPONENTIAL_SMOOTHING)
    assert forecast(sales, smoothing).base_forecast is not None


def test_too_few_calculation_weeks_gives_no_forecast_and_names_the_numbers():
    """FR-8, R-6 (E11 b): 12 valid weeks of which 2 are unusual and excluded leave 10
    calculation weeks, and the result holds the window and the 10 that the warning names."""
    e11b = next(row["sales"] for row in reader.cases() if row["case"] == "E11 b")
    settings = ForecastSettings(window=12, unusual_weeks_included=False)
    result = forecast(e11b, settings)
    assert result.no_forecast_reason == core.TOO_FEW_CALCULATION_WEEKS
    assert result.required_calculation_weeks == 12
    assert len(result.valid_weeks) == 12
    assert len(result.calculation_weeks) == 10
    assert result.base_forecast is None

    # The same history with the unusual weeks included has 12 calculation weeks.
    included = forecast(
        e11b, dataclasses.replace(settings, unusual_weeks_included=True)
    )
    assert included.no_forecast_reason is None
    assert len(included.calculation_weeks) == 12


def test_an_excluded_unusual_week_still_counts_as_a_valid_week():
    """FR-16, R-6: 5 valid weeks, 2 of them unusual and excluded, leave 3 calculation
    weeks, so window 3 gives a forecast and window 4 gives none because of the window,
    not because of too few valid weeks."""
    sales = history(10, 10, 10, 30, 30)
    settings = ForecastSettings(window=3, unusual_weeks_included=False)
    assert forecast(sales, settings).base_forecast == 10
    narrow = forecast(sales, dataclasses.replace(settings, window=4))
    assert narrow.no_forecast_reason == core.TOO_FEW_CALCULATION_WEEKS
    assert len(narrow.valid_weeks) == 5


def test_exponential_smoothing_needs_one_calculation_week():
    """FR-6, FR-8, R-6: the exponential smoothing asks for 1 calculation week, whatever
    the window."""
    settings = ForecastSettings(method=defaults.EXPONENTIAL_SMOOTHING, window=12)
    result = forecast(history(10, 20, 30), settings)
    assert result.required_calculation_weeks == 1
    assert result.base_forecast is not None


def test_the_stock_on_hand_does_not_change_the_base_forecast():
    """FR-5, AD-2 (E1): the stock on hand is an input from Story 2.4 on and is not used yet."""
    sales = history(12, 15, 11, 14, 13, 16, 12, 15)
    assert forecast(sales, stock_on_hand=0) == forecast(sales, stock_on_hand=500)


def test_the_units_of_a_stockout_week_are_never_used():
    """R-1, R-3, R-4 (E7, E17): another number of units in a stockout week gives the
    same result."""
    for method in defaults.METHODS:
        settings = ForecastSettings(method=method)
        a = core.forecast_product(
            [Week(20, False), Week(22, False), Week(0, True), Week(21, False)],
            0,
            settings,
        )
        b = core.forecast_product(
            [Week(20, False), Week(22, False), Week(900, True), Week(21, False)],
            0,
            settings,
        )
        assert a == b


def test_the_weeks_are_read_once_and_never_changed():
    """FR-5, AD-2 (E7): any iterable of weeks works, and a list is left as it was."""
    weeks = core_weeks(history(20, 22, "S", 21, 23))
    before = list(weeks)
    from_list = core.forecast_product(weeks, 0, ForecastSettings())
    from_generator = core.forecast_product(
        (week for week in weeks), 0, ForecastSettings()
    )
    assert weeks == before
    assert from_list == from_generator


def test_the_result_is_frozen_and_holds_the_settings_used():
    """FR-5, AD-2, AD-5 (E1): a frozen ProductResult that carries its settings and plain numbers."""
    settings = ForecastSettings(window=4)
    result = forecast(history(10, 11, 12, 13), settings)
    assert result.settings is settings
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.base_forecast = 0
    assert isinstance(result.base_forecast, float)
    assert all(
        isinstance(level, float)
        for level in forecast(
            history(10, 11, 12), ForecastSettings(method=defaults.EXPONENTIAL_SMOOTHING)
        ).levels
    )


def test_an_unknown_method_is_refused():
    """FR-20, AD-9 (E1): a method that is not one of the two is never taken for exponential
    smoothing."""
    with pytest.raises(ValueError):
        forecast(history(10, 11, 12), ForecastSettings(method="trend"))


@pytest.mark.parametrize("window", [0, 1, -3, 13, 2.5, 3.0, "3", None, True])
def test_a_window_outside_its_definition_is_refused(window):
    """FR-20, AD-9 (E1): the window is a whole number from 2 to 12. A window of 0 would
    divide by zero, and a negative window would give a number that looks like a forecast.
    The core refuses them as the settings form will (Story 3.1)."""
    with pytest.raises(ValueError, match="window"):
        forecast(history(10, 11, 12), ForecastSettings(window=window))


@pytest.mark.parametrize(
    "factor", [0, 0.05, Decimal("0.0"), 0.95, 1, 5, -0.3, float("nan"), float("inf")]
)
def test_a_smoothing_factor_outside_its_range_is_refused(factor):
    """FR-6, FR-20, AD-9 (E2): the factor is from 0.1 to 0.9. A factor outside it, or not a
    number, would give levels that look like a forecast."""
    settings = ForecastSettings(
        method=defaults.EXPONENTIAL_SMOOTHING, smoothing_factor=factor
    )
    with pytest.raises(ValueError, match="smoothing factor"):
        forecast(history(10, 11, 12), settings)


@pytest.mark.parametrize("window", [defaults.WINDOW.minimum, defaults.WINDOW.maximum])
@pytest.mark.parametrize(
    "factor",
    [
        defaults.SMOOTHING_FACTOR.minimum,
        defaults.SMOOTHING_FACTOR.maximum,
        float(defaults.SMOOTHING_FACTOR.minimum),
        float(defaults.SMOOTHING_FACTOR.maximum),
    ],
)
def test_the_ends_of_the_ranges_are_accepted(window, factor):
    """FR-20, AD-9: both ends of each range are allowed, as a Decimal (as the model stores
    them) and as a float, and the float 0.9 is not taken for more than the Decimal 0.9."""
    for method in defaults.METHODS:
        settings = ForecastSettings(
            method=method, window=window, smoothing_factor=factor
        )
        assert forecast(history(*range(1, 15)), settings).base_forecast is not None


def test_the_window_is_checked_for_exponential_smoothing_too():
    """FR-6, FR-20, AD-9: the window belongs to the company settings, so a window of 0 is
    refused although exponential smoothing does not use it."""
    settings = ForecastSettings(method=defaults.EXPONENTIAL_SMOOTHING, window=0)
    with pytest.raises(ValueError, match="window"):
        forecast(history(10, 11, 12), settings)


def test_the_settings_are_checked_even_when_there_is_no_forecast():
    """FR-8, AD-9 (E11 a): a bad setting is not hidden by a product with too few weeks, so
    it fails on the first product and not on the first one with enough data."""
    with pytest.raises(ValueError):
        forecast(history(30, "S", 25), ForecastSettings(window=0))
    with pytest.raises(ValueError):
        forecast([], ForecastSettings(smoothing_factor=2))


def test_the_forecast_settings_start_at_the_fr_20_defaults():
    """FR-20, AD-9: ForecastSettings() reads the defaults of settings.py."""
    settings = ForecastSettings()
    assert settings.method == defaults.DEFAULT_METHOD
    assert settings.window == defaults.WINDOW.default
    assert settings.smoothing_factor == defaults.SMOOTHING_FACTOR.default
    assert settings.unusual_weeks_included is defaults.DEFAULT_UNUSUAL_WEEKS_INCLUDED
