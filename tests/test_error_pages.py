"""The Norwegian error pages and the error log (Story 1.4; AD-12, NFR-10, NFR-5,
UX-DR13, UX-DR41).

Each page is checked against its text in the Message Catalogue in
EXPERIENCE.md, the copy source. Through assert_error_page, every page test also
checks that the page is Norwegian (NFR-5), that it is the not-found panel
(UX-DR13) and that its text is the catalogue's, verbatim (UX-DR41). The tests
use no database, so they also show that no error page reads it.
"""

import io
import logging
import re
from pathlib import Path

import pytest
from django.core.exceptions import PermissionDenied
from django.db import InterfaceError, OperationalError
from django.test import Client
from django.urls import path
from pytest_django.asserts import assertContains, assertNotContains

from prognose.urls import urlpatterns as app_urlpatterns

EXPERIENCE = (
    Path(__file__).resolve().parents[1]
    / "_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/EXPERIENCE.md"
)
# What no error page may show: the text of Django's default and debug pages,
# and the message of the test errors.
HIDDEN_TEXT = (
    "Traceback",
    "Not Found",
    "Forbidden",
    "Bad Request",
    "Server Error",
    "Method Not Allowed",
    "CSRF",
    "Testfeil",
)
LINK = '<a class="standalone-link" href="/produkter/">{}</a>'
ERRORS = {
    "server": RuntimeError,
    "tilgang": PermissionDenied,
    "database": OperationalError,
    "grensesnitt": InterfaceError,
}


def raise_error(request, name):
    """A test view that raises the named error."""
    raise ERRORS[name]("Testfeil")


class DatabaseErrorBeforeView:
    """A test middleware that raises a database error before the view, as a
    middleware that reads the session can."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        raise OperationalError("Testfeil")


class DatabaseErrorAfterView(DatabaseErrorBeforeView):
    """A test middleware that raises a database error after the view, as saving
    the session can."""

    def __call__(self, request):
        self.get_response(request)
        raise OperationalError("Testfeil")


urlpatterns = [*app_urlpatterns, path("feil/<str:name>/", raise_error)]
pytestmark = pytest.mark.urls(__name__)


def catalogue_text(message):
    """Return the text of a Message Catalogue row and its link text, or None."""
    catalogue = EXPERIENCE.read_text(encoding="utf-8").split("## Message Catalogue")[1]
    for line in catalogue.split("\n## ")[0].splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] == message:
            quoted = re.findall(r"«(.+?)»", cells[2])
            return quoted[0], (quoted[1] if len(quoted) > 1 else None)
    raise LookupError(message)


def heading(message):
    """Return the page title for a message: its first sentence without the full stop."""
    return catalogue_text(message)[0].partition(". ")[0].removesuffix(".")


def assert_error_page(response, status, message):
    """NFR-5, UX-DR13, UX-DR41: assert that the response is the not-found panel
    with the message's text, and with no English or debug text.

    The first sentence is the page title, the rest of the text is a paragraph,
    and the link «Til produktoversikten» is there only when the catalogue names
    it. A Content-Length header must match the body, or a browser cuts it off.
    """
    text, link = catalogue_text(message)
    rest = text.partition(". ")[2]

    assert response.status_code == status
    assert response["Content-Type"] == "text/html; charset=utf-8"
    if response.has_header("Content-Length"):
        assert int(response["Content-Length"]) == len(response.content)
    title = f"<title>{heading(message)} – Prognose</title>"
    assertContains(response, title, html=True, status_code=status)
    assertContains(
        response, f"<h1>{heading(message)}</h1>", html=True, status_code=status
    )
    if rest:
        assertContains(response, f"<p>{rest}</p>", html=True, status_code=status)
    if link:
        assertContains(response, LINK.format(link), html=True, status_code=status)
    else:
        assertNotContains(response, "<a ", status_code=status)
    for hidden in HIDDEN_TEXT:
        assertNotContains(response, hidden, status_code=status)


def error_client(**options):
    """Return a test client that gives the error page instead of raising the error."""
    return Client(raise_request_exception=False, **options)


def test_unknown_address_shows_the_not_found_page(client):
    """NFR-10, NFR-5, AD-12, UX-DR13, UX-DR41: an unknown address gives 404 with
    «Siden finnes ikke» and the link to the product overview, and no debug
    page."""
    assert_error_page(client.get("/finnes-ikke/"), 404, "Not found")


@pytest.mark.parametrize("name", ["database", "grensesnitt"])
def test_database_error_in_a_view_shows_the_503_page(name):
    """AD-12, NFR-10, NFR-5, UX-DR13, UX-DR41: a database error in a view gives
    503 with the Database unavailable text and no link, and keeps the headers
    that the other middleware set, such as the security headers."""
    response = error_client().get(f"/feil/{name}/")

    assert_error_page(response, 503, "Database unavailable")
    assert response["X-Content-Type-Options"] == "nosniff"


@pytest.mark.parametrize(
    "middleware", ["DatabaseErrorBeforeView", "DatabaseErrorAfterView"]
)
def test_database_error_in_another_middleware_shows_the_503_page(settings, middleware):
    """AD-12, NFR-5, UX-DR13, UX-DR41: the 503 handling sits in the outermost
    middleware, so a database error raised in another middleware, before or
    after the view, also gives the 503 page."""
    outermost, *others = settings.MIDDLEWARE
    assert outermost == "web.middleware.ErrorPageMiddleware"
    settings.MIDDLEWARE = [outermost, f"{__name__}.{middleware}", *others]

    assert_error_page(error_client().get("/"), 503, "Database unavailable")


def test_database_error_shows_the_503_page_also_with_debug_on(settings):
    """AD-12, NFR-10, NFR-5, UX-DR13, UX-DR41: with DEBUG on, a database error
    still gives the 503 page as HTML, also to a request that does not accept
    HTML, for which Django's debug page is plain text."""
    settings.DEBUG = True
    response = error_client().get("/feil/database/", HTTP_ACCEPT="application/json")

    assert_error_page(response, 503, "Database unavailable")


