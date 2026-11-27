"""The product list in R-12 order (Story 2.8).

FR-2, FR-24, NFR-6, NFR-8, AD-2, AD-4, UX-DR16 to UX-DR18, UX-DR44. The expected figures of
Testbedrift A are the mockup's and the core's (AD-17); the Message Catalogue texts are
written out, as the catalogue fixes them.
"""

import re
from pathlib import Path

import answer_key
import pytest
from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext
from test_company_data import add_product

from explanation import product_list as words
from explanation import trust as trust_words
from forecasting import display
from forecasting import forecast as core
from forecasting.settings import ForecastSettings
from forecasting.weeks import Week
from web import company_data
from web.models import Company

ITEM = re.compile(
    r'<a class="p(card|row)([^"]*)" href="/produkter/(\d+)/"( aria-current="page")?>'
    r"(.*?)</a>",
    re.DOTALL,
)
GROUP = re.compile(
    r'<section class="group" aria-labelledby="g-(\w+)">\s*<h(\d) class="grp" id="g-\w+">'
    r"(.*?)</h\d>(.*?)</section>",
    re.DOTALL,
)


def plain(html):
    return " ".join(re.sub(r"<[^>]+>", " ", html).split())


def groups_of(html):
    """The groups of a page: (key, heading level, heading text, items), where an item is
    (kind, extra classes, number, selected, text, html)."""
    return [
        (
            key,
            int(level),
            plain(heading),
            [
                (kind, classes, number, bool(current), plain(inner), inner)
                for kind, classes, number, current, inner in ITEM.findall(body)
            ],
        )
        for key, level, heading, body in GROUP.findall(html)
    ]


def page(company, path="/produkter/"):
    client = Client()
    client.force_login(company)
    response = client.get(path)
    assert response.status_code == 200
    return response.content.decode()


@pytest.fixture
def page_a(seeded):
    company = Company.objects.get(customer_number="1001")
    return company, page(company)


def item_of(html, number):
    (item,) = [
        item
        for _, _, _, items in groups_of(html)
        for item in items
        if item[2] == number
    ]
    return item


# The groups and their order.


def test_testbedrift_a_has_the_three_groups_in_r_12_order_with_the_mockups_figures(
    page_a,
):
    """FR-24, UX-DR16, E13, E24: «Bestill snart» has the mockup's 4 products and 31 units,
    «Uten prognose» its 1 product and «Øvrige produkter» the other 25, each group in the
    order of the core's overview, and the whole list in the order of `build_overview`."""
    company, html = page_a
    overview = company_data.load_company_data(company).overview
    figures = answer_key.mockup_overview()

    groups = groups_of(html)

    assert [(key, heading) for key, _, heading, _ in groups] == [
        (
            "order_soon",
            f"Bestill snart {figures['order_soon']} produkter · 31 enheter foreslått",
        ),
        ("without_forecast", "Uten prognose 1 produkt · du bestemmer selv"),
        ("others", "Øvrige produkter 25 · etter varenummer"),
    ]
    assert figures["units"] == 31
    assert [[item[2] for item in items] for _, _, _, items in groups] == [
        list(overview.order_soon),
        list(overview.without_forecast),
        list(overview.others),
    ]
    assert [item[2] for _, _, _, items in groups for item in items] == list(
        overview.order
    )
    assert [kind for _, _, _, items in groups for kind, *_ in items] == (
        ["card"] * 5 + ["row"] * 25
    )


def test_the_mockups_products_show_the_mockups_quantity_and_stock(page_a):
    """FR-24, UX-DR46: every product of the mockup's overview has its stock and quantity in
    the list, the quantity «–» without a forecast."""
    _, html = page_a

    for name, shown in answer_key.mockup_products().items():
        text = item_of(html, shown["number"])[4]
        assert text.startswith(f"{name} Foreslått {shown['quantity']} "), name
        assert f"Lager {shown['stock']}" in text, name


def test_the_list_has_the_headings_of_its_page(page_a):
    """UX-DR16, UX-DR44: the overview has the page title with the count, the list is the
    labeled region «Produkter», and the groups are h2, below the h1 that names the page."""
    _, html = page_a

    assert re.search(r"<h1 [^>]*>Produktoversikt <span>30 produkter</span></h1>", html)
    assert '<nav class="list-column" aria-label="Produkter">' in html
    assert [level for _, level, _, _ in groups_of(html)] == [2, 2, 2]
    assert html.count("<h1") == 1


