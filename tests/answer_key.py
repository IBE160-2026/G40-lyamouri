"""Read the reference spreadsheet, the answer key (Story 1.5; DR-3, AD-17).

The tests read the cases, the rule test products and the checks in
reference/reference-examples.xlsx with openpyxl, and the reference examples,
the FR-21 table and the FR-20 defaults from the PRD, so that no expected value
is copied into test code. reference/README.md documents the columns and the
notation parsed here.
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
# The approved mockup, the source of Strøsand 25 kg's last 12 weeks (UX-DR46).
MOCKUP = (
    REPO_ROOT
    / "_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15"
    / "mockups/konsept-d-kombinert.html"
)
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
# The settings that the input of a reference example can state, case-insensitive.
STATED_SETTINGS = {
    "window": (r"window (\d+)", int),
    "smoothing_factor": (r"α = ([0-9.]+)", float),
    "scenario_percentage": (r"scenario percentage (\d+)%", int),
    "safety_margin": (r"safety margin (\d+)%", int),
    "stock_on_hand": (r"stock on hand (\d+)", int),
}


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


def _prd_text():
    return PRD.read_text(encoding="utf-8")


def _prd_section(start, end):
    return _prd_text().split(start)[1].split(end)[0]


def _cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def prd_reference_examples():
    """Return the rows of the table in PRD §5.7 by example, such as «E11 a»:
    the rule, the priority, the input and the expected result."""
    examples = {}
    for line in _prd_section("### 5.7 ", "\n## ").splitlines():
        if line.startswith("| E"):
            example, rule_priority, prd_input, prd_result = _cells(line)
            match = re.fullmatch(r"(.*) \((Must|Should|Could)\)", rule_priority)
            if match is None:
                raise ValueError(
                    f"{example}: no rule and priority in {rule_priority!r}"
                )
            examples[example] = {
                "rule": match[1],
                "priority": match[2],
                "prd_input": prd_input,
                "prd_result": prd_result,
            }
    return examples


def prd_sales_history():
    """Return the series of E1 to E4, which PRD §5.7 gives above its table."""
    match = re.search(
        r"Sales history for E1 to E4: ([0-9, ]+) \(", _prd_section("### 5.7 ", "\n## ")
    )
    return parse_sales(match[1])


def prd_case_inputs(example, examples):
    """Return (series, settings) as PRD §5.7 states them for an example: the
    series is a list of weeks, or None where the example gives none, and the
    settings hold only those that its input names. A reference such as «E1 with
    …», «E4 inputs» or «E14 data» takes over that example's inputs first."""
    text = examples[example]["prd_input"]
    series, settings = None, {}
    reference = re.match(r"(E\d+(?: [a-z])?)(?= with| inputs| data|$)", text)
    if reference:
        series, inherited = prd_case_inputs(reference[1], examples)
        settings = dict(inherited)
    elif re.fullmatch(r"E[1-4]", example):
        series = prd_sales_history()
    sales = re.search(r"Sales ([0-9S, ]+)", text)
    years = re.search(r"Year 1: ([0-9S, ]+)\. Year 2: ([0-9S, ]+)\.", text)
    if sales:
        series = parse_sales(sales[1].strip())
    elif years:
        series = parse_sales(f"{years[1]}, {years[2]}")
    lowered = text.lower()
    if "exponential smoothing" in lowered:
        settings["method"] = "exponential_smoothing"
    elif "moving average" in lowered:
        settings["method"] = "moving_average"
    for column, (pattern, cast) in STATED_SETTINGS.items():
        values = {cast(v) for v in re.findall(pattern, text, re.IGNORECASE)}
        if len(values) == 1:
            settings[column] = values.pop()
    if "4-week cycle" in text:
        settings["cycle_length"] = 4
    if (
        lowered.startswith("seasonal adjustment,")
        or "seasonal adjustment on" in lowered
    ):
        settings["seasonal_adjustment"] = "on"
    if "excluded by the setting" in text:
        settings["unusual_weeks_setting"] = "excluded"
    return series, settings


def prd_variants(example, examples):
    """Return the alternatives that an example's input in PRD §5.7 names, which
    the cases take as their variants: «(E4)» and «(E6)» in E13, «Product A» and
    «Product B» in E24, and the two latest valid weeks in E12."""
    text = examples[example]["prd_input"]
    return (
        set(re.findall(r"\((E\d+)\)", text))
        | set(re.findall(r"Product ([A-Z])\b", text))
        | set(re.findall(r"(?:latest valid week at|then at) position (\d+)", text))
    )


def prd_fr21_variants():
    """Return (setting changed, value that changes, example) for the rows of the
    FR-21 table whose example is a variant beyond PRD §5.7, such as «E1 with
    window 4 instead of 3»."""
    variants = []
    for line in _prd_section("#### FR-21:", "#### FR-22:").splitlines():
        if line.startswith("| "):
            setting, value, example = _cells(line)
            if re.match(r"E\d+ with ", example):
                variants.append((setting, value, example))
    return variants


def prd_rule_test_examples():
    """Return the examples that FR-3 builds the rule test products from, such
    as E1 to E4. An item that is neither a range nor an example raises."""
    listed = re.search(r"reference-example series in §5\.7 \(([^)]*)\)", _prd_text())
    if listed is None:
        raise ValueError("FR-3 names no reference-example series")
    examples = []
    for item in listed[1].split(", "):
        span = re.fullmatch(r"E(\d+)(?: to E(\d+))?", item)
        if span is None:
            raise ValueError(f"FR-3: cannot read {item!r}")
        first, last = int(span[1]), int(span[2] or span[1])
        examples += [f"E{n}" for n in range(first, last + 1)]
    return examples


def prd_defaults():
    """Return the FR-20 defaults by setting column, which the rule test products use."""
    defaults = {}
    for line in _prd_section("#### FR-20:", "#### FR-21:").splitlines():
        if line.startswith("| ") and not line.startswith("| Setting"):
            setting, default, _allowed = _cells(line)
            defaults[setting] = default
    return {
        "method": defaults["Forecasting method"].lower().replace(" ", "_"),
        "window": int(defaults["Window (moving average)"].split()[0]),
        "smoothing_factor": float(defaults["Smoothing factor (exponential smoothing)"]),
        "scenario_percentage": int(defaults["Scenario percentage"].rstrip("%")),
        "safety_margin": int(defaults["Safety margin"].rstrip("%")),
        "unusual_weeks_setting": defaults["Unusual weeks"].lower(),
        "seasonal_adjustment": defaults["Seasonal adjustment"].lower(),
    }


def mockup_recent_weeks():
    """Return the 12 weeks of the sales table in the approved mockup: the units
    sold in the row «Solgt», and the stockout weeks that the row «Status» marks."""
    html = MOCKUP.read_text(encoding="utf-8")

    def cells(label):
        row = re.search(rf'<tr><th scope="row">{label}</th>(.*?)</tr>', html)
        return re.findall(r"<td[^>]*>(.*?)</td>", row[1])

    return [
        Week(int(units), stockout='class="tag out"' in status)
        for units, status in zip(cells("Solgt"), cells("Status"), strict=True)
    ]
