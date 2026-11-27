"""The weeks of cover, the order-soon status and the overview (Story 2.6).

R-12, FR-24, AD-2, UX-DR33, UX-DR35. The expected values of E13, E23 and E24 are read from
the reference spreadsheet, and the order-soon, units and without-forecast figures of
Testbedrift A from the approved mockup (AD-17). Its figure of 4 products with a warning is
the one UX-DR46 states, since the E8 product adds one to the mockup's 3. They use no
database.
"""

import json
from pathlib import Path

import answer_key
import answer_key_reader as reader
import pytest

from forecasting import display
from forecasting import forecast as core
from forecasting.overview import Neighbours, WeekFigures, build_overview
from forecasting.settings import ForecastSettings
from forecasting.weeks import Week

SEED_DIR = Path(__file__).resolve().parents[1] / "data" / "seed"


def row_of(name):
    return next(row for row in reader.cases() if row["case"] == name)


def settings_of(row):
    return ForecastSettings(
        method=row["method"],
        window=row["window"],
        smoothing_factor=row["smoothing_factor"],
        unusual_weeks_included=row["unusual_weeks_setting"] == "included",
        scenario_percentage=row["scenario_percentage"],
        safety_margin=row["safety_margin"],
    )


def result_of(row):
    weeks = [Week(week.units_sold, week.stockout) for week in row["sales"]]
    return core.forecast_product(weeks, row["stock_on_hand"], settings_of(row))


def steady(units, stock, length=5):
    """A product that sells `units` in each of `length` weeks, with `stock` on hand."""
    return core.forecast_product(
        [Week(units, False)] * length, stock, ForecastSettings()
    )


def too_little_data():
    """Two valid weeks: no forecast (R-6)."""
    return core.forecast_product([Week(8, False)] * 2, 3, ForecastSettings())


def seed_results(file_name):
    company = json.loads((SEED_DIR / file_name).read_text(encoding="utf-8"))
    results = {}
    for product in company["products"]:
        out = set(product["stockout_positions"])
        weeks = [
            Week(units, position in out)
            for position, units in enumerate(product["units_sold"], start=1)
        ]
        results[product["product_number"]] = core.forecast_product(
            weeks, product["stock_on_hand"], ForecastSettings()
        )
    return results


@pytest.mark.parametrize("name", ["E13 (E4)", "E13 (E6)"])
def test_the_weeks_of_cover_and_the_order_soon_status_are_the_spreadsheets(name):
    """R-12, E13, FR-24: weeks of cover is the stock ÷ the week-1 normal forecast, shown with
    one decimal, and order-soon status follows the suggested order quantity."""
    row = row_of(name)
    result = result_of(row)

    assert result.weeks_of_cover == pytest.approx(
        row["weeks_of_cover"], abs=reader.TOLERANCE
    )
    assert display.one_decimal(result.weeks_of_cover) == row["weeks_of_cover_shown"]
    assert result.order_soon is row["order_soon"]


def test_a_product_with_a_zero_forecast_has_no_cover_and_no_order_soon_status():
    """R-12, E23: weeks of cover is «–» (None) and there is no order-soon status."""
    row = row_of("E23")
    result = result_of(row)

    assert result.base_forecast == 0
    assert row["weeks_of_cover"] is None
    assert row["weeks_of_cover_shown"] == "–"
    assert result.weeks_of_cover is None
    assert result.order_soon is row["order_soon"] is False
    assert result.suggested_order_quantity == row["suggested_order_quantity"]


def test_a_product_without_a_forecast_has_no_cover_and_no_order_soon_status():
    """R-12, FR-8, FR-24: no forecast gives no weeks of cover and no order-soon status."""
    result = too_little_data()

    assert result.base_forecast is None
    assert result.weeks_of_cover is None
    assert result.order_soon is False


def test_a_stock_that_covers_the_need_is_not_order_soon_but_has_cover():
    """R-12: the stock covers the forecast plus the margin, so the quantity is 0 and the
    product is not order-soon; the cover is the stock ÷ the forecast."""
    result = steady(10, 11)

    assert result.suggested_order_quantity == 0
    assert result.order_soon is False
    assert result.weeks_of_cover == pytest.approx(1.1)


def test_floating_point_dust_above_the_need_is_not_order_soon():
    """R-9, R-12: 50 × 1.1 is 55.00000000000001, so the unrounded order is above 0, but the
    suggested quantity, rounded to 6 decimals and then up, is 0, and so is the status."""
    result = steady(50, 55)

    assert result.order_unrounded > 0
    assert result.suggested_order_quantity == 0
    assert result.order_soon is False


