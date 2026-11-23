"""Norwegian display text (AD-3). Story 2.3 adds the number formats and the other week labels."""


def header_week_label(iso_year, iso_week):
    """The latest data week as the app header shows it, with the year: «uke 45, 2026»."""
    return f"uke {iso_week}, {iso_year}"
