"""The forecast of a product (R-2 to R-8, R-13, R-15, R-16; FR-5 to FR-8, FR-10 to FR-12, FR-15 to FR-19).

`forecast_product` classifies the weeks (R-1, R-10, R-11), chooses the calculation weeks,
and calculates the base forecast with the moving average or exponential smoothing, or
gives no forecast and the reason. From the base forecast it gives the week forecasts
(R-5), the scenarios (R-7) and the suggested order quantity (R-8), which is rounded up
once through `forecasting/rounding.py` (R-9). It also gives the active warnings, the notes
and the confidence label (`forecasting/trust.py`). It works on positions in the sales history,
from 1 for the oldest week (AD-8), keeps full float precision and returns numbers only,
no formatted values and no text (AD-3, AD-4). Only the standard library and the modules
of `forecasting/` are imported (AD-1).
"""

from dataclasses import dataclass

from forecasting.horizon import HORIZON_WEEKS
from forecasting.rounding import round_up_to_units
from forecasting.settings import (
    METHODS,
    MOVING_AVERAGE,
    SAFETY_MARGIN,
    SCENARIO_PERCENTAGE,
    SMOOTHING_FACTOR,
    WINDOW,
    ForecastSettings,
)
from forecasting.trust import (
    WEEKS_REPEAT_WEEK_1,
    active_warnings,
    confidence,
    recent_only,
    weeks_since_latest_valid,
)
from forecasting.weeks import classify_weeks

# R-6: a forecast needs at least this many valid weeks.
MINIMUM_VALID_WEEKS = 3
# The reasons for no forecast, checked in this order (R-6).
TOO_FEW_VALID_WEEKS = "too_few_valid_weeks"
TOO_FEW_CALCULATION_WEEKS = "too_few_calculation_weeks"


@dataclass(frozen=True)
class WeekScenarios:
    """The three scenarios of one horizon week (R-7): the pessimistic one is never below 0."""

    normal: float
    optimistic: float
    pessimistic: float


@dataclass(frozen=True)
class ProductResult:
    """What the core has calculated for one product.

    The positions are those of the valid, unusual, level-shift and calculation weeks.
    `levels` has the level after each calculation week for exponential smoothing and is
    empty for the moving average. `base_forecast` is None, with the reason in
    `no_forecast_reason`, when there is no forecast; `required_calculation_weeks` is the
    window for the moving average and 1 for exponential smoothing.

    `week_forecasts` and `scenarios` have one entry for each of the 3 horizon weeks, week 1
    first. Without seasonal adjustment the week forecasts equal the base forecast, and
    `notes` has the code of the FR-7 note. The order is calculated from week 1 only:
    `safety_margin_amount` is week 1 × the margin, `order_unrounded` is week 1 × (1 + the
    margin) − the stock on hand, which may be negative, and `suggested_order_quantity` is
    that value rounded up to whole units and never below 0 (R-8, R-9). All of them are None
    when there is no forecast (FR-8). `stock_on_hand` is the stock at the end of the latest
    data week (R-13), also without a forecast.

    `weeks_of_cover` is the stock on hand ÷ the week-1 normal forecast, unrounded, and None
    when there is no forecast or the week-1 forecast is 0 (R-12, E23). `order_soon` is True
    when the suggested order quantity is above 0 (R-12), and False without a forecast.

    `history_length` is the number of weeks in the sales history, stockout weeks included.
    `warnings` are the active warnings of R-15 in its order and `notes` the notes, as codes
    (`forecasting/trust.py`); `confidence_label` is the label of R-16 and
    `confidence_condition` the condition that decided it. The `recent_` fields are the
    positions of the stockout, unusual and level-shift weeks in the last 12 weeks, and the
    units sold in the recent unusual weeks, in the same order. `weeks_since_latest_valid` is
    None for a product with no valid week. `explanation/` writes every text from these.
    """

    settings: ForecastSettings
    valid_weeks: tuple[int, ...]
    unusual_weeks: tuple[int, ...]
    level_shift_weeks: tuple[int, ...]
    calculation_weeks: tuple[int, ...]
    levels: tuple[float, ...]
    base_forecast: float | None
    no_forecast_reason: str | None
    required_calculation_weeks: int
    stock_on_hand: int
    week_forecasts: tuple[float, ...] | None
    scenarios: tuple[WeekScenarios, ...] | None
    safety_margin_amount: float | None
    order_unrounded: float | None
    suggested_order_quantity: int | None
    weeks_of_cover: float | None
    order_soon: bool
    history_length: int
    warnings: tuple[str, ...]
    notes: tuple[str, ...]
    confidence_label: str
    confidence_condition: str
    weeks_since_latest_valid: int | None
    recent_stockout_weeks: tuple[int, ...]
    recent_unusual_weeks: tuple[int, ...]
    recent_unusual_units: tuple[int, ...]
    recent_level_shift_weeks: tuple[int, ...]