def test_failed_csrf_check_shows_the_expired_form_page():
    """AD-12, NFR-10, NFR-5, UX-DR13, UX-DR41: a form sent without a valid CSRF
    token gives 403 with the Expired form text, never the Server error text."""
    response = Client(enforce_csrf_checks=True).post("/")

    assert_error_page(response, 403, "Expired form")
    assertNotContains(response, heading("Server error"), status_code=403)


def test_other_403_shows_the_server_error_page():
    """AD-12, NFR-5, UX-DR13, UX-DR41: a 403 that is not a failed CSRF check
    gives the Server error text and the link, never the expired-form text."""
    response = error_client().get("/feil/tilgang/")

    assert_error_page(response, 403, "Server error")
    assertNotContains(response, heading("Expired form"), status_code=403)


def test_bad_request_shows_the_server_error_page(client):
    """AD-12, NFR-10, NFR-5, UX-DR13, UX-DR41: a request the app cannot use,
    here one for an unknown host, gives 400 with the Server error text and the
    link."""
    assert_error_page(client.get("/", HTTP_HOST="evil.example"), 400, "Server error")


def test_wrong_method_shows_the_server_error_page_and_keeps_allow(client):
    """AD-12, NFR-10, NFR-5, UX-DR13, UX-DR41: a method the page does not take
    gives 405 with the Server error text, and the Allow header still names the
    methods it takes."""
    response = client.options("/")

    assert_error_page(response, 405, "Server error")
    assert response["Allow"] == "GET, HEAD"


@pytest.fixture
def console():
    """Collect what the console handler from LOGGING writes during the test."""
    handler = logging.getHandlerByName("console")
    stream = io.StringIO()
    previous = handler.setStream(stream)
    yield stream
    handler.setStream(previous)


def test_server_error_shows_its_page_and_is_logged_without_secrets(console, settings):
    """AD-12, NFR-10, NFR-4, NFR-5, UX-DR13, UX-DR41: with DEBUG off, an
    unexpected error in a POST gives 500 with the Server error text and the
    link, and reaches the console with its traceback, but not the request body,
    the session secret, a database URL in either scheme or the database
    password. Only the names of leaked values are shown if the test fails."""
    password = "hemmelig-passord-123"
    data = {"kundenummer": "10001", "passord": password}
    response = error_client().post("/feil/server/", data)
    output = console.getvalue()
    database_password = settings.DATABASES["default"]["PASSWORD"]
    leaked = [
        name
        for name, found in [
            ("the posted password", password in output),
            ("the request body", "kundenummer" in output),
            ("the session secret", settings.SECRET_KEY in output),
            ("a database URL", re.search(r"postgres(?:ql)?://", output) is not None),
            (
                "the database password",
                bool(database_password) and database_password in output,
            ),
        ]
        if found
    ]

    assert not settings.DEBUG
    assert_error_page(response, 500, "Server error")
    assertNotContains(response, password, status_code=500)
    assert "Internal Server Error: /feil/server/" in output
    assert "RuntimeError: Testfeil" in output
    assert leaked == []


def test_warnings_and_security_errors_are_logged(console):
    """AD-12: with DEBUG off, the warning for an unknown address, a failed CSRF
    check and a request for an unknown host also reach the console."""
    Client().get("/finnes-ikke/")
    Client(enforce_csrf_checks=True).post("/")
    Client().get("/", HTTP_HOST="evil.example")
    output = console.getvalue()

    assert "Not Found: /finnes-ikke/" in output
    assert "Forbidden (CSRF cookie not set.): /" in output
    assert "Invalid HTTP_HOST header: 'evil.example'." in output


def test_logging_keeps_runserver_lines_and_prints_each_error_once():
    """AD-12: "django.server", which prints runserver's requests, keeps its
    handler at INFO, and the two configured loggers do not pass their records
    on to the "django" logger, which would print them again with DEBUG on."""
    server = logging.getLogger("django.server")

    assert server.handlers
    assert server.level == logging.INFO
    assert not logging.getLogger("django.request").propagate
    assert not logging.getLogger("django.security").propagate
