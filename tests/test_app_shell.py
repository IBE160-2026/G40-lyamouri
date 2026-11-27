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
    "web/login.html",
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
FONT_PROPERTIES = {"font", "font-family", "font-size", "font-weight", "line-height"}
# An outline value that removes the focus ring, such as none, 0 or 0px.
OUTLINE_REMOVED = re.compile(r"(?:^|\s)(?:none|0(?:px)?)(?=\s|$|!)")


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
        assert set(values) == set(TYPOGRAPHY_PROPERTIES), role
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
    """AD-11, UX-DR1: outside the top-level :root, no rule defines a custom
    property, so no token is given another value, every var() names a token, no
    color is written as a value, and fonts and radii are var() values. The 16 px
    text in fields on touch screens is the one fixed size."""
    defined = set(token_properties())

    for media, selector, block in css_rules():
        if (media, selector) == ("", ":root"):
            continue
        for name, value in block.items():
            where = (media, selector, name, value)
            assert not name.startswith("--"), where
            assert set(re.findall(r"var\(\s*(--[\w-]+)", value)) <= defined, where
            assert not COLOR_VALUE.search(value), where
            if name in FONT_PROPERTIES or name.endswith("radius"):
                touch_text = (media, name, value) == (TOUCH, "font-size", "16px")
                assert re.fullmatch(r"var\(--[\w-]+\)", value) or touch_text, where


def test_stylesheet_loads_nothing_from_outside_the_app():
    """NFR-1, AD-11, UX-DR2: no import, web font or URL in any letter case, so a
    page needs only the system fonts and this local stylesheet, and runserver
    --insecure finds it in the web app."""
    css = stylesheet().lower()

    for banned in ("@import", "@font-face", "url(", "image-set("):
        assert banned not in css
    assert Path(finders.find("web/app.css")) == STYLESHEET


def test_look_is_flat_without_motion_letter_spacing_or_uppercase():
    """AD-11, UX-DR2, UX-DR4, UX-DR43: no shadows, gradients, transitions or
    animation, no letter-spacing and no uppercase text, in any letter case."""
    css = stylesheet().lower()

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
    """NFR-11, UX-DR3, UX-DR4: every focusable element shows the blue focus ring,
    and no rule removes an outline, also not with 0px, !important or the
    outline-style and outline-width longhands."""
    assert rule(":focus-visible") == {
        "outline": "3px solid var(--color-blue)",
        "outline-offset": "2px",
    }
    assert not [
        (selector, name, value)
        for _, selector, block in css_rules()
        for name, value in block.items()
        if name in {"outline", "outline-style", "outline-width"}
        and OUTLINE_REMOVED.search(value)
    ]


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
    """NFR-6, UX-DR7, UX-DR14: on a touch screen, buttons, fields, selects, text
    areas, stand-alone links, the links of the product list and the links of the app header are at least
    44 × 44 px, and fields use 16 px text."""
    targets = (
        'button, input:not([type="radio"], [type="checkbox"]), select, textarea, '
        ".standalone-link, .product-table a, .header-nav a"
    )

    assert rule(targets, TOUCH) == {"min-width": "44px", "min-height": "44px"}
    assert rule("input, select, textarea", TOUCH) == {"font-size": "16px"}


