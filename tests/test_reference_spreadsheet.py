"""The reference spreadsheet is the answer key (Story 1.5; DR-3, AD-17, FR-3, FR-21, NFR-4).

The tests read reference/reference-examples.xlsx with openpyxl and take the
reference examples, the FR-21 table and the FR-20 defaults from the PRD, so
neither holds an expected value. They use no database.
"""

import re
import zipfile
from datetime import date
from decimal import Decimal

import answer_key
import answer_key_reader as reader
import openpyxl
import pytest

from forecasting import settings as defaults

# The columns that each FR-21 «value that changes» names.
FR21_COLUMNS = {
    "Base forecast (moving average)": ("base_forecast",),
    "Base forecast (exponential smoothing)": ("base_forecast",),
    "Optimistic and pessimistic scenario": ("optimistic", "pessimistic"),
    "Suggested order quantity": ("suggested_order_quantity",),
}
# The column that each FR-21 «setting changed» names.
FR21_SETTINGS = {
    "Window": "window",
    "Smoothing factor": "smoothing_factor",
    "Scenario percentage": "scenario_percentage",
    "Safety margin": "safety_margin",
}
# A variant named after a setting value, with the setting and the other value.
SETTING_VARIANTS = {
    "included": ("unusual_weeks_setting", "excluded"),
    "excluded": ("unusual_weeks_setting", "included"),
    "off": ("seasonal_adjustment", "on"),
    "on": ("seasonal_adjustment", "off"),
}
# The demo product that acts as a rule test product (UX-DR46).
DEMO_PRODUCT = "Strøsand 25 kg"
# R-9 display text: a decimal comma, with two decimals on the order line.
SHOWN = {
    "base_forecast_shown": r"−?\d+,\d",
    "weeks_of_cover_shown": r"−?\d+,\d",
    "order_unrounded_shown": r"−?\d+,\d\d",
}
# The inputs that each kind of formula in the sheet checks is written with.
FORMULA_INPUTS = [
    (
        {
            "order_unrounded",
            "optimistic_order_unrounded",
            "pessimistic_order_unrounded",
        },
        r"\*\(1\+(\d+)/100\)-(\d+)$",
        ("safety_margin", "stock_on_hand"),
    ),
    ({"optimistic"}, r"\*\(1\+(\d+)/100\)$", ("scenario_percentage",)),
    ({"pessimistic"}, r"\*\(1-(\d+)/100\)\)$", ("scenario_percentage",)),
    ({"weeks_of_cover"}, r"(\d+)/F\d+\)?$", ("stock_on_hand",)),
    ({"overstock_note"}, r"AND\(F\d+=0,(\d+)>0\)", ("stock_on_hand",)),
]
# A level of exponential smoothing after the first, which is the first week's sales.
LEVEL = r"=([0-9.]+)\*\d+\+\(1-([0-9.]+)\)\*F\d+"
# A local path, such as the absPath that Excel writes into a workbook it saves.
LOCAL_PATH = re.compile(
    rb"absPath|/Users/|/home/|[A-Z]:\\Users\\|file:///", re.IGNORECASE
)
# How close a recorded value in the checks must be to the answer key's.
SAME = 1e-9


def variant(case):
    """Return the variant in a case's name, such as «excluded» in «E8 (excluded)»."""
    match = re.fullmatch(r".* \((.+)\)", case["case"])
    return match[1] if match else None


def test_every_reference_example_has_a_case():
    """DR-3, AD-17, SM-1: every example in PRD §5.7, E1 to E30 with its lettered
    cases, has a case in the workbook."""
    examples = {case["example"] for case in reader.cases()}
    assert [e for e in answer_key.prd_reference_examples() if e not in examples] == []


def test_every_case_has_an_expected_value():
    """DR-3, AD-17: every case records at least one expected value."""
    cases = reader.cases()
    assert [c["case"] for c in cases if not reader.expected_values(c)] == []


