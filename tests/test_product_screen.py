"""The product screen: the decision panel, the trust panel and the list (Story 2.7).

FR-2, FR-8, FR-11, FR-19, FR-25, NFR-6, NFR-8, NFR-11, AD-2, AD-4, AD-7, UX-DR6, UX-DR7,
UX-DR10, UX-DR20, UX-DR22, UX-DR24, UX-DR44. The expected quantities, labels and
warnings of the rule test products are read from the reference spreadsheet and the
mockup (AD-17); the Message Catalogue texts are written out, as the catalogue fixes them.
"""

import re
from html.parser import HTMLParser

import answer_key
import answer_key_reader as reader
import generate_seed
import pytest
from conftest import create_account
from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext
from pytest_django.asserts import assertRedirects
from test_company_data import add_product
from test_error_pages import assert_error_page

from forecasting import trust
from web import views
from web.models import Company, CompanySettings, Product

TAGS_ONLY = re.compile(r"<[^>]+>")
FOCUSABLE = ("a", "button", "input", "select", "textarea")
KINDS = {"høy": "hoy", "middels": "middels", "lav": "lav"}
WORDS = {"høy": "Høy", "middels": "Middels", "lav": "Lav"}
SEED_LOGINS = {"A": ("1001", "testbedrift-a"), "B": ("1002", "testbedrift-b")}


class Screen(HTMLParser):
    """The parts of a product page that the tests read."""

    def __init__(self, html):
        super().__init__()
        self.focusable = []  # (tag, href or tabindex) in document order
        self.regions = []  # (tag, aria-label) in document order
        self.headings = []  # (tag, text)
        self.rows = []  # (classes, text) of the warning rows
        self.current = []  # the text of every aria-current link
        self._open = None
        self._row = None
        self._link = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = (attrs.get("class") or "").split()
        if tag in FOCUSABLE or attrs.get("tabindex") == "0":
            self.focusable.append((tag, attrs.get("href") or attrs.get("tabindex")))
        if "aria-label" in attrs:
            self.regions.append((tag, attrs["aria-label"]))
        if tag in ("h1", "h2", "h3"):
            self._open = [tag, ""]
        if tag == "li" and "warning" in classes:
            self._row = [classes, ""]
        if tag == "a" and attrs.get("aria-current") == "page":
            self._link = ""

    def handle_data(self, data):
        if self._open:
            self._open[1] += data
        if self._row:
            self._row[1] += data
        if self._link is not None:
            self._link += data

    def handle_endtag(self, tag):
        if self._open and tag == self._open[0]:
            self.headings.append(tuple(self._open))
            self._open = None
        if tag == "li" and self._row:
            self.rows.append((self._row[0], " ".join(self._row[1].split())))
            self._row = None
        if tag == "a" and self._link is not None:
            self.current.append(self._link)
            self._link = None


def text_of(html, pattern):
    """The text inside the first element that matches the pattern (one group)."""
    return " ".join(TAGS_ONLY.sub(" ", re.search(pattern, html, re.DOTALL)[1]).split())


def decision_of(html):
    """The quantity, its classes and its caption in the decision panel."""
    quantity = re.search(r'<b class="quantity([^"]*)">([^<]*)</b>', html)
    caption = text_of(html, r'<p class="big">.*?</b><span>(.*?)</span>')
    return quantity[2], quantity[1].split(), caption


def logged_in(company):
    client = Client()
    client.force_login(company)
    return client


def open_product(company, number):
    response = logged_in(company).get(f"/produkter/{number}/")
    assert response.status_code == 200
    return response.content.decode()


@pytest.fixture
def seed_pages(seeded):
    """The product pages of the seed companies, which the tests read once each."""
    cache = {}

    def page(side, number):
        if (side, number) not in cache:
            company = Company.objects.get(customer_number=SEED_LOGINS[side][0])
            cache[side, number] = open_product(company, number)
        return cache[side, number]

    return page


# The product with an order, the two stockout weeks and an unusual week (E1, E4).


