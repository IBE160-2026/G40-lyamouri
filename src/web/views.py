"""Views (AD-11)."""

from django.shortcuts import render
from django.views.decorators.http import require_safe


@require_safe
def start(request):
    """The start page at /. It reads no data."""
    return render(request, "web/start.html")