def test_an_empty_group_is_not_shown_and_the_summaries_use_the_singular(db):
    """FR-24, UX-DR16, AD-4: without a product to order soon there is no «Bestill snart»,
    and a group of one says «1 produkt», «1 enhet» and «1 ·»."""
    company = Company.objects.create(customer_number="9001", name="Liten")
    add_product(company, "10001", (10, 10, 10), stock=100)
    add_product(company, "10002", (), stock=3)

    groups = groups_of(page(company))

    assert [heading for _, _, heading, _ in groups] == [
        "Uten prognose 1 produkt · du bestemmer selv",
        "Øvrige produkter 1 · etter varenummer",
    ]

    add_product(company, "10003", (10, 10, 10), stock=0)

    groups = groups_of(page(company))
    assert groups[0][2] == "Bestill snart 1 produkt · 11 enheter foreslått"
    assert groups[0][3][0][2] == "10003"


def test_group_summaries_are_the_catalogues_in_singular_and_plural():
    """AD-4, UX-DR16: the three summaries of the catalogue, with 1, 2 and 0 as counts."""
    assert (
        words.group_summary(words.ORDER_SOON, 1, 1) == "1 produkt · 1 enhet foreslått"
    )
    assert (
        words.group_summary(words.ORDER_SOON, 4, 31)
        == "4 produkter · 31 enheter foreslått"
    )
    assert (
        words.group_summary(words.WITHOUT_FORECAST, 1)
        == "1 produkt · du bestemmer selv"
    )
    assert (
        words.group_summary(words.WITHOUT_FORECAST, 2)
        == "2 produkter · du bestemmer selv"
    )
    assert words.group_summary(words.OTHERS, 25) == "25 · etter varenummer"
    assert words.product_count(1) == "1 produkt"
    assert words.product_count(30) == "30 produkter"
    assert words.product_count(0) == "0 produkter"
    with pytest.raises(ValueError):
        words.group_summary("other", 1)


# The cards and the rows.


def test_a_card_shows_name_number_quantity_stock_forecast_cover_label_and_reason(
    page_a,
):
    """FR-24, UX-DR17, E1, E4: Strøsand 25 kg is a card of «Bestill snart» with its name, its
    number, «Foreslått» over 11 in blue, the stock, the week-1 forecast, the weeks of cover,
    the label and the reason without the label word and the full stop. The whole card
    is one link."""
    _, html = page_a

    kind, classes, _, selected, text, inner = item_of(html, "10012")

    assert (kind, classes, selected) == ("card", "", False)
    assert text == (
        "Strøsand 25 kg Foreslått 11 Varenr. 10012 Lager 5 Ukeprognose uke 1 14,3 "
        "Uker dekning 0,3 Middels 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene"
    )
    assert "qty-ink" not in inner


def test_a_card_without_a_forecast_has_the_red_reason_dashes_and_the_dashed_border(
    page_a,
):
    """FR-24, FR-8, UX-DR17: Snøskuffe aluminium has the dashed card, the FR-8 reason in place
    of the week-1 forecast, «–» in ink for the quantity and the weeks of cover, and the
    label «Lav» without a second copy of the reason, as in the mockup."""
    _, html = page_a

    kind, classes, _, _, text, inner = item_of(html, "10040")

    assert (kind, classes) == ("card", " nofc")
    assert text == (
        "Snøskuffe aluminium Foreslått – Varenr. 10040 Lager 6 "
        "Ingen prognose: færre enn 3 gyldige uker Uker dekning – Lav"
    )
    assert (
        '<span class="reason">Ingen prognose: færre enn 3 gyldige uker</span>' in inner
    )
    assert '<b class="qty-ink">–</b>' in inner
    assert "Ukeprognose" not in text
    assert 'class="why"' not in inner


