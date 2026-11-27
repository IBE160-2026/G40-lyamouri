"""The wording of the decision panel (Story 2.7; FR-8, FR-11, UX-DR22, AD-3, AD-4).

The quantities and the stocks are read from the reference spreadsheet (AD-17). They use
no database.
"""

import answer_key_reader as reader
import pytest

from explanation import decision
from forecasting import display
from forecasting import forecast as core
from forecasting.settings import ForecastSettings
from forecasting.weeks import Week


def case(name):
    return next(row for row in reader.cases() if row["case"] == name)


def result_of(row):
    return core.forecast_product(
        [Week(w.units_sold, w.stockout) for w in row["sales"]],
        row["stock_on_hand"],
        ForecastSettings(),
    )


def test_a_forecast_gives_the_quantity_and_the_week_of_the_suggestion():
    """FR-11, UX-DR22, E4: the quantity of the spreadsheet and the caption with the week
    after the latest data week, and no sentence below."""
    row = case("E4")
    texts = decision.decision_texts(result_of(row), 2026, 45)

    assert texts.quantity == str(row["suggested_order_quantity"])
    assert texts.caption == "Foreslått bestillingsmengde for neste uke, uke 46"
    assert texts.note is None


def test_an_order_of_zero_is_a_quantity_and_not_a_missing_value():
    """FR-11, E6: 0 is written as «0», with the same caption as any forecast."""
    row = case("E6")
    texts = decision.decision_texts(result_of(row), 2026, 45)

    assert row["suggested_order_quantity"] == 0
    assert texts.quantity == "0"
    assert texts.caption.startswith("Foreslått bestillingsmengde for neste uke")


def test_without_a_forecast_the_panel_says_that_the_user_decides():
    """FR-8, UX-DR22, E11 a: «–», «Ingen foreslått bestillingsmengde» and the sentence of
    the Message Catalogue, word for word. No week is needed."""
    row = case("E11 a")
    texts = decision.decision_texts(result_of(row), None, None)

    assert texts == (
        "–",
        "Ingen foreslått bestillingsmengde",
        (
            "Prognose foreslår ingen mengde for dette produktet. "
            "Du bestemmer bestillingen selv."
        ),
    )
    assert texts.quantity == display.MISSING


@pytest.mark.parametrize(
    ("year", "week", "label"),
    [(2026, 52, "uke 53"), (2026, 53, "uke 1/2027"), (2027, 52, "uke 1/2028")],
)
def test_the_week_of_the_suggestion_follows_the_iso_calendar(year, week, label):
    """R-5, UX-DR42: week 53 of 2026 exists and is followed by week 1 of 2027, which
    carries its year; 2027 has 52 weeks."""
    texts = decision.decision_texts(result_of(case("E4")), year, week)

    assert texts.caption == f"Foreslått bestillingsmengde for neste uke, {label}"


def test_a_forecast_needs_the_latest_data_week():
    """FR-11: a forecast without the week is a TypeError from the horizon, so the
    caption is never written with a wrong week."""
    with pytest.raises(TypeError):
        decision.decision_texts(result_of(case("E4")), None, None)
