"""The two-account test: a company sees only its own data (Story 1.8; FR-2, SM-4,
AD-7).

Every story that adds a route or a list adds it to ROUTES, with what it shows
of a company's data, so that the test checks it for both companies (AD-7).
"""

import ast
import inspect
import re
from pathlib import Path

import pytest
from django.test import Client

from web import queries
from web.models import CompanySettings, Product

SRC = Path(__file__).resolve().parents[1] / "src"
# Every route that shows company data, with its method (AD-7). A route that takes
# a product number gives the same 404 page for another company's product as for an
# unknown address (test_product_screen.py). Both companies have a product 10001.
ROUTES = [("get", "/produkter/"), ("get", "/produkter/10001/")]
# What each company's pages may show, and the other's may never show.
OWN = {
    0: [
        "Testbedrift A",
        "Hammer fra A",
        "Sag fra A",
        "Tang fra A",
        "7371",
        "7372",
        "7373",
        "uke 45, 2026",
    ],
    1: ["Testbedrift B", "Spade fra B", "Rive fra B", "8481", "8482", "uke 44, 2026"],
}
# The files that may use a model manager for company data: the queries module
# and the seed loader (AD-7), and the seed reader, whose «products» are plain
# records read from files that touch no database. The models and the
# migrations only define the managers.
MANAGER_USERS = {
    "web/queries.py",
    "web/management/commands/load_seed.py",
    "web/seed.py",
}
COMPANY_MODELS = ("Product", "SalesWeek", "CompanySettings", "Company")
# The ways round a function in queries.py: another manager and the related managers.
MANAGER_NAMES = {
    "_default_manager",
    "_base_manager",
    "products",
    "sales_weeks",
    "company_settings",
}


TOKEN = re.compile(r'name="csrfmiddlewaretoken" value="[^"]+"')


def page(client, method, path):
    """The page as text, without the masked CSRF tokens, which are random text
    that could hold any digits."""
    return TOKEN.sub("", getattr(client, method)(path).content.decode())


@pytest.mark.parametrize(("method", "path"), ROUTES)
@pytest.mark.parametrize("index", [0, 1])
def test_each_company_sees_only_its_own_data(two_companies, index, method, path):
    """FR-2, SM-4: logged in as A, no page shows a name, a stock figure or a week of B,
    and the other way round."""
    own, other = two_companies[index], two_companies[1 - index]
    client = Client()
    client.force_login(own.company)

    content = page(client, method, path)

    for text in OWN[index]:
        assert text in content, text
    for text in OWN[1 - index]:
        assert text not in content, text
    assert other.company.name not in content


@pytest.mark.parametrize(("method", "path"), ROUTES)
def test_company_pages_are_not_kept_by_the_browser(two_companies, method, path):
    """FR-2, NFR-10: a page with company data says that no cache may keep it, so
    Back after «Logg ut» asks the server and gets the login page instead of the
    company's list from the history."""
    client = Client()
    client.force_login(two_companies[0].company)

    response = getattr(client, method)(path)

    assert "no-store" in response["Cache-Control"]
    assert "private" in response["Cache-Control"]


def test_a_shared_product_number_shows_each_companys_own_product(two_companies):
    """FR-2, AD-7: both companies have a product 10001, and each sees its own
    name and stock, never the other's."""
    for index, (name, stock) in enumerate(
        [("Hammer fra A", 7371), ("Spade fra B", 8481)]
    ):
        client = Client()
        client.force_login(two_companies[index].company)

        content = client.get("/produkter/").content.decode()

        assert re.search(
            rf"<td>10001</td>\s*<td><a [^>]*>{name}</a></td>\s*<td class=\"number\">{stock}</td>",
            content,
        )


def test_two_logged_in_companies_at_once_keep_their_own_data(two_companies):
    """FR-2, SM-4: two browsers logged in at the same time each get their own company's page."""
    a_client, b_client = Client(), Client()
    a_client.force_login(two_companies[0].company)
    b_client.force_login(two_companies[1].company)

    assert "Hammer fra A" in a_client.get("/produkter/").content.decode()
    assert "Spade fra B" in b_client.get("/produkter/").content.decode()
    assert "Spade fra B" not in a_client.get("/produkter/").content.decode()


def test_logging_in_as_another_company_replaces_the_first(two_companies):
    """FR-1, FR-2: a browser that logs in as B after A shows B's data, with nothing left of A's."""
    a, b = two_companies
    client = Client()
    client.post("/", {"customer_number": "1001", "password": a.password})
    client.post("/", {"customer_number": "1002", "password": b.password})

    content = client.get("/produkter/").content.decode()

    assert "Rive fra B" in content
    assert "Hammer fra A" not in content


