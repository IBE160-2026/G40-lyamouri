"""WSGI entry point. Vercel runs it as one function in fra1 (AD-13).

Vercel finds it through WSGI_APPLICATION in the settings.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prognose.settings")

application = get_wsgi_application()
