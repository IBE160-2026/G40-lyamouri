"""Read the reference spreadsheet, the answer key (Story 1.5; DR-3, AD-17).

The tests read the cases, the rule test products and the checks in
reference/reference-examples.xlsx with openpyxl, and the reference examples
from the PRD, so that no expected value is copied into test code.
reference/README.md documents the columns and the notation parsed here.
"""

import re
from pathlib import Path
from typing import NamedTuple

import openpyxl

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = REPO_ROOT / "reference/reference-examples.xlsx"
PRD = (
    REPO_ROOT
    / "_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md"
)
# The sheets of expected values, which hold values only.
ANSWER_KEY_SHEETS = ("cases", "products")
NONE = "none"
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
            return None
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(f"{column} is a number or «none», not {value!r}")
        if column in INTEGER_COLUMNS:
            if not float(value).is_integer():
                raise ValueError(f"{column} is a whole number, not {value!r}")
            return int(value)
        return float(value)
    return value


def read_rows(sheet, path=WORKBOOK):
    """Return the rows of a sheet as dicts of cell values keyed by the header
    in row 1, leaving out empty cells. The answer-key sheets hold values only,
    so a formula there, which openpyxl cannot calculate, raises ValueError."""
    workbook = openpyxl.load_workbook(path, read_only=True)
    try:
        rows = workbook[sheet].iter_rows()
        header = []
        for cell in next(rows):
            if cell.value is None:
                break
            header.append(cell.value)
        result = []
        for row in rows:
            cells = row[: len(header)]
            if sheet in ANSWER_KEY_SHEETS:
                for cell in cells:
                    if cell.data_type == "f":
                        raise ValueError(
                            f"{sheet}!{cell.coordinate} holds a formula; "
                            "the answer key holds values only"
                        )
            # A row in read-only mode can be shorter than the header.
            values = {
                h: c.value
                for h, c in zip(header, cells, strict=False)
                if c.value is not None
            }
            if values:
                result.append(values)
        return result
    finally:
        workbook.close()


def read_typed(sheet, path=WORKBOOK):
    return [
        {column: parse_value(column, value) for column, value in row.items()}
        for row in read_rows(sheet, path)
    ]


def cases():
    """Return the cases: the reference examples of PRD §5.7, a row per variant,
    and the FR-21 variants."""
    return read_typed("cases")


def products():
    """Return the rule test products with their series, stock and expected results."""
    return read_typed("products")


def expected_values(case):
    return {column: case[column] for column in CASE_EXPECTED if column in case}


def _prd_section(start, end):
    return PRD.read_text(encoding="utf-8").split(start)[1].split(end)[0]


def _cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def prd_reference_examples():
    """Return the rows of the table in PRD §5.7 by example, such as «E11 a»:
    the rule, the priority, the input and the expected result."""
    examples = {}
    for line in _prd_section("### 5.7 ", "\n## ").splitlines():
        if line.startswith("| E"):
            example, rule_priority, prd_input, prd_result = _cells(line)
            rule, priority = re.fullmatch(
                r"(.*) \((Must|Should)\)", rule_priority
            ).groups()
            examples[example] = {
                "rule": rule,
                "priority": priority,
                "prd_input": prd_input,
                "prd_result": prd_result,
            }
    return examples


def prd_fr21_variants():
    """Return (value that changes, example) for the rows of the FR-21 table
    whose example is a variant beyond PRD §5.7, such as «E1 with window 4
    instead of 3»."""
    variants = []
    for line in _prd_section("#### FR-21:", "#### FR-22:").splitlines():
        if line.startswith("| "):
            _setting, value, example = _cells(line)
            if re.match(r"E\d+ with ", example):
                variants.append((value, example))
    return variants


def prd_rule_test_examples():
    """Return the examples that FR-3 builds the rule test products from, such
    as E1 to E4."""
    ranges = re.search(
        r"reference-example series in §5\.7 \(([^)]*)\)",
        PRD.read_text(encoding="utf-8"),
    )
    examples = []
    for first, last in re.findall(r"E(\d+) to E(\d+)", ranges.group(1)):
        examples += [f"E{n}" for n in range(int(first), int(last) + 1)]
    return examples
