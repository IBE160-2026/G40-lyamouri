"""The wording of the warnings, the notes and the confidence label (AD-4; FR-7, FR-8, FR-15 to FR-19, UX-DR40).

Every text follows its row of the EXPERIENCE.md Message Catalogue word for word. The
numbers and the week numbers come from the `ProductResult` and are written through
`forecasting/display.py` (AD-3, AD-5); a week's ISO week comes from the latest data week
through `forecasting/horizon.py`. A level shift has its place in the reason only, because
its warning text is FR-17b (Should). Only the standard library and `forecasting/` are
imported (AD-1).
"""

from typing import NamedTuple

from forecasting import display, trust
from forecasting.forecast import (
    MINIMUM_VALID_WEEKS,
    TOO_FEW_CALCULATION_WEEKS,
    TOO_FEW_VALID_WEEKS,
)
from forecasting.horizon import week_at_position

LABEL_WORDS = {trust.LAV: "Lav", trust.MIDDELS: "Middels", trust.HOY: "Høy"}
FLAT_WEEKS_NOTE = (
    "Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar hensyn til trend "
    "eller sesong."
)


class WarningText(NamedTuple):
    """An active warning with the text that the product screen lists for it."""

    code: str
    text: str


def _number(value):
    return display.whole_number(value)


def _list(items):
    """«38», «38 og 39» or «38, 39 og 40»."""
    items = list(items)
    if len(items) < 2:
        return "".join(items)
    return f"{', '.join(items[:-1])} og {items[-1]}"


def _count(number, singular, plural):
    """«1 utsolgt uke» or «2 utsolgte uker»."""
    return f"{_number(number)} {singular if number == 1 else plural}"


def _sentence(phrase):
    return f"{phrase[0].upper()}{phrase[1:]}."


def _week_numbers(result, positions, iso_year, iso_week):
    """The week numbers of positions, the year only at New Year: «38 og 39», «52 og 1/2027»."""
    return _list(
        display.axis_week_label(
            *week_at_position(position, result.history_length, iso_year, iso_week)
        )
        for position in positions
    )


def _stockout_text(result, iso_year, iso_week):
    weeks = _week_numbers(result, result.recent_stockout_weeks, iso_year, iso_week)
    return f"Uke {weeks}: utsolgt, holdt utenfor beregningen."


def _unusual_text(result, iso_year, iso_week):
    weeks = _week_numbers(result, result.recent_unusual_weeks, iso_year, iso_week)
    units = _list(_number(units) for units in result.recent_unusual_units)
    used = (
        "tatt med i beregningen"
        if result.settings.unusual_weeks_included
        else "holdt utenfor beregningen"
    )
    return f"Uke {weeks}: uvanlig høyt salg ({units}), {used}."


def _old_data_text(result):
    weeks = _number(result.weeks_since_latest_valid)
    return (
        f"Det har gått {weeks} uker siden siste gyldige uke, så prognosen bygger på "
        "gamle data."
    )


def _insufficient_data_text(result):
    if result.no_forecast_reason == TOO_FEW_VALID_WEEKS:
        valid = _count(len(result.valid_weeks), "gyldig uke", "gyldige uker")
        return (
            f"Produktet har {valid}. Prognose regner ut en prognose når produktet har "
            f"minst {_number(MINIMUM_VALID_WEEKS)} gyldige uker."
        )
    if result.no_forecast_reason == TOO_FEW_CALCULATION_WEEKS:
        window = _number(result.settings.window)
        return (
            f"Glidende gjennomsnitt over {window} uker trenger {window} uker brukt i "
            f"beregningen. Produktet har {_number(len(result.calculation_weeks))}."
        )
    raise ValueError(f"no insufficient-data text for {result.no_forecast_reason!r}")


def warning_texts(result, iso_year, iso_week):
    """The text of each active warning, in R-15 order, for a product whose latest data week
    is the given ISO year and week. A level shift has none until FR-17b (Should); any other
    warning without a text is a KeyError, so a new warning is never left out silently."""
    texts = {
        trust.STOCKOUT_WEEKS: lambda: _stockout_text(result, iso_year, iso_week),
        trust.UNUSUAL_WEEKS: lambda: _unusual_text(result, iso_year, iso_week),
        trust.OLD_DATA: lambda: _old_data_text(result),
        trust.INSUFFICIENT_DATA: lambda: _insufficient_data_text(result),
    }
    return tuple(
        WarningText(warning, texts[warning]())
        for warning in result.warnings
        if warning != trust.LEVEL_SHIFT
    )


