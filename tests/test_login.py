"""Innlogging at /, logout, and the CSRF checks of both forms (Stories 1.1, 1.4 and
1.8; FR-1, AD-6, AD-10, NFR-3, NFR-10, UX-DR8, UX-DR38).

The page texts are read from the Message Catalogue in EXPERIENCE.md, the copy
source, and the login uses the real hashes and passwords of the seed files.
"""

import io
import logging
import re

import pytest
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertRedirects,
    assertTemplateUsed,
)
from test_error_pages import assert_error_page, catalogue_text

from prognose import urls
from web.models import Company

LOGIN_ERROR = catalogue_text("Login error")[0]
INTRO = "Prognose foreslår hvor mye du bør bestille neste uke, og viser hvordan tallene er regnet."
WORDMARK_ONLY_HEADER = (
    '<header class="app-header"><span class="wordmark">Prognose</span></header>'
)
TOKEN = re.compile(r'name="csrfmiddlewaretoken" value="([^"]+)"')


def credentials(account):
    return {
        "customer_number": account.company.customer_number,
        "password": account.password,
    }


def csrf_token(response):
    """The token of the first form in the page, which the CSRF cookie belongs to."""
    return TOKEN.search(response.content.decode()).group(1)


def session_ids(client):
    """The primary key of the company that the client's session holds, or None.

    The test client's own session property would create a session, so this reads
    the stored one from the cookie.
    """
    cookie = client.cookies.get(settings.SESSION_COOKIE_NAME)
    if cookie is None:
        return None
    return SessionStore(cookie.value).get("_auth_user_id")


def test_login_page_is_the_wireframe_with_a_wordmark_only_header(client):
    """FR-1, UX-DR8, NFR-11, NFR-6: the page has the title «Logg inn», the line,
    the fields with visible labels, the primary button and the README note, a
    header with only the wordmark, and one form that Enter submits."""
    response = client.get("/")

    assertTemplateUsed(response, "web/login.html")
    assert response["Content-Type"] == "text/html; charset=utf-8"
    assertContains(response, '<html lang="nb">')
    assertContains(response, "<title>Logg inn – Prognose</title>", html=True)
    assertContains(response, "<h1>Logg inn</h1>", html=True)
    assertContains(response, f"<p>{INTRO}</p>", html=True)
    assertContains(response, WORDMARK_ONLY_HEADER, html=True)
    assertContains(
        response, '<label for="id_customer_number">Kundenummer</label>', html=True
    )
    assertContains(response, '<label for="id_password">Passord</label>', html=True)
    assertContains(
        response,
        '<button type="submit" class="button-primary">Logg inn</button>',
        html=True,
    )
    assertContains(response, "Innloggingen for testbedriftene står i README.")
    assertNotContains(response, 'role="alert"')
    content = response.content.decode()
    # One form with its submit button and no script: Enter in a field submits it.
    assert content.count("<form") == 1
    assert 'method="post"' in content
    assert "<script" not in content


def test_login_page_reads_no_data_for_a_visitor_without_a_session(client, db):
    """FR-1, AD-6: the login page of a visitor with no session cookie reads nothing
    from the database."""
    with CaptureQueriesContext(connection) as queries:
        assert client.get("/").status_code == 200

    assert len(queries) == 0


def test_login_page_has_a_data_icon_and_no_src_or_href_with_a_host(client):
    """NFR-1: the icon is an empty data: URL, and no src or href holds a URL with a host."""
    response = client.get("/")

    assertContains(response, '<link rel="icon" href="data:,">', html=True)
    assert not re.search(r'(?:src|href)="(?:[a-z]+:)?//', response.content.decode())


def test_login_page_answers_get_head_and_post_only(client):
    """AD-10: a method the page does not take gets 405."""
    assert client.head("/").status_code == 200
    assert client.options("/").status_code == 405