def _check_percentage(name, value, allowed):
    """A whole percent inside its FR-20 range, both ends included (a bool is not one)."""
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or not allowed.minimum <= value <= allowed.maximum
    ):
        raise ValueError(
            f"the {name} is a whole number from {allowed.minimum} to "
            f"{allowed.maximum}, not {value!r}"
        )


def check_settings(settings):
    """Refuse a setting outside the FR-20 definitions (AD-9).

    The settings form refuses them first and gives the user a message (Story 3.1), so
    this is the core's own guard: a window of 0 would divide by zero, a negative window
    or a factor outside its range would give a number that looks like a forecast. The
    ranges are read from `settings.py`, and the window is checked even when the
    exponential smoothing does not use it, because the settings belong together. The
    scenario percentage and the safety margin are whole percents.
    """
    if settings.method not in METHODS:
        raise ValueError(f"not a forecast method: {settings.method!r}")
    window = settings.window
    # A bool is an int, but 0 and 1 are below the smallest window.
    if not isinstance(window, int) or not WINDOW.minimum <= window <= WINDOW.maximum:
        raise ValueError(
            f"the window is a whole number from {WINDOW.minimum} to {WINDOW.maximum}, "
            f"not {window!r}"
        )
    # Both ends are converted to float, so that 0.9 as a float is not above a Decimal 0.9.
    if (
        not float(SMOOTHING_FACTOR.minimum)
        <= float(settings.smoothing_factor)
        <= float(SMOOTHING_FACTOR.maximum)
    ):
        raise ValueError(
            f"the smoothing factor is from {SMOOTHING_FACTOR.minimum} to "
            f"{SMOOTHING_FACTOR.maximum}, not {settings.smoothing_factor!r}"
        )
    _check_percentage(
        "scenario percentage", settings.scenario_percentage, SCENARIO_PERCENTAGE
    )
    _check_percentage("safety margin", settings.safety_margin, SAFETY_MARGIN)


def check_stock_on_hand(stock_on_hand):
    """Refuse a stock on hand that is not a whole number of at least 0 (R-13).

    The database column cannot hold a negative number, so this is the core's own guard: a
    negative stock would raise the order quantity, and a string or a float would be taken
    for a number. A bool is an int in Python, but it is not a stock. 0 is a stock.
    """
    if isinstance(stock_on_hand, bool) or not isinstance(stock_on_hand, int):
        raise TypeError(f"the stock on hand is a whole number, not {stock_on_hand!r}")
    if stock_on_hand < 0:
        raise ValueError(f"the stock on hand is at least 0, not {stock_on_hand!r}")


def scenarios_of(week_forecast, scenario_percentage):
    """The three scenarios of one week forecast F and the scenario percentage s (R-7).

    Optimistic is F × (1 + s), and pessimistic is the larger of 0 and F × (1 − s).
    """
    share = scenario_percentage / 100
    return WeekScenarios(
        normal=week_forecast,
        optimistic=week_forecast * (1 + share),
        pessimistic=max(0.0, week_forecast * (1 - share)),
    )