def test_every_variant_of_an_example_is_present():
    """DR-3: an example compared under two settings has a case for each, and an
    example whose input in PRD §5.7 names its alternatives, such as E13's «(E4)»
    and «(E6)», has a case for each of them."""
    cases = reader.cases()
    names = {case["case"] for case in cases}
    for case in cases:
        label = variant(case)
        if label in SETTING_VARIANTS:
            other = SETTING_VARIANTS[label][1]
            assert case["case"].replace(f"({label})", f"({other})") in names, case[
                "case"
            ]
    examples = answer_key.prd_reference_examples()
    for example in examples:
        labels = answer_key.prd_variants(example, examples)
        if labels:
            found = {variant(c) for c in cases if c["example"] == example}
            assert found == labels, example


def test_cases_quote_their_reference_example_from_the_prd():
    """DR-3: each case names the rule and priority of its example and quotes its
    input and expected result from PRD §5.7 verbatim, so an example changed in
    the PRD fails here until the workbook follows it."""
    prd = answer_key.prd_reference_examples()
    for case in reader.cases():
        if case["example"] == "FR-21":
            continue
        quoted = {column: case.get(column) for column in prd[case["example"]]}
        assert quoted == prd[case["example"]], case["case"]


def test_case_series_and_settings_follow_the_prd():
    """DR-3, AD-17: each case has the series and the settings that PRD §5.7
    states for its example, following references such as «E1 with …» or «E14
    data», and a variant named after a setting has that setting. Examples that
    give no series, such as E5 or E29 c, use the series that reference/README.md
    lists."""
    examples = answer_key.prd_reference_examples()
    for case in reader.cases():
        if case["example"] == "FR-21":
            continue
        label = variant(case)
        source = label if label in examples else case["example"]
        series, settings = answer_key.prd_case_inputs(source, examples)
        if label in SETTING_VARIANTS:
            settings[SETTING_VARIANTS[label][0]] = label
        if series is not None:
            assert case["sales"] == series, case["case"]
        assert {column: case.get(column) for column in settings} == settings, case[
            "case"
        ]


def test_every_fr21_variant_changes_the_setting_the_prd_names():
    """FR-21, AD-17: the FR-21 cases are exactly the variants that the FR-21
    table describes beyond PRD §5.7, such as «E1 with window 4 instead of 3».
    Each has its base example's series and settings except the changed one,
    which has the new value, and records the value that the change affects,
    calculated by hand, so that Story 3.2 reads it from the workbook."""
    cases = {case["case"]: case for case in reader.cases()}
    variants = {c["prd_input"]: c for c in cases.values() if c["example"] == "FR-21"}
    rows = answer_key.prd_fr21_variants()
    assert rows
    assert set(variants) == {example for _setting, _value, example in rows}
    for setting, value, example in rows:
        changed, base = variants[example], cases[example.split(" with ")[0]]
        column = FR21_SETTINGS[setting]
        new = re.search(r"with (?:window |factor )?([0-9.]+)%? instead of", example)
        assert changed[column] == type(base[column])(new[1]), example
        others = [s for s in reader.SETTINGS if s != column]
        assert {s: changed[s] for s in others} == {s: base[s] for s in others}, example
        assert changed["sales"] == base["sales"], example
        assert all(column in changed for column in FR21_COLUMNS[value]), example


def test_every_rule_test_product_has_its_series_stock_and_expected_results():
    """FR-3, DR-3, UX-DR46: the products cover every example that FR-3 builds the
    rule test products from, each lettered case included, name only examples of
    PRD §5.7, include the demo product Strøsand 25 kg, and each has its company,
    its series, its stock on hand and every expected result that FR-3 lists."""
    products = reader.products()
    ids = answer_key.prd_reference_examples()
    named = {e.strip() for p in products for e in p["examples"].split(",")}
    assert named <= set(ids)
    examples = answer_key.prd_rule_test_examples()
    assert examples
    for example in examples:
        lettered = [i for i in ids if i == example or i.startswith(f"{example} ")]
        assert lettered and set(lettered) <= named, example
    assert DEMO_PRODUCT in {p["product"] for p in products}
    required = ("company", "sales", "stock_on_hand", *reader.PRODUCT_EXPECTED)
    for product in products:
        assert [c for c in required if c not in product] == [], product["product"]


