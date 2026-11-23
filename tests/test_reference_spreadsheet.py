"""The reference spreadsheet is the answer key (Story 1.5; DR-3, AD-17, FR-3, FR-21, NFR-4).

The tests read reference/reference-examples.xlsx with openpyxl and take the
list of reference examples from the PRD, so neither holds an expected value.
They use no database.
"""

import re
import zipfile
from datetime import date

import answer_key
import openpyxl
import pytest

# The columns that each FR-21 «value that changes» names.
FR21_COLUMNS = {
    "Base forecast (moving average)": ("base_forecast",),
    "Base forecast (exponential smoothing)": ("base_forecast",),
    "Optimistic and pessimistic scenario": ("optimistic", "pessimistic"),
    "Suggested order quantity": ("suggested_order_quantity",),
}
# A local path, such as the absPath that Excel writes into a workbook it saves.
LOCAL_PATH = re.compile(
    rb"absPath|/Users/|/home/|[A-Z]:\\Users\\|file:///", re.IGNORECASE
)
# How close a recorded value in the checks must be to the answer key's.
SAME = 1e-9


def test_every_reference_example_has_a_case_with_an_expected_result():
    """DR-3, AD-17, SM-1: every example in PRD §5.7, E1 to E30 with its lettered
    cases, has a case in the workbook, and every case has an expected value."""
    cases = answer_key.cases()
    examples = {case["example"] for case in cases}
    assert [e for e in answer_key.prd_reference_examples() if e not in examples] == []
    assert [c["case"] for c in cases if not answer_key.expected_values(c)] == []


def test_cases_quote_their_reference_example_from_the_prd():
    """DR-3: each case names the rule and priority of its example and quotes its
    input and expected result from PRD §5.7 verbatim, so an example changed in
    the PRD fails here until the workbook follows it."""
    prd = answer_key.prd_reference_examples()
    for case in answer_key.cases():
        if case["example"] == "FR-21":
            continue
        quoted = {column: case.get(column) for column in prd[case["example"]]}
        assert quoted == prd[case["example"]], case["case"]


def test_every_fr21_variant_has_its_expected_value():
    """FR-21, AD-17: each setting change that the FR-21 table describes beyond
    PRD §5.7, such as «E1 with window 4 instead of 3», is a case with the value
    it changes, calculated by hand, so that Story 3.2 reads it from the workbook."""
    cases = {case["case"]: case for case in answer_key.cases()}
    variants = {c["prd_input"]: c for c in cases.values() if c["example"] == "FR-21"}
    assert answer_key.prd_fr21_variants()
    for value, example in answer_key.prd_fr21_variants():
        variant = variants[example]
        assert all(column in variant for column in FR21_COLUMNS[value]), example
        assert variant["sales"] == cases[example.split(" with ")[0]]["sales"], example


def test_every_rule_test_product_has_its_series_stock_and_expected_results():
    """FR-3, DR-3: the products cover every example that FR-3 builds the rule
    test products from, and each product has its company, its series, its stock
    on hand and every expected result that FR-3 lists."""
    products = answer_key.products()
    covered = {e.strip() for p in products for e in p["examples"].split(",")}
    for example in answer_key.prd_rule_test_examples():
        assert any(c == example or c.startswith(f"{example} ") for c in covered), (
            example
        )
    required = ("company", "sales", "stock_on_hand", *answer_key.PRODUCT_EXPECTED)
    for product in products:
        assert [c for c in required if c not in product] == [], product["product"]


def test_a_product_named_after_an_example_uses_its_series():
    """FR-3, AD-15: a rule test product named after an example has the sales of
    that example's cases, so the product screen and the workbook show the same
    case."""
    series = {}
    for case in answer_key.cases():
        series.setdefault(case["example"], case["sales"])
    named = [p for p in answer_key.products() if p["product"] in series]
    assert named
    for product in named:
        assert product["sales"] == series[product["product"]], product["product"]


def test_every_value_follows_the_schema():
    """DR-3, AD-17: every cell parses as reference/README.md describes it (the
    readers raise otherwise), the keys are unique, the settings are the FR-20
    values, positions lie inside the series, the warnings are R-15's in its
    order, and the labels are R-16's."""
    cases, products = answer_key.cases(), answer_key.products()
    assert len({c["case"] for c in cases}) == len(cases)
    assert len({p["product"] for p in products}) == len(products)
    for case in cases:
        assert case["method"] in answer_key.METHODS, case["case"]
        assert case["unusual_weeks_setting"] in answer_key.UNUSUAL_WEEKS_SETTINGS
        assert case["seasonal_adjustment"] in answer_key.SEASONAL_ADJUSTMENT
        assert case["cycle_length"] in (4, 52), case["case"]
    for product in products:
        assert product["company"] in ("A", "B"), product["product"]
    for subject in cases + products:
        name = subject.get("case") or subject["product"]
        weeks = len(subject["sales"])
        for column in answer_key.POSITION_COLUMNS & subject.keys():
            assert all(1 <= p <= weeks for p in subject[column]), name
        if "warnings" in subject:
            assert set(subject["warnings"]) <= set(answer_key.WARNINGS), name
            assert subject["warnings"] == sorted(
                subject["warnings"], key=answer_key.WARNINGS.index
            ), name
        if "confidence_label" in subject:
            assert subject["confidence_label"] in answer_key.LABELS, name


