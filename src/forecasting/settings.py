"""The FR-20 defaults and ranges, defined once (AD-9).

The model defaults, `load_seed` and, later, the settings form and the rules
read these values and keep no copy. Only the standard library is imported (AD-1).
"""

from dataclasses import dataclass
from decimal import Decimal

MOVING_AVERAGE = "moving_average"
EXPONENTIAL_SMOOTHING = "exponential_smoothing"
METHODS = (MOVING_AVERAGE, EXPONENTIAL_SMOOTHING)
DEFAULT_METHOD = MOVING_AVERAGE

DEFAULT_UNUSUAL_WEEKS_INCLUDED = True
DEFAULT_SEASONAL_ADJUSTMENT = False


@dataclass(frozen=True)
class Range:
    """A number setting with its default and its allowed values, both ends included."""

    default: int | Decimal
    minimum: int | Decimal
    maximum: int | Decimal


# Whole numbers, in weeks.
WINDOW = Range(default=3, minimum=2, maximum=12)
# One decimal.
SMOOTHING_FACTOR = Range(
    default=Decimal("0.3"), minimum=Decimal("0.1"), maximum=Decimal("0.9")
)
# Whole numbers, in percent.
SCENARIO_PERCENTAGE = Range(default=10, minimum=0, maximum=50)
SAFETY_MARGIN = Range(default=10, minimum=0, maximum=100)


@dataclass(frozen=True)
class ForecastSettings:
    """The settings that the base forecast reads (FR-20), with the defaults above.

    The smoothing factor may be a `Decimal`, as the model stores it; the core converts it.
    """

    method: str = DEFAULT_METHOD
    window: int = WINDOW.default
    smoothing_factor: Decimal | float = SMOOTHING_FACTOR.default
    unusual_weeks_included: bool = DEFAULT_UNUSUAL_WEEKS_INCLUDED
