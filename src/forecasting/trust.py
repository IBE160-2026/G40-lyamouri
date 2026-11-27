"""The active warnings, the notes and the confidence label (R-15, R-16; FR-7, FR-8, FR-15 to 19).

The rules work on positions in the sales history, from 1 for the oldest week (AD-8), and
return codes and numbers only: the wording of every warning, note and reason is written by
`explanation/` (AD-4). The recent period is the last 12 positions of the history, stockout
weeks included. Only the standard library is imported (AD-1).
"""

# R-15: the active warnings, in the order of the rule and with the names of the reference
# spreadsheet. The seasonal pattern (FR-36) is Should and comes with Epic 5.
STOCKOUT_WEEKS = "stockout_weeks"
UNUSUAL_WEEKS = "unusual_weeks"
LEVEL_SHIFT = "level_shift"
OLD_DATA = "old_data"
INSUFFICIENT_DATA = "insufficient_data"
WARNINGS = (STOCKOUT_WEEKS, UNUSUAL_WEEKS, LEVEL_SHIFT, OLD_DATA, INSUFFICIENT_DATA)

# The notes (R-15): they never change the label. Only FR-7 is built.
WEEKS_REPEAT_WEEK_1 = "weeks_repeat_week_1"

# R-16: the labels, from the lowest.
LAV = "lav"
MIDDELS = "middels"
HOY = "høy"

# R-16: the condition that decided the label, checked in this order. A product without a
# forecast has the reason for it as its condition (`forecast.TOO_FEW_VALID_WEEKS` and
# `forecast.TOO_FEW_CALCULATION_WEEKS`).
FEWER_THAN_12_VALID_WEEKS = "fewer_than_12_valid_weeks"
ACTIVE_WARNING = "active_warning"
SHORT_HISTORY = "short_history"
FEWER_THAN_100_VALID_WEEKS = "fewer_than_100_valid_weeks"
ALL_CLEAR = "all_clear"

# R-15, R-16: the thresholds. The rules fix these numbers, so they are not company
# settings and not in settings.py (AD-9).
RECENT_WEEKS = 12
OLD_DATA_WEEKS = 8
LOW_VALID_WEEKS = 12
HIGH_HISTORY_WEEKS = 104
HIGH_VALID_WEEKS = 100


def recent_positions(history_length):
    """The positions of the recent period, oldest first: the last 12 weeks of the history,
    or all of them when it is shorter (R-15)."""
    return range(max(1, history_length - RECENT_WEEKS + 1), history_length + 1)


def recent_only(positions, history_length):
    """The positions that fall in the recent period. Earlier ones are not active warnings."""
    recent = recent_positions(history_length)
    return tuple(position for position in positions if position in recent)


def weeks_since_latest_valid(valid_weeks, history_length):
    """How many weeks the latest valid week lies before the latest data week, by position
    (FR-18), or None when the product has no valid week."""
    return history_length - valid_weeks[-1] if valid_weeks else None


def active_warnings(
    recent_stockout_weeks,
    recent_unusual_weeks,
    recent_level_shift_weeks,
    since_latest_valid,
    has_forecast,
):
    """The active warnings in R-15 order, each counted by R-16.

    Old data is more than 8 weeks since the latest valid week, so 9 gives it and 8 does not
    (E12). A product with no valid week has no latest valid week and no old-data warning.
    Insufficient data is active whenever there is no forecast. Unusual weeks count whether
    the setting includes them or not (FR-16).
    """
    return tuple(
        warning
        for warning, active in (
            (STOCKOUT_WEEKS, bool(recent_stockout_weeks)),
            (UNUSUAL_WEEKS, bool(recent_unusual_weeks)),
            (LEVEL_SHIFT, bool(recent_level_shift_weeks)),
            (
                OLD_DATA,
                since_latest_valid is not None and since_latest_valid > OLD_DATA_WEEKS,
            ),
            (INSUFFICIENT_DATA, not has_forecast),
        )
        if active
    )


def confidence(no_forecast_reason, valid_count, history_length, warnings):
    """The confidence label and the condition that decided it, the first of R-16 that applies.

    1. No forecast, or fewer than 12 valid weeks: lav. 2. An active warning, a sales history
    shorter than 104 weeks (stockout weeks counted) or fewer than 100 valid weeks: middels.
    3. Otherwise høy. A product without a forecast has the reason for it as its condition.
    """
    if no_forecast_reason is not None:
        return LAV, no_forecast_reason
    if valid_count < LOW_VALID_WEEKS:
        return LAV, FEWER_THAN_12_VALID_WEEKS
    if warnings:
        return MIDDELS, ACTIVE_WARNING
    if history_length < HIGH_HISTORY_WEEKS:
        return MIDDELS, SHORT_HISTORY
    if valid_count < HIGH_VALID_WEEKS:
        return MIDDELS, FEWER_THAN_100_VALID_WEEKS
    return HOY, ALL_CLEAR
