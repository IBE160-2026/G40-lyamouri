"""Read the PRD and the mockup for the answer-key tests (Story 1.5; DR-3, AD-17).

The tests read the reference examples, the FR-21 table, and the FR-20 defaults
and ranges from the PRD, and Strøsand 25 kg's weeks from the mockup, so that no
expected value is copied into test code. The workbook itself is read by
reference/answer_key_reader.py, which the seed generator shares (Story 1.6).
"""

import re
from decimal import Decimal
from pathlib import Path

from answer_key_reader import Week, parse_sales

REPO_ROOT = Path(__file__).resolve().parents[1]
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
# The settings that the input of a reference example can state, case-insensitive.
STATED_SETTINGS = {
    "window": (r"window (\d+)", int),
    "smoothing_factor": (r"α = ([0-9.]+)", float),
    "scenario_percentage": (r"scenario percentage (\d+)%", int),
    "safety_margin": (r"safety margin (\d+)%", int),
    "stock_on_hand": (r"stock on hand (\d+)", int),
}


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


def prd_ranges():
    """Return the FR-20 allowed values of each number setting by its column, as
    (minimum, maximum) Decimals."""
    ranges = {}
    for line in _prd_section("#### FR-20:", "#### FR-21:").splitlines():
        if line.startswith("| ") and not line.startswith("| Setting"):
            setting, _default, allowed = _cells(line)
            match = re.fullmatch(r"([0-9.]+)%? to ([0-9.]+)(?:%| weeks)?", allowed)
            if match:
                ranges[setting] = (Decimal(match[1]), Decimal(match[2]))
    return {
        "window": ranges["Window (moving average)"],
        "smoothing_factor": ranges["Smoothing factor (exponential smoothing)"],
        "scenario_percentage": ranges["Scenario percentage"],
        "safety_margin": ranges["Safety margin"],
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


def mockup_products():
    """Return the products of the approved mockup's overview by name: the
    product number, the stock on hand, the week-1 forecast as shown («8,0»,
    or None where there is no forecast) and the suggested quantity as shown."""
    html = MOCKUP.read_text(encoding="utf-8")
    products = {}
    for chunk in re.split(r'<span class="nm">', html)[1:]:
        name = chunk.split("</span>")[0]
        text = " ".join(
            re.sub(r"<[^>]*>", " ", chunk.split('class="trust"')[0]).split()
        )
        number = re.search(r"Varenr\. (\d{5})", text)
        stock = re.search(r"Lager (\d+)", text)
        if name in products or number is None or stock is None:
            continue
        forecast = re.search(r"Ukeprognose uke 1:? ([\d,]+)", text)
        quantity = re.search(r"Foreslått (\d+|–)", text)
        products[name] = {
            "number": number[1],
            "stock": int(stock[1]),
            "forecast": forecast[1] if forecast else None,
            "quantity": quantity[1],
        }
    return products


def mockup_overview():
    """Return the figures that the mockup's overview states: the number of
    products, the products to order soon with the units suggested for them,
    and the products without a forecast."""
    html = MOCKUP.read_text(encoding="utf-8")
    text = " ".join(re.sub(r"<[^>]*>", " ", html).split())
    total = re.search(r"Produktoversikt (\d+) produkter", text)
    soon = re.search(r"Bestill snart (\d+) produkter · (\d+) enheter foreslått", text)
    without = re.search(r"Uten prognose (\d+) produkt", text)
    return {
        "products": int(total[1]),
        "order_soon": int(soon[1]),
        "units": int(soon[2]),
        "without_forecast": int(without[1]),
    }