def test_correct_login_opens_the_product_overview(client, two_companies):
    """FR-1, AD-10: the right number and password log in and redirect to
    /produkter/, which then shows the company's products."""
    a, _ = two_companies

    response = client.post("/", credentials(a))

    assertRedirects(response, "/produkter/")
    assert session_ids(client) == str(a.company.pk)
    assertContains(client.get("/produkter/"), "Hammer fra A")


def test_login_keeps_the_hash_and_stores_no_plain_password(client, two_companies):
    """FR-1, NFR-3: a login does not rewrite the seed's hash, and the password
    reaches neither the session store, the console log nor the page."""
    a, _ = two_companies
    seed_hash = a.company.password
    handler = logging.getHandlerByName("console")
    stream = io.StringIO()
    previous = handler.setStream(stream)
    try:
        wrong = client.post("/", {**credentials(a), "password": "hemmelig-feil-123"})
        client.post("/", credentials(a))
    finally:
        handler.setStream(previous)
    a.company.refresh_from_db()

    assert a.company.password == seed_hash
    assert a.company.password.startswith("pbkdf2_sha256$")
    assert a.company.last_login is not None
    stored = " ".join(Session.objects.values_list("session_data", flat=True))
    for secret in (a.password, "hemmelig-feil-123"):
        assert secret not in stream.getvalue()
        assert secret not in stored
        assertNotContains(wrong, secret)


@pytest.mark.parametrize(
    "change",
    [
        {"customer_number": "9999"},
        {"password": "feil-passord"},
        {"password": " testbedrift-a "},
        {"customer_number": ""},
        {"password": ""},
        {"customer_number": "10\x0001"},
        {"customer_number": "1" * 500},
    ],
    ids=[
        "unknown number",
        "wrong password",
        "password with spaces",
        "blank number",
        "blank password",
        "NUL character",
        "very long number",
    ],
)
def test_failed_login_shows_one_message_and_keeps_the_number(
    client, two_companies, change
):
    """FR-1, UX-DR8, UX-DR38: whatever is wrong, the same message stands above
    the fields with role="alert", the customer number is kept, the password field is empty, and nobody is logged in."""
    a, _ = two_companies
    data = {**credentials(a), **change}

    response = client.post("/", data)

    assert response.status_code == 200
    assertTemplateUsed(response, "web/login.html")
    content = response.content.decode()
    assert content.count('role="alert"') == 1
    assert f"</span>{LOGIN_ERROR}</p>" in content
    assert content.index('role="alert"') < content.index("<label")
    assertContains(response, 'aria-describedby="login-error"', count=2)
    assertContains(response, 'aria-invalid="true"', count=2)
    assert 'type="password" id="id_password" name="password" autocomplete' in content
    assert 'name="password" value' not in content
    assert f'value="{data["customer_number"]}"' in content
    assert session_ids(client) is None


def test_wrong_number_and_wrong_password_give_the_same_page(client, two_companies):
    """FR-1: nothing in the answer tells a wrong number from a wrong password."""
    a, _ = two_companies

    def page(data):
        html = client.post("/", data).content.decode()
        return TOKEN.sub("", re.sub(r'value="[^"]*"', "", html))

    assert page({"customer_number": "9999", "password": a.password}) == page(
        {"customer_number": "1001", "password": "feil"}
    )


def test_customer_number_is_trimmed_but_the_password_is_not(client, two_companies):
    """FR-1: spaces around the customer number are ignored, those of the password count."""
    a, _ = two_companies

    assertRedirects(
        client.post("/", {**credentials(a), "customer_number": " 1001 "}), "/produkter/"
    )


def test_logged_in_user_is_sent_from_the_login_page_to_the_overview(
    client, two_companies
):
    """NFR-10, AD-10: opening / again after the login, as Back or a reload does,
    shows the product overview, not the form."""
    a, _ = two_companies
    client.force_login(a.company)

    assertRedirects(client.get("/"), "/produkter/")
    first = client.get("/produkter/").content.decode()
    again = client.get("/produkter/").content.decode()
    # Each page has its own masked CSRF token, in the logout form.
    assert TOKEN.sub("", again) == TOKEN.sub("", first)


