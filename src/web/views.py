"""Views (AD-11)."""

import logging

from django.contrib import auth
from django.contrib.auth.decorators import login_not_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import csrf
from django.views.decorators.cache import never_cache
from django.views.decorators.http import (
    require_http_methods,
    require_POST,
    require_safe,
)

from explanation import decision, product_list, settings_bar, worksheet
from explanation import trust as trust_texts
from forecasting import display, trust
from web import company_data
from web.forms import LoginForm

logger = logging.getLogger("django.security.csrf")

# UX-DR5, UX-DR20: the style name and the shape of each trust label. The shape is
# decoration beside the word.
LABELS = {
    trust.HOY: ("hoy", "circle"),
    trust.MIDDELS: ("middels", "triangle"),
    trust.LAV: ("lav", "square"),
}
# UX-DR24, UX-DR5: the kind of each active warning and its shape. Data problems are red
# and demand patterns amber. A warning without a row here is a KeyError, so a new
# warning is never left out silently.
WARNING_ROWS = {
    trust.STOCKOUT_WEEKS: ("data", "square-outline"),
    trust.UNUSUAL_WEEKS: ("pattern", "triangle"),
    trust.OLD_DATA: ("data", "ring"),
    trust.INSUFFICIENT_DATA: ("data", "ring"),
}

# FR-1: the same message for every failed login, never naming the wrong field.
LOGIN_ERROR = "Feil kundenummer eller passord."


def header_context(company, current, data):
    """What the app header and the settings bar of a logged-in page show (UX-DR14,
    UX-DR15).

    current names the page marked as the current one. The latest data week is derived
    from the company's sales weeks (AD-8) and the settings are the company's; both come
    from the loader's data.
    """
    week = data.latest_week
    return {
        "app_header": {
            "company_name": company.name,
            "latest_week": display.header_week_label(*week) if week else None,
            "current": current,
            "settings_bar": {
                "label": settings_bar.LABEL,
                "values": settings_bar.settings_texts(data.settings),
                "note": settings_bar.SCOPE_NOTE,
            },
        }
    }


def label_context(result):
    """The trust label of a result as the templates place it: its word, style and shape."""
    return {
        "word": trust_texts.LABEL_WORDS[result.confidence_label],
        "kind": LABELS[result.confidence_label][0],
        "shape": LABELS[result.confidence_label][1],
    }


def list_context(data, selected=None):
    """The product list of a page (FR-24, UX-DR16 to UX-DR18): the groups of R-12 in
    their order, each product joined with its result. The order and the groups come from
    `build_overview` (AD-2); an empty group is not shown. `selected` is the product number
    of the open product screen."""
    overview = data.overview
    products = {product.product_number: product for product in data.product_list}
    groups = []
    for key, numbers in (
        (product_list.ORDER_SOON, overview.order_soon),
        (product_list.WITHOUT_FORECAST, overview.without_forecast),
        (product_list.OTHERS, overview.others),
    ):
        if not numbers:
            continue
        groups.append(
            {
                "key": key,
                "heading": product_list.HEADINGS[key],
                "summary": product_list.group_summary(
                    key, len(numbers), overview.figures.units_suggested
                ),
                "cards": key != product_list.OTHERS,
                "items": [
                    {
                        "product": products[number],
                        "result": data.results[number],
                        "selected": number == selected,
                        "label": label_context(data.results[number]),
                        "reason": trust_texts.card_reason(data.results[number]),
                        "no_forecast_text": trust_texts.list_text(data.results[number]),
                    }
                    for number in numbers
                ],
            }
        )
    return {
        "groups": groups,
        "product_count": product_list.product_count(len(products)),
        "no_data": product_list.NO_DATA,
        "has_products": bool(products),
    }


@login_not_required
@require_http_methods(["GET", "HEAD", "POST"])
def login(request):
    """Innlogging at / (FR-1, AD-6, AD-10). A login is followed by a redirect."""
    if request.method != "POST":
        if request.user.is_authenticated:
            return redirect("products")
        return render(request, "web/login.html")

    form = LoginForm(request.POST)
    company = None
    if form.is_valid():
        company = auth.authenticate(
            request,
            customer_number=form.cleaned_data["customer_number"],
            password=form.cleaned_data["password"],
        )
    if company is None:
        # The customer number is kept and the password is never sent back.
        return render(
            request,
            "web/login.html",
            {
                "error": LOGIN_ERROR,
                "customer_number": request.POST.get("customer_number", ""),
            },
        )
    auth.login(request, company)
    return redirect("products")


@require_POST
def logout(request):
    """Ends the session and opens Innlogging (FR-1, AD-6, AD-10). A GET gives 405."""
    auth.logout(request)
    return redirect("login")


@never_cache
@require_safe
def product_overview(request):
    """The product overview at /produkter/ (FR-2, FR-24): the company's own products in
    the groups of R-12. Story 2.11 adds «Denne uken» to the right of the list."""
    company = request.user
    data = company_data.load_company_data(company)
    context = header_context(company, "products", data)
    context.update(list_context(data))
    return render(request, "web/products.html", context)


@never_cache
@require_safe
def product_screen(request, product_number):
    """The product screen at /produkter/<varenummer>/ (FR-2, FR-11, FR-19, FR-25, FR-35).

    A product number that the company does not have, another company's included, gives
    the page of an unknown address (AD-7).
    """
    company = request.user
    data = company_data.load_company_data(company)
    result = data.results.get(product_number)
    if result is None:
        raise Http404
    product = next(p for p in data.product_list if p.product_number == product_number)
    # Without a sales week there is no forecast, and no text then needs the week.
    iso_year, iso_week = data.latest_week or (None, None)
    context = header_context(company, "products", data)
    context.update(list_context(data, product_number))
    context.update(
        {
            "product": product,
            "result": result,
            "label": label_context(result),
            "reason": trust_texts.confidence_reason(result),
            "decision": decision.decision_texts(result, iso_year, iso_week),
            "sheet": worksheet.worksheet_texts(result, iso_year, iso_week),
            "warnings": [
                {
                    "text": warning.text,
                    "kind": WARNING_ROWS[warning.code][0],
                    "shape": WARNING_ROWS[warning.code][1],
                }
                for warning in trust_texts.warning_texts(result, iso_year, iso_week)
            ],
        }
    )
    return render(request, "web/product.html", context)


def csrf_failure(request, reason=""):
    """The 403 page for a failed CSRF check, except where the answer is already known (NFR-10).

    Logging in rotates the CSRF token, so every login form that was open before
    the login fails the check afterwards: a second POST of the same form, and
    an old form that Back brings up after a logout. For a visitor who is logged
    in, the login form gets the result of the first login, the product
    overview. A POST from a visitor who is not logged in gets the login page,
    with a fresh form, as every page does without a login. Only a logged-in
    visitor's other forms, such as the logout, get the expired-form page. A
    failed check never logs anybody in or out, so another site cannot use these
    redirects.
    """
    if request.method == "POST":
        target = None
        if not request.user.is_authenticated:
            target = "login"
        elif request.path == reverse("login"):
            target = "products"
        if target:
            # Django logs a refusal only when the answer is a 403, so log it here.
            logger.warning("Forbidden (%s): %s", reason, request.path)
            return redirect(target)
    return csrf.csrf_failure(request, reason=reason)
