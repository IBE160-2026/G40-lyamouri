"""Valid weeks, unusual weeks and level shifts (Story 2.1; FR-15, FR-16, FR-17, R-1, R-10, R-11).

The expected valid weeks, unusual weeks and level-shift weeks are read from the
reference spreadsheet for every case and rule test product that states them, so
no expected value is copied into the tests (AD-17). They use no database.
"""

import ast
from pathlib import Path

import answer_key_reader as reader
import pytest

from forecasting import weeks as core

# The examples that Story 2.1 must check, as the spreadsheet names them (PRD §5.7).
LISTED_EXAMPLES = {
    "E7",
    "E8",
    "E9",
    "E10",
    "E15",
    "E16",
    "E18 a",
    "E18 b",
    "E19",
}
STATED = ("valid_weeks", "unusual_weeks", "level_shift_weeks")
CASES = [row for row in reader.cases() if any(column in row for column in STATED)]
PRODUCTS = [row for row in reader.products() if "unusual_weeks" in row]


def core_weeks(sales):
    return [core.Week(week.units_sold, week.stockout) for week in sales]


def classify(sales):
    return core.classify_weeks(core_weeks(sales))


def assert_stated_values_match(row):
    """Compare every classification value that the row states, and only those.
    The valid weeks are also compared by position: R-1 makes every week that is
    not a stockout week valid, and the spreadsheet states only their number."""
    result = classify(row["sales"])
    assert result.valid == tuple(
        position for position, week in enumerate(row["sales"], 1) if not week.stockout
    )
    if "valid_weeks" in row:
        assert len(result.valid) == row["valid_weeks"]
    if "unusual_weeks" in row:
        assert list(result.unusual) == row["unusual_weeks"]
    if "level_shift_weeks" in row:
        assert list(result.level_shift) == row["level_shift_weeks"]


def history(*units):
    """A history of valid weeks, or of stockout weeks for a unit written as «S»."""
    return [
        core.Week(0, True) if unit == "S" else core.Week(unit, False) for unit in units
    ]


@pytest.mark.parametrize("row", CASES, ids=lambda row: row["case"])
def test_every_case_that_states_its_weeks_matches_the_spreadsheet(row):
    """FR-15, FR-16, FR-17, R-1, R-10, R-11: the valid weeks, unusual weeks and
    level-shift weeks of the case match what the reference spreadsheet states
    for it (the case name in the test id gives its E-n)."""
    assert_stated_values_match(row)


@pytest.mark.parametrize("row", PRODUCTS, ids=lambda row: row["product"])
def test_every_rule_test_product_matches_the_spreadsheet(row):
    """FR-3, FR-16, FR-17, R-10, R-11: the unusual weeks and level-shift weeks of
    each rule test product match what the reference spreadsheet states for it."""
    assert_stated_values_match(row)


def test_the_listed_examples_are_all_checked():
    """FR-15, FR-16, FR-17, SM-1: E7, E8, E9, E10, E15, E16, E18 a and b and E19
    each state at least one value that the classification is compared with, in
    every variant, so a renamed or emptied row cannot make the tests pass."""
    checked = {row["example"] for row in CASES}
    assert LISTED_EXAMPLES <= checked
    variants = {row["case"] for row in CASES if row["example"] in LISTED_EXAMPLES}
    expected = {
        row["case"] for row in reader.cases() if row["example"] in LISTED_EXAMPLES
    }
    assert variants == expected
    assert len(PRODUCTS) == len(reader.products())


def test_stockout_weeks_are_not_valid_weeks_and_never_flagged():
    """FR-15, R-1, E7: every week that is not a stockout week is valid, in time
    order, and no stockout week is ever unusual or in a level shift."""
    case = next(row for row in reader.cases() if row["case"] == "E7")
    result = classify(case["sales"])
    stockouts = {p for p, week in enumerate(case["sales"], 1) if week.stockout}
    assert stockouts
    assert result.valid == tuple(
        p for p in range(1, len(case["sales"]) + 1) if p not in stockouts
    )
    assert result.valid == (1, 2, 5, 6)
    assert result.unusual == () and result.level_shift == ()


def test_the_units_of_a_stockout_week_are_never_used():
    """FR-15, R-1, E7, E16: giving every stockout week of every case no sales or
    a huge number of sales changes nothing, in the baseline or in a run."""
    for row in reader.cases():
        weeks = core_weeks(row["sales"])
        for units in (0, 10_000):
            changed = [
                core.Week(units, True) if week.stockout else week for week in weeks
            ]
            assert core.classify_weeks(changed) == core.classify_weeks(weeks), row[
                "case"
            ]


def test_a_history_without_valid_weeks_has_nothing_to_classify():
    """FR-15, R-1: an empty history and a history of stockout weeks only give
    three empty results."""
    empty = core.WeekClassification(valid=(), unusual=(), level_shift=())
    assert core.classify_weeks([]) == empty
    assert core.classify_weeks(history("S", "S", "S", "S")) == empty


