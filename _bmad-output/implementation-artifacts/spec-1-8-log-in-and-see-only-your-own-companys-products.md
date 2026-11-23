---
title: 'Story 1.8: Log in and see only your own company''s products'
type: 'feature'
created: '2026-11-23'
status: 'done'
route: 'dispatch'
baseline_commit: '7aeb0a7bb7c66258ea101f2718c6b97611d30627'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The app has no login. `/` is a placeholder, every address is open, and no code reads company data, so FR-1 and FR-2 are unbuilt and the data from Story 1.7 is unreachable.

**Approach:** Build Innlogging at `/` and a POST logout, deny every other page by default, and add `/produkter/`, a simple list of the logged-in company's products. All company data is read through `web/queries.py`, and an automated two-account test checks every route and list.

## Boundaries & Constraints

**Always:**
- Texts are verbatim from the Message Catalogue and the Innlogging wireframe (UX-DR8). A failed login shows «Feil kundenummer eller passord.» in a red-tint row with `role="alert"` above the fields, the same for a wrong number, a wrong password and blank fields; the number is kept and the password is empty.
- `LoginRequiredMiddleware` is Django's, after `AuthenticationMiddleware`, with `LOGIN_URL` the login page and no `next` parameter, so the redirect has no open target. The login view and the test views that raise errors are exempt (`login_not_required`). Error pages show no company data.
- Login, logout and a reload are Post/Redirect/Get (AD-10). A second POST of the login form after the first has logged in, and a second logout POST, give the same result as the first, not the 403 page: a failed CSRF check on `/` for a logged-in user redirects to `/produkter/`, and on `/logg-ut/` for a logged-out user to `/`. A GET to `/` for a logged-in user redirects to `/produkter/`. `/logg-ut/` takes only POST.
- The password goes only to `authenticate()` with the stored seed hash and is never logged or stored. The hash is not rewritten by a login.
- `web/queries.py` holds every read of company data. Each function takes the company first and filters by it. Views and forms use no manager or related manager for `Product`, `SalesWeek` or `CompanySettings`.
- The app header of a logged-in page, from the view's context: «[name] · siste registrerte uke: uke [45], [2026]», «Produktoversikt» with `aria-current="page"` (weight 600, 2 px white underline), and «Logg ut» as a POST form with the CSRF token. The week is derived from the sales weeks and is never stored (AD-8). `forecasting/display.py` builds the label, with a test, and Story 2.3 extends it.
- A focus ring in the app header is white, 3 px, with the same offset (decision of 2026-11-23, to meet WCAG 1.4.11); the change is a row in the DESIGN.md change log.
- The list shows product number, name and stock on hand, ordered by product number. Pages are checked at 320 px, 390 × 844 and 820 × 1180, and on the real iPhone 13 over the local network.

**Never:**
- No new model, migration or dependency, no forecasting rule, no product page, search, settings or other route (Epic 2 replaces the list). No user-created account, password reset or «husk meg».
- No raw SQL, and no `--reset` outside `load_seed`.
- No warning for a missing `.secret_key` (BH-13 of Story 1.1): `load_seed` creates it and the README says so. The open point is closed as «not built».

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Login page | GET `/`, logged out | The wireframe: «Logg inn», the line, «Kundenummer», «Passord», «Logg inn», the README note; wordmark-only header | N/A |
| Correct login | POST `1001` / `testbedrift-a` | 302 to `/produkter/`, A's 30 products, A's header | N/A |
| Wrong login | wrong number, wrong password, a blank field, or a NUL character | 200, the one message with `role="alert"`, number kept, password empty | the same message in every case |
| Not logged in | any route but `/`, with GET or POST | 302 to `/` | N/A |
| Logged in at `/` | GET | 302 to `/produkter/` | N/A |
| Double submit | the same login form POSTed twice, with CSRF checks on | both end at `/produkter/`, no 403 | the failure view redirects |
| Logout | POST `/logg-ut/`, a second one | session ended, 302 to `/`; the second also | GET gives 405 and keeps the session |
| Isolation | A logged in, B's data exists | no B name, number or stock in any list or header, and the same the other way | N/A |
| Database stopped | logged in, any page | the 503 page, without header or company data | N/A |

