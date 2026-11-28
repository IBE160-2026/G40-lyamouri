"""The wording of the worksheet «Slik er tallene regnet ut» (AD-4; FR-7, FR-10, FR-12, FR-15, FR-16, FR-35, UX-DR28 to UX-DR30, UX-DR42).

The sentences follow the EXPERIENCE.md Message Catalogue word for word, and the lines of
the calculation use the exact FR-12 and FR-35 formats. Every number and every week label
is written through `forecasting/display.py` (AD-3), and a week's ISO week comes from the
latest data week through `forecasting/horizon.py`. The texts read the `ProductResult`
only. Only the standard library and `forecasting/` are imported (AD-1).
"""

from typing import NamedTuple

from explanation.trust import FLAT_WEEKS_NOTE
from forecasting import display, trust
from forecasting.horizon import horizon_weeks, week_at_position
from forecasting.settings import MOVING_AVERAGE

# UX-DR28: the sales table shows the recent period, which R-15 counts as 12 weeks.
SALES_ROWS = trust.RECENT_WEEKS
ROUNDING_NOTE = "Tallene er avrundet for visning."
SAFETY_MARGIN_NOTE = (
    "Sikkerhetsmarginen er en enkel tommelfingerregel. Leveringstid og varer som "
    "allerede er bestilt, er ikke tatt med."
)
SCENARIO_NOTE = (
    "Scenarioene viser hva som skjer hvis salget blir {percent} høyere eller lavere. "
    "De er ikke sannsynligheter."
)
NO_SALES_WEEKS = "Produktet har ingen salgsuker."
COVERED = " (lageret dekker behovet)"

# The kinds and shapes of the status tags (UX-DR30, NFR-7): the word is always text and the
# shape is decoration beside it. An unusual week that the setting leaves out has its own
# kind, shape and words, so it is never mistaken for one that is taken into the calculation.
OUT, UNUSUAL, UNUSUAL_OUT, SHIFT, USED = (
    "out",
    "unusual",
    "unusual-out",
    "shift",
    "used",
)
SHAPES = {
    OUT: "square-outline",
    UNUSUAL: "triangle",
    UNUSUAL_OUT: "triangle-outline",
    SHIFT: "diamond",
    USED: None,
}
WORDS = {
    OUT: "utsolgt",
    UNUSUAL: "uvanlig",
    UNUSUAL_OUT: "uvanlig, holdt utenfor",
    SHIFT: "nytt nivå",
    USED: "brukt",
}


class Tag(NamedTuple):
    """A status tag of the sales table: its words, its kind (the style) and its shape."""

    text: str
    kind: str
    shape: str | None


class SalesColumn(NamedTuple):
    """One week of the sales table: its week label, its units sold and its tags."""

    week: str
    units: str
    tags: tuple[Tag, ...]


class LevelRow(NamedTuple):
    """One calculation week of the exponential-smoothing table."""

    week: str
    units: str
    level: str


class Calculation(NamedTuple):
    """«Prognoseutregning»: the formula line, the weeks used (moving average), the rounding
    note (exponential smoothing) and the table of levels, then the weeks left out and, with
    unusual weeks excluded, the number of weeks used. A part that does not apply is None."""

    formula: str
    used: str | None
    rounding_note: str | None
    levels: tuple[LevelRow, ...]
    left_out: str | None
    used_count: str | None


class ScenarioRow(NamedTuple):
    label: str
    values: tuple[str, ...]
    normal: bool


class Scenarios(NamedTuple):
    """«Ukeprognoser og scenarioer»: the columns, the rows, the scenario sentence and the
    FR-7 note (None when no note applies)."""

    columns: tuple[str, ...]
    rows: tuple[ScenarioRow, ...]
    text: str
    note: str | None


class OrderCalculation(NamedTuple):
    """«Utregning av bestillingsmengde»: the line, its rounding note and the safety-margin
    sentence below it."""

    line: str
    rounding_note: str
    margin_note: str


class Worksheet(NamedTuple):
    """The texts of the worksheet. Without a forecast only the sales table remains."""

    sales_heading: str
    sales: tuple[SalesColumn, ...]
    tag_sentence: str | None
    no_sales: str | None
    calculation: Calculation | None
    scenarios: Scenarios | None
    order: OrderCalculation | None


def _iso_week(result, position, iso_year, iso_week):
    return week_at_position(position, result.history_length, iso_year, iso_week)


def _weeks(result, positions, iso_year, iso_week, with_year=False):
    """«uke 43, 44 og 45» for positions. The year follows every week of the list when
    `with_year` is true, and the first week of a new year always."""
    return display.week_list(
        [_iso_week(result, position, iso_year, iso_week) for position in positions],
        with_year,
    )