def test_a_row_has_the_meta_line_the_quantity_in_ink_and_no_reason_for_high(page_a):
    """FR-24, UX-DR18: Malertape 25 mm, a product with the label «høy», has the one meta
    line of the mockup, «Foreslått» over 0, the label, and no reason."""
    company, html = page_a
    result = company_data.load_company_data(company).results["10001"]
    assert trust_words.card_reason(result) is None

    kind, _, _, _, text, inner = item_of(html, "10001")

    assert kind == "row"
    assert (
        text
        == "Malertape 25 mm Foreslått 0 Varenr. 10001 · Lager 40 · Ukeprognose uke 1: 9,3 · Uker dekning 4,3 Høy"
    )
    assert 'class="why"' not in inner
    # A row never colours its quantity, because 0 is not an order (UX-DR18).
    assert "<small>Foreslått</small> <b>0</b>" in inner
    assert "qty-ink" not in inner


def test_a_row_with_a_lower_label_shows_the_reason(page_a):
    """FR-24, UX-DR18: Tetningslist 6 m has the reason of the mockup after its label."""
    _, html = page_a

    _, _, _, _, text, inner = item_of(html, "10019")

    assert text.endswith("Middels Kortere salgshistorikk enn 104 uker")
    assert '<span class="why">Kortere salgshistorikk enn 104 uker</span>' in inner


def test_a_level_shift_reason_starts_with_a_capital_letter(page_a):
    """UX-DR17: the mockup's card for a new level says «Nytt nivå de siste 12 ukene»."""
    _, html = page_a

    assert item_of(html, "10004")[4].endswith("Middels Nytt nivå de siste 12 ukene")


def test_every_item_shows_the_reason_unless_the_label_is_high(page_a):
    """FR-24, UX-DR17, UX-DR18: for every product of Testbedrift A, the item has the
    label word and, for «Middels» and «Lav» with a forecast, the reason from
    `explanation/`; «Høy» and a product without a forecast, whose red reason already says
    it (the user's decision 2026-11-27), have none."""
    company, html = page_a
    data = company_data.load_company_data(company)

    for _, _, _, items in groups_of(html):
        for _, _, number, _, _, inner in items:
            result = data.results[number]
            reason = trust_words.card_reason(result)
            assert (reason is None) == (
                trust_words.LABEL_WORDS[result.confidence_label] == "Høy"
                or result.base_forecast is None
            )
            assert (f'<span class="why">{reason}</span>' in inner) == bool(reason), (
                number
            )


@pytest.mark.parametrize(
    ("weeks", "label", "reason"),
    [
        ([Week(10, False)] * 104, "Høy", None),
        (
            [Week(10, False)] * 11 + [Week(10, True)],
            "Lav",
            "Færre enn 12 gyldige uker. 1 utsolgt uke de siste 12 ukene",
        ),
        ([Week(10, False)] * 2, "Lav", None),
    ],
)
def test_the_card_reason_is_the_reason_without_label_and_last_full_stop(
    weeks, label, reason
):
    """AD-4, UX-DR17: the catalogue's reasons without the label word and the last full
    stop, the inner full stops kept and the first letter in capital, and none for «høy» and
    none without a forecast, whose card shows the FR-8 reason in red instead."""
    result = core.forecast_product(weeks, 0, ForecastSettings())

    assert trust_words.LABEL_WORDS[result.confidence_label] == label
    assert trust_words.card_reason(result) == reason
    if reason:
        assert (
            trust_words.confidence_reason(result)
            == f"{label}: {reason[0].lower()}{reason[1:]}."
        )


def test_the_trust_panel_keeps_the_reason_that_the_card_leaves_out():
    """FR-19, UX-DR24: for a product without a forecast the full reason of the label is
    still the catalogue's, so only the list leaves it out."""
    result = core.forecast_product([Week(10, False)] * 2, 0, ForecastSettings())

    assert (
        trust_words.confidence_reason(result)
        == "Lav: ingen prognose, færre enn 3 gyldige uker."
    )
    assert trust_words.card_reason(result) is None


def test_the_selected_item_has_aria_current_and_only_one_has(page_a):
    """UX-DR17, UX-DR44: on a product screen exactly the open product's card has
    aria-current, also a card without a forecast, which keeps its class for the red reason."""
    company, _ = page_a

    for number, classes in (("10012", ""), ("10040", " nofc"), ("10001", "")):
        html = page(company, f"/produkter/{number}/")
        items = [item for _, _, _, items in groups_of(html) for item in items]
        selected = [item for item in items if item[3]]

        assert [(item[2], item[1]) for item in selected] == [(number, classes)]
        assert html.count('aria-current="page"') == 2  # the header link and the item
        assert '<span class="reason">' in item_of(html, "10040")[5]