</frozen-after-approval>

## Code Map

- `src/web/views.py` -- `start` is replaced by `login`, `logout`, `product_overview`, `csrf_failure`; `@require_safe` is the pattern.
- `src/web/middleware.py` -- `ErrorPageMiddleware` stays; `LoginRequiredMiddleware` is added here (redirect field disabled).
- `src/prognose/settings.py`, `src/prognose/urls.py` -- `MIDDLEWARE` (line 53), `LOGIN_URL`, `CSRF_FAILURE_VIEW`; URL map from AD-11 (`/`, `/logg-ut/`, `/produkter/`).
- `src/web/queries.py` (new), `src/web/forms.py` (new, `LoginForm`), `src/forecasting/display.py` (new, stdlib only; `tests/test_core_imports.py` checks it).
- `src/web/templates/web/base.html` -- the header block; `start.html` becomes `login.html`; `products.html` is new; `error.html` line 9 uses `{% url %}` (BH-6 of Story 1.4).
- `src/web/static/web/app.css` -- tokens only: form fields, buttons, error row, header meta and links, white focus in the header, the table; the coarse-pointer block gets the header links.
- `tests/test_start_page.py` becomes `tests/test_login.py`; `tests/test_error_pages.py` (its urlconf adds `raise_error`, which needs the exemption, and its `/` tests), `tests/test_app_shell.py` (`PAGES`); new `tests/test_product_overview.py`, `tests/test_isolation.py`, `tests/test_forecasting_display.py`.
- Documents: `README.md` (login, phone test), `docs/statustabell.md`, `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, DESIGN.md (focus rule and change log), `sprint-status.yaml`, `.logs/mounia-03/issues.md` (lines 87, 96, 109 to 111, 124), `deferred-work.md`.

## Tasks & Acceptance

**Execution:**
- [x] `src/forecasting/display.py`, `tests/test_forecasting_display.py` -- the header week label «uke 45, 2026» -- AD-3
- [x] `src/web/queries.py` -- `products_for_company`, `latest_data_week`, both company-first -- AD-7
- [x] `src/web/forms.py`, `views.py`, `middleware.py`, `urls.py`, `prognose/settings.py` -- login, logout, the overview, deny by default, the CSRF failure view -- FR-1, AD-6, AD-10
- [x] templates and `app.css` -- the wireframe, the header, the list, the white focus ring -- UX-DR8, UX-DR14, UX-DR38
- [x] `tests/test_login.py`, `test_product_overview.py`, `test_isolation.py` -- one test per matrix row, logs and session free of the password, the hash unchanged, a source scan for managers outside `queries.py`, and the two-account test with a list of routes that later stories extend -- FR-1, FR-2, SM-4, NFR-3, NFR-10
- [x] adapt the existing tests (error pages, app shell) to the new `/` and the exemption
- [x] documents above, `sprint-status.yaml` to `review`, the open points -- DR-7

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check` and `uv run ruff format --check`, when they run locally and in CI, then they pass, and `makemigrations --check` finds no change.
- Given the phone test, when the user starts Prognose over the local network and logs in as each company on the real iPhone 13, then each sees only its own products and the QA log records the date and iOS version (NFR-6); the user reports the result, and the app is stopped and `PROGNOSE_LAN_HOST` removed afterwards.

## Implementation Notes

