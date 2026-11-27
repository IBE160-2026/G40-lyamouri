"""The wording of the decision panel «Hva bør du bestille?» (AD-4; FR-8, FR-11, UX-DR22).

The texts follow the EXPERIENCE.md Message Catalogue word for word. The quantity is
written through `forecasting/display.py` (AD-3) and the week of the suggestion comes from
the latest data week through `forecasting/horizon.py`. Only the standard library and
`forecasting/` are imported (AD-1).
"""

from typing import NamedTuple

from forecasting import display
from forecasting.horizon import horizon_weeks

NO_QUANTITY = "Ingen foreslått bestillingsmengde"
NO_DECISION = "Prognose foreslår ingen mengde for dette produktet. Du bestemmer bestillingen selv."


class DecisionTexts(NamedTuple):
    """What the decision panel shows: the quantity, the line beside it and, without a
    forecast, the sentence below it (None with a forecast)."""

    quantity: str
    caption: str
    note: str | None


def decision_texts(result, iso_year, iso_week):
    """The texts of the decision panel for a product whose company has its latest data
    week in the given ISO year and week. Without a forecast the ISO week is not used, so
    a product without any sales week needs none."""
    if result.suggested_order_quantity is None:
        return DecisionTexts(display.MISSING, NO_QUANTITY, NO_DECISION)
    week = display.week_label(*horizon_weeks(iso_year, iso_week)[0])
    return DecisionTexts(
        display.suggested_quantity(result.suggested_order_quantity),
        f"Foreslått bestillingsmengde for neste uke, {week}",
        None,
    )