@pytest.mark.parametrize("template", PAGES)
def test_every_page_has_the_shell(template):
    """NFR-11, NFR-6, NFR-1, AD-11, UX-DR7, UX-DR14, UX-DR44: Norwegian as the language,
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


def test_focus_ring_in_the_app_header_is_white():
    """NFR-11, UX-DR4, UX-DR14: a focused control in the app header gets a white
    outline instead of the blue one, which gives only about 2.4:1 on navy, under
    the 3:1 of WCAG 1.4.11. It is no thinner and no nearer than the blue ring."""
    blue = rule(":focus-visible")
    header = rule(".app-header :focus-visible")

    assert blue["outline"] == "3px solid var(--color-blue)"
    assert blue["outline-offset"] == "2px"
    assert header == {"outline-color": "var(--color-on-header)"}
    tokens = token_properties()
    assert tokens["--color-on-header"] == "#FFFFFF"
    assert tokens["--color-header"] == "#0E2236"


def test_script_reloads_a_page_that_the_browser_restores_from_its_cache():
    """NFR-10, AD-6, AD-10, AD-11: app.js reloads a page that Safari restores
    from its back/forward cache (`pageshow` with `persisted`), so Back after
    «Logg ut» asks the server. It keeps no state, makes no request of its own and
    names no address with a host (NFR-1)."""
    script = finders.find("web/app.js")
    source = Path(script).read_text(encoding="utf-8")
    code = "\n".join(
        line for line in source.splitlines() if not line.lstrip().startswith("//")
    )

    assert 'addEventListener("pageshow"' in code
    assert "event.persisted" in code
    assert "window.location.reload()" in code
    for forbidden in (
        "fetch(",
        "XMLHttpRequest",
        "localStorage",
        "sessionStorage",
        "cookie",
    ):
        assert forbidden not in code
    assert not re.search(r"https?://|//[a-z]", code)


def test_pages_without_a_login_have_no_script(client):
    """NFR-1, AD-11: the login page and the error pages load no script, so the
    logged-out pages work as plain HTML."""
    assert "<script" not in client.get("/").content.decode()
    assert "<script" not in client.get("/finnes-ikke/").content.decode()


def test_the_product_screen_has_two_columns_that_become_one_up_to_900_px():
    """NFR-6, UX-DR6, UX-DR7: from 901 px the list (392 px, 340 px up to 1180 px) and the
    product scroll on their own; up to 900 px one column with the product first on
    screen and no scroll frame; below 1181 px the panels stack."""
    narrow, one_column = "@media (max-width: 1180px)", "@media (max-width: 900px)"

    assert rule(".shell")["grid-template-columns"] == (
        "var(--space-list-width) minmax(0, 1fr)"
    )
    assert rule(".list")["overflow-y"] == rule(".detail")["overflow-y"] == "auto"
    assert rule(".decide")["grid-template-columns"] == "repeat(2, minmax(0, 1fr))"
    assert rule(".shell", narrow)["grid-template-columns"] == (
        "var(--space-list-width-narrow) minmax(0, 1fr)"
    )
    assert rule(".decide", narrow)["grid-template-columns"] == "minmax(0, 1fr)"
    assert rule(".shell", one_column) == {
        "display": "flex",
        "flex-direction": "column",
    }
    assert rule(".detail", one_column)["order"] == "-1"
    assert rule(".detail", one_column)["overflow"] == "visible"
    assert rule(".list", one_column)["overflow"] == "visible"
    assert rule(".has-shell", one_column)["height"] == "auto"
    tokens = design_tokens()["spacing"]
    assert (tokens["list-width"], tokens["list-width-narrow"]) == ("392px", "340px")


def test_the_skip_link_is_out_of_sight_until_it_has_focus():
    """UX-DR44: the skip link «Gå til produktet» moves off screen without display:none, so
    it stays the first focusable element, and shows when it has focus."""
    hidden, shown = rule(".skip-link"), rule(".skip-link:focus")

    assert hidden["transform"] == "translateY(-100%)"
    assert "display" not in hidden
    assert shown["transform"] == "none"


def test_the_decision_and_the_trust_panel_use_the_colors_of_the_design():
    """UX-DR20, UX-DR22, UX-DR24: the quantity is blue and 0 or «–» ink, the trust labels
    are green, amber and red on their tints, and data problems are red-tint and demand
    patterns amber-tint."""
    assert rule(".big .quantity")["color"] == "var(--color-blue)"
    assert rule(".big .quantity-ink")["color"] == "var(--color-ink)"
    assert rule(".big .quantity")["font-size"] == "var(--font-order-number-size)"
    for kind, color in (("hoy", "green"), ("middels", "amber"), ("lav", "red")):
        assert rule(f".pill-{kind}") == {
            "background": f"var(--color-{color}-tint)",
            "color": f"var(--color-{color})",
        }
    assert rule(".warning-data")["background"] == "var(--color-red-tint)"
    assert rule(".warning-pattern")["background"] == "var(--color-amber-tint)"
    assert rule(".icon-square-outline")["stroke"] == "var(--color-red)"
    assert rule(".icon-triangle")["fill"] == "var(--color-amber)"
    assert rule(".icon-ring")["stroke"] == "var(--color-red)"