- 2026-11-23: built in the build session, not by a subagent, because the user approved subagents for the reviews only. The epic context was used as it was, as in Story 1.7: the later PRD and spine changes touch nothing here.
- Branch `story/1-8-log-in-and-see-only-your-own-companys-products` from `7aeb0a7`, code and tests in `a078c90`. 312 tests after the review and the Safari retest, 1 skipped (the Docker check, because Docker is not on the PATH of this shell).
- `LoginRequiredMiddleware` is a subclass of Django's with `redirect_field_name = None`, so the redirect has no `next` and no address from the request is trusted. The login view and the test view `raise_error` use `login_not_required`.
- Logging in rotates the CSRF token, so a second POST of the same form fails the check. `csrf_failure` gives it the result of the first (a logged-in user goes to `/produkter/`). A logout does not rotate the token, so a second logout POST passes the check and the login middleware redirects it. A failed check never logs anybody in or out.
- Error pages stay wordmark-only; their link now uses `{% url %}` (open point BH-6 of Story 1.4). The focus ring in the header is white, with a row in the UX change log and the epics change log, both with «hash follows» until the commit exists.
- Mutations applied to the code and then restored, all caught: the products or the week not filtered by company; the login check removed; the CSRF failure view removed; the failure redirect for anonymous visitors removed, and the one for logged-in visitors widened; `require_POST` removed from the logout; the CSRF check removed from the login; a field named in the message; `next` honoured; `never_cache` removed; the week ordered by week only; the hash rewritten by the login; the session row left after the logout; the number not kept.
- Run locally against the development database: `runserver` on port 8765 with curl: `/produkter/` logged out gave 302 to `/`; a wrong login gave the alert and kept «1001»; the login as Testbedrift A gave A's header, 30 products and none of B's; a GET to `/logg-ut/` gave 405. The manual checks (Safari at three widths and the real iPhone 13) are the user's.
- 2026-11-23, manual test in Safari (three findings after the review): (1) Back after «Logg ut» showed the overview again, while a reload went to the login. The server was right (`Cache-Control: no-store` is sent, and a request without the session is redirected); Safari restores the page from its back/forward cache, which WebKit leaves to `pageshow`. The user chose a small `app.js` that reloads a page restored from that cache, on logged-in pages only, with AD-11 amended and a row in the spine and epics change logs. Without the script nothing else changes. (2) An old login form sent again after a login and logout gave «Skjemaet er utløpt», because the login rotates the CSRF token; reproduced with curl. `csrf_failure` now sends every POST of a visitor who is not logged in to a fresh login page, and logs the refusal itself, because Django logs only a 403. The expired-form page is left to a logged-in visitor's other forms. This goes one step beyond the Always list, which named only the logged-in login form and the logged-out logout. (3) The reload after logout going to the login page is correct and needed no change.

## Spec Change Log

## Review Triage Log

BMAD Code Review (2026-11-23): Blind Hunter (BH), Edge Case Hunter (EC), Verification Gap (VG) and Acceptance Auditor (AA), as four independent subagents, on the working-tree diff from `7aeb0a7` (73.5 kB, 26 files, N = 9 for the Blind Hunter). The spec went to the Edge Case Hunter as the claims file and to the Acceptance Auditor. 35 findings from the four reports, grouped by cause into 7 medium entries (BH-3, BH-4, BH-7, EC-1, AA-2, AA-3 and VG-1) and the rest low or false. 19 findings were patched, 13 rejected and 3 false; none was deferred, and BH-1 stays an open point in issues.md. No finding needed a decision from the user. The fixes are in the working tree; nothing is committed yet.