def test_a_product_with_an_order_shows_the_decision_and_the_trust(seed_pages):
    """FR-11, FR-19, UX-DR10, UX-DR22, UX-DR24, E4: Strøsand 25 kg (the approved mockup's
    product) shows its quantity in blue, the week of the suggestion, the header line,
    the label with its reason, and a red row for the stockout weeks before an amber
    row for the unusual week."""
    html = seed_pages("A", "10012")
    mockup = answer_key.mockup_products()["Strøsand 25 kg"]

    quantity, classes, caption = decision_of(html)
    assert (quantity, classes) == (mockup["quantity"], [])
    assert caption == "Foreslått bestillingsmengde for neste uke, uke 46"
    assert text_of(html, r'<p class="product-meta">(.*?)</p>') == (
        f"Varenr. {mockup['number']} · Lagerbeholdning {mockup['stock']} · "
        "Uker dekning 0,3"
    )
    assert text_of(html, r'<p class="trust-label">(.*?)</p>') == "Middels"
    assert "Middels: 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene." in html
    assert Screen(html).rows == [
        (
            ["warning", "warning-data"],
            "Uke 38 og 39: utsolgt, holdt utenfor beregningen.",
        ),
        (
            ["warning", "warning-pattern"],
            "Uke 42: uvanlig høyt salg (31), tatt med i beregningen.",
        ),
    ]


def test_the_two_panels_have_their_headings_and_one_page_title(seed_pages):
    """UX-DR44, UX-DR16: one h1, the product name; the panels have h2 and the list has an h2
    with the product count."""
    screen = Screen(seed_pages("A", "10012"))

    assert [h for h in screen.headings if h[0] == "h1"] == [("h1", "Strøsand 25 kg")]
    assert [text for tag, text in screen.headings if tag == "h2"] == [
        "Produktoversikt 30 produkter",
        "Hva bør du bestille?",
        "Kan du stole på prognosen?",
        "Slik er tallene regnet ut",
    ]


def test_a_product_without_a_forecast_says_that_the_user_decides(seed_pages):
    """FR-8, UX-DR22, E11 a: Snøskuffe aluminium (two valid weeks) shows «–», the
    missing quantity and the sentence, «–» as the weeks of cover, «Lav» and a red row
    with the insufficient-data text of the catalogue."""
    html = seed_pages("A", "10040")

    quantity, classes, caption = decision_of(html)
    assert (quantity, classes, caption) == (
        "–",
        ["quantity-ink"],
        "Ingen foreslått bestillingsmengde",
    )
    assert (
        "Prognose foreslår ingen mengde for dette produktet. "
        "Du bestemmer bestillingen selv." in html
    )
    assert "Uker dekning –" in text_of(html, r'<p class="product-meta">(.*?)</p>')
    assert text_of(html, r'<p class="trust-label">(.*?)</p>') == "Lav"
    assert Screen(html).rows == [
        (
            ["warning", "warning-data"],
            (
                "Produktet har 2 gyldige uker. Prognose regner ut en prognose når "
                "produktet har minst 3 gyldige uker."
            ),
        )
    ]


def test_an_order_of_zero_is_in_ink_with_its_caption(seed_pages):
    """FR-11, UX-DR22: 0 is not an order, so «0» is not blue, and it has the caption of
    a forecast. The product has a high label, which has no warning row."""
    html = seed_pages("A", "10043")

    quantity, classes, caption = decision_of(html)
    assert (quantity, classes) == ("0", ["quantity-ink"])
    assert caption == "Foreslått bestillingsmengde for neste uke, uke 46"
    assert Screen(html).rows == []
    assert (
        "<ul" not in html.split("Kan du stole på prognosen?")[1].split("</section>")[0]
    )


def test_a_forecast_of_zero_has_no_weeks_of_cover(db):
    """FR-24, E23: a product that sells nothing has «–» as its weeks of cover and an
    order of 0 in ink."""
    row = next(r for r in reader.cases() if r["case"] == "E23")
    company = Company.objects.create(customer_number="9001", name="E23-bedrift")
    add_product(
        company,
        "10001",
        [w.units_sold for w in row["sales"]],
        stock=row["stock_on_hand"],
    )

    html = open_product(company, "10001")

    assert decision_of(html)[:2] == ("0", ["quantity-ink"])
    assert "Uker dekning –" in text_of(html, r'<p class="product-meta">(.*?)</p>')


