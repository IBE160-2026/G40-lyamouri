"""The loader of a company's forecast data (Story 2.7; AD-2, AD-7, AD-9, NFR-8).

They use the database, and the expected results are the core's own for the same weeks.
"""

from datetime import date, timedelta
from decimal import Decimal

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext

from forecasting import forecast as core
from forecasting.overview import build_overview
from forecasting.settings import ForecastSettings
from forecasting.weeks import Week
from web import company_data
from web.models import Company, CompanySettings, Product, SalesWeek


def add_product(company, number, units, stock=10, stockouts=(), last_week=(2026, 45)):
    """A product whose weeks end at last_week, with the weeks stored in the given order."""
    product = Product.objects.create(
        company=company, product_number=number, name=f"P{number}", stock_on_hand=stock
    )
    monday = date.fromisocalendar(*last_week, 1)
    SalesWeek.objects.bulk_create(
        SalesWeek(
            product=product,
            position=position,
            iso_year=iso.year,
            iso_week=iso.week,
            units_sold=sold,
            stockout=position in stockouts,
        )
        for position, sold in enumerate(units, start=1)
        for iso in [(monday - timedelta(weeks=len(units) - position)).isocalendar()]
    )
    return product


def weeks_of(units, stockouts=()):
    return [Week(sold, p in stockouts) for p, sold in enumerate(units, start=1)]


@pytest.fixture
def company(db):
    return Company.objects.create(customer_number="9001", name="Lastebedrift")


def test_every_product_gets_the_result_of_the_core_for_its_own_weeks(company):
    """AD-2: the result of each product equals `forecast_product` on that product's
    weeks and stock, so the weeks of one product never go to another, also when a
    product has no weeks between two that have, and when weeks are stored out of order."""
    add_product(company, "10001", (12, 15, 11, 14, 13, 16, 12, 15), stock=5)
    Product.objects.create(
        company=company, product_number="10002", name="Uten uker", stock_on_hand=3
    )
    add_product(company, "10003", (0, 4, 0, 4, 9, 3, 8), stock=0, stockouts=(1, 3))
    # The weeks of this product are written from the last to the first.
    last = Product.objects.create(
        company=company, product_number="10004", name="Baklengs", stock_on_hand=2
    )
    for position in (4, 3, 2, 1):
        SalesWeek.objects.create(
            product=last,
            position=position,
            iso_year=2026,
            iso_week=41 + position,
            units_sold=position * 10,
            stockout=False,
        )

    data = company_data.load_company_data(company)

    expected = {
        "10001": core.forecast_product(
            weeks_of((12, 15, 11, 14, 13, 16, 12, 15)), 5, ForecastSettings()
        ),
        "10002": core.forecast_product([], 3, ForecastSettings()),
        "10003": core.forecast_product(
            weeks_of((0, 4, 0, 4, 9, 3, 8), (1, 3)), 0, ForecastSettings()
        ),
        "10004": core.forecast_product(
            weeks_of((10, 20, 30, 40)), 2, ForecastSettings()
        ),
    }
    assert data.results == expected
    assert [p.product_number for p in data.product_list] == sorted(expected)
    assert data.latest_week == (2026, 45)


def test_the_overview_is_built_from_the_results(company):
    """AD-2: the loader gives the overview of build_overview for the same results."""
    add_product(company, "10001", (12, 15, 11, 14, 13, 16, 12, 15), stock=5)
    add_product(company, "10002", (5, 5, 5), stock=100)

    data = company_data.load_company_data(company)

    assert data.overview == build_overview(data.results, {})
    assert data.overview.order == ("10001", "10002")


def test_a_company_without_a_settings_row_gets_the_fr_20_defaults(company):
    """FR-20, AD-9: no row means the defaults of the core."""
    add_product(company, "10001", (5, 6, 7))

    data = company_data.load_company_data(company)

    assert data.results["10001"].settings == ForecastSettings()


def test_a_company_gets_its_own_settings_and_never_another_companys(two_companies):
    """FR-20, AD-7: B has a settings row and A has none, so A has the defaults, and B's row
    is B's alone."""
    a, b = two_companies
    CompanySettings.objects.create(company=b.company, window=7, safety_margin=30)

    assert company_data.load_company_data(a.company).results["10001"].settings == (
        ForecastSettings()
    )
    settings_b = company_data.load_company_data(b.company).results["10001"].settings
    assert (settings_b.window, settings_b.safety_margin) == (7, 30)


def test_every_setting_of_the_row_reaches_the_core(company):
    """FR-20, AD-9: the method, the window, the factor, the unusual weeks, the
    scenario percentage and the safety margin of the row are the core's settings."""
    add_product(company, "10001", (5, 6, 7, 8, 9, 10))
    CompanySettings.objects.create(
        company=company,
        method="exponential_smoothing",
        window=5,
        smoothing_factor=Decimal("0.6"),
        unusual_weeks_included=False,
        scenario_percentage=25,
        safety_margin=40,
    )

    data = company_data.load_company_data(company)

    assert data.results["10001"].settings == ForecastSettings(
        method="exponential_smoothing",
        window=5,
        smoothing_factor=Decimal("0.6"),
        unusual_weeks_included=False,
        scenario_percentage=25,
        safety_margin=40,
    )


def test_a_company_without_products_has_no_week(company):
    """AD-8: nothing to load gives empty results and no latest week."""
    data = company_data.load_company_data(company)

    assert data.results == {}
    assert data.product_list == ()
    assert data.latest_week is None
    assert data.overview.order == ()


def test_only_the_given_companys_products_are_loaded(two_companies):
    """AD-7: both companies have a product 10001, and each loader call gives its own."""
    a, b = two_companies

    data_a = company_data.load_company_data(a.company)
    data_b = company_data.load_company_data(b.company)

    assert set(data_a.results) == {"10001", "10002", "10003"}
    assert set(data_b.results) == {"10001", "20001"}
    assert data_a.results["10001"].stock_on_hand == 7371
    assert data_b.results["10001"].stock_on_hand == 8481
    assert data_a.latest_week == (2026, 45)
    assert data_b.latest_week == (2026, 44)


def queries_of(function, *args):
    with CaptureQueriesContext(connection) as queries:
        function(*args)
    return len(queries)


@pytest.mark.parametrize("products", [1, 3, 50])
def test_the_number_of_queries_does_not_depend_on_the_number_of_products(
    company, products
):
    """AD-2, NFR-8: settings, products, sales weeks and the latest week are four
    queries for 1, 3 or 50 products of 104 weeks."""
    units = tuple(10 + week % 7 for week in range(104))
    for number in range(products):
        add_product(company, f"{10000 + number}", units, stock=number)

    assert queries_of(company_data.load_company_data, company) == 4
