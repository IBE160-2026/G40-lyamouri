"""URL routes (AD-11). Slugs are Norwegian."""

from django.urls import path

from web import views

urlpatterns = [
    path("", views.start, name="start"),
]