def forecast_product(weeks, stock_on_hand, settings):
    """Calculate the base forecast of one product from its weeks, oldest first.

    `stock_on_hand` is the stock at the end of the latest data week (R-13). The weeks are
    read once and never changed. A setting outside its FR-20 definition raises ValueError,
    and a stock that is not a whole number of at least 0 raises TypeError or ValueError,
    before anything is calculated (`check_settings`, `check_stock_on_hand`).
    """
    check_settings(settings)
    check_stock_on_hand(stock_on_hand)
    weeks = tuple(weeks)
    classification = classify_weeks(weeks)
    # R-2: unusual weeks leave the calculation when the setting excludes them. They stay
    # valid weeks for R-6, and level-shift weeks are never unusual, so they always stay.
    calculation_weeks = tuple(
        position
        for position in classification.valid
        if settings.unusual_weeks_included or position not in classification.unusual
    )
    sales = [weeks[position - 1].units_sold for position in calculation_weeks]

    required = settings.window if settings.method == MOVING_AVERAGE else 1

    reason = None
    if len(classification.valid) < MINIMUM_VALID_WEEKS:
        reason = TOO_FEW_VALID_WEEKS
    elif len(sales) < required:
        reason = TOO_FEW_CALCULATION_WEEKS

    levels = []
    base_forecast = None
    if reason is None and settings.method == MOVING_AVERAGE:
        base_forecast = sum(sales[-required:]) / required
    elif reason is None:
        alpha = float(settings.smoothing_factor)
        level = sales[0]
        levels.append(float(level))
        for units in sales[1:]:
            level = alpha * units + (1 - alpha) * level
            levels.append(level)
        base_forecast = levels[-1]

    week_forecasts = scenarios = None
    safety_margin_amount = order_unrounded = suggested_order_quantity = None
    weeks_of_cover = None
    if base_forecast is not None:
        # R-5: without seasonal adjustment (Epic 5) every week repeats the base forecast.
        week_forecasts = (base_forecast,) * HORIZON_WEEKS
        scenarios = tuple(
            scenarios_of(week_forecast, settings.scenario_percentage)
            for week_forecast in week_forecasts
        )
        # R-8: only week 1 feeds the order. The margin is a whole percent.
        week_1 = week_forecasts[0]
        margin = settings.safety_margin / 100
        safety_margin_amount = week_1 * margin
        order_unrounded = week_1 * (1 + margin) - stock_on_hand
        suggested_order_quantity = max(0, round_up_to_units(order_unrounded))
        # R-12: no cover to give when nothing is expected to sell (E23).
        if week_1 > 0:
            weeks_of_cover = stock_on_hand / week_1

    history_length = len(weeks)
    recent_stockout_weeks = recent_only(
        (position for position, week in enumerate(weeks, start=1) if week.stockout),
        history_length,
    )
    recent_unusual_weeks = recent_only(classification.unusual, history_length)
    recent_level_shift_weeks = recent_only(classification.level_shift, history_length)
    since_latest_valid = weeks_since_latest_valid(classification.valid, history_length)
    warnings = active_warnings(
        recent_stockout_weeks,
        recent_unusual_weeks,
        recent_level_shift_weeks,
        since_latest_valid,
        base_forecast is not None,
    )
    confidence_label, confidence_condition = confidence(
        reason, len(classification.valid), history_length, warnings
    )

    return ProductResult(
        settings=settings,
        valid_weeks=classification.valid,
        unusual_weeks=classification.unusual,
        level_shift_weeks=classification.level_shift,
        calculation_weeks=calculation_weeks,
        levels=tuple(levels),
        base_forecast=base_forecast,
        no_forecast_reason=reason,
        required_calculation_weeks=required,
        stock_on_hand=stock_on_hand,
        week_forecasts=week_forecasts,
        scenarios=scenarios,
        safety_margin_amount=safety_margin_amount,
        order_unrounded=order_unrounded,
        suggested_order_quantity=suggested_order_quantity,
        weeks_of_cover=weeks_of_cover,
        order_soon=suggested_order_quantity is not None
        and suggested_order_quantity > 0,
        history_length=history_length,
        warnings=warnings,
        # R-15: without seasonal adjustment (Epic 5) weeks 2 and 3 repeat week 1.
        notes=() if week_forecasts is None else (WEEKS_REPEAT_WEEK_1,),
        confidence_label=confidence_label,
        confidence_condition=confidence_condition,
        weeks_since_latest_valid=since_latest_valid,
        recent_stockout_weeks=recent_stockout_weeks,
        recent_unusual_weeks=recent_unusual_weeks,
        recent_unusual_units=tuple(
            weeks[position - 1].units_sold for position in recent_unusual_weeks
        ),
        recent_level_shift_weeks=recent_level_shift_weeks,
    )