def test_a_run_of_unusual_weeks_is_broken_by_a_week_that_is_not_unusual():
    """FR-17, R-11: as in E8, one or two unusual weeks stay unusual weeks. Here
    unusual, normal, unusual, unusual is not a level shift,
    because the three unusual weeks are not in a row among the valid weeks."""
    result = core.classify_weeks(history(20, 22, 21, 60, 21, 60, 60))
    assert result.unusual == (4, 6, 7)
    assert result.level_shift == ()


def test_the_same_run_with_a_stockout_inside_is_still_a_level_shift():
    """FR-17, R-11: as in E9 and E16, the run counts valid weeks only, so a
    stockout week between the unusual weeks does not break it."""
    result = core.classify_weeks(history(20, 22, 21, 60, "S", 60, "S", 60))
    assert result.level_shift == (4, 6, 8)
    assert result.unusual == ()


def test_a_fourth_high_week_after_a_level_shift_is_checked_against_the_new_level():
    """FR-17, R-10, R-11: as in E15, the weeks of a level shift stay in the baseline,
    so a fourth high week at the new level is normal and a spike above it is unusual."""
    normal = core.classify_weeks(history(20, 22, 21, 60, 60, 60, 61))
    spike = core.classify_weeks(history(20, 22, 21, 60, 60, 60, 130))
    assert normal.level_shift == (4, 5, 6) and normal.unusual == ()
    assert spike.level_shift == (4, 5, 6) and spike.unusual == (7,)


def test_the_baseline_uses_the_three_most_recent_earlier_weeks_only():
    """R-10: as in E18 a and E18 b, old weeks do not count, and the comparison is exact:
    twice the baseline is not unusual and one more unit is."""
    assert core.classify_weeks(history(100, 100, 100, 10, 10, 10, 20)).unusual == ()
    assert core.classify_weeks(history(100, 100, 100, 10, 10, 10, 21)).unusual == (7,)
    # The smallest baseline above 0 works the same way: 2 is not unusual, 3 is.
    assert core.classify_weeks(history(1, 1, 1, 2)).unusual == ()
    assert core.classify_weeks(history(1, 1, 1, 3)).unusual == (4,)


def test_a_baseline_of_zero_never_gives_an_unusual_week():
    """FR-16, R-10, E10: with a median of 0, whether all three weeks are 0 or
    two of them are, any sales are normal."""
    assert core.classify_weeks(history(0, 0, 0, 5, 50)).unusual == ()
    assert core.classify_weeks(history(0, 9, 0, 5)).unusual == ()


def test_a_week_with_fewer_than_three_earlier_valid_weeks_is_not_checked():
    """FR-16, R-10, E19: weeks 1 to 3 are never flagged, even far above the weeks
    before them, and stockout weeks in front do not count as earlier weeks. They
    still enter later baselines, so week 4 is compared with them."""
    assert core.classify_weeks(history(20, 22, 60, 21)).unusual == ()
    assert core.classify_weeks(history(20, "S", 60, 22, 21)).unusual == ()
    assert core.classify_weeks(history(20, 60, 60, 60)).level_shift == ()
    assert core.classify_weeks(history(20, 60, 60, 60, 60)).unusual == ()
    assert core.classify_weeks(history(20, 22, 60, 130)).unusual == (4,)


def test_a_second_level_shift_follows_the_first_at_the_new_level():
    """FR-17, R-11, E15: three weeks above 2 × the new level are a second level
    shift, and the first one stays."""
    result = core.classify_weeks(history(20, 22, 21, 60, 60, 60, 130, 130, 130))
    assert result.level_shift == (4, 5, 6, 7, 8, 9)
    assert result.unusual == ()


def test_low_sales_are_never_flagged():
    """FR-16, R-10: only high sales are flagged, however far below the baseline."""
    assert core.classify_weeks(history(20, 22, 21, 0)).unusual == ()


def test_the_classification_does_not_change_its_input_and_takes_any_iterable():
    """AD-1: the history is read, never changed, and a tuple or a generator works
    as well as a list."""
    weeks = history(20, 22, 21, 60, 60, 60)
    before = list(weeks)
    expected = core.classify_weeks(weeks)
    assert weeks == before
    assert core.classify_weeks(tuple(weeks)) == expected
    assert core.classify_weeks(week for week in weeks) == expected


def test_the_module_imports_only_what_it_needs_and_reads_no_calendar():
    """AD-1, AD-8: the classification works on positions, so the module imports
    no clock, calendar or file module, only dataclasses, statistics and typing.
    tests/test_core_imports.py allows every standard-library module, so this test
    is the one that keeps the clock out."""
    source = Path(core.__file__).read_text(encoding="utf-8")
    imported = {
        node.module
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.ImportFrom)
    } | {
        alias.name
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert imported <= {"dataclasses", "statistics", "typing"}
