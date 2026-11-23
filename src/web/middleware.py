"""The outermost middleware: the error pages that Django's handlers do not render (AD-12).

Django turns an exception into a response in the layer that raised it, so no
middleware sees an exception from the layers inside it. Django sends
got_request_exception while it handles the exception, so note_database_error
can mark the request there, and ErrorPageMiddleware then shows the 503 page.
"""

import sys

from django.contrib.auth import middleware as auth_middleware
from django.db import InterfaceError, OperationalError
from django.template.loader import render_to_string

# The errors Django raises when the database does not answer.
DATABASE_ERRORS = (InterfaceError, OperationalError)


def note_database_error(sender, request=None, **kwargs):
    """Mark the request when the exception Django is handling is a database error.

    WebConfig.ready() connects it to got_request_exception.
    """
    if request is not None and isinstance(sys.exception(), DATABASE_ERRORS):
        request.database_unavailable = True


class ErrorPageMiddleware:
    """Gives a database error the 503 page and a 405 the Server error page.

    It is the first entry in MIDDLEWARE, so that it also handles a database
    error raised in any other middleware. The 503 page is rendered after all of
    them have run, without the request, so it reads nothing from the database.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if getattr(request, "database_unavailable", False):
            return replace_page(response, "503.html", 503)
        if response.status_code == 405:
            # The method decorators send 405 with an empty body.
            return replace_page(response, "500.html", 405)
        return response


def replace_page(response, template, status):
    """Put the page in the response that the other layers made, keeping its headers.

    The headers that stay are, for example, the security headers and Allow.
    The old body may have had another type, such as Django's plain-text debug
    page, and CommonMiddleware has already set Content-Length for it.
    """
    response.status_code = status
    response["Content-Type"] = "text/html; charset=utf-8"
    response.content = render_to_string(template)
    response["Content-Length"] = str(len(response.content))
    return response


class LoginRequiredMiddleware(auth_middleware.LoginRequiredMiddleware):
    """Denies every page by default: a request without a login goes to the login page (AD-6).

    Only a view marked login_not_required is exempt, which the login page is.
    Error pages are not routed views, so the middleware never sees them. The
    redirect has no next parameter: the login always opens the product
    overview, so no address from the request is trusted.
    """

    redirect_field_name = None
