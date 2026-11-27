"""The wording of the product list (AD-4; FR-24, UX-DR16, UX-DR17, NFR-5).

The group headings, their summaries in singular and plural, the product count and the
empty state follow the EXPERIENCE.md Message Catalogue word for word. Counts and units
are written through `forecasting/display.py` (AD-3). Only the standard library and
`forecasting/` are imported (AD-1).
"""

from forecasting import display

ORDER_SOON = "order_soon"
WITHOUT_FORECAST = "without_forecast"
OTHERS = "others"

HEADINGS = {
    ORDER_SOON: "Bestill snart",
    WITHOUT_FORECAST: "Uten prognose",
    OTHERS: "Øvrige produkter",
}
# FR-24: what a company without products sees, with the exact load command of the README.
LOAD_COMMAND = "uv run python src/manage.py load_seed"
NO_DATA = f"Ingen data er lastet inn. Kjør {LOAD_COMMAND} som står i README."


def _products(count):
    """«1 produkt» or «4 produkter»."""
    return f"{display.whole_number(count)} {'produkt' if count == 1 else 'produkter'}"


def product_count(count):
    """The count beside the heading «Produktoversikt»: «30 produkter»."""
    return _products(count)


def group_summary(group, count, units=0):
    """The summary at the right of a group heading: «4 produkter · 31 enheter foreslått»,
    «1 produkt · du bestemmer selv» or «25 · etter varenummer». `units` is the sum of the
    suggested quantities, which only «Bestill snart» shows."""
    if group == ORDER_SOON:
        unit = "enhet" if units == 1 else "enheter"
        return f"{_products(count)} · {display.whole_number(units)} {unit} foreslått"
    if group == WITHOUT_FORECAST:
        return f"{_products(count)} · du bestemmer selv"
    if group == OTHERS:
        return f"{display.whole_number(count)} · etter varenummer"
    raise ValueError(f"no summary for the group {group!r}")
