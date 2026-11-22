---
title: 'Story 1.4: Norwegian app shell and error pages'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'dispatch'
baseline_commit: 'dc7673ef04886aafc0d9797e6b24a07001a8e1d3'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The start page is unstyled, and every error shows a Django default page in English: «Not Found», «403 Forbidden» for a failed CSRF check, «Bad Request (400)», «Server Error (500)» for a stopped database, and an empty body for 405. With DEBUG off, Django sends errors only to e-mail, so nothing reaches the console (NFR-10, AD-12).

**Approach:** One stylesheet with the DESIGN.md tokens and a base template with the logged-out app header give every page the approved look. Norwegian templates for Django's own error handlers, and an outermost middleware for 503 and 405, put the Message Catalogue texts in the not-found panel, and `LOGGING` sends errors to the console. The DEBUG rule in the last criterion is already built and tested in Story 1.1 (`env.debug_setting`, `test_only_dotenv_turns_debug_on`).

## Boundaries & Constraints

**Always:**
- `web/static/web/app.css` defines exactly the frontmatter tokens, with the values copied verbatim: `--color-<name>` (26), `--font-<role>-family`, `-size`, `-weight` and `-line-height` (17 roles), `--radius-<key>` (5) and `--space-<key>` (13, `list-width` to `text-measure` included). Outside `:root`, colors, font families, font sizes and radii come only from these variables; the touch rule's `font-size: 16px` is the one exception.
- Every page extends `web/base.html`: `lang="nb"`, the viewport tag, the `data:,` icon, the stylesheet through `{% static %}`, and a header with only the wordmark «Prognose». No script and no URL with a host; no `@import`, `url(` or `@font-face`.
- Focus is `:focus-visible` with a 3 px `--color-blue` outline 2 px outside the element. No shadows, gradients, transitions or animation. The header wraps (`flex-wrap: wrap`). Touch screens are `@media (pointer: coarse)`: buttons, fields, selects, text areas and stand-alone links get at least 44 × 44 px, and fields 16 px text. Radio buttons and the switch get their target from their label in their own stories (DESIGN.md).
- An error page shows the first sentence of its catalogue text, without the full stop, as the `h1` of the not-found panel, the rest as a paragraph, and the link «Til produktoversikten» only where the catalogue names it (Not found, Server error). The link goes to `/produkter/` (AD-11); Story 1.8 builds that page, so until then the link gives the 404 page. The panel is centered and at most 420 px wide, like the login panel, and `<title>` is the heading followed by « – Prognose». Error templates use no `request` or `user`, so they read nothing from the database.
- The start page keeps its `h1` «Prognose» and its sentence, in the same panel.
- New tests name an NFR-n or AD-n (D-10), plus the UX-DR-n they check, and use no database.

**Never:**
- No login, logged-in header, navigation, settings bar, `LoginRequiredMiddleware` or `/produkter/` route (Story 1.8); no `app.js`; no new dependency.
- No change to `prognose/env.py`, the spine, DESIGN.md or EXPERIENCE.md.
- No `try/except` around `get_response` for the 503 (Design Notes).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Unknown address | `GET /finnes-ikke/` | 404, «Siden finnes ikke» and the link | N/A |
| Database error in a view | a view raises `OperationalError` or `InterfaceError` | 503, the Database unavailable text, no link | the page reads nothing from the database |
| Database error in middleware | another middleware raises `OperationalError` before or after the view | 503, as above | as above |
| Failed CSRF check | `POST /` without a token | 403, «Skjemaet er utløpt» and «Last siden på nytt og prøv igjen.» | never the Server error text |
| Other 403 | a view raises `PermissionDenied` | 403, the Server error text and the link | never the expired-form text |
| Bad request | `GET /` with `Host: evil.example` | 400, the Server error text and the link | N/A |
| Wrong method | `OPTIONS /` | 405, the Server error text and the link; `Allow: GET, HEAD` is kept | N/A |
| Server error | a view raises `RuntimeError` on a POST with a password field | 500, the Server error text and the link | the console shows the error, but not the password, the secret or a database URL |

</frozen-after-approval>

## Code Map