def test_login_ignores_a_next_address(client, two_companies):
    """AD-6: no address from the request decides where a login or the login
    redirect leads, so there is no open redirect."""
    a, _ = two_companies

    assertRedirects(client.get("/produkter/?next=https://evil.example/"), "/")
    assertRedirects(
        client.post("/?next=https://evil.example/", credentials(a)), "/produkter/"
    )


# A sample address for each route with a parameter (Story 2.7).
SAMPLE_ADDRESSES = {"produkter/<str:product_number>/": "produkter/10001/"}


def exempt_routes():
    return [
        pattern
        for pattern in urls.urlpatterns
        if not getattr(pattern.callback, "login_required", True)
    ]


def test_only_the_login_page_is_exempt_from_the_login():
    """FR-1, AD-6: the middleware denies by default, and only the login page is
    exempt. A later route that is not exempt needs no change here."""
    assert [pattern.name for pattern in exempt_routes()] == ["login"]


@pytest.mark.parametrize("enforce_csrf", [False, True], ids=["no CSRF", "CSRF"])
@pytest.mark.parametrize("method", ["get", "post"])
@pytest.mark.parametrize(
    "pattern",
    [pattern for pattern in urls.urlpatterns if pattern.name != "login"],
    ids=lambda pattern: pattern.name,
)
def test_every_page_but_the_login_sends_a_visitor_to_the_login_page(
    pattern, method, enforce_csrf
):
    """FR-1, AD-6, NFR-10: a request without a login, with GET or POST, gets the
    login page. A browser's POST carries no token when the session and the CSRF
    cookie are gone, so it must do so with the CSRF check on too. A route with
    a parameter needs a sample address added to SAMPLE_ADDRESSES."""
    address = SAMPLE_ADDRESSES.get(str(pattern.pattern), str(pattern.pattern))
    assert "<" not in address, "Give this route a sample address."
    client = Client(enforce_csrf_checks=enforce_csrf)

    response = getattr(client, method)(f"/{address}")

    assertRedirects(response, "/")


def test_middleware_order_puts_the_login_check_after_the_authentication(settings):
    """AD-6, AD-12: the error handling stays outermost, and the login check runs
    after the authentication that it reads."""
    middleware = settings.MIDDLEWARE
    assert middleware[0] == "web.middleware.ErrorPageMiddleware"
    assert middleware.index(
        "web.middleware.LoginRequiredMiddleware"
    ) > middleware.index("django.contrib.auth.middleware.AuthenticationMiddleware")
    assert settings.LOGIN_URL == "login"


# Logout


def test_logout_post_ends_the_session(client, two_companies):
    """FR-1, AD-6, AD-10: POST /logg-ut/ ends the session on the server, so the
    old session cookie is worthless, and opens the login page; the product
    overview then needs a new login."""
    a, _ = two_companies
    client.force_login(a.company)
    old_cookie = client.cookies[settings.SESSION_COOKIE_NAME].value
    assert Session.objects.filter(session_key=old_cookie).exists()

    assertRedirects(client.post("/logg-ut/"), "/")

    assert session_ids(client) is None
    assert not Session.objects.filter(session_key=old_cookie).exists()
    replayed = Client()
    replayed.cookies[settings.SESSION_COOKIE_NAME] = old_cookie
    assertRedirects(replayed.get("/produkter/"), "/")


def test_logout_get_does_not_end_the_session(client, two_companies):
    """FR-1, AD-6, AD-10: a GET to /logg-ut/, such as a link or a prefetch, gives
    405 and leaves the session alone."""
    a, _ = two_companies
    client.force_login(a.company)

    assert client.get("/logg-ut/").status_code == 405
    assert session_ids(client) == str(a.company.pk)
    assert client.get("/produkter/").status_code == 200