def test_a_product_without_sales_weeks_still_has_its_screen(two_companies):
    """FR-8: a product with no week has no forecast, and the page needs no week for it."""
    a, _ = two_companies
    Product.objects.create(
        company=a.company, product_number="10009", name="Uten uker", stock_on_hand=3
    )

    html = open_product(a.company, "10009")

    assert decision_of(html)[0] == "–"
    assert text_of(html, r'<p class="trust-label">(.*?)</p>') == "Lav"


def test_the_week_of_the_suggestion_can_be_week_1_of_the_next_year(db):
    """R-5, UX-DR42: with the latest data in week 53 of 2026 the suggestion is for
    «uke 1/2027»."""
    account = create_account(
        "9002",
        "Nyttårsbedrift",
        "testbedrift-a.json",
        "x",
        [("10001", "Spade", 1)],
        (2026, 53),
    )

    assert decision_of(open_product(account.company, "10001"))[2] == (
        "Foreslått bestillingsmengde for neste uke, uke 1/2027"
    )


# The 11 rule test products of the spreadsheet (FR-3, DR-3).


RULE_PRODUCTS = [
    (key, company["file"], company["company"], number)
    for company in generate_seed.COMPANIES
    for key, (number, _name) in company["from_workbook"].items()
]


def test_the_rule_test_products_are_found_in_both_seed_companies():
    """FR-3: the products below come from both companies, and none is left out."""
    assert len(RULE_PRODUCTS) == 11
    assert {side for *_, side, _ in RULE_PRODUCTS} == {"A", "B"}


@pytest.mark.parametrize(
    ("key", "file_name", "side", "number"), RULE_PRODUCTS, ids=lambda v: str(v)
)
def test_a_rule_test_product_shows_what_the_spreadsheet_states(
    seed_pages, key, file_name, side, number
):
    """FR-11, FR-19, FR-25, SM-1: the suggested order quantity, the label and the rows
    of each rule test product equal the spreadsheet's, in R-15 order."""
    expected = next(row for row in reader.products() if row["product"] == key)
    html = seed_pages(side, number)
    quantity, classes, _ = decision_of(html)

    stated = expected["suggested_order_quantity"]
    assert quantity == ("–" if stated is None else str(stated))
    assert ("quantity-ink" in classes) == (not stated)
    assert (
        text_of(html, r'<p class="trust-label">(.*?)</p>')
        == WORDS[expected["confidence_label"]]
    )
    assert f"pill-{KINDS[expected['confidence_label']]}" in html
    # A level shift has a place in the reason but no row until FR-17b (Should).
    rows = [w for w in expected["warnings"] if w != trust.LEVEL_SHIFT]
    kinds = {
        trust.STOCKOUT_WEEKS: "warning-data",
        trust.UNUSUAL_WEEKS: "warning-pattern",
        trust.OLD_DATA: "warning-data",
        trust.INSUFFICIENT_DATA: "warning-data",
    }
    assert [classes[1] for classes, _ in Screen(html).rows] == [kinds[w] for w in rows]


@pytest.mark.parametrize("side", ["A", "B"])
def test_every_product_of_the_seed_companies_has_a_screen(seeded, side):
    """FR-2, FR-25: all 62 products open without an error, each with one h1, a
    decision panel and a trust panel, and no row without text."""
    company = Company.objects.get(customer_number=SEED_LOGINS[side][0])
    client = logged_in(company)
    numbers = list(company.products.values_list("product_number", flat=True))

    for number in numbers:
        html = client.get(f"/produkter/{number}/").content.decode()
        screen = Screen(html)
        assert html.count("<h1") == 1, number
        assert ("h2", "Hva bør du bestille?") in screen.headings, number
        assert ("h2", "Kan du stole på prognosen?") in screen.headings, number
        assert all(text for _, text in screen.rows), number
        assert len(screen.rows) <= 2, number
    assert len(numbers) == {"A": 30, "B": 32}[side]


