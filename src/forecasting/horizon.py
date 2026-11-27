"""The weeks of the forecast horizon (R-5, FR-7; AD-8).

Week 1 is the ISO week after the latest data week, and weeks 2 and 3 follow it. This is
the only calendar arithmetic in the core: every other order and distance uses positions
in the sales history. The function reads no clock, so the same latest data week always
gives the same labels. Only the standard library is imported (AD-1).
"""

from datetime import date, timedelta

# R-5: the number of weeks that the forecast shows.
HORIZON_WEEKS = 3


def horizon_weeks(iso_year, iso_week):
    """The ISO year and week of horizon weeks 1 to 3 after the latest data week.

    A year with 53 ISO weeks has a week 53 before the new year (2026 has one), and the
    first days of January can belong to the last ISO week of the previous year, so the year
    of each horizon week is read from its own date and not taken from the start year. A
    week that does not exist, such as week 53 of 2025, or one so late that the calendar ends
    before the horizon does, is a ValueError that names the year and week.
    """
    for value in (iso_year, iso_week):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"not an ISO year and week: {iso_year!r}, {iso_week!r}")
    try:
        monday = date.fromisocalendar(iso_year, iso_week, 1)
        weeks = []
        for step in range(1, HORIZON_WEEKS + 1):
            following = (monday + timedelta(weeks=step)).isocalendar()
            weeks.append((following.year, following.week))
    except (ValueError, OverflowError):
        raise ValueError(
            f"no horizon after ISO year {iso_year!r}, week {iso_week!r}"
        ) from None
    return tuple(weeks)
