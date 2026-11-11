"""python manage.py load_seed (AD-12).

This first version only creates the local session secret when it is missing.
The seed data is added in Story 1.2.
"""

import os
import secrets

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Lager den hemmelige nøkkelen i .secret_key hvis fila mangler."

    def handle(self, *args, **options):
        path = settings.SECRET_KEY_FILE
        if path.exists():
            self.stdout.write(f"{path.name} finnes allerede og er ikke endret.")
            return
        # Only the owner may read or write the file (mode 0600).
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            file.write(secrets.token_urlsafe(50))
        self.stdout.write(self.style.SUCCESS(f"Lagde {path.name}."))
