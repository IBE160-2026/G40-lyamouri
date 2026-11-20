"""README step 5: uv run python src/manage.py runserver --insecure (Story 1.1; AD-13, NFR-1).

These tests have no database access.
"""

from django.core.handlers.wsgi import WSGIHandler
from django.core.management import get_commands, load_command_class
from django.core.servers.basehttp import get_internal_wsgi_application


def test_runserver_comes_from_staticfiles_and_accepts_insecure():
    """AD-13, NFR-1: runserver is the version from django.contrib.staticfiles,
    the one that has the --insecure option of the documented start command."""
    app_name = get_commands()["runserver"]
    command = load_command_class(app_name, "runserver")
    options = command.create_parser("manage.py", "runserver").parse_args(["--insecure"])

    assert app_name == "django.contrib.staticfiles"
    assert options.insecure_serving is True


def test_runserver_loads_the_wsgi_application():
    """AD-13, NFR-1: the application that runserver serves loads from
    WSGI_APPLICATION."""
    assert isinstance(get_internal_wsgi_application(), WSGIHandler)
