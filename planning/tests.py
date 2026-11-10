"""Start page, error pages, health check and load_seed (Story 1.1; AD-5, AD-12, NFR-3, NFR-10).

The page tests use SimpleTestCase where a view must not touch the database.
"""

import os
import tempfile
from io import StringIO
from pathlib import Path
from unittest import mock

from django.contrib.staticfiles import finders
from django.core.management import call_command
from django.db import OperationalError, connection
from django.http import HttpResponse
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from django.urls import path

from prognose.env import load_secret_key

# A view without login_not_required, used as ROOT_URLCONF by LoginRequiredTests.
urlpatterns = [path("privat/", lambda request: HttpResponse("privat"))]


class StartPageTests(SimpleTestCase):
    def test_start_page_is_norwegian_and_uses_the_stylesheet(self):
        response = self.client.get("/")
        self.assertContains(response, '<html lang="nb">')
        self.assertContains(response, "<h1>Prognose</h1>", html=True)
        self.assertContains(
            response, '<link rel="stylesheet" href="/static/css/app.css">', html=True
        )

    def test_stylesheet_is_a_static_file(self):
        self.assertIsNotNone(finders.find("css/app.css"))


class LoginRequiredTests(SimpleTestCase):
    """AD-5: a view needs a login unless it is marked login_not_required."""

    @override_settings(ROOT_URLCONF=__name__)
    def test_views_need_a_login_by_default(self):
        response = self.client.get("/privat/")
        self.assertRedirects(response, "/?next=/privat/", fetch_redirect_response=False)


class NotFoundTests(SimpleTestCase):
    """NFR-10 and UX-DR9: unknown addresses get the Norwegian «Ikke funnet» page."""

    def test_unknown_address(self):
        with self.assertLogs("django.request", "WARNING"):
            response = self.client.get("/finnes-ikke/")
        self.assertContains(
            response, "<h1>Ikke funnet</h1>", status_code=404, html=True
        )
        self.assertContains(
            response, '<a href="/">Til startsiden</a>', status_code=404, html=True
        )
        self.assertContains(response, '<html lang="nb">', status_code=404)
        # Never Django's debug page, which explains the URLconf.
        self.assertNotContains(response, "URLconf", status_code=404)


class HealthTests(TestCase):
    """AD-15 and DR-10: /helse/ proves that the app reads its database."""

    def test_answers_ok_after_one_read_of_the_company_table(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get("/helse/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")
        self.assertEqual(len(queries), 1)
        self.assertIn('"accounts_company"', queries[0]["sql"])

    def test_database_error_gives_the_norwegian_error_page(self):
        client = Client(raise_request_exception=False)
        failing_database = mock.patch(
            "django.db.backends.utils.CursorWrapper.execute",
            side_effect=OperationalError("database unavailable"),
        )
        with failing_database, self.assertLogs("django.request", "ERROR"):
            response = client.get("/helse/")
        self.assertContains(
            response, "<h1>Noe gikk galt</h1>", status_code=500, html=True
        )
        self.assertContains(response, '<html lang="nb">', status_code=500)


class LoadSeedTests(SimpleTestCase):
    """AD-12 and NFR-3: load_seed creates the local session secret once."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.secret_file = Path(folder.name) / ".secret_key"

    def load_seed(self):
        output = StringIO()
        with override_settings(SECRET_KEY_FILE=self.secret_file):
            call_command("load_seed", stdout=output)
        return output.getvalue()

    def test_creates_the_missing_secret_file_for_the_owner_only(self):
        self.assertIn("Lagde .secret_key", self.load_seed())
        key = self.secret_file.read_text(encoding="utf-8")
        self.assertRegex(key, r"^[A-Za-z0-9_-]{67}$")  # secrets.token_urlsafe(50)
        if os.name == "posix":  # Windows has no owner-only file mode
            self.assertEqual(self.secret_file.stat().st_mode & 0o777, 0o600)

    def test_leaves_an_existing_secret_unchanged(self):
        self.secret_file.write_text("eksisterende-nokkel", encoding="utf-8")
        self.assertIn("er ikke endret", self.load_seed())
        self.assertEqual(
            self.secret_file.read_text(encoding="utf-8"), "eksisterende-nokkel"
        )

    def test_running_twice_keeps_the_first_secret_which_the_settings_read(self):
        self.load_seed()
        first = self.secret_file.read_text(encoding="utf-8")
        self.load_seed()
        self.assertEqual(self.secret_file.read_text(encoding="utf-8"), first)
        self.assertEqual(load_secret_key(self.secret_file), first)
