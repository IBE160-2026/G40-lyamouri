"""The one loader of a company's forecast data (AD-2, AD-7, NFR-8).

It reads the company's settings, products and sales weeks through `web/queries.py` in a
fixed number of queries, whatever the number of products, calls the core for each product
and builds the overview. The results are never stored (AD-2). Nothing else calculates,
rounds, sorts or groups domain values for a page.
"""

from dataclasses import dataclass
from itertools import groupby
from operator import itemgetter

from forecasting.forecast import forecast_product
from forecasting.overview import build_overview
from forecasting.settings import ForecastSettings
from forecasting.weeks import Week
from web import queries


@dataclass(frozen=True)
class CompanyData:
    """What a page needs of a company: its products by product number, the result and
    the overview of each, and the latest data week as an ISO year and week, or None
    when the company has no sales week (AD-8). `results` is keyed by product number."""

    product_list: tuple
    results: dict
    overview: object
    latest_week: tuple[int, int] | None


def forecast_settings(row):
    """The core's settings from the company's settings row. Without a row, or for what
    the row does not hold, the FR-20 defaults of the core apply (AD-9)."""
    if row is None:
        return ForecastSettings()
    return ForecastSettings(
        method=row.method,
        window=row.window,
        smoothing_factor=row.smoothing_factor,
        unusual_weeks_included=row.unusual_weeks_included,
        scenario_percentage=row.scenario_percentage,
        safety_margin=row.safety_margin,
    )


def load_company_data(company):
    """Read the company's data in four queries and calculate every product."""
    settings = forecast_settings(queries.settings_for_company(company))
    products = tuple(queries.products_for_company(company))
    weeks = {
        product_id: tuple(Week(units, stockout) for _, units, stockout in rows)
        for product_id, rows in groupby(
            queries.sales_weeks_for_company(company), key=itemgetter(0)
        )
    }
    results = {
        product.product_number: forecast_product(
            weeks.get(product.id, ()), product.stock_on_hand, settings
        )
        for product in products
    }
    # No adjustments until FR-29 (Epic 8).
    return CompanyData(
        product_list=products,
        results=results,
        overview=build_overview(results, {}),
        latest_week=queries.latest_data_week(company),
    )
