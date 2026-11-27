"""The weeks of the forecast horizon (Story 2.4; R-5, FR-7, AD-8).

Only these labels use calendar arithmetic. The tests read no clock and use no database.
"""

import ast
from datetime import date
from pathlib import Path

import pytest

from forecasting import display
from forecasting.horizon import HORIZON_WEEKS, horizon_weeks

SOURCE = Path(__file__).resolve().parents[1] / "src" / "forecasting" / "horizon.py"


def iso_weeks(first_year, last_year):
    """Every ISO week of the years in order, from the rule that a year has 52 weeks, or 53
    when 28 December falls in week 53, and not from date arithmetic on the week itself."""
    return [
        (year, week)
        for year in range(first_year, last_year + 1)
        for week in range(1, date(year, 12, 28).isocalendar().week + 1)
    ]


@pytest.mark.parametrize(
    ("latest", "expected"),
    [
        ((2026, 45), ((2026, 46), (2026, 47), (2026, 48))),
        ((2026, 52), ((2026, 53), (2027, 1), (2027, 2))),
        ((2026, 53), ((2027, 1), (2027, 2), (2027, 3))),
        ((2025, 52), ((2026, 1), (2026, 2), (2026, 3))),
        ((2027, 1), ((2027, 2), (2027, 3), (2027, 4))),
    ],
)
def test_week_1_is_the_iso_week_after_the_latest_data_week(latest, expected):
    """AD-8, R-5, FR-7: week 1 follows the latest data week, and weeks 2 and 3 follow it,
    also over a year with 53 ISO weeks (2026) and over one with 52 (2025)."""
    assert horizon_weeks(*latest) == expected


def test_the_horizon_is_three_weeks_of_every_iso_week_in_a_run_of_years():
    """AD-8: for every ISO week from 2015 to 2035 the next three are the following ones in
    the sequence of the years."""
    weeks = iso_weeks(2015, 2035)
    assert len(weeks) == len(set(weeks))
    for index in range(len(weeks) - HORIZON_WEEKS):
        following = tuple(weeks[index + 1 : index + 1 + HORIZON_WEEKS])
        assert horizon_weeks(*weeks[index]) == following


def test_the_labels_of_the_horizon_carry_the_year_at_the_new_year():
    """AD-3, UX-DR42, AD-8: the horizon of 2026 week 52 is written «uke 53», «uke 1/2027»
    and «uke 2», through display.py: only week 1 carries its year in a list."""
    labels = [display.week_label(*week) for week in horizon_weeks(2026, 52)]
    assert labels == ["uke 53", "uke 1/2027", "uke 2"]
    axis = [display.axis_week_label(*week) for week in horizon_weeks(2026, 52)]
    assert axis == ["53", "1/2027", "2"]


@pytest.mark.parametrize(
    ("year", "week"),
    [(2025, 53), (2026, 54), (2026, 0), (0, 1), (10000, 1), (9999, 52)],
)
def test_a_week_that_does_not_exist_is_a_value_error_naming_it(year, week):
    """AD-8: 2025 has no week 53, no year or week outside the calendar is taken, and the
    end of the calendar (9999 week 52) is the same error and not an OverflowError."""
    with pytest.raises(ValueError, match=rf"year {year}, week {week}"):
        horizon_weeks(year, week)


@pytest.mark.parametrize(
    "bad", [(True, 5), (2026, True), ("2026", 5), (2026, "5"), (None, 5), (2026.0, 5)]
)
def test_a_year_or_week_that_is_not_a_whole_number_is_a_type_error(bad):
    """AD-8: a bool, a string, a float or nothing is not an ISO year or week."""
    with pytest.raises(TypeError, match="ISO year and week"):
        horizon_weeks(*bad)


def test_the_horizon_reads_no_clock():
    """AD-1, AD-8: no domain code reads today's date, so the module names no clock."""
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    names = {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)}
    names |= {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    assert not names & {"today", "now", "utcnow", "time", "monotonic", "localtime"}
