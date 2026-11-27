"""The template filters for domain numbers (Story 2.3; AD-3, NFR-5)."""

import re
from pathlib import Path

import pytest
from django.template import engines

from forecasting import display

TEMPLATES = Path(__file__).resolve().parents[1] / "src" / "web" / "templates"


def render(source, **context):
    return engines["django"].from_string("{% load prognose %}" + source).render(context)


@pytest.mark.parametrize(
    ("name", "function"),
    [
        ("one_decimal", display.one_decimal),
        ("two_decimals", display.two_decimals),
        ("whole_number", display.whole_number),
        ("percent", display.percent),
    ],
)
@pytest.mark.parametrize("value", [14.333333333333334, 10.25, -0.25, 0, 70, 1234567.5])
def test_each_filter_gives_what_display_gives(name, function, value):
    """AD-3, NFR-5: a template filter is `forecasting/display.py` and nothing of its
    own, for a float, an integer and a negative number, and Django adds no grouping."""
    assert render("{{ value|" + name + " }}", value=value) == function(value)


def test_a_filter_output_is_not_changed_by_the_template_engine():
    """NFR-5: the minus sign U+2212 and the no-break space before «%» reach the page
    as they are, and are not turned into entities or a hyphen."""
    assert render("{{ a|two_decimals }} {{ b|percent }}", a=-40, b=10) == (
        "−40,00 10 %"
    )


@pytest.mark.parametrize(
    ("name", "value", "error"),
    [
        (name, value, error)
        for name in ("one_decimal", "two_decimals", "whole_number", "percent")
        for value, error in [
            (None, TypeError),
            ("", TypeError),
            ("70", TypeError),
            (True, TypeError),
            (float("nan"), ValueError),
            (float("inf"), ValueError),
        ]
    ],
)
def test_a_filter_refuses_what_is_not_a_number(name, value, error):
    """AD-3: a missing value, a string, a bool, NaN or infinity fails in the
    template with the error of the rounding, instead of printing wrongly."""
    with pytest.raises(error, match="cannot round"):
        render("{{ value|" + name + " }}", value=value)


def test_the_product_list_writes_every_number_through_a_filter():
    """AD-3, FR-2, FR-24: the stock, the week-1 forecast, the quantity and the weeks of
    cover of the product list are printed by the filters of `forecasting/display.py`, so
    no list prints a raw number. An integer prints the same either way, so the template
    source is what the test reads."""
    source = (TEMPLATES / "web" / "_product_list.html").read_text(encoding="utf-8")

    assert "{% load prognose %}" in source
    for value, name in [
        ("item.product.stock_on_hand", "whole_number"),
        ("item.result.week_forecasts.0", "one_decimal"),
        ("item.result.suggested_order_quantity", "suggested_quantity"),
        ("item.result.weeks_of_cover", "weeks_of_cover"),
    ]:
        assert re.search(rf"\{{\{{\s*{re.escape(value)}\|{name}\s*\}}\}}", source), (
            value
        )
        assert not re.search(rf"\{{\{{\s*{re.escape(value)}\s*\}}\}}", source), value


@pytest.mark.parametrize(
    ("name", "function"),
    [
        ("weeks_of_cover", display.weeks_of_cover),
        ("suggested_quantity", display.suggested_quantity),
    ],
)
@pytest.mark.parametrize("value", [None, 0, 0.349, 11, 14.333333333333334])
def test_the_missing_value_filters_give_what_display_gives(name, function, value):
    """AD-3, FR-24, E23: the filters of the product screen are `forecasting/display.py`,
    and a missing value reaches the page as «–»."""
    assert render("{{ value|" + name + " }}", value=value) == function(value)
    assert render("{{ value|" + name + " }}", value=None) == "–"