def test_products_use_the_series_of_their_source():
    """FR-3, AD-15, UX-DR46: a rule test product named after an example has the
    series of every case of that example, and Strøsand 25 kg repeats the series
    of E1 to E4 before the 12 weeks of the approved mockup, so the product screen
    and the workbook show the same case."""
    by_example = {}
    for case in reader.cases():
        by_example.setdefault(case["example"], []).append(case["sales"])
    products = {product["product"]: product for product in reader.products()}
    named = [p for p in products.values() if p["product"] in by_example]
    assert named
    for product in named:
        assert all(s == product["sales"] for s in by_example[product["product"]])
    demo = products[DEMO_PRODUCT]["sales"]
    recent, history = answer_key.mockup_recent_weeks(), answer_key.prd_sales_history()
    earlier = len(demo) - len(recent)
    assert demo[earlier:] == recent
    assert demo[:earlier] == [history[i % len(history)] for i in range(earlier)]


def formula_inputs(check, subject):
    """Yield (written, expected) for each input that a formula in the sheet
    checks is written with."""
    formula, value = check["recalculated"], check["value"]
    for values, pattern, columns in FORMULA_INPUTS:
        if value in values:
            match = re.search(pattern, formula)
            assert match, (check["key"], value, formula)
            for column, written in zip(columns, match.groups(), strict=True):
                yield float(written), subject[column]
    moving = subject["method"] == "moving_average"
    if value == "levels" and check["item"] > 1:
        level = re.fullmatch(LEVEL, formula)
        assert level, (check["key"], value, formula)
        yield float(level[1]), subject["smoothing_factor"]
        yield float(level[2]), subject["smoothing_factor"]
    if value == "base_forecast":
        terms = re.fullmatch(r"=\(([0-9+]+)\)/(\d+)", formula)
        adjusted = re.fullmatch(r"=AVERAGE\(F(\d+):F(\d+)\)", formula)
        none = re.search(r"<(\d+)\),\"none\"", formula)
        if terms:
            yield int(terms[2]), subject["window"]
            yield len(terms[1].split("+")), subject["window"]
        elif adjusted:
            yield int(adjusted[2]) - int(adjusted[1]) + 1, subject["window"]
        elif none:
            yield int(none[1]), subject["window"] if moving else 1
    if value == "warnings" and check.get("item") == "insufficient_data":
        needed = re.search(r"<(\d+)\)$", formula)
        yield int(needed[1]), subject["window"] if moving else 1


def test_check_formulas_use_the_inputs_of_their_subject():
    """AD-17, DR-3: the stock on hand, the safety margin, the scenario
    percentage, the window and the smoothing factor that the formulas in the
    sheet checks are written with equal the inputs of their case, or of their
    product with the FR-20 defaults, so an input changed without its checks
    fails."""
    defaults = answer_key.prd_defaults()
    subjects = {("cases", c["case"]): c for c in reader.cases()}
    subjects |= {
        ("products", p["product"]): {**defaults, **p} for p in reader.products()
    }
    compared = 0
    for check in reader.read_rows("checks"):
        subject = subjects[(check["sheet"], check["key"])]
        for written, expected in formula_inputs(check, subject):
            assert written == expected, (check["key"], check["recalculated"])
            compared += 1
    assert compared


def test_every_case_uses_settings_inside_the_fr20_limits():
    """FR-20, AD-9, DR-3: the method of each case is one of the core's, and its
    window, smoothing factor, scenario percentage and safety margin lie inside
    the ranges that forecasting/settings.py holds, so no case asks the core for
    a setting that a company cannot choose."""
    ranges = {
        "window": defaults.WINDOW,
        "smoothing_factor": defaults.SMOOTHING_FACTOR,
        "scenario_percentage": defaults.SCENARIO_PERCENTAGE,
        "safety_margin": defaults.SAFETY_MARGIN,
    }
    for case in reader.cases():
        assert case["method"] in defaults.METHODS, case["case"]
        for column, allowed in ranges.items():
            value = Decimal(str(case[column]))
            assert allowed.minimum <= value <= allowed.maximum, (case["case"], column)