def test_second_logout_gives_the_same_result(two_companies):
    """NFR-10, AD-10: a second POST of the logout form, with the CSRF check on,
    sends the visitor to the login page again, with no error."""
    a, _ = two_companies
    client = Client(enforce_csrf_checks=True)
    client.force_login(a.company)
    token = csrf_token(client.get("/produkter/"))

    first = client.post("/logg-ut/", {"csrfmiddlewaretoken": token})
    second = client.post("/logg-ut/", {"csrfmiddlewaretoken": token})

    assertRedirects(first, "/")
    assertRedirects(second, "/")


def test_logout_after_the_session_and_the_csrf_cookie_are_gone_opens_the_login_page():
    """NFR-10, AD-10: a logout POST from a form that outlived both the session
    and the CSRF cookie, such as a page left open overnight, gives the login
    page, not the expired-form page. It logs nobody out, since nobody is in."""
    client = Client(enforce_csrf_checks=True)

    assertRedirects(client.post("/logg-ut/"), "/")
    assertRedirects(client.post("/logg-ut/", {"csrfmiddlewaretoken": "x" * 64}), "/")


# CSRF


def test_login_form_has_a_csrf_token_and_the_page_sets_the_cookie(two_companies):
    """AD-10, NFR-3: the login form carries a CSRF token, and the page sets the
    cookie it belongs to."""
    response = Client(enforce_csrf_checks=True).get("/")

    assert TOKEN.search(response.content.decode())
    assert "csrftoken" in response.cookies


def test_login_without_a_valid_csrf_token_logs_nobody_in(two_companies):
    """AD-10, NFR-3, NFR-10: a login POST with no token, a forged token, no
    cookie or another origin logs nobody in, even with the right password. The
    visitor gets a fresh login page, not an error."""
    a, _ = two_companies
    client = Client(enforce_csrf_checks=True)
    page = client.get("/")
    token = csrf_token(page)

    responses = [
        client.post("/", credentials(a)),
        client.post("/", {**credentials(a), "csrfmiddlewaretoken": "x" * 64}),
        client.post(
            "/",
            {**credentials(a), "csrfmiddlewaretoken": token},
            HTTP_ORIGIN="http://evil.example",
        ),
        Client(enforce_csrf_checks=True).post(
            "/", {**credentials(a), "csrfmiddlewaretoken": token}
        ),
    ]

    for response in responses:
        assertRedirects(response, "/")
    assert session_ids(client) is None
    assert Session.objects.count() == 0


def test_old_login_form_after_a_login_and_logout_gives_a_fresh_form(two_companies):
    """NFR-10, AD-10: Back after a logout brings up the login form from before
    the login, whose CSRF token the login has rotated. Sending it must not give
    the expired-form page: the visitor gets the login page, which logs in with
    the new form."""
    a, _ = two_companies
    client = Client(enforce_csrf_checks=True)
    old_form = {**credentials(a), "csrfmiddlewaretoken": csrf_token(client.get("/"))}
    client.post("/", old_form)
    products = client.get("/produkter/")
    client.post("/logg-ut/", {"csrfmiddlewaretoken": csrf_token(products)})

    response = client.post("/", old_form)

    assertRedirects(response, "/")
    assert session_ids(client) is None
    fresh = {**credentials(a), "csrfmiddlewaretoken": csrf_token(client.get("/"))}
    assertRedirects(client.post("/", fresh), "/produkter/")


def test_a_refused_form_is_still_logged(two_companies):
    """AD-12: a failed CSRF check that ends in a redirect is logged as before,
    without the request body."""
    a, _ = two_companies
    handler = logging.getHandlerByName("console")
    stream = io.StringIO()
    previous = handler.setStream(stream)
    try:
        Client(enforce_csrf_checks=True).post("/", credentials(a))
    finally:
        handler.setStream(previous)

    assert "Forbidden (CSRF cookie not set.): /" in stream.getvalue()
    assert a.password not in stream.getvalue()


def test_login_with_a_valid_csrf_token_works(two_companies):
    """AD-10: the same login with the page's token and cookie passes the check."""
    a, _ = two_companies
    client = Client(enforce_csrf_checks=True)
    token = csrf_token(client.get("/"))

    response = client.post("/", {**credentials(a), "csrfmiddlewaretoken": token})

    assertRedirects(response, "/produkter/")