def test_the_overview_page_has_no_selected_item(page_a):
    """UX-DR44: on the overview nothing is selected."""
    _, html = page_a

    assert not [i for _, _, _, items in groups_of(html) for i in items if i[3]]


def test_the_product_screen_has_the_same_list_below_the_list_heading(page_a):
    """FR-24, UX-DR16: beside a product the list has the same groups, the count in the
    heading and the groups one level below it."""
    company, overview_html = page_a

    html = page(company, "/produkter/10012/")

    def shape(html):
        return [
            (key, heading, [item[2] for item in items])
            for key, _, heading, items in groups_of(html)
        ]

    assert shape(html) == shape(overview_html)
    assert (
        '<h2 class="list-title">Produktoversikt <span>30 produkter</span></h2>' in html
    )
    assert [level for _, level, _, _ in groups_of(html)] == [3, 3, 3]


# A company without products.


def test_a_company_without_products_is_told_to_load_the_data(db):
    """FR-24, Message Catalogue «No products»: the exact sentence with the load command
    of the README, no group and no product."""
    company = Company.objects.create(customer_number="9002", name="Tom")

    html = page(company)

    assert groups_of(html) == []
    assert (
        '<p class="empty">Ingen data er lastet inn. Kjør uv run python src/manage.py '
        "load_seed som står i README.</p>"
    ) in html
    assert "0 produkter" in html


def test_the_load_command_is_the_one_of_the_readme():
    """FR-24, AD-4: the command in the sentence is a command that the README gives."""
    readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(
        encoding="utf-8"
    )

    assert f"\n{words.LOAD_COMMAND}\n" in readme


# Isolation and queries.


def test_the_list_holds_only_the_logged_in_companys_products(seeded):
    """FR-2, SM-4: each seed company's list has its own products and none of the
    other's, on both pages."""
    for number, mine, theirs in (("1001", "10", "20"), ("1002", "20", "10")):
        company = Company.objects.get(customer_number=number)
        first = f"{mine}001" if mine == "10" else "20001"
        for path in ("/produkter/", f"/produkter/{first}/"):
            numbers = [
                item[2]
                for _, _, _, items in groups_of(page(company, path))
                for item in items
            ]
            assert numbers
            assert all(n.startswith(mine) for n in numbers)
            assert not any(n.startswith(theirs) for n in numbers)


def test_the_overview_makes_the_same_number_of_queries_for_50_products_of_104_weeks(db):
    """AD-2, NFR-8: three products or fifty products of 104 weeks give the overview the
    same number of queries: the 2 of the login and the 4 of the loader."""
    units = tuple(10 + week % 7 for week in range(104))
    counts = []
    for name, products in (("Liten", 3), ("Stor", 50)):
        company = Company.objects.create(customer_number=name, name=name)
        for number in range(products):
            add_product(company, f"{10000 + number}", units, stock=number)
        client = Client()
        client.force_login(company)
        with CaptureQueriesContext(connection) as queries:
            assert client.get("/produkter/").status_code == 200
        counts.append(len(queries))

    assert counts[0] == counts[1] <= 6


def test_the_list_follows_the_order_of_the_core_for_50_products(db):
    """FR-24, E24: with 50 products the page lists them in the order of `build_overview`
    and every number of the list is the one of the display module."""
    company = Company.objects.create(customer_number="9003", name="Mange")
    for number in range(50):
        add_product(
            company, f"{10000 + number}", (10 + number % 5,) * 20, stock=number * 2
        )

    data = company_data.load_company_data(company)
    html = page(company)

    assert [i[2] for _, _, _, items in groups_of(html) for i in items] == list(
        data.overview.order
    )
    for _, _, number, _, text, _ in (
        i for _, _, _, items in groups_of(html) for i in items
    ):
        result = data.results[number]
        assert f"Uker dekning {display.weeks_of_cover(result.weeks_of_cover)}" in text


def test_the_label_and_the_reason_are_separated_in_the_text_of_a_card(page_a):
    """FR-24, NFR-11: with the tags removed and nothing put in their place, the label word
    and the reason still read as two words, so a tool that reads the link text does not run
    them together."""
    _, html = page_a

    inner = item_of(html, "10004")[5]

    assert "Middels Nytt nivå de siste 12 ukene" in " ".join(
        re.sub(r"<[^>]+>", "", inner).split()
    )