def list_text(result):
    """The text that a list shows for a product without a forecast, or None with one."""
    if result.no_forecast_reason == TOO_FEW_VALID_WEEKS:
        return f"Ingen prognose: færre enn {_number(MINIMUM_VALID_WEEKS)} gyldige uker"
    if result.no_forecast_reason == TOO_FEW_CALCULATION_WEEKS:
        return "Ingen prognose: færre uker enn vinduet"
    return None


def note_texts(result):
    """The text of each note of the product. Only the FR-7 note is built, so any other note
    is a KeyError and never left out silently."""
    texts = {trust.WEEKS_REPEAT_WEEK_1: FLAT_WEEKS_NOTE}
    return tuple(texts[note] for note in result.notes)


def _recent_phrase(result):
    """The recent-period warnings as one phrase, or None: «2 utsolgte uker og 1 uvanlig
    uke de siste 12 ukene»."""
    parts = []
    if result.recent_stockout_weeks:
        parts.append(
            _count(len(result.recent_stockout_weeks), "utsolgt uke", "utsolgte uker")
        )
    if result.recent_unusual_weeks:
        parts.append(
            _count(len(result.recent_unusual_weeks), "uvanlig uke", "uvanlige uker")
        )
    if result.recent_level_shift_weeks:
        parts.append("nytt nivå")
    if not parts:
        return None
    return f"{_list(parts)} de siste {_number(trust.RECENT_WEEKS)} ukene"


def _old_data_phrase(result):
    if trust.OLD_DATA not in result.warnings:
        return None
    return (
        f"gamle data, {_number(result.weeks_since_latest_valid)} uker siden siste "
        "gyldige uke"
    )


def _condition_phrase(result, warning_phrases):
    """The deciding condition of R-16 as a phrase."""
    condition = result.confidence_condition
    if condition == TOO_FEW_VALID_WEEKS:
        return f"ingen prognose, færre enn {_number(MINIMUM_VALID_WEEKS)} gyldige uker"
    if condition == TOO_FEW_CALCULATION_WEEKS:
        return "ingen prognose, færre uker enn vinduet"
    if condition == trust.FEWER_THAN_12_VALID_WEEKS:
        return f"færre enn {_number(trust.LOW_VALID_WEEKS)} gyldige uker"
    if condition == trust.ACTIVE_WARNING:
        return warning_phrases[0]
    if condition == trust.SHORT_HISTORY:
        return f"kortere salgshistorikk enn {_number(trust.HIGH_HISTORY_WEEKS)} uker"
    if condition == trust.FEWER_THAN_100_VALID_WEEKS:
        return f"færre enn {_number(trust.HIGH_VALID_WEEKS)} gyldige uker"
    if condition == trust.ALL_CLEAR:
        return (
            f"minst {_number(trust.HIGH_HISTORY_WEEKS)} uker salgshistorikk, minst "
            f"{_number(trust.HIGH_VALID_WEEKS)} gyldige uker og ingen varsler"
        )
    raise ValueError(f"no reason text for the condition {condition!r}")


def confidence_reason(result):
    """The reason for the label: «Middels: 2 utsolgte uker og 1 uvanlig uke de siste 12
    ukene.» It names the deciding condition, then each other active warning as a sentence.

    The warnings of the recent period are one phrase and old data is another. When an
    active warning decides, the first phrase is the condition. Insufficient data is named
    by the condition of a product without a forecast, so it is not repeated.
    """
    warning_phrases = [
        phrase
        for phrase in (_recent_phrase(result), _old_data_phrase(result))
        if phrase is not None
    ]
    label = LABEL_WORDS[result.confidence_label]
    sentences = [f"{label}: {_condition_phrase(result, warning_phrases)}."]
    others = (
        warning_phrases[1:]
        if result.confidence_condition == trust.ACTIVE_WARNING
        else warning_phrases
    )
    sentences.extend(_sentence(phrase) for phrase in others)
    return " ".join(sentences)
