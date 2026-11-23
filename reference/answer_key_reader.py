"""Read the reference spreadsheet, the answer key (Stories 1.5 and 1.6; DR-3, AD-15, AD-17).

The tests and the seed generator read the cases and the rule test products in
reference-examples.xlsx with openpyxl, so that no expected value or series is
copied into code. reference/README.md documents the columns and the notation
parsed here. The module sits beside the workbook it reads, and a caller puts
this folder on its import path.
"""

import re
from pathlib import Path
from typing import NamedTuple

import openpyxl

WORKBOOK = Path(__file__).resolve().parent / "reference-examples.xlsx"
# The sheets of expected values, which hold values only.
ANSWER_KEY_SHEETS = ("cases", "products")
NONE = "none"
# A calculated number matches a recorded one when they differ by less than this.
TOLERANCE = 0.0005
# The active warnings of R-15, in its order; seasonal_pattern is Should (FR-36).
WARNINGS = (
    "stockout_weeks",
    "unusual_weeks",
    "level_shift",
    "old_data",
    "insufficient_data",
    "seasonal_pattern",
)
LABELS = ("lav", "middels", "høy")
METHODS = ("moving_average", "exponential_smoothing")
UNUSUAL_WEEKS_SETTINGS = ("included", "excluded")
SEASONAL_ADJUSTMENT = ("on", "off")
# Every case writes out all of these: the FR-20 settings, the cycle and the stock.
SETTINGS = (
    "method",
    "window",
    "smoothing_factor",
    "scenario_percentage",
    "safety_margin",
    "unusual_weeks_setting",
    "seasonal_adjustment",
    "cycle_length",
    "stock_on_hand",
)

INTEGER_COLUMNS = {
    "window",
    "scenario_percentage",
    "safety_margin",
    "cycle_length",
    "stock_on_hand",
    "valid_weeks",
    "calculation_weeks",
    "suggested_order_quantity",
    "optimistic_order_quantity",
    "pessimistic_order_quantity",
    "overview_position",
    "weeks_since_latest_valid",
}
NUMBER_COLUMNS = {
    "smoothing_factor",
    "mean_of_means",
    "base_forecast",
    "normal",
    "optimistic",
    "pessimistic",
    "order_unrounded",
    "optimistic_order_unrounded",
    "pessimistic_order_unrounded",
    "weeks_of_cover",
}
# The inputs among the numbers, which are never «none».
INPUT_NUMBERS = {
    "window",
    "smoothing_factor",
    "scenario_percentage",
    "safety_margin",
    "cycle_length",
    "stock_on_hand",
}
NUMBER_LIST_COLUMNS = {
    "levels",
    "week_number_means",
    "seasonal_indices",
    "adjusted_sales_used",
    "week_forecasts",
}
POSITION_COLUMNS = {"unusual_weeks", "level_shift_weeks"}
FLAG_COLUMNS = {
    "order_soon",
    "overstock_note",
    "seasonal_adjustment_used",
    "seasonal_pattern",
}
SHOWN_COLUMNS = {"base_forecast_shown", "order_unrounded_shown", "weeks_of_cover_shown"}
# The expected values of a case, in the order of the sheet.
CASE_EXPECTED = (
    "valid_weeks",
    "unusual_weeks",
    "level_shift_weeks",
    "calculation_weeks",
    "levels",
    "week_number_means",
    "mean_of_means",
    "seasonal_indices",
    "adjusted_sales_used",
    "base_forecast",
    "base_forecast_shown",
    "week_forecasts",
    "normal",
    "optimistic",
    "pessimistic",
    "order_unrounded",
    "order_unrounded_shown",
    "suggested_order_quantity",
    "optimistic_order_unrounded",
    "optimistic_order_quantity",
    "pessimistic_order_unrounded",
    "pessimistic_order_quantity",
    "weeks_of_cover",
    "weeks_of_cover_shown",
    "order_soon",
    "overview_position",
    "overstock_note",
    "weeks_since_latest_valid",
    "seasonal_adjustment_used",
    "seasonal_pattern",
    "warnings",
    "confidence_label",
)
# The expected results that FR-3 lists for every rule test product.
PRODUCT_EXPECTED = (
    "base_forecast",
    "suggested_order_quantity",
    "unusual_weeks",
    "level_shift_weeks",
    "warnings",
    "confidence_label",
)
# A whole number of units sold, or «S» with the units sold in a stockout week.
SALES_WEEK = re.compile(r"(?P<units>\d+)|S(?P<stockout_units>\d*)")