def test_each_warning_has_the_kind_and_shape_of_the_design():
    """UX-DR5, UX-DR24: stockout is a hollow square, unusual a triangle, and old and
    insufficient data a ring with «!»; data problems are red and demand patterns amber.
    The mapping itself is checked here, and the pages below draw each shape."""
    assert views.WARNING_ROWS == {
        trust.STOCKOUT_WEEKS: ("data", "square-outline"),
        trust.UNUSUAL_WEEKS: ("pattern", "triangle"),
        trust.OLD_DATA: ("data", "ring"),
        trust.INSUFFICIENT_DATA: ("data", "ring"),
    }
    assert views.LABELS == {
        trust.HOY: ("hoy", "circle"),
        trust.MIDDELS: ("middels", "triangle"),
        trust.LAV: ("lav", "square"),
    }


@pytest.mark.parametrize(
    ("side", "number", "icons"),
    [
        ("A", "10012", ["icon-square-outline", "icon-triangle"]),
        ("A", "10040", ["icon-ring"]),
        # Parasoll 2 m has the stockout weeks and the old-data warning (E12).
        ("B", "20015", ["icon-square-outline", "icon-ring"]),
    ],
)
def test_the_rows_draw_their_shapes(seed_pages, side, number, icons):
    """UX-DR5, UX-DR24: each row has its own icon, which is hidden from screen readers."""
    html = seed_pages(side, number)

    assert (
        re.findall(r'<svg class="icon (icon-[a-z-]+)"[^>]*aria-hidden="true">', html)
        == icons
    )


@pytest.mark.parametrize(
    ("number", "shape"),
    [("10043", "<circle"), ("10012", "<path"), ("10040", "<rect")],
)
def test_the_trust_label_draws_its_shape_beside_the_word(seed_pages, number, shape):
    """UX-DR5, UX-DR20: «Høy» is a circle, «Middels» a triangle and «Lav» a square, in
    the header and in the trust panel, and the shape is hidden from screen readers."""
    html = seed_pages("A", number)
    # The list has small labels of its own (Story 2.8); this is the product area.
    pills = re.findall(
        r'<span class="pill [^"]*">(.*?)</span>', html[html.index("<main") :]
    )

    assert len(pills) == 2
    for pill in pills:
        assert pill.startswith(
            '<svg width="14" height="14" viewBox="0 0 12 12" aria-hidden="true">'
            + shape
        )


def test_every_warning_but_the_level_shift_has_a_row_kind():
    """UX-DR24, AD-4: a warning without a row would be a KeyError on the page, so each
    warning of R-15 has its kind and shape, except the level shift, which has no text
    until FR-17b."""
    assert set(views.WARNING_ROWS) == set(trust.WARNINGS) - {trust.LEVEL_SHIFT}
    assert {kind for kind, _ in views.WARNING_ROWS.values()} == {"data", "pattern"}
    assert set(views.LABELS) == {trust.HOY, trust.MIDDELS, trust.LAV}


# The list and the page structure.


def test_the_list_links_each_product_and_marks_the_open_one(two_companies):
    """UX-DR6, UX-DR44, FR-2: every name links to its product screen, and only the open
    product has aria-current."""
    a, _ = two_companies
    html = open_product(a.company, "10002")

    links = re.findall(
        r'<a class="prow" href="(/produkter/\d+/)"[^>]*>\s*<span class="nm">([^<]*)</span>',
        html,
    )
    assert links == [
        ("/produkter/10001/", "Hammer fra A"),
        ("/produkter/10002/", "Sag fra A"),
        ("/produkter/10003/", "Tang fra A"),
    ]
    # The header marks the product overview, and the list the open product.
    current = Screen(html).current
    assert len(current) == 2
    assert current[0] == "Produktoversikt"
    assert " ".join(current[1].split()).startswith("Sag fra A")


