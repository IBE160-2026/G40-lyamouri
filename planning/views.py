"""The start page and the health check. Both are open without login (AD-5)."""

from django.contrib.auth.decorators import login_not_required
from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import Company


@login_not_required
def start(request):
    """The Norwegian start page. It reads no data."""
    return render(request, "planning/start.html")


@login_not_required
def health(request):
    """Answer ok after one ORM read, which proves the database answers.

    It reads no company data, only whether the company table can be queried.
    A database error gives the Norwegian 500 page.
    """
    Company.objects.exists()
    return HttpResponse("ok", content_type="text/plain; charset=utf-8")