def test_a_stock_one_unit_short_of_the_need_is_order_soon():
    """R-12: the quantity is above 0 as soon as the stock is below forecast × (1 + margin)."""
    result = steady(10, 10)

    assert result.suggested_order_quantity == 1
    assert result.order_soon is True


def test_the_products_with_the_same_cover_are_sorted_by_product_number():
    """R-12, E24, FR-24: A and B both have weeks of cover 0.0, so A comes first; the
    positions are the spreadsheet's."""
    rows = {key: row_of(f"E24 ({key})") for key in "AB"}
    results = {row["product_number"]: result_of(row) for row in rows.values()}

    overview = build_overview(dict(reversed(results.items())), {})

    for row in rows.values():
        assert results[row["product_number"]].weeks_of_cover == row["weeks_of_cover"]
        assert (
            overview.order.index(row["product_number"]) + 1
            == (row["overview_position"])
        )
    assert overview.order_soon == ("A", "B")


def test_the_order_soon_products_are_sorted_by_the_cover_not_by_its_display():
    """R-12, AD-3: 0.34 and 0.31 both show «0,3», and the lower real value comes first
    although it has the higher product number."""
    results = {"A": steady(100, 34), "B": steady(100, 31)}

    overview = build_overview(results, {})

    assert [display.one_decimal(results[n].weeks_of_cover) for n in "AB"] == [
        "0,3",
        "0,3",
    ]
    assert overview.order_soon == ("B", "A")


def test_ties_are_broken_by_the_product_number_as_text():
    """R-12, E24: products with the same cover are sorted by their whole number, as text,
    so «10» comes before «2» and «10012» before «10021»."""
    tied = {number: steady(10, 4) for number in ("10021", "10012", "2", "10", "10005")}

    overview = build_overview(dict(reversed(tied.items())), {})

    assert overview.order_soon == ("10", "10005", "10012", "10021", "2")


def test_the_groups_come_in_the_order_of_r_12_each_by_its_own_key():
    """R-12, FR-24: order-soon by cover, then those without a forecast by number, then the
    others by number."""
    results = {
        "5": steady(10, 400),
        "9": too_little_data(),
        "2": steady(10, 8),
        "7": steady(10, 2),
        "3": too_little_data(),
        "1": steady(10, 400),
        "4": steady(10, 12),
        # A forecast of 0 is a forecast: no cover, no order-soon status, not «uten prognose».
        "6": steady(0, 0),
    }

    overview = build_overview(results, {})

    assert overview.order_soon == ("7", "2")
    assert overview.without_forecast == ("3", "9")
    assert overview.others == ("1", "4", "5", "6")
    assert overview.order == ("7", "2", "3", "9", "1", "4", "5", "6")


def test_the_week_figures_count_the_right_sets():
    """FR-24, UX-DR33: the order-soon products, the sum of the quantities, the products
    without a forecast and the products with an active warning, a product without a
    forecast included (its warning is insufficient data)."""
    results = {
        "1": steady(10, 2),
        "2": steady(10, 8),
        "3": steady(10, 400),
        "4": too_little_data(),
    }

    figures = build_overview(results, {}).figures

    assert figures == WeekFigures(
        order_soon=2,
        units_suggested=results["1"].suggested_order_quantity
        + results["2"].suggested_order_quantity,
        without_forecast=1,
        with_warning=1,
    )
    assert results["3"].warnings == ()
    assert results["4"].warnings == ("insufficient_data",)


def test_a_product_with_a_warning_and_a_forecast_counts_in_the_figures():
    """UX-DR33, FR-15: a stockout week in the recent period is an active warning."""
    sold_out = [Week(10, False)] * 4 + [Week(0, True)]
    results = {
        "1": core.forecast_product(sold_out, 400, ForecastSettings()),
        "2": steady(10, 400),
    }

    assert results["1"].warnings == ("stockout_weeks",)
    assert build_overview(results, {}).figures.with_warning == 1


def test_a_warning_does_not_decide_the_group_the_status_does():
    """R-12, AD-2: a product with a warning but no order-soon status is in the other
    products, and an order-soon product without a warning is in the first group."""
    sold_out = [Week(10, False)] * 4 + [Week(0, True)]
    warned = core.forecast_product(sold_out, 400, ForecastSettings())
    results = {"1": warned, "2": steady(10, 2)}

    overview = build_overview(results, {})

    assert warned.warnings and not warned.order_soon
    assert not results["2"].warnings and results["2"].order_soon
    assert (overview.order_soon, overview.others) == (("2",), ("1",))


