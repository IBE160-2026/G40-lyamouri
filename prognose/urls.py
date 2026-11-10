"""URL routes. Slugs are Norwegian.

Unknown addresses get templates/404.html and errors get templates/500.html,
through Django's default error handlers.
"""

from django.urls import path

from planning import views

urlpatterns = [
    path("", views.start, name="start"),
    path("helse/", views.health, name="health"),
]
