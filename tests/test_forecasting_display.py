"""The week label of the app header (Story 1.8) and the number formats and week labels (Story 2.3; AD-3, NFR-5, UX-DR14, UX-DR42)."""

from decimal import Decimal

import pytest

from forecasting import display


def test_header_week_label_has_the_week_and_the_year():
    """AD-3, UX-DR14: the header shows the latest data week as «uke 45, 2026»,
    and the first week of a new year keeps its year."""
    assert display.header_week_label(2026, 45) == "uke 45, 2026"
    assert display.header_week_label(2027, 1) == "uke 1, 2027"


@pytest.mark.parametrize(
    ("function", "value", "expected"),
    [
        (display.one_decimal, 14.333333333333334, "14,3"),
        (display.one_decimal, 10.25, "10,3"),
        (display.one_decimal, 10.249999999999998, "10,3"),
        (display.one_decimal, 0.0, "0,0"),
        (display.one_decimal, -0.04, "0,0"),
        (display.one_decimal, -0.25, "−0,3"),
        (display.one_decimal, 1234.5, "1234,5"),
        (display.two_decimals, 0.0667, "0,07"),
        (display.two_decimals, -40, "−40,00"),
        (display.two_decimals, 1234567.891, "1234567,89"),
        (display.whole_number, 70, "70"),
        (display.whole_number, 70.5, "71"),
        (display.whole_number, 1234567, "1234567"),
        (display.whole_number, -3, "−3"),
        (display.percent, 10, "10 %"),
        (display.percent, 12.5, "13 %"),
        (display.percent, 0, "0 %"),
        (display.format_number, 0.12346, "0,123"),
    ],
)
def test_numbers_have_a_decimal_comma_the_minus_sign_and_no_grouping(
    function, value, expected
):
    """NFR-5, AD-3, UX-DR42, E20, E21: a decimal comma, the minus sign U+2212, no
    thousands grouping, and a no-break space before «%»."""
    if function is display.format_number:
        assert function(value, 3) == expected
    else:
        assert function(value) == expected


def test_a_number_never_has_a_point_a_hyphen_or_an_ordinary_space():
    """NFR-5, AD-3: the characters that the formats rule out, over a range of values,
    and the characters that they require: U+2212 for a negative number and U+00A0
    before «%»."""
    for value in (-1234.5, -0.5, -0.04, 0, 0.5, 1234.5, 1e6, 1e15, 12345678.9):
        for text in (
            display.one_decimal(value),
            display.two_decimals(value),
            display.whole_number(value),
            display.percent(value),
        ):
            assert "." not in text
            assert "-" not in text
            assert " " not in text
            assert "e" not in text.lower()
    assert display.one_decimal(-0.5).startswith("\u2212")
    assert display.percent(-12).startswith("\u2212")
    assert display.percent(5).endswith("\u00a0%")
    assert display.one_decimal(-0.04) == "0,0"


@pytest.mark.parametrize(
    ("year", "week", "with_year", "label", "axis"),
    [
        (2026, 46, False, "uke 46", "46"),
        (2026, 46, True, "uke 46/2026", "46"),
        (2025, 10, True, "uke 10/2025", "10"),
        (2027, 1, False, "uke 1/2027", "1/2027"),
        (2027, 1, True, "uke 1/2027", "1/2027"),
        (2026, 53, False, "uke 53", "53"),
        (2026, 2, False, "uke 2", "2"),
    ],
)
def test_week_labels_use_the_iso_week_and_the_year_at_new_year(
    year, week, with_year, label, axis
):
    """AD-3, UX-DR42: «uke 46», the year in a list that reaches before the recent
    period, and the year on week 1 in lists and on chart axes («1/2027»)."""
    assert display.week_label(year, week, with_year) == label
    assert display.axis_week_label(year, week) == axis


@pytest.mark.parametrize(
    ("function", "value", "expected"),
    [
        (display.weeks_of_cover, 0.349, "0,3"),
        (display.weeks_of_cover, 0.0, "0,0"),
        (display.weeks_of_cover, 1.5, "1,5"),
        (display.weeks_of_cover, None, "–"),
        (display.suggested_quantity, 11, "11"),
        (display.suggested_quantity, 0, "0"),
        (display.suggested_quantity, None, "–"),
    ],
)
def test_a_missing_value_is_the_en_dash_and_zero_is_a_number(function, value, expected):
    """FR-8, FR-24, E23, UX-DR42: «–» (U+2013) stands for a value that a product does not
    have, and 0 is written as 0, never as «–»."""
    assert function(value) == expected
    assert display.MISSING == "–"


@pytest.mark.parametrize(
    "function", [display.weeks_of_cover, display.suggested_quantity]
)
@pytest.mark.parametrize(
    ("value", "error"),
    [
        ("", TypeError),
        ("11", TypeError),
        (False, TypeError),
        (float("nan"), ValueError),
    ],
)
def test_a_missing_value_function_refuses_what_is_not_a_number(function, value, error):
    """AD-3: only None is missing; any other non-number fails as in the rounding, so a
    wrong value never prints as «–»."""
    with pytest.raises(error, match="cannot round"):
        function(value)


# The worksheet (Story 2.9; FR-7, FR-35, UX-DR42).


@pytest.mark.parametrize(
    ("number", "iso_year", "iso_week", "expected"),
    [
        (1, 2026, 46, "Uke 1 · uke 46"),
        (2, 2026, 47, "Uke 2 · uke 47"),
        (3, 2027, 1, "Uke 3 · uke 1/2027"),
    ],
)
def test_a_horizon_column_names_its_week_with_the_year_at_new_year(
    number, iso_year, iso_week, expected
):
    """UX-DR42: «Uke 1 · uke 46», with a middle dot (U+00B7) and the year on week 1."""
    assert display.horizon_column_label(number, iso_year, iso_week) == expected
    assert "·" in expected


@pytest.mark.parametrize(
    ("weeks", "with_year", "expected"),
    [
        ([(2026, 38)], False, "uke 38"),
        ([(2026, 38), (2026, 39)], False, "uke 38 og 39"),
        ([(2026, 43), (2026, 44), (2026, 45)], False, "uke 43, 44 og 45"),
        ([(2025, 10), (2025, 11)], True, "uke 10/2025 og 11/2025"),
        ([(2026, 53), (2027, 1)], False, "uke 53 og 1/2027"),
        ([(2026, 40)], True, "uke 40/2026"),
    ],
)
def test_a_list_of_weeks_is_one_phrase_with_the_year_decided_by_the_list(
    weeks, with_year, expected
):
    """UX-DR42, FR-15: «uke 38 og 39», the year on every week of a list that reaches before
    the recent period, and on the first week of a new year always."""
    assert display.week_list(weeks, with_year) == expected


@pytest.mark.parametrize(
    ("iso_year", "iso_week", "with_year", "expected"),
    [
        (2026, 46, False, "46"),
        (2026, 46, True, "46/2026"),
        (2027, 1, False, "1/2027"),
    ],
)
def test_a_week_in_a_table_has_no_word_and_the_year_only_when_asked(
    iso_year, iso_week, with_year, expected
):
    """UX-DR42: the cell of a table is «46», «46/2026» or «1/2027»."""
    assert display.week_item(iso_year, iso_week, with_year) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [(0.3, "0,3"), (1 - 0.3, "0,7"), (1 - 0.9, "0,1"), (Decimal("0.5"), "0,5")],
)
def test_a_smoothing_factor_and_its_complement_have_one_decimal(value, expected):
    """FR-6, R-9: 1 − 0.9 is 0,1, not 0,09999999999999998."""
    assert display.factor(value) == expected
