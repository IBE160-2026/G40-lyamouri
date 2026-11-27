"""Every warning and every confidence label comes from a seed product (Story 2.5).

SM-7, SM-10, FR-3, FR-8, FR-15 to FR-19. The core runs for every product of both test
companies with the FR-20 defaults, as the loader will (Story 2.6). No test uses the
database, and the seed files are read, never changed.
"""

import json
from datetime import timedelta
from pathlib import Path

import answer_key
import generate_seed
import pytest

from explanation import trust as words
from forecasting import forecast as core
from forecasting import trust
from forecasting.overview import build_overview
from forecasting.settings import ForecastSettings
from forecasting.weeks import Week

SEED_DIR = Path(__file__).resolve().parents[1] / "data" / "seed"
FILES = ("testbedrift-a.json", "testbedrift-b.json")


def results(files=FILES):
    """(product, result, latest ISO year and week) for every product of the companies."""
    found = []
    for name in files:
        company = json.loads((SEED_DIR / name).read_text(encoding="utf-8"))
        for product in company["products"]:
            out = set(product["stockout_positions"])
            weeks = [
                Week(units, position in out)
                for position, units in enumerate(product["units_sold"], start=1)
            ]
            monday = generate_seed.monday_of(
                *generate_seed.parse_week(product["first_week"])
            ) + timedelta(weeks=len(weeks) - 1)
            latest = (monday.isocalendar().year, monday.isocalendar().week)
            result = core.forecast_product(
                weeks, product["stock_on_hand"], ForecastSettings()
            )
            found.append((product, result, latest))
    return found


RESULTS = results()


def test_every_warning_is_triggered_by_at_least_one_test_product():
    """SM-7, FR-3, FR-8, FR-15 to FR-18: stockout weeks, unusual weeks, a level shift, old
    data and insufficient data are each active for a seed product."""
    triggered = {warning for _, result, _ in RESULTS for warning in result.warnings}

    assert triggered == set(trust.WARNINGS)


def test_every_confidence_label_including_high_is_given_to_a_test_product():
    """SM-7, FR-19: «lav», «middels» and «høy» each belong to a seed product, and so do the
    conditions of R-16 below that the data can show; no seed product has fewer calculation
    weeks than the window or fewer than 100 valid weeks without a warning, and E11 b and
    E29 g in the spreadsheet cover those."""
    labels = {result.confidence_label for _, result, _ in RESULTS}
    conditions = {result.confidence_condition for _, result, _ in RESULTS}

    assert labels == {trust.LAV, trust.MIDDELS, trust.HOY}
    assert conditions >= {
        core.TOO_FEW_VALID_WEEKS,
        trust.FEWER_THAN_12_VALID_WEEKS,
        trust.ACTIVE_WARNING,
        trust.SHORT_HISTORY,
        trust.ALL_CLEAR,
    }


def test_a_product_is_low_because_it_has_too_few_valid_weeks_for_the_sm_10_check():
    """SM-10, FR-19, FR-25: Snøskuffe aluminium has 2 valid weeks, and its reason names the
    condition that decided the label, as the product screen will show it."""
    ((_product, result, _),) = (
        found for found in RESULTS if found[0]["name"] == "Snøskuffe aluminium"
    )

    assert len(result.valid_weeks) == 2
    assert result.confidence_label == trust.LAV
    assert result.confidence_condition == core.TOO_FEW_VALID_WEEKS
    assert words.confidence_reason(result).startswith(
        "Lav: ingen prognose, færre enn 3 gyldige uker."
    )
    assert words.list_text(result) == "Ingen prognose: færre enn 3 gyldige uker"


@pytest.mark.parametrize(
    "found", RESULTS, ids=lambda found: f"{found[0]['product_number']}"
)
def test_every_product_has_its_texts_and_they_match_its_result(found):
    """AD-4, AD-5, FR-7, FR-19: each product has a reason that starts with its label, one
    text for each active warning but the level shift, and the FR-7 note with a forecast."""
    _product, result, latest = found
    reason = words.confidence_reason(result)
    warning_codes = [text.code for text in words.warning_texts(result, *latest)]

    assert reason.startswith(
        {"lav": "Lav: ", "middels": "Middels: ", "høy": "Høy: "}[
            result.confidence_label
        ]
    )
    assert warning_codes == [w for w in result.warnings if w != trust.LEVEL_SHIFT]
    assert bool(words.note_texts(result)) == (result.base_forecast is not None)
    assert (words.list_text(result) is None) == (result.base_forecast is not None)


def test_denne_uken_for_testbedrift_a_matches_the_mockup_and_the_ux_flow():
    """UX-DR46, FR-24, E13, E24: the core gives Testbedrift A the week figures of the mockup
    and Flow 1 (4 products to order soon, 31 units, 1 without a forecast, 4 with a
    warning), each product of the mockup its quantity and its trust label, and the other 26
    products no warning, no stockout week and no unusual week. This replaces
    the stand-in R-8 of `test_seed_data.py` (Story 1.6, VG-2, AA-2)."""
    found = results(FILES[:1])
    by_number = {product["product_number"]: result for product, result, _ in found}
    mockup = answer_key.mockup_products()
    shown = answer_key.mockup_overview()
    e8 = generate_seed.COMPANIES[0]["from_workbook"]["E8"][0]
    with_warning = {
        mockup["Strøsand 25 kg"]["number"],
        mockup["Skruer 4×40 mm, 200 stk."]["number"],
        mockup["Snøskuffe aluminium"]["number"],
        e8,
    }

    figures = build_overview(by_number, {}).figures

    assert len(by_number) == shown["products"]
    assert (figures.order_soon, figures.units_suggested, figures.without_forecast) == (
        shown["order_soon"],
        shown["units"],
        shown["without_forecast"],
    )
    assert figures.with_warning == 4
    assert {n for n, r in by_number.items() if r.warnings} == with_warning
    for name, product in mockup.items():
        result = by_number[product["number"]]
        quantity = result.suggested_order_quantity
        assert ("–" if quantity is None else str(quantity)) == product["quantity"], name
        assert result.confidence_label == product["label"], name
    for number in set(by_number) - with_warning:
        result = by_number[number]
        assert not result.warnings, number
        assert len(result.valid_weeks) == result.history_length, number
        assert not result.unusual_weeks, number
