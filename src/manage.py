"""Django's command-line utility for Prognose.

Run it through uv from the repository root, for example:
    uv run python src/manage.py migrate
"""

import os
import sys


def main():
    # Always Prognose's settings, also when another project's are exported.
    os.environ["DJANGO_SETTINGS_MODULE"] = "prognose.settings"
    try:
        from django.core.management import execute_from_command_line
    except ImportError as error:
        raise ImportError(
            "Fant ikke Django. Kjør «uv sync --locked» i prosjektmappa, og start "
            "kommandoen med uv run, for eksempel "
            "«uv run python src/manage.py migrate»."
        ) from error
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
