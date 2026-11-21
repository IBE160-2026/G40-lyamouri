"""WSGI entry point, which runserver finds through WSGI_APPLICATION."""

import os

from django.core.wsgi import get_wsgi_application

# Always Prognose's settings, also when another project's are exported.
os.environ["DJANGO_SETTINGS_MODULE"] = "prognose.settings"

application = get_wsgi_application()
