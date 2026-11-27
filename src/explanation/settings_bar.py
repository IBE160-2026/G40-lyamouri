"""The wording of the settings bar (AD-4; FR-20, FR-21, UX-DR15).

It shows the settings in use as the Message Catalogue and Innstillinger name them. The
numbers are written through `forecasting/display.py` (AD-3). Only the standard library
and `forecasting/` are imported (AD-1).
"""

from forecasting import display
from forecasting.settings import EXPONENTIAL_SMOOTHING, MOVING_AVERAGE

LABEL = "Innstillinger i bruk:"
SCOPE_NOTE = "Endringen gjelder alle produkter i bedriften."


def _method(settings):
    if settings.method == MOVING_AVERAGE:
        return f"Glidende gjennomsnitt, {display.whole_number(settings.window)} uker"
    if settings.method == EXPONENTIAL_SMOOTHING:
        return f"Eksponentiell glatting, faktor {display.one_decimal(settings.smoothing_factor)}"
    raise ValueError(f"no text for the method {settings.method!r}")


def settings_texts(settings):
    """The values of the settings bar, in its order: the method with its window or factor,
    the scenario percentage, the safety margin and the unusual weeks. Seasonal adjustment
    joins them with FR-9 (Epic 5)."""
    unusual = "tas med" if settings.unusual_weeks_included else "holdes utenfor"
    return (
        _method(settings),
        f"Scenarioprosent {display.percent(settings.scenario_percentage)}",
        f"Sikkerhetsmargin {display.percent(settings.safety_margin)}",
        f"Uvanlige uker: {unusual}",
    )