def test_the_skip_link_is_first_and_the_list_comes_before_the_product(two_companies):
    """UX-DR10, UX-DR44, UX-DR7: «Gå til produktet» is the first focusable element and
    leads to the product region; the list region comes before it in the HTML, which a
    narrow screen shows in the other order with CSS only."""
    a, _ = two_companies
    html = open_product(a.company, "10001")
    screen = Screen(html)

    assert screen.focusable[0] == ("a", "#valgt-produkt")
    assert '<a class="skip-link" href="#valgt-produkt">Gå til produktet</a>' in html
    assert 'id="valgt-produkt"' in html
    assert [
        name for _, name in screen.regions if name in ("Produkter", "Valgt produkt")
    ] == [
        "Produkter",
        "Valgt produkt",
    ]
    assert html.index('aria-label="Produkter"') < html.index('id="valgt-produkt"')
    # The list scrolls with its links, and the product region can be focused to scroll;
    # so can each scroll frame of the worksheet inside it (Story 2.9): here the sales table
    # and the scenario table, because the moving average has no table of levels.
    assert [f for f in screen.focusable if f[1] == "0"] == [
        ("main", "0"),
        ("div", "0"),
        ("div", "0"),
    ]


def test_the_header_marks_the_product_overview_and_shows_the_latest_week(two_companies):
    """UX-DR14: as in the mockup's product screen, «Produktoversikt» is the current page,
    and the week is the company's own."""
    a, _ = two_companies
    html = open_product(a.company, "10001")

    assert '<a href="/produkter/" aria-current="page">Produktoversikt</a>' in html
    assert "siste registrerte uke: uke 45, 2026" in html


def test_the_page_uses_no_script_but_the_shell_one_and_names_its_title(two_companies):
    """NFR-1, NFR-11: the title names the product, and the page loads only the app's
    own script and stylesheet."""
    a, _ = two_companies
    html = open_product(a.company, "10001")

    assert "<title>Hammer fra A – Prognose</title>" in html
    assert re.findall(r'<script src="([^"]+)"', html) == ["/static/web/app.js"]


# Isolation, login and methods.


def test_another_companys_product_gives_the_page_of_an_unknown_address(two_companies):
    """FR-2, AD-7: A asks for B's number 20001, and gets exactly the page that an unknown
    number gets, with nothing of B's, and with 404."""
    a, b = two_companies
    client = logged_in(a.company)

    other = client.get("/produkter/20001/")
    unknown = client.get("/produkter/99999/")

    assert_error_page(other, 404, "Not found")
    assert other.content == unknown.content
    for text in ("Spade fra B", "Rive fra B", "8481", "8482", b.company.name):
        assert text not in other.content.decode()
    assert logged_in(b.company).get("/produkter/20001/").status_code == 200


def test_a_shared_number_opens_each_companys_own_product(two_companies):
    """FR-2, AD-7: both companies have 10001, and each page shows its own name and stock."""
    a, b = two_companies

    assert "Lagerbeholdning 7371" in open_product(a.company, "10001")
    assert "Lagerbeholdning 8481" in open_product(b.company, "10001")
    assert "Spade fra B" not in open_product(a.company, "10001")


@pytest.mark.parametrize("path", ["/produkter/10001/", "/produkter/99999/"])
def test_a_visitor_without_a_login_goes_to_the_login_page(client, db, path):
    """FR-1, AD-6: a product address, known or not, sends a visitor to the login."""
    assertRedirects(client.get(path), "/")


def test_the_page_is_not_kept_and_takes_safe_methods_only(two_companies):
    """NFR-10: no-store, a HEAD is fine, and a POST gives 405."""
    a, _ = two_companies
    client = logged_in(a.company)

    response = client.get("/produkter/10001/")
    assert "no-store" in response["Cache-Control"]
    assert "private" in response["Cache-Control"]
    assert client.head("/produkter/10001/").status_code == 200
    assert client.post("/produkter/10001/").status_code == 405


# NFR-8.


def count_queries(client, path):
    with CaptureQueriesContext(connection) as queries:
        assert client.get(path).status_code == 200
    return len(queries)


