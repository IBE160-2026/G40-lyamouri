"""Nothing outside the rounding and display modules rounds or formats a domain number
(Story 2.3; AD-2, AD-3).

The test reads the source with ast and the templates and scripts as text, so it imports
nothing from the app. `rounding.py` is the only module that rounds, and `display.py` the
only one that writes a domain number as text: the guard finds the calls, the rounding
modes, the Django number filters and the script methods that would do it elsewhere. It
does not look at every f-string, because identifiers such as «2026-W45» use `:02d`.
"""

import ast
import re
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
ROUNDING = SRC / "forecasting" / "rounding.py"
SOURCE_FILES = sorted(
    path
    for path in SRC.rglob("*.py")
    if "migrations" not in path.parts and path != ROUNDING
)
TEMPLATES = sorted(
    path for suffix in ("html", "txt") for path in SRC.rglob(f"*.{suffix}")
)
SCRIPTS = sorted(SRC.rglob("*.js"))
# What rounds or formats a number in the standard library or in Django.
ROUNDING_CALLS = {
    "round",
    "quantize",
    "to_integral_value",
    "to_integral_exact",
    "ceil",
    "floor",
    "trunc",
}
FORMATTING_NAMES = {
    "floatformat",
    "intcomma",
    "intword",
    "apnumber",
    "filesizeformat",
    "number_format",
    "localize",
    "unlocalize",
}
FORMATTING_MODULES = {
    "django.contrib.humanize",
    "django.utils.formats",
    "django.utils.numberformat",
    "django.template.defaultfilters",
}
DJANGO_NUMBER_FILTER = re.compile(
    r"\|\s*(?:floatformat|intcomma|intword|apnumber|filesizeformat|stringformat"
    r"|date|time|timesince|timeuntil|localize|unlocalize)\b"
    r"|\{%\s*(?:localize|unlocalize|widthratio|now)\b"
    r"|\{%\s*load\s+(?:humanize|l10n)\b"
)
SCRIPT_NUMBER_FORMAT = re.compile(
    r"\.toFixed\b|\.toLocale\w*|Intl\.NumberFormat|Math\.(?:round|floor|ceil|trunc)\b"
)


def rounding_in(source):
    """What in source rounds or formats a number: calls, rounding modes (also as an
    attribute, as in `decimal.ROUND_UP`), Django number functions and their modules."""
    found = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call):
            function = node.func
            name = function.id if isinstance(function, ast.Name) else None
            name = function.attr if isinstance(function, ast.Attribute) else name
            if name in ROUNDING_CALLS:
                found.append(name)
        names = []
        if isinstance(node, ast.Attribute):
            names.append(node.attr)
        elif isinstance(node, ast.Name):
            names.append(node.id)
        elif isinstance(node, ast.ImportFrom):
            names.extend(alias.name for alias in node.names)
            if node.module in FORMATTING_MODULES:
                found.append(node.module)
        elif isinstance(node, ast.Import):
            found.extend(a.name for a in node.names if a.name in FORMATTING_MODULES)
        found.extend(
            name
            for name in names
            if name.startswith("ROUND_") or name in FORMATTING_NAMES
        )
    return found


@pytest.mark.parametrize(
    "path", SOURCE_FILES, ids=lambda path: path.relative_to(SRC).as_posix()
)
def test_no_module_but_rounding_rounds_a_number(path):
    """AD-2, AD-3: no `round()`, `quantize`, `ceil` or rounding mode outside
    `forecasting/rounding.py`."""
    assert rounding_in(path.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize(
    "path", TEMPLATES, ids=lambda path: path.relative_to(SRC).as_posix()
)
def test_no_template_formats_a_number_with_django(path):
    """AD-3, NFR-5: no Django number or date filter in a template, because the
    template filters of `web/templatetags/prognose.py` call `forecasting/display.py`."""
    assert DJANGO_NUMBER_FILTER.findall(path.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize(
    "path", SCRIPTS, ids=lambda path: path.relative_to(SRC).as_posix()
)
def test_no_script_formats_a_number(path):
    """AD-3, AD-11: no `toFixed`, `toLocaleString`, `Intl.NumberFormat` or `Math.round`
    in a script, because the server writes every domain number."""
    assert SCRIPT_NUMBER_FORMAT.findall(path.read_text(encoding="utf-8")) == []


def test_django_adds_no_thousands_grouping_of_its_own():
    """NFR-5, AD-3: no number is grouped by Django's localisation, so a bare number in
    a template cannot print as «1 234»."""
    from django.conf import settings

    assert not settings.USE_THOUSAND_SEPARATOR


def test_the_guard_reads_the_source_and_the_templates():
    """AD-3: the test finds the core, the app and the templates, so a moved folder
    cannot make it pass without checking anything."""
    packages = {path.relative_to(SRC).parts[0] for path in SOURCE_FILES}

    assert {"forecasting", "web"} <= packages
    assert any(path.name == "products.html" for path in TEMPLATES)
    assert any(path.name == "app.js" for path in SCRIPTS)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("round(x, 1)", ["round"]),
        ("x.quantize(unit)", ["quantize"]),
        ("import math\nmath.ceil(x)", ["ceil"]),
        ("import math\nmath.trunc(x)", ["trunc"]),
        ("from decimal import ROUND_HALF_UP", ["ROUND_HALF_UP"]),
        ("import decimal\ny = decimal.ROUND_DOWN", ["ROUND_DOWN"]),
        (
            "from django.template.defaultfilters import floatformat",
            ["django.template.defaultfilters", "floatformat"],
        ),
        ("import django.contrib.humanize", ["django.contrib.humanize"]),
        ("total = a + b", []),
    ],
)
def test_the_guard_finds_what_it_is_meant_to_find(source, expected):
    """AD-3: the checker itself, on a few snippets, so that it cannot go quiet."""
    assert sorted(rounding_in(source)) == sorted(expected)


@pytest.mark.parametrize(
    ("text", "pattern", "found"),
    [
        ("{{ x|floatformat:1 }}", DJANGO_NUMBER_FILTER, True),
        ("{{ x | intcomma }}", DJANGO_NUMBER_FILTER, True),
        ("{% widthratio a b 100 %}", DJANGO_NUMBER_FILTER, True),
        ("{% load humanize %}", DJANGO_NUMBER_FILTER, True),
        ("{% load prognose %}{{ x|whole_number }}", DJANGO_NUMBER_FILTER, False),
        ('<div class="localize-box">', DJANGO_NUMBER_FILTER, False),
        ("x.toFixed(1)", SCRIPT_NUMBER_FORMAT, True),
        ("n.toLocaleString('nb')", SCRIPT_NUMBER_FORMAT, True),
        ("Math.round(x)", SCRIPT_NUMBER_FORMAT, True),
        ("el.textContent = label", SCRIPT_NUMBER_FORMAT, False),
    ],
)
def test_the_text_patterns_find_what_they_are_meant_to_find(text, pattern, found):
    """AD-3: the template and script patterns, on a few snippets, with a class name
    that only contains «localize» as a false alarm."""
    assert bool(pattern.search(text)) is found
