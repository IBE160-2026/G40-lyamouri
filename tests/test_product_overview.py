"""The product overview and the app header (Story 1.8; FR-2, AD-3, AD-7, AD-12,
UX-DR14, NFR-10).

Epic 2 replaces the list, so these tests check only what this story builds.
"""

import re
from unittest import mock

import pytest
from django.db import OperationalError, connection
from django.db.backends.base.base import BaseDatabaseWrapper
from django.test import Client
from django.test.utils import CaptureQueriesContext
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateUsed,
)
from test_error_pages import assert_error_page

from web import queries
from web.models import Company, Product, SalesWeek


def rows(response):
    """The (number, name, stock) of each row of the product table."""
    body = response.content.decode().split("<tbody>")[1]
    return [
        tuple(re.findall(r"<td[^>]*>(.*?)</td>", row))
        for row in re.findall(r"<tr>(.*?)</tr>", body, re.DOTALL)
    ]


def test_overview_lists_only_the_companys_products_by_product_number(
    client, two_companies
):
    """FR-2: the list holds the logged-in company's products with the product
    number, the name and the stock on hand, by product number."""
    a, _ = two_companies
    Product.objects.create(
        company=a.company, product_number="09999", name="Først", stock_on_hand=1
    )
    client.force_login(a.company)

    response = client.get("/produkter/")

    assertTemplateUsed(response, "web/products.html")
    assert rows(response) == [
        ("09999", "Først", "1"),
        ("10001", "Hammer fra A", "7371"),
        ("10002", "Sag fra A", "7372"),
        ("10003", "Tang fra A", "7373"),
    ]
    assertContains(response, "<title>Produktoversikt – Prognose</title>", html=True)
    assert response.content.decode().count("<h1") == 1


@pytest.mark.parametrize(
    ("index", "header"),
    [
        (0, "Testbedrift A · siste registrerte uke: uke 45, 2026"),
        (1, "Testbedrift B · siste registrerte uke: uke 44, 2026"),
    ],
)
def test_app_header_shows_the_company_and_its_own_latest_week(
    client, two_companies, index, header
):
    """UX-DR14, AD-3, AD-8: the header shows the company and the week label from
    forecasting/display.py, and the week is each company's own: A ends in week
    45 and B in week 44."""
    client.force_login(two_companies[index].company)

    response = client.get("/produkter/")

    assertContains(response, f'<span class="header-meta">{header}</span>', html=True)
    assertContains(
        response,
        '<a href="/produkter/" aria-current="page">Produktoversikt</a>',
        html=True,
    )
    assertContains(response, '<nav class="header-nav" aria-label="Hovedmeny">')
    assertContains(response, '<span class="wordmark">Prognose</span>', html=True)


def test_app_header_without_sales_weeks_has_only_the_company(client, db):
    """UX-DR14, AD-8: a company with no sales weeks has no latest week to show."""
    company = Company.objects.create_user("5000", "x", name="Tom bedrift")
    client.force_login(company)

    response = client.get("/produkter/")

    assertContains(response, '<span class="header-meta">Tom bedrift</span>', html=True)
    assertNotContains(response, "siste registrerte uke")


def test_latest_data_week_is_derived_from_the_sales_weeks(two_companies, db):
    """AD-8, AD-7: the latest data week is the company's latest ISO year and
    week, and none for a company without data."""
    a, b = two_companies
    empty = Company.objects.create_user("5000", "x", name="Tom bedrift")

    assert queries.latest_data_week(a.company) == (2026, 45)
    assert queries.latest_data_week(b.company) == (2026, 44)
    assert queries.latest_data_week(empty) is None


