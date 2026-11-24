"""The base forecast of a product (R-2, R-3, R-4, R-6; FR-5, FR-6, FR-8, FR-16, FR-17).

`forecast_product` classifies the weeks (R-1, R-10, R-11), chooses the calculation weeks,
and calculates the base forecast with the moving average or exponential smoothing, or
gives no forecast and the reason. It works on positions in the sales history, from 1 for
the oldest week (AD-8), keeps full float precision and returns numbers only, no rounded
values and no text (AD-3, AD-4). Story 2.4 adds the week forecasts and the order quantity.
Only the standard library is imported (AD-1).
"""

from dataclasses import dataclass

from forecasting.settings import (
    METHODS,
    MOVING_AVERAGE,
    SMOOTHING_FACTOR,
    WINDOW,
    ForecastSettings,
)
from forecasting.weeks import classify_weeks

# R-6: a forecast needs at least this many valid weeks.
MINIMUM_VALID_WEEKS = 3
# The reasons for no forecast, checked in this order (R-6).
TOO_FEW_VALID_WEEKS = "too_few_valid_weeks"
TOO_FEW_CALCULATION_WEEKS = "too_few_calculation_weeks"


@dataclass(frozen=True)
class ProductResult:
    """What the core has calculated for one product.

    The positions are those of the valid, unusual, level-shift and calculation weeks.
    `levels` has the level after each calculation week for exponential smoothing and is
    empty for the moving average. `base_forecast` is None, with the reason in
    `no_forecast_reason`, when there is no forecast; `required_calculation_weeks` is the
    window for the moving average and 1 for exponential smoothing.
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


def check_settings(settings):
    """Refuse a method, window or smoothing factor outside the FR-20 definitions (AD-9).

    The settings form refuses them first and gives the user a message (Story 3.1), so
    this is the core's own guard: a window of 0 would divide by zero, a negative window
    or a factor outside its range would give a number that looks like a forecast. The
    ranges are read from `settings.py`, and the window is checked even when the
    exponential smoothing does not use it, because the settings belong together.
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


def forecast_product(weeks, stock_on_hand, settings):
    """Calculate the base forecast of one product from its weeks, oldest first.

    `stock_on_hand` is part of the signature of AD-2 and is not used until Story 2.4.
    The weeks are read once and never changed. A setting outside its FR-20 definition
    raises ValueError before anything is calculated (`check_settings`).
    """
    check_settings(settings)
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
    )
