"""The app shell: the stylesheet and the layout every page shares (Story 1.4;
AD-11, NFR-1, NFR-6, NFR-11).

The tests read the tokens from the DESIGN.md frontmatter, the design's single
source, and use no database.
"""

import re
from pathlib import Path

import pytest
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from pytest_django.asserts import assertInHTML

REPO_ROOT = Path(__file__).resolve().parents[1]
# docs/DESIGN.md is a symbolic link to this file. A checkout without symbolic
# links turns it into a text file, so the tests read the file itself.
DESIGN = (
    REPO_ROOT
    / "_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/DESIGN.md"
)
STYLESHEET = REPO_ROOT / "src/web/static/web/app.css"
# Every template that renders a whole page.
PAGES = [
    "web/start.html",
    "400.html",
    "403.html",
    "403_csrf.html",
    "404.html",
    "500.html",
    "503.html",
]
TYPOGRAPHY_PROPERTIES = {
    "fontFamily": "family",
    "fontSize": "size",
    "fontWeight": "weight",
    "lineHeight": "line-height",
}
TOUCH = "@media (pointer: coarse)"
COLOR_VALUE = re.compile(
    r"#[0-9a-f]{3,8}\b|\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch)\("
    r"|(?<![\w-])(?:white|black)(?![\w-])",
    re.IGNORECASE,
)
FONT_AND_RADIUS = {
    "font",
    "font-family",
    "font-size",
    "font-weight",
    "line-height",
    "border-radius",
}


def design_tokens():
    """Return the colors, typography, rounded and spacing sections of DESIGN.md.

    The frontmatter is YAML with two-space indents and one value per line, so a
    small reader is enough, and the tests need no YAML package. A typography
    role maps to a dict of its four properties.
    """
    frontmatter = DESIGN.read_text(encoding="utf-8").split("---\n")[1]
    sections = {}
    entries = entry = None
    for line in frontmatter.splitlines():
        indent = len(line) - len(line.lstrip())
        key, _, value = line.strip().partition(":")
        key, value = key.strip("'"), value.strip().strip("'")
        if indent == 0:
            entries = sections.setdefault(key, {})
        elif indent == 2:
            entry = entries[key] = value or {}
        elif indent == 4:
            entry[key] = value
    return {
        name: sections[name] for name in ("colors", "typography", "rounded", "spacing")
    }


def token_properties():
    """Return each token's custom property, named as the stylesheet names it, with its value."""
    tokens = design_tokens()
    properties = {f"--color-{name}": value for name, value in tokens["colors"].items()}
    for role, values in tokens["typography"].items():
        for key, suffix in TYPOGRAPHY_PROPERTIES.items():
            properties[f"--font-{role}-{suffix}"] = values[key]
    properties |= {
        f"--radius-{name}": value for name, value in tokens["rounded"].items()
    }
    properties |= {
        f"--space-{name}": value for name, value in tokens["spacing"].items()
    }
    return properties


def stylesheet():
    """Return the stylesheet without its comments."""
    css = STYLESHEET.read_text(encoding="utf-8")
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def css_rules():
    """Return (media query, selector, declarations) for every rule in the stylesheet.

    The media query is "" outside @media, and the whitespace in a selector is
    collapsed to single spaces.
    """
    css = stylesheet()
    rules, preludes, start = [], [], 0
    for index, char in enumerate(css):
        if char == "{":
            preludes.append(" ".join(css[start:index].split()))
        elif char == "}":
            prelude = preludes.pop()
            if not prelude.startswith("@"):
                media = preludes[-1] if preludes else ""
                rules.append((media, prelude, declarations(css[start:index])))
        else:
            continue
        start = index + 1
    return rules


def declarations(block):
    """Return the property: value pairs of a declaration block as a dict."""
    pairs = (part.split(":", 1) for part in block.split(";") if part.strip())
    return {name.strip(): value.strip() for name, value in pairs}


def rule(selector, media=""):
    """Return the declarations of the one rule with this selector."""
    (block,) = [b for m, s, b in css_rules() if (m, s) == (media, selector)]
    return block


def test_stylesheet_defines_every_design_token_with_the_same_value():
    """AD-11, NFR-1, UX-DR1: :root holds every token in the DESIGN.md
    frontmatter as a custom property with the same value, and nothing else: 26
    colors, 17 typography roles, 5 radii and 13 spacing values."""
    tokens = design_tokens()

    assert [len(tokens[name]) for name in tokens] == [26, 17, 5, 13]
    assert rule(":root") == token_properties()