def test_reader_refuses_a_formula_in_the_answer_key(tmp_path):
    """AD-17: the cases and products sheets hold values only. The reader refuses
    a formula, which openpyxl cannot calculate, instead of reading it as a
    missing value."""
    path = tmp_path / "answer-key.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "cases"
    sheet.append(["case", "base_forecast"])
    sheet.append(["E1", "=(16+12+15)/3"])
    workbook.save(path)
    with pytest.raises(ValueError, match=r"cases!B2 holds a formula"):
        answer_key.read_rows("cases", path)


def recorded_matches(value, column, item, recorded):
    """Whether a check records the answer key's value for the column."""
    if column in answer_key.NUMBER_LIST_COLUMNS:
        return abs(value[item - 1] - recorded) < SAME
    if column in answer_key.POSITION_COLUMNS:
        if isinstance(item, int):
            return recorded == (item in value)
        if item == "other":
            return recorded is False
        run = [int(p) for p in str(item).split(",")]
        return recorded is True and all(p in value for p in run)
    if column == "warnings":
        return recorded == (item in value)
    if column in answer_key.FLAG_COLUMNS:
        return recorded == ("yes" if value else "no")
    if column in answer_key.SHOWN_COLUMNS and value != "–":
        return recorded == float(value.replace(",", "."))
    if value is None:
        return recorded == answer_key.NONE
    if isinstance(value, str):
        return recorded == value
    return abs(value - recorded) < SAME


def test_every_expected_value_is_recalculated_in_the_checks():
    """DR-3, AD-17: the sheet checks recalculates every expected value with a
    visible formula: each element of a list, each listed position, and each
    warning of R-15. Each check records the value the answer key holds, so a
    value changed without its check fails."""
    subjects = {("cases", c["case"]): c for c in answer_key.cases()}
    subjects |= {("products", p["product"]): p for p in answer_key.products()}
    covered = {}
    for check in answer_key.read_rows("checks"):
        assert str(check["recalculated"]).startswith("="), check
        if "recorded" not in check:
            continue
        assert str(check["match"]).startswith("="), check
        subject = subjects[(check["sheet"], check["key"])]
        column, item = check["value"], check.get("item")
        assert column in subject, check
        assert recorded_matches(subject[column], column, item, check["recorded"]), check
        covered.setdefault((check["sheet"], check["key"], column), []).append(check)
    for (sheet, key), subject in subjects.items():
        columns = (
            answer_key.CASE_EXPECTED
            if sheet == "cases"
            else answer_key.PRODUCT_EXPECTED
        )
        for column in (c for c in columns if c in subject):
            checks = covered.get((sheet, key, column), [])
            assert checks, f"{key}: {column} has no check"
            items = {check.get("item") for check in checks}
            value = subject[column]
            if column in answer_key.NUMBER_LIST_COLUMNS:
                assert items >= set(range(1, len(value) + 1)), f"{key}: {column}"
            if column in answer_key.POSITION_COLUMNS:
                checked = set()
                for check in checks:
                    if check["recorded"] is True:
                        checked |= {int(p) for p in str(check["item"]).split(",")}
                assert checked == set(value), f"{key}: {column}"
            if column == "warnings":
                should = subject.get("priority") == "Should"
                codes = answer_key.WARNINGS if should else answer_key.WARNINGS[:-1]
                assert items == set(codes), f"{key}: warnings"


def test_the_hand_check_is_recorded_with_its_date():
    """DR-3, AD-17: check_log records each check of the expected values with its
    date, who made it, what it covered, how and the result."""
    log = answer_key.read_rows("check_log")
    assert log
    for entry in log:
        date.fromisoformat(entry["date"])
        assert all(entry.get(c) for c in ("checked_by", "scope", "method", "result")), (
            entry
        )


def test_workbook_holds_no_local_path():
    """NFR-4: no part of the workbook holds a local file path, such as the
    absPath that Excel writes into a workbook it saves."""
    with zipfile.ZipFile(answer_key.WORKBOOK) as archive:
        hits = [n for n in archive.namelist() if LOCAL_PATH.search(archive.read(n))]
    assert hits == []
