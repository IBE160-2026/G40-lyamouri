"""Norwegian display text (AD-3, NFR-5, UX-DR42).

Numbers are rounded through `rounding.py` (R-9) and written with a decimal comma, the
minus sign U+2212, no thousands grouping and a no-break space before «%». Week labels
come from an ISO year and week. The template filters, the explanation and the chart all
call this module, and nothing else formats a domain number. Only the standard library
and `forecasting/rounding.py` are imported (AD-1).
"""

from forecasting.rounding import round_for_display

MINUS_SIGN = "\u2212"
NO_BREAK_SPACE = "\u00a0"
# R-9: the decimals of each kind of number. Seasonal indices and adjusted values come with FR-9.
FORECAST_DECIMALS = 1
UNROUNDED_ORDER_DECIMALS = 2
WHOLE_NUMBER_DECIMALS = 0
# A value that a product does not have, such as the weeks of cover without a forecast (E23, FR-24).
MISSING = "\u2013"


def format_number(value, decimals):
    """The value rounded half away from zero to `decimals` and written as «−40,00»."""
    rounded = round_for_display(value, decimals)
    text = f"{abs(rounded):.{decimals}f}".replace(".", ",")
    return MINUS_SIGN + text if rounded < 0 else text


def one_decimal(value):
    """A forecast, a scenario, the weeks of cover or the safety margin amount: «10,3»."""
    return format_number(value, FORECAST_DECIMALS)


def two_decimals(value):
    """The unrounded result on the order calculation line: «0,07»."""
    return format_number(value, UNROUNDED_ORDER_DECIMALS)


def whole_number(value):
    """An order quantity, a stock on hand or any whole number: «70»."""
    return format_number(value, WHOLE_NUMBER_DECIMALS)


def weeks_of_cover(value):
    """The weeks of cover as «0,3», or «–» when the product has none (FR-24, E23)."""
    return MISSING if value is None else one_decimal(value)


def suggested_quantity(value):
    """The suggested order quantity as «11», or «–» without a forecast (FR-8, FR-24)."""
    return MISSING if value is None else whole_number(value)


def percent(value):
    """A percentage as a whole number, with a no-break space before «%»: «10 %»."""
    return f"{whole_number(value)}{NO_BREAK_SPACE}%"


def header_week_label(iso_year, iso_week):
    """The latest data week as the app header shows it, with the year: «uke 45, 2026»."""
    return f"uke {iso_week}, {iso_year}"


def week_label(iso_year, iso_week, with_year=False):
    """A week in a list: «uke 46», or «uke 10/2025» in a list that reaches before the
    recent period. The first week of a new year always carries its year: «uke 1/2027»."""
    if with_year or iso_week == 1:
        return f"uke {iso_week}/{iso_year}"
    return f"uke {iso_week}"


def axis_week_label(iso_year, iso_week):
    """A week on a chart axis, the week number only: «46», and «1/2027» in a new year."""
    return f"{iso_week}/{iso_year}" if iso_week == 1 else str(iso_week)


def factor(value):
    """A smoothing factor, or its complement, with its one decimal: «0,3»."""
    return one_decimal(value)


def week_item(iso_year, iso_week, with_year=False):
    """A week inside a list or a table, without the word «uke»: «46», «10/2025».

    The year follows when the list reaches before the recent period, and on the first
    week of a new year, which always carries it (UX-DR42)."""
    return f"{iso_week}/{iso_year}" if with_year or iso_week == 1 else str(iso_week)


def week_list(weeks, with_year=False):
    """Weeks as one phrase: «uke 38», «uke 38 og 39», «uke 43, 44 og 45».

    `weeks` are ISO years and weeks in time order. `with_year` is decided by the list as
    a whole, so that every week of a list that reaches before the recent period carries
    its year: «uke 10/2025 og 11/2025»."""
    items = [week_item(year, week, with_year) for year, week in weeks]
    if not items:
        raise ValueError("a list of weeks needs at least one week")
    if len(items) == 1:
        return f"uke {items[0]}"
    return f"uke {', '.join(items[:-1])} og {items[-1]}"


def horizon_column_label(number, iso_year, iso_week):
    """The column of horizon week `number` (1 to 3) of the scenario table: «Uke 1 · uke 46»."""
    return f"Uke {number} \u00b7 {week_label(iso_year, iso_week)}"