def test_the_page_makes_the_same_number_of_queries_for_50_products_of_104_weeks(db):
    """AD-2, NFR-8: three products or fifty products of 104 weeks give the same number
    of queries: the 2 of the login and the 4 of the loader, with the latest week read once."""
    units = tuple(10 + week % 7 for week in range(104))
    counts = []
    for name, products in (("Liten", 3), ("Stor", 50)):
        company = Company.objects.create(customer_number=name, name=name)
        for number in range(products):
            add_product(company, f"{10000 + number}", units, stock=number)
        counts.append(count_queries(logged_in(company), "/produkter/10001/"))

    assert counts[0] == counts[1] <= 6


# The worksheet «Slik er tallene regnet ut» (Story 2.9).
# FR-7, FR-10, FR-12, FR-15, FR-16, FR-35, NFR-6, NFR-11, AD-4, UX-DR7, UX-DR28 to UX-DR30.


def squash(markup):
    """The text of some markup with its spaces squashed to one; a no-break space stays."""
    return re.sub(r"[ \t\r\n]+", " ", TAGS_ONLY.sub(" ", markup)).strip()


def sheet_html(html):
    """The worksheet panel of a product page."""
    return html.split('<section class="panel sheet"')[1].split("</section>")[0]


def sheet_lines(html, css_class):
    """The text of each paragraph with the class, such as «calc» or «fine»."""
    return [
        " ".join(TAGS_ONLY.sub(" ", match).split())
        for match in re.findall(
            rf'<p class="{css_class}">(.*?)</p>', sheet_html(html), re.DOTALL
        )
    ]


def sheet_cells(html, table):
    """The text of the cells of each row of a table of the worksheet."""
    body = re.search(
        rf'<table class="{table}">(.*?)</table>', sheet_html(html), re.DOTALL
    )
    return [
        [
            " ".join(TAGS_ONLY.sub(" ", cell).split())
            for cell in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.DOTALL)
        ]
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", body[1], re.DOTALL)
    ]


def mockup_sheet():
    """The worksheet of the approved mockup, which the page of Strøsand 25 kg must equal
    where EXPERIENCE.md words the lines in the same way (UX-DR28)."""
    html = answer_key.MOCKUP.read_text(encoding="utf-8")
    return html.split('<section class="panel" aria-labelledby="t-sheet">')[1].split(
        "</section>"
    )[0]


def test_the_worksheet_of_the_mockups_product_equals_the_mockup(seed_pages):
    """UX-DR28 (E1, E3, E4): the sales table, the tags, the sentence below it, the two
    calculation lines and the scenario values of Strøsand 25 kg are the mockup's."""
    page = seed_pages("A", "10012")
    mock = mockup_sheet()
    mock_weeks = mock.split('<table class="weeks">')[1].split("</table>")[0]
    mock_rows = [
        [
            " ".join(TAGS_ONLY.sub(" ", cell).split())
            for cell in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.DOTALL)
        ]
        for row in re.findall(r"<tr>(.*?)</tr>", mock_weeks, re.DOTALL)
    ]
    rows = sheet_cells(page, "weeks")

    # The week header, the units sold and the status row are the mockup's, tag by tag.
    assert rows == mock_rows
    assert rows[0] == ["Uke", *[str(week) for week in range(34, 46)]]
    assert rows[1][1:] == [str(w.units_sold) for w in answer_key.mockup_recent_weeks()]
    assert rows[2][0] == "Status"
    assert rows[2][5:7] == ["utsolgt", "utsolgt"]
    assert rows[2][9] == "uvanlig"
    assert (
        sheet_lines(page, "fine")[0]
        == re.search(r'<p class="fine">(«Brukt».*?)</p>', mock)[1]
    )
    calc = sheet_lines(page, "calc")
    mock_calc = [
        " ".join(TAGS_ONLY.sub(" ", c).split())
        for c in re.findall(r'<p class="calc">(.*?)</p>', mock, re.DOTALL)
    ]
    assert calc == mock_calc
    assert [row[1:] for row in sheet_cells(page, "scen")[1:]] == [
        ["15,8", "15,8", "15,8"],
        ["14,3", "14,3", "14,3"],
        ["12,9", "12,9", "12,9"],
    ]
    assert sheet_cells(page, "scen")[0] == [
        "Scenario",
        "Uke 1 · uke 46",
        "Uke 2 · uke 47",
        "Uke 3 · uke 48",
    ]