def test_rules_take_colors_fonts_and_radii_only_from_the_tokens():
    """AD-11, UX-DR1: outside :root, every var() names a token, no color is
    written as a value, and fonts and radii are var() values. The 16 px text in
    fields on touch screens is the one fixed size."""
    defined = set(token_properties())

    for media, selector, block in css_rules():
        if selector == ":root":
            continue
        for name, value in block.items():
            where = (media, selector, name, value)
            assert set(re.findall(r"var\((--[\w-]+)\)", value)) <= defined, where
            assert not COLOR_VALUE.search(value), where
            if name in FONT_AND_RADIUS:
                touch_text = (media, name, value) == (TOUCH, "font-size", "16px")
                assert re.fullmatch(r"var\(--[\w-]+\)", value) or touch_text, where


def test_stylesheet_loads_nothing_from_outside_the_app():
    """NFR-1, AD-11: no import, web font or URL, so a page needs only the system
    fonts and this local stylesheet, and runserver --insecure finds it in the
    web app."""
    css = stylesheet()

    for banned in ("@import", "@font-face", "url("):
        assert banned not in css
    assert Path(finders.find("web/app.css")) == STYLESHEET


def test_look_is_flat_without_motion_letter_spacing_or_uppercase():
    """AD-11, UX-DR2, UX-DR4, UX-DR43: no shadows, gradients, transitions or
    animation, no letter-spacing and no uppercase text."""
    css = stylesheet()

    for banned in (
        "shadow",
        "gradient",
        "transition",
        "animation",
        "@keyframes",
        "letter-spacing",
        "uppercase",
    ):
        assert banned not in css


def test_focus_is_a_three_pixel_blue_outline_two_pixels_outside():
    """NFR-11, UX-DR4: every focusable element shows the focus ring, and no rule
    removes an outline."""
    assert rule(":focus-visible") == {
        "outline": "3px solid var(--color-blue)",
        "outline-offset": "2px",
    }
    assert not [b for _, _, b in css_rules() if b.get("outline") in {"0", "none"}]


def test_body_uses_the_system_font_with_tabular_numerals():
    """NFR-1, UX-DR2: the text uses the system UI stack, not a web font, and
    every number has tabular numerals."""
    body = rule("body")

    assert body["font-family"] == "var(--font-body-family)"
    assert body["font-variant-numeric"] == "tabular-nums"
    assert token_properties()["--font-body-family"].startswith("system-ui,")


def test_header_is_navy_and_wraps_instead_of_being_cut_off():
    """NFR-6, UX-DR7, UX-DR14: the app header has the header colors and 10 × 20
    px padding, and wraps its items onto more lines on a narrow screen."""
    header = rule(".app-header")

    assert header["background"] == "var(--color-header)"
    assert header["color"] == "var(--color-on-header)"
    assert header["padding"] == "10px var(--space-5)"
    assert header["flex-wrap"] == "wrap"


def test_touch_screens_get_44_pixel_targets_and_16_pixel_fields():
    """NFR-6, UX-DR7: on a touch screen, buttons, fields, selects, text areas and
    stand-alone links are at least 44 × 44 px, and fields use 16 px text."""
    targets = (
        'button, input:not([type="radio"], [type="checkbox"]), select, textarea, '
        ".standalone-link"
    )

    assert rule(targets, TOUCH) == {"min-width": "44px", "min-height": "44px"}
    assert rule("input, select, textarea", TOUCH) == {"font-size": "16px"}


@pytest.mark.parametrize("template", PAGES)
def test_every_page_has_the_shell(template):
    """NFR-11, NFR-6, NFR-1, AD-11, UX-DR14, UX-DR44: Norwegian as the language,
    the responsive viewport tag, the empty icon, the local stylesheet, the
    logged-out header with only the wordmark, one h1, and no script or URL with
    a host."""
    html = render_to_string(template)

    assert html.startswith("<!doctype html>\n")
    assert '<html lang="nb">' in html
    assertInHTML(
        '<meta name="viewport" content="width=device-width, initial-scale=1">', html
    )
    assertInHTML('<link rel="icon" href="data:,">', html)
    assertInHTML('<link rel="stylesheet" href="/static/web/app.css">', html)
    assertInHTML(
        '<header class="app-header"><span class="wordmark">Prognose</span></header>',
        html,
    )
    assert html.count("<h1") == 1
    assert "<script" not in html
    assert not re.search(r'(?:src|href)="(?:[a-z]+:)?//', html)
