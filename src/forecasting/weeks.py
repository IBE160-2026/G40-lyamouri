"""Valid weeks, unusual weeks and level shifts (R-1, R-10, R-11; FR-15, FR-16, FR-17).

The rules work on positions in the sales history, from 1 for the oldest week (AD-8),
and on whole units, so the comparison with 2 × the baseline is exact. They do not read
the setting that includes or excludes unusual weeks; the calculation weeks (R-2) do.
Only the standard library is imported (AD-1).
"""

from dataclasses import dataclass
from statistics import median
from typing import NamedTuple

# R-10: the baseline is the median of this many earlier valid weeks, and a week is
# unusual when its sales are more than this factor times the baseline. The rules fix
# these numbers, so they are not company settings and not in settings.py (AD-9).
BASELINE_WEEKS = 3
OUTLIER_FACTOR = 2
# R-11: this many unusual valid weeks in a row, the last one included, are a level shift.
LEVEL_SHIFT_WEEKS = 3


class Week(NamedTuple):
    """One week of a product's sales history. The units of a stockout week are never used (R-1)."""

    units_sold: int
    stockout: bool


@dataclass(frozen=True)
class WeekClassification:
    """The positions of the valid weeks, the unusual weeks and the level-shift weeks, oldest first."""

    valid: tuple[int, ...]
    unusual: tuple[int, ...]
    level_shift: tuple[int, ...]


def classify_weeks(weeks):
    """Classify a sales history, oldest week first, in one forward pass over the valid weeks.

    Valid weeks are all weeks but the stockout weeks (R-1). A valid week is unusual when
    its sales are more than 2 × the baseline, the median of the 3 most recent earlier
    valid weeks that are not unusual weeks, level-shift weeks included. A week with fewer
    than 3 such weeks is not checked, a baseline of 0 never gives an unusual week, and only
    high sales are flagged (R-10). When a week becomes unusual and the two valid weeks
    before it are unusual too, the three become level-shift weeks at once (R-11).
    The weeks are read once and never changed, so any iterable of weeks works.
    """
    weeks = tuple(weeks)
    valid = []
    unusual = set()
    level_shift = set()
    for position, week in enumerate(weeks, start=1):
        if week.stockout:
            continue
        earlier = [
            weeks[earlier_position - 1].units_sold
            for earlier_position in valid
            if earlier_position not in unusual
        ][-BASELINE_WEEKS:]
        if len(earlier) == BASELINE_WEEKS:
            baseline = median(earlier)
            if baseline > 0 and week.units_sold > OUTLIER_FACTOR * baseline:
                run = [*valid[-(LEVEL_SHIFT_WEEKS - 1) :], position]
                # A flagged week has at least 3 earlier valid weeks, so the run is complete.
                if unusual.issuperset(run[:-1]):
                    unusual.difference_update(run)
                    level_shift.update(run)
                else:
                    unusual.add(position)
        valid.append(position)
    return WeekClassification(
        valid=tuple(valid),
        unusual=tuple(sorted(unusual)),
        level_shift=tuple(sorted(level_shift)),
    )