def test_every_value_follows_the_schema():
    """DR-3, AD-17: every cell parses as reference/README.md describes it (the
    readers name the cell otherwise), the keys are unique, every case writes out
    all the settings, positions are sorted valid weeks inside the series, the
    warnings are R-15's in its order and without repeats, with seasonal_pattern
    only in Should cases, the displayed values are R-9 text, and the labels are
    R-16's."""
    cases, products = reader.cases(), reader.products()
    assert len({c["case"] for c in cases}) == len(cases)
    assert len({p["product"] for p in products}) == len(products)
    for case in cases:
        name = case["case"]
        assert [s for s in reader.SETTINGS if s not in case] == [], name
        assert case["method"] in reader.METHODS, name
        assert case["unusual_weeks_setting"] in reader.UNUSUAL_WEEKS_SETTINGS, name
        assert case["seasonal_adjustment"] in reader.SEASONAL_ADJUSTMENT, name
        assert case["cycle_length"] in (4, 52), name
        for column, pattern in SHOWN.items():
            if column in case:
                shown = str(case[column])
                assert shown == "–" or re.fullmatch(pattern, shown), (name, column)
    for product in products:
        assert product["company"] in ("A", "B"), product["product"]
    for subject in cases + products:
        name = subject.get("case") or subject["product"]
        weeks = subject["sales"]
        for column in reader.POSITION_COLUMNS & subject.keys():
            positions = subject[column]
            assert positions == sorted(set(positions)), (name, column)
            for p in positions:
                assert 1 <= p <= len(weeks) and not weeks[p - 1].stockout, (name, p)
        if "warnings" in subject:
            warnings = subject["warnings"]
            assert set(warnings) <= set(reader.WARNINGS), name
            order = sorted(set(warnings), key=reader.WARNINGS.index)
            assert warnings == order, name
            if subject.get("priority") != "Should":
                assert "seasonal_pattern" not in warnings, name
        if "confidence_label" in subject:
            assert subject["confidence_label"] in reader.LABELS, name


@pytest.mark.parametrize("cell", ["B2", "D2", "C1"])
def test_reader_refuses_a_formula_in_the_answer_key(tmp_path, cell):
    """AD-17: the cases and products sheets hold values only. The reader refuses
    a formula anywhere in them, under the header, beyond it or in the header row,
    instead of reading it as a missing value."""
    path = tmp_path / "answer-key.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "cases"
    sheet.append(["case", "base_forecast"])
    sheet.append(["E1", 14.333])
    sheet[cell] = "=(16+12+15)/3"
    workbook.save(path)
    with pytest.raises(ValueError, match=rf"cases!{cell} holds a formula"):
        reader.read_rows("cases", path)


def test_reader_names_the_cell_of_a_value_it_cannot_read(tmp_path):
    """DR-3: a value that does not follow the notation, such as «1O» in a
    series, fails with the sheet and the cell that hold it."""
    path = tmp_path / "answer-key.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "cases"
    sheet.append(["case", "sales"])
    sheet.append(["E1", "12, 1O"])
    workbook.save(path)
    with pytest.raises(ValueError, match=r"cases!B2 \(sales\): not a sales week"):
        reader.read_typed("cases", path)


def recorded_matches(value, column, item, recorded):
    """Whether a check records the answer key's value for the column."""
    if column in reader.NUMBER_LIST_COLUMNS:
        return abs(value[item - 1] - recorded) < SAME
    if column in reader.POSITION_COLUMNS:
        if isinstance(item, int):
            return recorded == (item in value)
        if item == "other":
            return recorded is False
        run = [int(p) for p in str(item).split(",")]
        return recorded == all(p in value for p in run)
    if column == "warnings":
        return recorded == (item in value)
    if column in reader.FLAG_COLUMNS:
        return recorded == ("yes" if value else "no")
    if column in reader.SHOWN_COLUMNS and value != "–":
        return recorded == float(value.replace(",", "."))
    if value is None:
        return recorded == reader.NONE
    if isinstance(value, str):
        return recorded == value
    return abs(value - recorded) < SAME