def test_latest_data_week_crosses_the_new_year(db):
    """AD-8, AD-3: the latest week is the latest year first, then the week, so a
    history that runs over New Year ends in week 2 of 2026, not week 52 of
    2025, and the header says so."""
    company = Company.objects.create_user("5000", "x", name="Nyttår AS")
    product = Product.objects.create(
        company=company, product_number="50001", name="Gave", stock_on_hand=1
    )
    SalesWeek.objects.bulk_create(
        SalesWeek(
            product=product,
            position=position,
            iso_year=year,
            iso_week=week,
            units_sold=1,
            stockout=False,
        )
        for position, (year, week) in enumerate(
            [(2025, 51), (2025, 52), (2026, 1), (2026, 2)], start=1
        )
    )
    client = Client()
    client.force_login(company)

    assert queries.latest_data_week(company) == (2026, 2)
    assertContains(
        client.get("/produkter/"), "Nyttår AS · siste registrerte uke: uke 2, 2026"
    )


def test_logged_in_page_has_the_shell_and_the_app_header(client, two_companies):
    """NFR-11, NFR-6, NFR-1, AD-11, UX-DR14: the overview has Norwegian as its
    language, the viewport tag, the local stylesheet, one h1, the one local
    script and no URL with a host, and its header holds the wordmark, the company line and the
    navigation, in that order."""
    client.force_login(two_companies[0].company)

    content = client.get("/produkter/").content.decode()

    assert content.startswith("<!doctype html>\n")
    assert '<html lang="nb">' in content
    assert (
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        in content
    )
    assert '<link rel="stylesheet" href="/static/web/app.css">' in content
    assert content.count("<h1") == 1
    # The one optional script of AD-11, local and deferred, and nothing else.
    assert content.count("<script") == 1
    assert '<script src="/static/web/app.js" defer></script>' in content
    assert not re.search(r'(?:src|href)="(?:[a-z]+:)?//', content)
    header = content[content.index("<header") : content.index("</header>")]
    assert (
        header.index("wordmark")
        < header.index("header-meta")
        < header.index("header-nav")
    )


def test_overview_uses_the_same_queries_for_any_number_of_products(
    client, two_companies
):
    """AD-7: the page does not look up each product separately."""
    a, _ = two_companies
    client.force_login(a.company)

    def count():
        with CaptureQueriesContext(connection) as captured:
            assert client.get("/produkter/").status_code == 200
        return len(captured)

    before = count()
    for number in range(30000, 30020):
        Product.objects.create(
            company=a.company, product_number=str(number), name="Ny", stock_on_hand=3
        )

    assert count() == before


def test_overview_answers_get_and_head_only(client, two_companies):
    """AD-10: the overview only shows information."""
    client.force_login(two_companies[0].company)

    assert client.head("/produkter/").status_code == 200
    assert client.post("/produkter/").status_code == 405


def test_error_page_of_a_logged_in_user_shows_no_company_data(client, two_companies):
    """AD-12, NFR-10: an unknown address gives the wordmark-only not-found page
    to a logged-in user too, with no company name, week or product."""
    client.force_login(two_companies[0].company)

    response = client.get("/finnes-ikke/")

    assert_error_page(response, 404, "Not found")
    assertNotContains(response, "Testbedrift A", status_code=404)
    assertNotContains(response, "Logg ut", status_code=404)


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("get", "/produkter/"),
        ("get", "/"),
        ("post", "/logg-ut/"),
        ("get", "/finnes-ikke/"),
    ],
)
def test_logged_in_user_with_a_stopped_database_gets_the_503_page(
    two_companies, method, path
):
    """AD-12, NFR-10: when the database does not answer, any page, also one that
    only reads the session, gives the 503 page, without the parts of the layout
    that read the database (the company, the week, the logout form)."""
    client = Client(raise_request_exception=False)
    client.force_login(two_companies[0].company)

    with mock.patch.object(
        BaseDatabaseWrapper,
        "ensure_connection",
        side_effect=OperationalError("Testfeil"),
    ):
        response = getattr(client, method)(path)

    if path == "/finnes-ikke/":
        # No view runs for an unknown address, so nothing reads the database.
        assert_error_page(response, 404, "Not found")
        return
    assert_error_page(response, 503, "Database unavailable")
    assertNotContains(response, "Testbedrift A", status_code=503)
    assertNotContains(response, "Logg ut", status_code=503)
    assertNotContains(response, "Testfeil", status_code=503)
