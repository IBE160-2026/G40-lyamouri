"""URL routes (AD-11). Slugs are Norwegian."""

from django.urls import path

from web import views

urlpatterns = [
    path("", views.login, name="login"),
    path("logg-ut/", views.logout, name="logout"),
    path("produkter/", views.product_overview, name="products"),
]