- `src/prognose/settings.py` -- add `web.middleware.ErrorPageMiddleware` first in `MIDDLEWARE`, and `LOGGING`; `DEBUG` stays as Story 1.1 built it. Django's default handlers and `CSRF_FAILURE_VIEW` already render `400.html`, `403.html`, `404.html`, `500.html` and `403_csrf.html` from the template root, so `urls.py` needs no `handler*` names.
- `src/web/apps.py` -- `WebConfig`; connect the receiver in `ready()`.
- `src/web/templates/web/start.html` and `src/web/views.py` (`start`, unchanged) -- the only page so far.
- `tests/test_start_page.py` -- keep; its `POST /` → 403 and `OPTIONS /` → 405 test still holds. `tests/test_settings.py` covers DEBUG, and its `load_settings` runs settings.py again, so new settings stay plain data.
- `_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/DESIGN.md` lines 10–142 (tokens) and `EXPERIENCE.md` lines 155–158 (Message Catalogue) -- the tests read them; `docs/DESIGN.md` is a symlink, so the tests use the real path.
- `…/mockups/konsept-d-kombinert.html` lines 33–37, 62–67 and 122–125 -- base, header and panel CSS to reuse; its variable names differ, and DESIGN.md wins.

## Tasks & Acceptance

**Execution:**
- [x] `src/web/static/web/app.css` -- create: the tokens; the base (box-sizing, canvas, ink, body role, tabular numerals, `overflow-wrap: break-word`); headings by role with more space above than below; paragraphs up to the text measure; blue links; the focus rule; `.app-header` (header colors, 10 px × `--space-5` padding, wrapping) and the wordmark; the panel (UX-DR21) and the centered one-panel page; the touch block.
- [x] `src/web/templates/web/base.html`, `src/web/templates/web/error.html` -- create the shell and the not-found panel layout.
- [x] `src/web/templates/404.html`, `500.html`, `503.html`, `403_csrf.html` -- create with the catalogue texts; `400.html` and `403.html` extend `500.html`.
- [x] `src/web/middleware.py` -- create `note_database_error`, which marks the request when `sys.exception()` is a connection error, and `ErrorPageMiddleware`, which returns the 503 page for a marked request and puts the Server error page in the body of a 405, keeping its headers.
- [x] `src/web/apps.py`, `src/prognose/settings.py` -- as in the Code Map; `LOGGING` gives the `django.request` and `django.security` loggers a `console` `StreamHandler` at WARNING with the default format (the message and any traceback), without propagation (Implementation Notes).
- [x] `src/web/templates/web/start.html`, `tests/test_start_page.py` -- extend the base; test the header.
- [x] `tests/test_app_shell.py` -- create: the tokens equal the frontmatter (read by a small reader, no YAML package), the counts, nothing else in `:root`, every `var()` defined, no literals outside `:root`, no external loads, no shadow, gradient, animation, letter-spacing or uppercase, the focus, header and touch rules, and every page's `lang`, viewport, icon, stylesheet, header and single `h1`.
- [x] `tests/test_error_pages.py` -- create: each matrix row, with the texts read from the catalogue; no English or debug text; test views and middleware in the module, with `pytest.mark.urls(__name__)` and `Client(raise_request_exception=False)`; the console text through the `console` handler.
- [ ] `docs/statustabell.md`, `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, `sprint-status.yaml` -- the status paragraph, the manual check and the review defects, the middleware case, the work log and the story status.

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check` and `uv run ruff format --check`, when they run locally and in CI, then they pass.
- Given `runserver --insecure` with DEBUG off, when `/` and `/finnes-ikke/` open in Safari's responsive view at 320 px, 390 × 844 and 820 × 1180, then the stylesheet loads, nothing scrolls sideways or is cut off, and the QA log records the result.

## Implementation Notes

