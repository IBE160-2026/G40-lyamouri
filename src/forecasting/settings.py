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
