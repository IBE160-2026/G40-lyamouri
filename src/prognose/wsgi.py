"""WSGI entry point, which runserver finds through WSGI_APPLICATION."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prognose.settings")

application = get_wsgi_application()