def test_double_submit_of_the_login_form_gives_the_same_result(two_companies):
    """NFR-10, AD-10: the login rotates the CSRF token, so a second POST of the
    same form fails the check. It must not show the 403 page, but give the
    result of the first: the product overview."""
    a, _ = two_companies
    client = Client(enforce_csrf_checks=True)
    data = {**credentials(a), "csrfmiddlewaretoken": csrf_token(client.get("/"))}

    first = client.post("/", data)
    second = client.post("/", data)

    assertRedirects(first, "/produkter/")
    assertRedirects(second, "/produkter/", fetch_redirect_response=False)
    assert session_ids(client) == str(a.company.pk)
    assert client.get("/produkter/").status_code == 200


def test_two_submits_that_cross_each_other_both_log_in(two_companies):
    """NFR-10, AD-10: two POSTs sent with the same cookie and token before the
    first answer has arrived both pass the check and both log in."""
    a, _ = two_companies
    first = Client(enforce_csrf_checks=True)
    token = csrf_token(first.get("/"))
    second = Client(enforce_csrf_checks=True)
    second.cookies["csrftoken"] = first.cookies["csrftoken"].value
    data = {**credentials(a), "csrfmiddlewaretoken": token}

    assertRedirects(first.post("/", data), "/produkter/", fetch_redirect_response=False)
    assertRedirects(
        second.post("/", data), "/produkter/", fetch_redirect_response=False
    )


def test_forged_login_cannot_switch_a_logged_in_company(two_companies):
    """FR-1, FR-2, NFR-3: a login POST that fails the CSRF check, as one from
    another site does, never logs in as the company in its body. A visitor who
    is already logged in is sent to the overview and stays the same company."""
    a, b = two_companies
    client = Client(enforce_csrf_checks=True)
    client.force_login(a.company)

    response = client.post("/", {**credentials(b), "csrfmiddlewaretoken": "x" * 64})

    assertRedirects(response, "/produkter/", fetch_redirect_response=False)
    assert session_ids(client) == str(a.company.pk)
    page = client.get("/produkter/")
    assertContains(page, "Hammer fra A")
    assertNotContains(page, "Rive fra B")


def test_logout_without_a_valid_csrf_token_is_refused(two_companies):
    """AD-10, AD-12: a logout POST with no token or a forged one gets the
    expired-form page and leaves the session, so another site cannot log the
    user out."""
    a, _ = two_companies
    client = Client(enforce_csrf_checks=True)
    client.force_login(a.company)

    for data in ({}, {"csrfmiddlewaretoken": "x" * 64}):
        assert_error_page(client.post("/logg-ut/", data), 403, "Expired form")
    assert session_ids(client) == str(a.company.pk)


def test_logout_form_is_a_post_form_with_a_csrf_token(client, two_companies):
    """FR-1, AD-6, AD-10, UX-DR14: «Logg ut» in the header is a POST form with a token."""
    a, _ = two_companies
    client.force_login(a.company)

    content = client.get("/produkter/").content.decode()

    form = re.search(
        r'<form method="post" action="/logg-ut/">(.*?)</form>', content, re.DOTALL
    )
    assert form
    assert TOKEN.search(form.group(1))
    assert '<button type="submit">Logg ut</button>' in form.group(1)


def test_a_company_that_does_not_exist_cannot_log_in(client, db):
    """FR-1: with no companies in the database, every login fails the same way."""
    assert Company.objects.count() == 0

    assertContains(
        client.post("/", {"customer_number": "1001", "password": "x"}), LOGIN_ERROR
    )


def test_seed_hashes_are_the_ones_that_log_in(client, two_companies):
    """FR-1, NFR-3: the seed's PBKDF2 hashes check both test companies' documented passwords."""
    for account in two_companies:
        assertRedirects(client.post("/", credentials(account)), "/produkter/")
        client.post("/logg-ut/")