def test_every_expected_value_is_recalculated_in_the_checks():
    """DR-3, AD-17: the sheet checks recalculates every expected value with a
    visible formula: each element of a list, each listed week and the other
    weeks of a position list, and each warning of R-15. Each check records the
    value that the answer key holds, and its match formula compares that row's
    recorded value with its recalculation, so a value changed without its check,
    or a check that compares another row, fails."""
    subjects = {("cases", c["case"]): c for c in reader.cases()}
    subjects |= {("products", p["product"]): p for p in reader.products()}
    covered = {}
    for check in reader.read_rows("checks"):
        assert str(check["recalculated"]).startswith("="), check
        if "recorded" not in check:
            assert "match" not in check, check
            continue
        n = check.number
        tolerance = f"=ABS(E{n}-F{n})<{reader.TOLERANCE}"
        assert check["match"] in (f"=E{n}=F{n}", tolerance), check
        subject = subjects[(check["sheet"], check["key"])]
        column, item = check["value"], check.get("item")
        assert column in subject, check
        assert recorded_matches(subject[column], column, item, check["recorded"]), check
        covered.setdefault((check["sheet"], check["key"], column), []).append(check)
    for (sheet, key), subject in subjects.items():
        columns = reader.CASE_EXPECTED if sheet == "cases" else reader.PRODUCT_EXPECTED
        for column in (c for c in columns if c in subject):
            checks = covered.get((sheet, key, column), [])
            assert checks, f"{key}: {column} has no check"
            items = {check.get("item") for check in checks}
            value = subject[column]
            if column in reader.NUMBER_LIST_COLUMNS:
                assert items >= set(range(1, len(value) + 1)), f"{key}: {column}"
            if column in reader.POSITION_COLUMNS:
                checked = set()
                for check in checks:
                    if check["recorded"] is True:
                        checked |= {int(p) for p in str(check["item"]).split(",")}
                assert checked == set(value), f"{key}: {column}"
                assert "other" in items, (
                    f"{key}: {column} has no check of the other weeks"
                )
            if column == "warnings":
                should = subject.get("priority") == "Should"
                codes = reader.WARNINGS if should else reader.WARNINGS[:-1]
                assert items == set(codes), f"{key}: warnings"


def test_the_check_summary_counts_every_match():
    """DR-3: the summary that the hand check reads beside the table in checks
    counts the matching checks and the checks, and says whether all match."""
    workbook = openpyxl.load_workbook(reader.WORKBOOK)
    sheet = workbook["checks"]
    summary = {sheet[f"J{row}"].value: sheet[f"K{row}"].value for row in (1, 2, 3)}
    assert summary == {
        "matching checks": "=COUNTIF(G:G,TRUE)",
        "checks": "=COUNTA(G:G)-1",
        "all match": "=K1=K2",
    }


def test_the_hand_check_is_recorded_with_its_date():
    """DR-3, AD-17: check_log records each check of the expected values with its
    date as ISO text, who made it, what it covered, how and the result."""
    log = reader.read_rows("check_log")
    assert log
    for entry in log:
        date.fromisoformat(entry["date"])
        assert all(entry.get(c) for c in ("checked_by", "scope", "method", "result")), (
            entry
        )


def test_the_latest_hand_check_covers_the_current_checks():
    """DR-3, AD-17: the latest check in check_log found every one of the checks
    in the sheet checks to match, so a workbook changed after its check, or a
    check that failed, fails here."""
    checks = sum("recorded" in check for check in reader.read_rows("checks"))
    latest = reader.read_rows("check_log")[-1]
    assert f"{checks} of {checks} checks match" in latest["result"], latest


def test_workbook_holds_no_local_path_or_user_name():
    """NFR-4: no part of the workbook holds a local file path, such as the
    absPath that Excel writes into a workbook it saves, and the file names only
    the group as its creator and no one as its last editor."""
    with zipfile.ZipFile(reader.WORKBOOK) as archive:
        hits = [n for n in archive.namelist() if LOCAL_PATH.search(archive.read(n))]
        core = archive.read("docProps/core.xml")
    assert hits == []
    assert b"<dc:creator>G40-lyamouri</dc:creator>" in core
    assert b"lastModifiedBy" not in core
