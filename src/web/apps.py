from django.apps import AppConfig
from django.core.signals import got_request_exception


class WebConfig(AppConfig):
    name = "web"

    def ready(self):
        from web.middleware import note_database_error

        # AD-12: lets ErrorPageMiddleware see a database error raised anywhere.
        got_request_exception.connect(note_database_error)