class Week(NamedTuple):
    units_sold: int
    stockout: bool


class Row(dict):
    """A sheet row as {column: value}, with its row number and each value's cell."""

    def __init__(self, values, number, cells):
        super().__init__(values)
        self.number = number
        self.cells = cells


def parse_sales(text):
    """Return the weeks of a sales series such as «12, 15, S, S2»."""
    weeks = []
    for token in (t.strip() for t in str(text).split(",")):
        match = SALES_WEEK.fullmatch(token)
        if match is None:
            raise ValueError(f"not a sales week: {token!r}")
        if match["units"] is not None:
            weeks.append(Week(int(match["units"]), stockout=False))
        else:
            weeks.append(Week(int(match["stockout_units"] or 0), stockout=True))
    return weeks


def parse_value(column, value):
    """Return the typed value of an answer-key cell, as reference/README.md
    describes it: «none» is an expected absence, lists are comma-separated, and
    flags are «yes» or «no»."""
    if column == "sales":
        return parse_sales(value)
    if column in POSITION_COLUMNS | NUMBER_LIST_COLUMNS or column == "warnings":
        if value == NONE:
            return []
        items = [item.strip() for item in str(value).split(",")]
        if column in POSITION_COLUMNS:
            return [int(item) for item in items]
        if column in NUMBER_LIST_COLUMNS:
            return [float(item) for item in items]
        return items
    if column in FLAG_COLUMNS:
        if value not in ("yes", "no"):
            raise ValueError(f"{column} is «yes» or «no», not {value!r}")
        return value == "yes"
    if column in INTEGER_COLUMNS | NUMBER_COLUMNS:
        if value == NONE:
            if column in INPUT_NUMBERS:
                raise ValueError(f"{column} is an input, so it cannot be «none»")
            return None
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"{column} is a number or «none», not {value!r}")
        if column in INTEGER_COLUMNS:
            if not float(value).is_integer():
                raise ValueError(f"{column} is a whole number, not {value!r}")
            return int(value)
        return float(value)
    return value


def read_rows(sheet, path=None):
    """Return the rows of a sheet as Rows keyed by the header in row 1, leaving
    out empty cells. The answer-key sheets hold values only, so a formula
    anywhere in them, which openpyxl cannot calculate, raises ValueError."""
    workbook = openpyxl.load_workbook(path or WORKBOOK, read_only=True)
    try:
        rows = list(workbook[sheet].iter_rows())
    finally:
        workbook.close()
    if sheet in ANSWER_KEY_SHEETS:
        for row in rows:
            for cell in row:
                if cell.data_type == "f":
                    raise ValueError(
                        f"{sheet}!{cell.coordinate} holds a formula; "
                        "the answer key holds values only"
                    )
    header = []
    for cell in rows[0]:
        if cell.value is None:
            break
        header.append(cell.value)
    result = []
    for row in rows[1:]:
        # A row in read-only mode can be shorter than the header.
        cells = {h: c for h, c in zip(header, row, strict=False) if c.value is not None}
        if cells:
            first = next(iter(cells.values()))
            result.append(
                Row(
                    {h: c.value for h, c in cells.items()},
                    first.row,
                    {h: c.coordinate for h, c in cells.items()},
                )
            )
    return result


def read_typed(sheet, path=None):
    """Return the rows of an answer-key sheet with typed values. A value that
    does not follow the notation raises ValueError naming its cell."""
    typed = []
    for row in read_rows(sheet, path):
        values = {}
        for column, value in row.items():
            try:
                values[column] = parse_value(column, value)
            except ValueError as error:
                cell = row.cells[column]
                raise ValueError(f"{sheet}!{cell} ({column}): {error}") from error
        typed.append(Row(values, row.number, row.cells))
    return typed


def cases():
    """Return the cases: the reference examples of PRD §5.7, a row per variant,
    and the FR-21 variants."""
    return read_typed("cases")


def products():
    """Return the rule test products with their series, stock and expected results."""
    return read_typed("products")


def expected_values(case):
    return {column: case[column] for column in CASE_EXPECTED if column in case}