def _reaches_before_recent(result, positions):
    """True when a list holds a week before the recent period, so that it carries years
    (UX-DR42). The decision is the list's, not each week's."""
    return any(position <= result.history_length - SALES_ROWS for position in positions)


def _capital(text):
    return f"{text[0].upper()}{text[1:]}"


def used_weeks(result):
    """The positions of the weeks that the forecast was calculated from (UX-DR30): the
    last N calculation weeks for the moving average and every calculation week for
    exponential smoothing. An empty tuple without a forecast."""
    if result.base_forecast is None:
        return ()
    if result.settings.method == MOVING_AVERAGE:
        return result.calculation_weeks[-result.required_calculation_weeks :]
    return result.calculation_weeks


def _excluded_unusual(result):
    """The unusual weeks that the setting leaves out of the calculation."""
    return () if result.settings.unusual_weeks_included else result.unusual_weeks


def _tags(result, position, used):
    kinds = []
    if position in result.stockout_weeks:
        kinds.append(OUT)
    if position in result.unusual_weeks:
        kinds.append(UNUSUAL if result.settings.unusual_weeks_included else UNUSUAL_OUT)
    if position in result.level_shift_weeks:
        kinds.append(SHIFT)
    if position in used:
        kinds.append(USED)
    return tuple(Tag(WORDS[kind], kind, SHAPES[kind]) for kind in kinds)


def _tag_sentence(result, shown, used, iso_year, iso_week):
    """The sentence below the sales table, which explains the tags that are on it, in the
    mockup's wording (UX-DR28)."""
    forecast = result.base_forecast is not None
    parts = []
    # Only a «brukt» tag that is on the table is explained: the weeks used can lie before
    # the shown weeks when the recent weeks are stockout weeks.
    if any(position in shown for position in used):
        if result.settings.method == MOVING_AVERAGE:
            parts.append(
                f"«Brukt» viser de {display.whole_number(len(used))} ukene i "
                "glidende gjennomsnitt."
            )
        else:
            parts.append("«Brukt» viser alle beregningsukene i eksponentiell glatting.")

    def weeks_of(positions):
        return _capital(_weeks(result, positions, iso_year, iso_week))

    stockouts = [p for p in shown if p in result.stockout_weeks]
    if stockouts:
        one = len(stockouts) == 1
        parts.append(
            f"{weeks_of(stockouts)} er {'en utsolgt uke' if one else 'utsolgte uker'} "
            "og er holdt utenfor beregningen."
        )
    unusual = [p for p in shown if p in result.unusual_weeks]
    if unusual:
        one = len(unusual) == 1
        name = "en uvanlig uke" if one else "uvanlige uker"
        if not forecast:
            # Without a forecast there is no calculation to take a week into or out of.
            parts.append(f"{weeks_of(unusual)} er {name}.")
        else:
            if result.settings.unusual_weeks_included:
                what, setting = "tatt med", "tas med"
            else:
                what, setting = "holdt utenfor", "holdes utenfor"
            parts.append(
                f"{weeks_of(unusual)} er {name} og er {what}, fordi innstillingen er "
                f"«{setting}»."
            )
    shifts = [p for p in shown if p in result.level_shift_weeks]
    if shifts:
        ending = " og er alltid tatt med i beregningen" if forecast else ""
        parts.append(f"{weeks_of(shifts)} er nytt nivå{ending}.")
    return " ".join(parts) or None


def _left_out(result, iso_year, iso_week):
    """«Holdt utenfor: uke 38 og 39 (utsolgt), uke 42 (uvanlig).»: every stockout week and
    every excluded unusual week of the whole history, stockout weeks first, each kind in
    time order, with the year on every week when the list reaches before the recent
    period (FR-15, FR-16, UX-DR42). None when nothing is left out."""
    groups = (
        (result.stockout_weeks, "utsolgt"),
        (_excluded_unusual(result), "uvanlig"),
    )
    groups = [(positions, reason) for positions, reason in groups if positions]
    if not groups:
        return None
    with_year = _reaches_before_recent(
        result, [p for positions, _ in groups for p in positions]
    )
    phrases = ", ".join(
        f"{_weeks(result, positions, iso_year, iso_week, with_year)} ({reason})"
        for positions, reason in groups
    )
    return f"Holdt utenfor: {phrases}."


