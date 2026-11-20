"""The start page at / (Story 1.1; AD-10, AD-11, NFR-1, NFR-6, NFR-11).

These tests have no database access, so they also show that the page reads no
data.
"""

import re

from pytest_django.asserts import assertContains, assertTemplateUsed


def test_start_page_is_norwegian_and_shows_the_wordmark(client):
    """NFR-11, NFR-6, AD-11: the page declares Norwegian, has the responsive
    viewport tag and shows the wordmark «Prognose»."""
    response = client.get("/")

    assertTemplateUsed(response, "web/start.html")
    assert response["Content-Type"] == "text/html; charset=utf-8"
    assertContains(response, '<html lang="nb">')
    assertContains(
        response,
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        html=True,
    )
    assertContains(response, "<h1>Prognose</h1>", html=True)


def test_start_page_has_a_data_icon_and_no_src_or_href_with_a_host(client):
    """NFR-1: the icon is an empty data: URL, so the browser does not ask for a
    favicon, and no double-quoted, lowercase src or href attribute holds a URL
    with a host, such as https://... or //..."""
    response = client.get("/")

    assertContains(response, '<link rel="icon" href="data:,">', html=True)
    assert not re.search(r'(?:src|href)="(?:[a-z]+:)?//', response.content.decode())


def test_start_page_only_answers_get_and_head(client):
    """AD-10: the start page has no form, so a POST gets 405."""
    assert client.head("/").status_code == 200
    assert client.post("/").status_code == 405
