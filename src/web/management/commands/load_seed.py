"""uv run python src/manage.py load_seed (AD-13, NFR-3).

For now the command only creates the local session secret when it is missing.
It loads no data.
"""

import os
import secrets
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from prognose.env import read_secret_key


class Command(BaseCommand):
    help = "Lager den hemmelige nøkkelen for øktene i .secret_key hvis fila mangler."

    def handle(self, *args, **options):
        path = Path(settings.SECRET_KEY_FILE)
        try:
            # O_EXCL: create the file only if it does not exist, so an existing
            # key is never rewritten. Only the owner may read or write it.
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            if not read_secret_key(path):
                raise CommandError(
                    f"{path.name} er tom. Slett fila og kjør load_seed på nytt."
                ) from None
            self.stdout.write(f"{path.name} finnes allerede og er ikke endret.")
            return
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            file.write(secrets.token_urlsafe(50))
        self.stdout.write(
            self.style.SUCCESS(f"Lagde {path.name} med en ny hemmelig nøkkel.")
        )
