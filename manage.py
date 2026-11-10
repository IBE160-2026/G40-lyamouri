#!/usr/bin/env python
"""Django's command-line utility for Prognose."""

import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prognose.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as error:
        raise ImportError(
            "Fant ikke Django. Aktiver det virtuelle miljøet (.venv) og kjør "
            "pip install -r requirements.txt."
        ) from error
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
