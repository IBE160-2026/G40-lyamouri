"""The week label of the app header (Story 1.8; AD-3, UX-DR14)."""

from forecasting import display


def test_header_week_label_has_the_week_and_the_year():
    """AD-3, UX-DR14: the header shows the latest data week as «uke 45, 2026»,
    and the first week of a new year keeps its year."""
    assert display.header_week_label(2026, 45) == "uke 45, 2026"
    assert display.header_week_label(2027, 1) == "uke 1, 2027"
