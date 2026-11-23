"""Every read of company data (AD-7).

Each function takes the logged-in company first and filters by it, so no page can
reach another company's data. Only load_seed and the migrations touch the tables
in other ways.
"""

from web.models import Product, SalesWeek


def products_for_company(company):
    """The company's products by product number (FR-2)."""
    return Product.objects.filter(company=company).order_by("product_number")


def latest_data_week(company):
    """The latest ISO year and week among the company's sales weeks, or None.

    It is derived from the data and never stored (AD-8).
    """
    return (
        SalesWeek.objects.filter(product__company=company)
        .order_by("-iso_year", "-iso_week")
        .values_list("iso_year", "iso_week")
        .first()
    )
