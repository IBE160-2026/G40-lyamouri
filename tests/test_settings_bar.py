"""The settings bar of every page after login (Story 2.8).

FR-20, FR-21, UX-DR7, UX-DR15, AD-4. The texts are the Message Catalogue's and UX-DR15's, written
out; the settings come from the company's settings row, or the FR-20 defaults without one.
"""

import re
from decimal import Decimal

import pytest
from django.test import Client
from test_company_data import add_product
from test_error_pages import assert_error_page

from explanation import settings_bar as words
from forecasting.settings import (
    EXPONENTIAL_SMOOTHING,
    MOVING_AVERAGE,
    ForecastSettings,
)
from web.models import Company, CompanySettings

NBSP = " "


def page(company, path="/produkter/"):
    client = Client()
    client.force_login(company)
    response = client.get(path)
    assert response.status_code == 200
    return response.content.decode()


def bar_of(html):
    return html[html.index('<div class="settings-bar">') :].split("</div>")[0]


def test_the_defaults_have_the_texts_of_ux_dr15():
    """UX-DR15, FR-20: the default settings read as the user story names them."""
    assert words.settings_texts(ForecastSettings()) == (
        "Glidende gjennomsnitt, 3 uker",
        f"Scenarioprosent 10{NBSP}%",
        f"Sikkerhetsmargin 10{NBSP}%",
        "Uvanlige uker: tas med",
    )


@pytest.mark.parametrize(
    ("settings", "texts"),
    [
        (
            ForecastSettings(method=MOVING_AVERAGE, window=12),
            "Glidende gjennomsnitt, 12 uker",
        ),
        (
            ForecastSettings(
                method=EXPONENTIAL_SMOOTHING, smoothing_factor=Decimal("0.3")
            ),
            "Eksponentiell glatting, faktor 0,3",
        ),
        (
            ForecastSettings(method=EXPONENTIAL_SMOOTHING, smoothing_factor=0.9),
            "Eksponentiell glatting, faktor 0,9",
        ),
    ],
)
def test_the_method_is_named_with_its_window_or_its_factor(settings, texts):
    """FR-20, UX-DR15: the window for the moving average, the factor with a decimal
    comma for exponential smoothing."""
    assert words.settings_texts(settings)[0] == texts


def test_each_other_setting_has_its_own_text():
    """FR-20, UX-DR15, UX-DR25: the percentages are whole numbers with a no-break space
    before «%», and the unusual weeks are «tas med» or «holdes utenfor»."""
    settings = ForecastSettings(
        scenario_percentage=0, safety_margin=100, unusual_weeks_included=False
    )

    assert words.settings_texts(settings)[1:] == (
        f"Scenarioprosent 0{NBSP}%",
        f"Sikkerhetsmargin 100{NBSP}%",
        "Uvanlige uker: holdes utenfor",
    )


def test_an_unknown_method_is_refused_instead_of_left_out():
    """AD-4: a method without a text is a loud error, never a silent gap in the bar."""
    with pytest.raises(ValueError):
        words.settings_texts(ForecastSettings(method="other"))


def test_both_pages_show_the_bar_without_the_button(two_companies):
    """UX-DR15: the overview and a product screen show the label, the four values and the
    note about all products, in that order and without «Endre innstillinger», which
    comes in Epic 3."""
    for path in ("/produkter/", "/produkter/10001/"):
        bar = bar_of(page(two_companies[0].company, path))

        assert [
            t.strip() for t in re.sub(r"<[^>]+>", "\n", bar).split("\n") if t.strip()
        ] == [
            "Innstillinger i bruk:",
            "Glidende gjennomsnitt, 3 uker",
            f"Scenarioprosent 10{NBSP}%",
            f"Sikkerhetsmargin 10{NBSP}%",
            "Uvanlige uker: tas med",
            "Endringen gjelder alle produkter i bedriften.",
        ]
        assert "Endre innstillinger" not in bar
        assert "<button" not in bar and "<a " not in bar


def test_the_bar_follows_the_company_settings_row(db):
    """FR-20, FR-21: a company's own settings are the ones in its bar, and another
    company's row never reaches it."""
    company = Company.objects.create(customer_number="9010", name="Egen")
    other = Company.objects.create(customer_number="9011", name="Annen")
    add_product(company, "10001", (10, 10, 10))
    CompanySettings.objects.create(
        company=company,
        method=EXPONENTIAL_SMOOTHING,
        smoothing_factor=Decimal("0.5"),
        scenario_percentage=20,
        safety_margin=0,
        unusual_weeks_included=False,
    )
    CompanySettings.objects.create(company=other, window=9)

    bar = bar_of(page(company))

    assert "Eksponentiell glatting, faktor 0,5" in bar
    assert f"Scenarioprosent 20{NBSP}%" in bar
    assert f"Sikkerhetsmargin 0{NBSP}%" in bar
    assert "Uvanlige uker: holdes utenfor" in bar
    assert "9 uker" not in bar


def test_the_bar_comes_after_the_header_and_before_the_list(two_companies):
    """UX-DR15, UX-DR43: Tab and reading order are the header, the settings bar, the list
    and the product."""
    html = page(two_companies[0].company, "/produkter/10001/")

    assert (
        html.index("</header>")
        < html.index('class="settings-bar"')
        < html.index('aria-label="Produkter"')
        < html.index('id="valgt-produkt"')
    )


def test_pages_without_a_login_and_the_error_pages_have_no_bar(client, two_companies):
    """AD-12, UX-DR13: the login and the error pages show no company data and so no bar."""
    assert "settings-bar" not in client.get("/").content.decode()
    client.force_login(two_companies[0].company)
    response = client.get("/finnes-ikke/")
    assert_error_page(response, 404, "Not found")
    assert "settings-bar" not in response.content.decode()


def test_the_values_are_separated_in_the_text_of_the_bar(two_companies):
    """UX-DR15, NFR-11: with the tags removed and nothing put in their place, the values
    still read as separate words, so a tool that reads the text of the bar does not run
    them together."""
    bar = bar_of(page(two_companies[0].company))

    text = " ".join(re.sub(r"<[^>]+>", "", bar).split())

    # split() also treats the no-break space as a space, which the test of the default texts checks.
    assert text == (
        "Innstillinger i bruk: Glidende gjennomsnitt, 3 uker "
        "Scenarioprosent 10 % Sikkerhetsmargin 10 % "
        "Uvanlige uker: tas med Endringen gjelder alle produkter i bedriften."
    )