def _formula(result, used, iso_year, iso_week):
    """The FR-35 line, the weeks used and the levels of one calculation (None for a part
    that does not apply)."""
    sales = result.sales
    forecast = display.one_decimal(result.base_forecast)
    if result.settings.method == MOVING_AVERAGE:
        window = display.whole_number(len(used))
        terms = " + ".join(display.whole_number(sales[p - 1]) for p in used)
        formula = (
            f"Glidende gjennomsnitt, {window} uker: ({terms}) / {window} = {forecast}"
        )
        with_year = _reaches_before_recent(result, used)
        weeks = _weeks(result, used, iso_year, iso_week, with_year)
        return formula, f"Uker brukt: {weeks}.", None, ()

    alpha = float(result.settings.smoothing_factor)
    factor = display.factor(alpha)
    # R-10 never checks the first three valid weeks, so a forecast has at least three
    # calculation weeks and the last update always has a previous level.
    formula = (
        f"Eksponentiell glatting, faktor {factor}: "
        f"{factor} × {display.whole_number(sales[used[-1] - 1])} + "
        f"{display.factor(1 - alpha)} × {display.one_decimal(result.levels[-2])} "
        f"= {forecast}"
    )
    with_year = _reaches_before_recent(result, used)
    levels = tuple(
        LevelRow(
            display.week_item(
                *_iso_week(result, position, iso_year, iso_week), with_year
            ),
            display.whole_number(sales[position - 1]),
            display.one_decimal(level),
        )
        for position, level in zip(used, result.levels, strict=True)
    )
    return formula, None, ROUNDING_NOTE, levels


def _calculation(result, used, iso_year, iso_week):
    formula, weeks_used, rounding_note, levels = _formula(
        result, used, iso_year, iso_week
    )
    used_count = None
    if _excluded_unusual(result):
        # At least 2 weeks are used (the smallest window), so the plural is always right.
        used_count = f"{display.whole_number(len(used))} uker brukt i beregningen."
    return Calculation(
        formula,
        weeks_used,
        rounding_note,
        levels,
        _left_out(result, iso_year, iso_week),
        used_count,
    )


def _scenarios(result, iso_year, iso_week):
    columns = tuple(
        display.horizon_column_label(number, *week)
        for number, week in enumerate(horizon_weeks(iso_year, iso_week), start=1)
    )

    def row(label, attribute, normal=False):
        values = tuple(
            display.one_decimal(getattr(scenario, attribute))
            for scenario in result.scenarios
        )
        return ScenarioRow(label, values, normal)

    note = FLAT_WEEKS_NOTE if trust.WEEKS_REPEAT_WEEK_1 in result.notes else None
    return Scenarios(
        columns,
        (
            row("Optimistisk", "optimistic"),
            row("Normal", "normal", normal=True),
            row("Pessimistisk", "pessimistic"),
        ),
        SCENARIO_NOTE.format(
            percent=display.percent(result.settings.scenario_percentage)
        ),
        None if note is None else f"Merknad: {note}",
    )


def _order(result):
    """The FR-12 line. «(lageret dekker behovet)» ends it when the quantity is 0 and there
    is stock, the rule of the overstock note (FR-14), so a product with no stock and no
    expected sales does not claim that its stock covers anything (E23)."""
    quantity = result.suggested_order_quantity
    line = (
        f"Prognose {display.one_decimal(result.week_forecasts[0])} + sikkerhetsmargin "
        f"{display.percent(result.settings.safety_margin)} "
        f"({display.one_decimal(result.safety_margin_amount)}) "
        f"{display.MINUS_SIGN} lager {display.whole_number(result.stock_on_hand)} = "
        f"{display.two_decimals(result.order_unrounded)} → foreslått "
        f"bestillingsmengde {display.whole_number(quantity)}"
    )
    if quantity == 0 and result.stock_on_hand > 0:
        line += COVERED
    return OrderCalculation(line, ROUNDING_NOTE, SAFETY_MARGIN_NOTE)


def worksheet_texts(result, iso_year, iso_week):
    """The worksheet of a product whose company has its latest data week in the given ISO
    year and week. Without a forecast it holds the sales table only (UX-DR10); a product
    without any sales week needs no ISO week."""
    heading = (
        f"Salgshistorikk, siste {display.whole_number(SALES_ROWS)} uker"
        if result.history_length > SALES_ROWS
        else "Salgshistorikk, alle ukene"
    )
    if not result.history_length:
        return Worksheet(heading, (), None, NO_SALES_WEEKS, None, None, None)

    shown = range(
        max(1, result.history_length - SALES_ROWS + 1), result.history_length + 1
    )
    used = used_weeks(result)
    sales = tuple(
        SalesColumn(
            display.week_item(*_iso_week(result, position, iso_year, iso_week)),
            display.whole_number(result.sales[position - 1]),
            _tags(result, position, used),
        )
        for position in shown
    )
    tag_sentence = _tag_sentence(result, shown, used, iso_year, iso_week)
    if result.base_forecast is None:
        return Worksheet(heading, sales, tag_sentence, None, None, None, None)
    return Worksheet(
        heading,
        sales,
        tag_sentence,
        None,
        _calculation(result, used, iso_year, iso_week),
        _scenarios(result, iso_year, iso_week),
        _order(result),
    )