def test_the_worksheet_has_its_subsections_in_order_and_the_catalogue_sentences(
    seed_pages,
):
    """UX-DR28, FR-12: the h3 headings in order, the left-out line, and the two fixed
    sentences below the scenarios and the order line."""
    page = seed_pages("A", "10012")
    screen = Screen(sheet_html(page))

    assert [text for tag, text in screen.headings if tag == "h3"] == [
        "Salgshistorikk, siste 12 uker",
        "Prognoseutregning",
        "Ukeprognoser og scenarioer",
        "Utregning av bestillingsmengde",
    ]
    body = squash(sheet_html(page))
    assert "Uker brukt: uke 43, 44 og 45." in body
    assert "Holdt utenfor: uke 38 og 39 (utsolgt)." in body
    assert (
        "Scenarioene viser hva som skjer hvis salget blir 10 % høyere eller "
        "lavere. De er ikke sannsynligheter." in body
    )
    assert (
        "Merknad: Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar "
        "hensyn til trend eller sesong." in body
    )
    assert (
        "Sikkerhetsmarginen er en enkel tommelfingerregel. Leveringstid og varer som "
        "allerede er bestilt, er ikke tatt med." in body
    )
    assert body.count("Tallene er avrundet for visning.") == 1


@pytest.mark.parametrize(
    ("key", "file_name", "side", "number"), RULE_PRODUCTS, ids=lambda v: str(v)
)
def test_every_rule_test_product_shows_the_forecast_and_the_quantity_of_the_spreadsheet(
    seed_pages, key, file_name, side, number
):
    """FR-12, FR-35, SM-1: the base forecast on the calculation line and the suggested
    quantity at the end of the order line are the spreadsheet's, for the 11 products."""
    expected = next(row for row in reader.products() if row["product"] == key)
    page = seed_pages(side, number)
    calc = sheet_lines(page, "calc")

    forecast = f"{expected['base_forecast']:.1f}".replace(".", ",")
    assert calc[0].startswith("Glidende gjennomsnitt, 3 uker: (")
    assert calc[0].endswith(f"= {forecast}")
    assert (
        f"foreslått bestillingsmengde {expected['suggested_order_quantity']}" in calc[1]
    )
    assert calc[1].startswith(f"Prognose {forecast} + sikkerhetsmargin 10 % (")


def test_the_unusual_weeks_of_the_spreadsheet_have_the_tag_of_a_week_taken_in(
    seed_pages,
):
    """FR-16 (E15): with the default setting an unusual week is «uvanlig», never
    «uvanlig, holdt utenfor», and a level shift is «nytt nivå»."""
    page = seed_pages("B", "20005")  # E15
    html = sheet_html(page)

    assert re.search(r'class="tag tag-unusual"', html)
    assert "tag-unusual-out" not in html
    assert re.search(r'class="tag tag-shift"', html)


def test_a_product_without_a_forecast_has_only_the_sales_table(seed_pages):
    """FR-8, UX-DR10 (10040): the sales table and its sentence, and no calculation, no
    scenarios and no order line."""
    page = seed_pages("A", "10040")
    screen = Screen(sheet_html(page))

    assert [text for tag, text in screen.headings if tag == "h3"] == [
        "Salgshistorikk, alle ukene"
    ]
    assert 'class="calc"' not in sheet_html(page)
    assert 'class="scen"' not in sheet_html(page)
    assert "Utregning av bestillingsmengde" not in page


def test_a_product_without_sales_weeks_has_no_table(two_companies):
    """FR-8: the sentence in place of the table, and nothing to calculate."""
    a, _ = two_companies
    Product.objects.create(
        company=a.company, product_number="10009", name="Uten uker", stock_on_hand=3
    )

    html = open_product(a.company, "10009")

    assert "Produktet har ingen salgsuker." in sheet_html(html)
    assert 'class="weeks"' not in sheet_html(html)
    assert 'class="calc"' not in sheet_html(html)


