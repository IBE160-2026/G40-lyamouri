"""Rounding (R-8, R-9; AD-3).

Every rounding in the app goes through this module. A value is first rounded to 6
decimals, so that a computer result such as 70.00000000000001 is 70 and not 71 (E5),
and then either up to whole units (R-8) or half away from zero for display (R-9). The
rounding uses `decimal` on the exact value of the float, never `round()`, which rounds
half to even (10.25 to 10.2). Only the standard library is imported (AD-1).
"""

from decimal import ROUND_CEILING, ROUND_HALF_UP, Decimal, InvalidOperation

# R-9: the first rounding, before the round-up or the display rounding.
INTERMEDIATE_DECIMALS = 6
# R-9: the most decimals that a display rounding can give.
MAXIMUM_DISPLAY_DECIMALS = INTERMEDIATE_DECIMALS


def _unit_of(decimals):
    return Decimal(1).scaleb(-decimals)


def _to_intermediate(value):
    """The value rounded to 6 decimals, half away from zero (ROUND_HALF_UP in `decimal`).

    Only an int, a float or a `Decimal` is a number: anything else, such as `None` or a
    string, is a `TypeError`, and a value that is not finite or too large for `decimal`
    is a `ValueError`, so a bad value fails the same way wherever it comes from.
    """
    if isinstance(value, bool) or not isinstance(value, int | float | Decimal):
        raise TypeError(f"cannot round {value!r}")
    number = Decimal(value)
    if not number.is_finite():
        raise ValueError(f"cannot round {value!r}")
    try:
        return number.quantize(_unit_of(INTERMEDIATE_DECIMALS), rounding=ROUND_HALF_UP)
    except InvalidOperation:
        raise ValueError(f"cannot round {value!r}") from None


def round_up_to_units(value):
    """The value rounded to 6 decimals and then up to a whole number of units (R-8, R-9)."""
    return int(_to_intermediate(value).to_integral_value(rounding=ROUND_CEILING))


def round_for_display(value, decimals):
    """The value rounded to 6 decimals and then half away from zero to `decimals` (R-9).

    A value that rounds to zero is a plain zero, never «−0».
    """
    if not 0 <= decimals <= MAXIMUM_DISPLAY_DECIMALS:
        raise ValueError(f"display decimals must be 0 to {MAXIMUM_DISPLAY_DECIMALS}")
    rounded = _to_intermediate(value).quantize(
        _unit_of(decimals), rounding=ROUND_HALF_UP
    )
    return abs(rounded) if rounded.is_zero() else rounded