| ID | Finding | Verdict | Route |
|---|---|---|---|
| BH-1 | The change-log rows end with «hash follows» | low | reject: filled in by the merge-log routine, tracked in issues.md |
| BH-2, EC-4, EC-5 | No throttling, lockout or `max_length` on the login | low | reject: one user per machine, the seed passwords are public and printed in the README, PBKDF2 hashes a long password in one pass, and the spec's Never list has no account protection |
| BH-3 | Logged-in pages can be cached, so Back after logout may show the list | medium | patch: `never_cache` on the overview, and a test of the header for every route in `ROUTES` |
| BH-4 | The logout test reads only the cookie | medium | patch: the session row must be gone and the old cookie worthless |
| BH-5, VG-3 | `products.html` is not under the shell test | low | patch: `test_logged_in_page_has_the_shell_and_the_app_header` |
| BH-6, EC-7 | No empty state, caption or word break in the product table | low | reject: the catalogue has no text for an empty list, both seed companies have products, Epic 2 replaces the list, and the manual check at 320 px covers the wrapping |
| BH-7, EC-9, VG-2 | The scan for managers is bypassed by `models.Product.objects`, an alias or `get_model`, and templates are not scanned | medium | patch: any `.objects`, any import of a company model and `get_model` count, a template scan, and a test that the scan finds the four bypasses |
| BH-8 | The isolation test could fail by chance on digits in a CSRF token | low | patch: the tokens are cut out before the check |
| BH-9 | `test_manage` collects the whole login suite in a subprocess | low | patch: it collects `tests/test_company.py`, which needs the settings but not the database |
| BH-10, EC-2 | A stale login form for another company, from a logged-in user, redirects silently | low | reject: the spec has the redirect, the header shows the company, and a CSRF failure must never switch the company |
| BH-11 | No session lifetime, and no `next` | low | reject: the spec's Always list leaves `next` out on purpose, and Django's default session age holds |
| BH-12 | No `aria-invalid`, no focus move, no `inputmode`, no sending state | low | patch for `aria-invalid`; reject the rest (no scripts, and customer numbers are not promised to be digits) |
| BH-13 | The new `label` and `input` rules are global | low | reject: one stylesheet of tokens is AD-11, and Epic 3 adjusts what its forms need |
| BH-14 | Header text is hard-coded, and the label has no tests of padding | low | reject: UX-DR14 gives the text verbatim and the week number has no padding |
| BH-15 | The phone test sends the password over plain HTTP | low | patch: the README says so |
| EC-1, AA-1 | A failed CSRF check on `/logg-ut/` for a logged-out visitor gives 403, not a redirect | medium | patch: any POST that fails the check for a visitor who is not logged in gets the login page |
| EC-3 | A logged-in user with no CSRF cookie cannot log out | low | reject: the expired-form page says to reload, and a logout that skips the check lets another site log the user out |
| EC-6, AA-4 | The customer number is not kept for a NUL character | low | patch: the posted number is echoed back (the template escapes it) |
| EC-8 | An `include()` route has no `callback` in the exemption test | low | reject: no include exists, and a later story that adds one changes the test with its route |
| AA-2 | A logged-out POST to any other route gets 403 | medium | patch: with EC-1, and the not-logged-in test now runs with the CSRF check on |
| AA-3 | The hash test does not compare with the seed hash | medium | patch: it compares the hash before and after |
| AA-5 | The documents and `sprint-status.yaml` are not changed | false | the documents are the last task, after the review, as in Story 1.7 |
| AA-6 | The change-log row is not in DESIGN.md | false | the pair's change log is in EXPERIENCE.md, and DESIGN.md holds the rule |
| AA-7 | The 30 products of the seed are not tested | low | patch: `test_the_seed_companies_see_only_their_own_products` logs in with the real seed and the real passwords |
| AA-8 | `web/seed.py` is exempt from the manager scan | false | its «products» are plain records read from files, and the comment says so |
| VG-1 | The latest week across a New Year is not tested | medium | patch: `test_latest_data_week_crosses_the_new_year` |

**Open points** (`issues.md`): the hash in the change-log rows (BH-1), and the manual checks.

## Design Notes

- Error pages stay wordmark-only, as Story 1.4 built them: Django gives only some handlers the request, so a header that read the company would read the database on an error page (AD-12). Their link «Til produktoversikten» leads to the login page when logged out.
- The stock number is printed as it is. Django prints an integer without grouping under `nb`, so it matches AD-3 for now; Story 2.3's filters take it over with the other numbers.

## Verification

**Commands:**
- `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` -- expected: pass.

**Manual checks:**
- Responsive view at 320 px, 390 × 844 and 820 × 1180 on `/` (also after a failed try) and `/produkter/`, then the real iPhone 13 as in the acceptance criteria.