def test_every_table_of_the_worksheet_scrolls_in_its_own_named_frame(seed_pages):
    """NFR-6, NFR-11, UX-DR7: each table sits in a region with a name that the keyboard
    can reach, so a table wider than the panel scrolls inside it and not the page."""
    html = sheet_html(seed_pages("A", "10012"))

    frames = re.findall(r'<div class="tablewrap[^"]*"([^>]*)>', html)
    assert len(frames) == html.count("<table") == 2
    for attributes in frames:
        assert 'role="region"' in attributes
        assert 'tabindex="0"' in attributes
        assert "aria-label" in attributes


def test_exponential_smoothing_shows_its_update_note_and_levels_on_the_page(db):
    """FR-35, R-9 (E2): the setting of the company changes the calculation: the last
    update, the note inside the box and a table of every calculation week."""
    row = next(r for r in reader.cases() if r["case"] == "E2")
    company = Company.objects.create(customer_number="9002", name="E2-bedrift")
    CompanySettings.objects.create(company=company, method="exponential_smoothing")
    add_product(company, "10001", [w.units_sold for w in row["sales"]], stock=0)

    html = open_product(company, "10001")

    assert sheet_lines(html, "calc")[0] == (
        "Eksponentiell glatting, faktor 0,3: 0,3 × 15 + 0,7 × 13,3 = 13,8 "
        "Tallene er avrundet for visning."
    )
    levels = sheet_cells(html, "levels")
    assert levels[0] == ["Uke", "Solgt", "Nivå"]
    assert [r[2] for r in levels[1:]] == [
        f"{x:.1f}".replace(".", ",") for x in row["levels"]
    ]
    assert "Uker brukt" not in sheet_html(html)
    assert Screen(html).headings.count(("h3", "Prognoseutregning")) == 1
    # The table of levels has a frame of its own that the keyboard reaches and a screen
    # reader names (NFR-11, UX-DR7).
    frame = re.search(
        r'<div class="tablewrap tablewrap-levels"([^>]*)>', sheet_html(html)
    )
    assert 'role="region"' in frame[1] and 'tabindex="0"' in frame[1]
    assert 'aria-label="Beregningsukene med salg og nivå"' in frame[1]


def test_unusual_weeks_left_out_are_told_apart_from_those_taken_in_on_the_page(db):
    """FR-16, NFR-7, UX-DR30 (E8): the tags differ in words, in shape and in class, and
    the weeks left out are listed with the number of weeks used."""
    row = next(r for r in reader.cases() if r["case"] == "E8 (excluded)")
    units = [w.units_sold for w in row["sales"]]
    pages = {}
    for included in (True, False):
        company = Company.objects.create(customer_number=f"90{included:d}3", name="E8")
        CompanySettings.objects.create(company=company, unusual_weeks_included=included)
        add_product(company, "10001", units, stock=50)
        pages[included] = sheet_html(open_product(company, "10001"))

    taken, left_out = pages[True], pages[False]
    assert 'tag tag-unusual"' in taken and "tag-unusual-out" not in taken
    assert "uvanlig, holdt utenfor" not in taken
    assert 'tag tag-unusual-out"' in left_out and 'tag tag-unusual"' not in left_out
    assert left_out.count("uvanlig, holdt utenfor") == 2
    # The hollow and the solid triangle are different drawings.
    assert (
        'fill="none" stroke="currentColor" stroke-width="1.5"/></svg>uvanlig, holdt'
        in left_out
    )
    assert "Holdt utenfor: uke 43 og 44 (uvanlig)." in " ".join(
        TAGS_ONLY.sub(" ", left_out).split()
    )
    assert "3 uker brukt i beregningen." in left_out
    assert "uker brukt i beregningen" not in taken


def test_the_worksheet_shows_each_companys_own_stock_for_a_shared_number(two_companies):
    """FR-2, AD-7: both companies have a product 10001, and each worksheet is built from
    the company's own stock on hand and the other's never appears."""
    a, b = two_companies

    page_a = sheet_html(open_product(a.company, "10001"))
    page_b = sheet_html(open_product(b.company, "10001"))

    assert "lager 7371 =" in squash(page_a)
    assert "lager 8481 =" in squash(page_b)
    assert "8481" not in page_a and "7371" not in page_b