- 2026-11-22: built in the build session, not by a subagent, because the user approved subagents for the reviews only. The epic context was used as it was: the spine change from Story 1.3 that made it formally stale touches nothing in it (the user's decision).
- `LOGGING`: the task first named the `django` logger. `dictConfig` resets the existing children of a logger it configures, so `django.server` would have lost its handler, and runserver's request lines at INFO would have disappeared. The settings configure `django.request` and `django.security` instead, without propagation, so a line is also not printed twice with DEBUG on. Checked with runserver: the request lines are unchanged, and «Not Found» and the CSRF warning reach the console with DEBUG off.
- Mutations, each caught and then restored by a scratchpad script that is not committed: no outermost middleware, the receiver not connected, a token value changed, a literal color in a rule, the expired-form text changed, no loggers in `LOGGING`, and the 405 branch off.
- runserver on 127.0.0.1:8765 with DEBUG off: `/` 200; `/finnes-ikke/` 404 with the Norwegian page; `/static/web/app.css` 200 `text/css`; a missing static file 404 with the Norwegian page; `DELETE /` 403, because the CSRF check comes before the method check.
- Found in the check of the tasks, with curl through runserver: `OPTIONS /` gave 405 with `Content-Length: 0` and an empty body, because `CommonMiddleware`, inside `ErrorPageMiddleware`, had set the length of the empty body, so a browser would show a blank page. The test client does not check the length. `replace_page` now puts the page into the response that the other layers made and sets `Content-Length` to the new body. The 503 page goes the same way, so the security headers stay. `assert_error_page` checks that a `Content-Length` matches the body, and an eighth mutation (the length not updated) is caught. Afterwards `OPTIONS /` gave 405 with 717 bytes and a matching length.
- The matrix row «Server error» was split across a page test and a log test; one test, `test_server_error_shows_its_page_and_is_logged_without_secrets`, now covers it.
- 130 tests pass (104 earlier and 26 new) with `~/.docker/bin` on PATH; without `docker` on PATH, `test_compose.py` skips. Ruff passes after `ruff format` of the two new test files.
- The documents task is finished after the review, because the QA log records the review findings and the user's check in Safari.

## Spec Change Log

## Review Triage Log

Review pass 1 (2026-11-22): Blind Hunter, run inline by the build session as in Stories 1.2 and 1.3, on the diff from `dc7673e` (51.3 kB, so at least 8 findings). Edge Case Hunter and Verification Gap were skipped here, because BMAD Code Review runs them as independent subagents on the pull request (D-8). The 405 length defect was found before this pass, in the task check (Implementation Notes).

| ID | Finding | Verdict | Evidence | Route |
|---|---|---|---|---|
| BH-1 | `@media (pointer: coarse)` misses touch screens whose primary input is a mouse or touchpad, such as hybrid laptops; `any-pointer: coarse` would cover them | low | Real, but phones and iPads, the touch devices NFR-6 names, report a coarse primary pointer, and a hybrid laptop keeps the desktop sizes | reject: the approved Intent chose `pointer: coarse`; raised with the user at the presentation |
| BH-2 | An error response other than 405 that a view returns without a body, such as an empty 400, gets no Norwegian page | low | No such view exists, and later stories re-render forms with their errors; a general branch adds complexity | reject |
| BH-3 | A loaded and changed session whose save fails after the view becomes `SessionInterrupted`, a 400 that Django sends without `got_request_exception`, so it shows the Server error page instead of 503 | low | Real for a database that stops between loading and saving the session in one request; Django converts the error before any hook | reject |
| BH-4 | The `var()` check in `test_app_shell.py` skips the `font` shorthand | low | A shorthand with a literal stack would pass | patch: `font` added to the checked properties |
| BH-5 | The color check catches only the names `white` and `black` | low | Hex values copied from the mockup are the realistic risk; a full name list adds little | reject |
| BH-6 | The link «Til produktoversikten» is a hard-coded `/produkter/`, which gives the 404 page until Story 1.8 | low | The approved Intent decides it (AD-11's URL map) | reject; the switch to `{% url %}` is an open point for Story 1.8 in `issues.md` |
| BH-7 | With DEBUG on, the 503 page replaces Django's debug page for a database error | false | Intended (Design Notes): the traceback still reaches the console through `django.request` | reject |
| BH-8 | `test_database_error_in_another_middleware_shows_the_503_page` checks the outermost entry after changing the settings | low | It checked the value captured before the change, but read as if it checked the new list | patch: the assertion comes first |
| BH-9 | The path to the UX folder is repeated in both new test modules | low | A rename of the folder fails both tests loudly | reject |
| BH-10 | «Last siden på nytt og prøv igjen.» after a POST: reloading resends the stale token | low | Real, but the text is the Message Catalogue's, verbatim, as the story requires | reject; the copy can be revised in Story 4.2 |

## Design Notes

Django wraps every middleware in `convert_exception_to_response`, so an exception becomes a response in the layer that raised it, and a `try/except` in an outer layer never sees it. Django sends `got_request_exception` inside that `except` block, so a receiver finds the exception in `sys.exception()` and marks the request, and the outermost middleware then replaces the finished response with the 503 page. This covers views, other middleware and DEBUG on, and the 503 page is rendered after every inner middleware has run.

```python
def note_database_error(sender, request=None, **kwargs):
    if request is not None and isinstance(sys.exception(), DATABASE_ERRORS):
        request.database_unavailable = True
```

No page reads the database before Story 1.8, so only the tests check the 503 page in this story; Story 1.8 tests it with a logged-in user.

## Verification

**Commands:**
- `uv run pytest` -- expected: every test passes, the 104 earlier ones included
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings

**Manual checks:**
- The second criterion, in Safari; `/static/web/app.css` answers 200 with DEBUG off.