def test_the_review_sequence_is_the_order_soon_products_and_then_those_without_forecast():
    """UX-DR32, UX-DR34: the other products are not in the sequence."""
    results = {
        "1": steady(10, 400),
        "2": too_little_data(),
        "3": steady(10, 2),
        "4": steady(10, 8),
    }

    assert build_overview(results, {}).review_sequence == ("3", "4", "2")


def test_each_product_has_its_previous_and_next_across_the_groups():
    """UX-DR35: the first has no previous, the last has no next, and the neighbours cross
    the borders between the groups."""
    results = {
        "1": steady(10, 400),
        "2": too_little_data(),
        "3": steady(10, 2),
        "4": steady(10, 8),
        "5": steady(10, 400),
    }

    neighbours = build_overview(results, {}).neighbours

    assert neighbours == {
        "3": Neighbours(None, "4"),
        "4": Neighbours("3", "2"),
        "2": Neighbours("4", "1"),
        "1": Neighbours("2", "5"),
        "5": Neighbours("1", None),
    }


def test_one_product_has_no_neighbours_and_no_products_give_an_empty_overview():
    """FR-24, UX-DR33, UX-DR35: edge cases of the groups, the figures and the links."""
    one = build_overview({"7": steady(10, 400)}, {})
    empty = build_overview({}, {})

    assert one.neighbours == {"7": Neighbours(None, None)}
    assert empty.order == empty.review_sequence == ()
    assert empty.neighbours == {}
    assert empty.figures == WeekFigures(0, 0, 0, 0)


def test_adjustments_are_refused_until_fr_29_is_built():
    """AD-2, FR-29: a non-empty adjustments input is an error, never ignored silently."""
    with pytest.raises(ValueError, match="FR-29"):
        build_overview({"1": steady(10, 2)}, {"1": 5})


def test_the_overview_does_not_change_the_results_or_depend_on_their_order():
    """AD-2: the same results in any order give the same overview."""
    results = {"1": steady(10, 2), "2": too_little_data(), "3": steady(10, 400)}

    forward = build_overview(results, {})
    backward = build_overview(dict(reversed(results.items())), {})

    assert forward == backward


def test_testbedrift_a_has_the_week_figures_of_the_mockup():
    """FR-24, UX-DR33, UX-DR46: 4 products to order soon, 31 units, 1 without a forecast and
    4 with a warning; the first three are the approved mockup's, and the warnings are the
    Epic 1 note's (the E8 product adds one to the mockup's 3)."""
    results = seed_results("testbedrift-a.json")
    mockup = answer_key.mockup_overview()

    overview = build_overview(results, {})

    assert overview.figures == WeekFigures(
        order_soon=mockup["order_soon"],
        units_suggested=mockup["units"],
        without_forecast=mockup["without_forecast"],
        with_warning=4,
    )
    assert overview.without_forecast == ("10040",)
    assert len(overview.order) == mockup["products"]
    assert sorted(overview.order) == sorted(results)


def test_every_seed_company_gets_a_complete_overview():
    """FR-24, AD-2, UX-DR33, UX-DR35: every product is in exactly one group and has its
    neighbours, each group follows its key, and the figures and the review sequence are
    those of the groups, for both test companies."""
    for file_name in ("testbedrift-a.json", "testbedrift-b.json"):
        results = seed_results(file_name)
        overview = build_overview(results, {})
        groups = (overview.order_soon, overview.without_forecast, overview.others)

        assert sum(len(group) for group in groups) == len(results)
        assert overview.order == (*groups[0], *groups[1], *groups[2])
        assert sorted(overview.order) == sorted(results)
        covers = [(results[n].weeks_of_cover, n) for n in overview.order_soon]
        assert covers == sorted(covers)
        assert all(results[n].order_soon for n in overview.order_soon)
        assert all(results[n].base_forecast is None for n in overview.without_forecast)
        assert list(overview.without_forecast) == sorted(overview.without_forecast)
        assert list(overview.others) == sorted(overview.others)
        assert not any(results[n].order_soon for n in overview.others)
        assert overview.review_sequence == (*groups[0], *groups[1])
        assert overview.figures == WeekFigures(
            order_soon=len(groups[0]),
            units_suggested=sum(
                r.suggested_order_quantity or 0 for r in results.values()
            ),
            without_forecast=len(groups[1]),
            with_warning=sum(1 for r in results.values() if r.warnings),
        )
        assert overview.neighbours == {
            number: Neighbours(
                overview.order[i - 1] if i else None,
                overview.order[i + 1] if i + 1 < len(overview.order) else None,
            )
            for i, number in enumerate(overview.order)
        }