def test_queries_return_only_the_given_companys_rows(two_companies):
    """AD-7: the data access gives a company its own products, and never the other's."""
    a, b = two_companies

    assert {p.name for p in queries.products_for_company(a.company)} == {
        "Hammer fra A",
        "Sag fra A",
        "Tang fra A",
    }
    assert {p.name for p in queries.products_for_company(b.company)} == {
        "Spade fra B",
        "Rive fra B",
    }
    assert Product.objects.count() == 5


def test_the_sales_week_and_settings_queries_return_only_the_given_companys_rows(
    two_companies,
):
    """AD-7: the sales weeks come only from the company's own products (3 weeks each),
    and a company without a settings row gets none, never another company's."""
    a, b = two_companies
    CompanySettings.objects.create(company=b.company, window=7)

    rows = list(queries.sales_weeks_for_company(a.company))

    assert {product_id for product_id, _, _ in rows} == {
        p.id for p in Product.objects.filter(company=a.company)
    }
    assert len(rows) == 9
    assert queries.settings_for_company(a.company) is None
    assert queries.settings_for_company(b.company).window == 7


def test_every_query_function_takes_the_company_first():
    """AD-7: each function in web/queries.py takes the logged-in company as its first argument."""
    functions = [
        function
        for _, function in inspect.getmembers(queries, inspect.isfunction)
        if function.__module__ == queries.__name__
    ]

    assert functions
    for function in functions:
        assert next(iter(inspect.signature(function).parameters)) == "company", function


def reads_company_data(tree):
    """The line numbers in a parsed module that use a manager, a related manager
    or a company model outside queries.py. Any `.objects` counts, whatever it
    hangs on (`models.Product.objects` too), and so does importing a company
    model by any name, or `get_model`."""
    lines = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Attribute)
            and (node.attr == "objects" or node.attr in MANAGER_NAMES | {"get_model"})
            or isinstance(node, ast.ImportFrom)
            and {alias.name for alias in node.names} & set(COMPANY_MODELS)
        ):
            lines.append(node.lineno)
    return lines


def test_no_view_or_form_uses_a_model_manager_for_company_data():
    """AD-7: outside web/queries.py, the seed loader, the seed reader, the models
    and the migrations, no code in web/ reaches company data except through
    queries.py. The source is read with ast, so a comment does not count."""
    offenders = []
    for path in sorted((SRC / "web").rglob("*.py")):
        relative = path.relative_to(SRC).as_posix()
        if relative in MANAGER_USERS or "/migrations/" in relative:
            continue
        if relative == "web/models.py":
            # The models module defines the company models and their managers.
            continue
        lines = reads_company_data(ast.parse(path.read_text(encoding="utf-8")))
        offenders += [f"{relative}:{line}" for line in lines]

    assert offenders == []


@pytest.mark.parametrize(
    "source",
    [
        "from web import models\nmodels.Product.objects.all()\n",
        "from web.models import Product as P\n",
        "apps.get_model('web', 'Product')\n",
        "request.user.products.all()\n",
    ],
)
def test_the_scan_finds_a_manager_behind_a_module_or_an_alias(source):
    """AD-7: the scan above flags `models.Product.objects`, an aliased import of
    a company model, `apps.get_model` and a related manager, so it cannot be
    passed by qualifying the name."""
    assert reads_company_data(ast.parse(source))


def test_no_template_reads_company_data_through_a_related_manager():
    """AD-7: a template never walks from the company to its data
    (`company.products.all`), which would be a read outside queries.py."""
    templates = sorted((SRC / "web" / "templates").rglob("*.html"))
    offenders = [
        path.name
        for path in templates
        if re.search(
            r"\.(?:products|sales_weeks|company_settings|objects)\b",
            path.read_text(encoding="utf-8"),
        )
    ]

    assert templates
    assert offenders == []


def test_the_seed_companies_see_only_their_own_products(seeded):
    """FR-1, FR-2, SM-4: with the real seed data and the real passwords, each test
    company logs in and sees its own 30 or 32 products and its own latest week
    (A ends in week 45, B in week 44), and none of the other's product numbers."""
    for number, password, count, week, mine, theirs in [
        ("1001", "testbedrift-a", 30, "uke 45, 2026", "100", "200"),
        ("1002", "testbedrift-b", 32, "uke 44, 2026", "200", "100"),
    ]:
        client = Client()
        response = client.post("/", {"customer_number": number, "password": password})
        assert response["Location"] == "/produkter/"

        content = page(client, "get", "/produkter/")

        assert f"siste registrerte uke: {week}" in content
        numbers = re.findall(r"<td>(\d{5})</td>", content)
        assert len(numbers) == count
        assert all(n.startswith(mine) for n in numbers)
        assert not any(n.startswith(theirs) for n in numbers)
