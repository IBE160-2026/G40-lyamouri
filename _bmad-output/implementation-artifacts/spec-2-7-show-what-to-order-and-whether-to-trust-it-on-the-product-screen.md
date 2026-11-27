---
title: 'Story 2.7: Show what to order and whether to trust it on the product screen'
type: 'feature'
created: '2026-11-27'
baseline_commit: '0116aaf45378037d405ce7187cd9a1974ab41f8c'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The core gives every product its order quantity, warnings and label, but no screen shows them. `/produkter/` is a plain list without links, there is no product route, no loader (`web/company_data.py`), no «–» for a missing value and no wording for the decision panel.

**Approach:** The loader reads a company's settings, products and sales weeks in a fixed number of queries and calls the core. `/produkter/<varenummer>/` shows the product header, the decision panel and the trust panel beside the product list, which now links. Epic 2's later stories add the rest of the screen.

## Boundaries & Constraints

**Always:**
- The page follows UX-DR6, UX-DR7, UX-DR10, UX-DR20, UX-DR22, UX-DR24 and UX-DR44: the skip link «Gå til produktet» is the first focusable element; the list is the region «Produkter» and the product the region «Valgt produkt»; one `h1` (the product name), `h2` for the panels; from 901 px two columns (392 px, 340 px up to 1180 px) that scroll separately; up to 900 px one column with the product first on screen and the list last, the HTML order unchanged and no scroll frame; at 1181 px the panels are side by side and equally high, below that they stack, decision first.
- All numbers go through `forecasting/display.py` (AD-3): the cover shows «–» when `weeks_of_cover` is None, the quantity «–» without a forecast. Every sentence that depends on a result comes from `explanation/` (AD-4): the caption «Foreslått bestillingsmengde for neste uke, uke [46]» (week from `horizon_weeks`), «Ingen foreslått bestillingsmengde», the «No decision» sentence, the label word, the reason and the warning texts from `explanation/trust.py`. Templates only place them.
- The quantity is blue when above 0 and ink when 0 or «–». The trust panel lists only active warnings in R-15 order with their shape: stockout a hollow red square on red-tint, unusual a filled amber triangle on amber-tint, old and insufficient data a ring with «!» on red-tint (UX-DR5). A level shift has no row yet; no empty-state text.
- The loader is the only reader of company data for the page (AD-2, AD-7): new functions in `web/queries.py` take the company first; the number of queries does not depend on the number of products. A product number of another company or an unknown one raises `Http404` and gives the page of an unknown address. The page is `never_cache`, safe methods only, and in `ROUTES` of the two-account test.
- The rows of the list link to the product, and the selected row has `aria-current="page"`.

**Never:**
- No progress bar, previous and next links, settings bar, chart, worksheet, explanation panel, search, groups or buttons (Stories 2.8 to 2.11, Epic 3, Epic 8); the list stays the list of Story 1.8 in product number order. No script, model, migration, seed or dependency change; no `round()` or formatting outside `display.py`; no model manager outside `queries.py`; `forecasting/` never imports `explanation/`; nothing is stored.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Forecast, order above 0 | Strøsand 25 kg (E1, E4), defaults | «11» in blue, the caption with «uke 46», the header «Varenr. 10012 · Lagerbeholdning 5 · Uker dekning 0,3», «Middels» with its reason, rows for weeks 38 and 39 (red) then week 42 (amber) | N/A |
| Order 0 | stock covers the need | «0» in ink, the same caption | N/A |
| No forecast | fewer than 3 valid weeks (E11 a) | «–», «Ingen foreslått bestillingsmengde», the sentence, cover «–», «Lav», one red row | N/A |
| Week-1 forecast 0 | E23 | cover «–», «0» in ink, no order-soon | N/A |
| Nothing to warn about | label «høy» | the label and reason, no row | N/A |
| New year | latest week 52 or 53 | the caption names «uke 1/2027» | N/A |
| No sales weeks | a product with none | no forecast, «–», the screen renders | N/A |
| Other company | A asks for B's number | the not-found page, none of B's data | `Http404` |
| Logged out | any visitor | redirect to the login | N/A |
| Number of queries | 3 or 50 products of 104 weeks | the same count | N/A |

</frozen-after-approval>

## Code Map

- `src/web/queries.py` -- `products_for_company`, `latest_data_week` are reused; add `settings_for_company` (the row or None) and `sales_weeks_for_company` (one query, by product and position).
- `src/web/company_data.py` (new) -- `load_company_data(company)`: settings (the FR-20 defaults without a row), `Week`s, `forecast_product`, `build_overview(results, {})`; returns products, results by product number, overview and latest week.
- `src/forecasting/display.py` -- `weeks_of_cover` and `suggested_quantity` (with «–»); `src/web/templatetags/prognose.py` registers them.
- `src/explanation/decision.py` (new) -- the decision panel texts; `src/explanation/trust.py` -- reuse `warning_texts`, `confidence_reason`, `LABEL_WORDS`.
- `src/web/views.py`, `src/web/urls.py` -- `product_screen` at `produkter/<str:product_number>/`; the rows' kind and shape.
- `src/web/templates/web/` -- `base.html` (skip-link block, body class), `product.html`, `_product_list.html`, `_trust_label.html` (new); `products.html` uses the list.
- `src/web/static/web/app.css` -- shell, list, header, panels, warning rows, pill, skip link; tokens only.
- `tests/` -- `test_company_data.py`, `test_product_screen.py`, `test_decision_text.py` (new); `test_isolation.py` (`ROUTES`, `OWN`), `test_login.py`, `test_product_overview.py`, `test_forecasting_display.py`, `test_number_filters.py` (extended).
- Documents: `docs/statustabell.md`, `qa-logg.md`, `ki-styringslogg.md`, `arbeidslogg.md`, `sprint-status.yaml`, `.logs/mounia-03/issues.md`.

## Tasks & Acceptance

**Execution:**
- [x] `src/web/queries.py`, `src/web/company_data.py` -- the loader -- AD-2, AD-7, NFR-8
- [x] `src/forecasting/display.py`, `src/web/templatetags/prognose.py`, `src/explanation/decision.py` -- «–» and the decision texts -- FR-8, FR-11, AD-3, AD-4
- [x] `src/web/views.py`, `src/web/urls.py`, templates, `app.css` -- the product screen and the linking list -- FR-2, FR-19, FR-25, UX-DR6 to UX-DR24
- [ ] tests above -- every matrix row, the two-account test, the query count, the seed products against the spreadsheet -- FR-2, FR-8, FR-11, FR-25, NFR-8, SM-1
- [x] the documents above, `sprint-status.yaml` to `review` -- DR-7

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `makemigrations --check`, when they run, then they pass.
- Given mutations of the new code (a warning order swapped, the zero in blue, a missing value shown as 0, a settings field not read, the company filter dropped, a query inside the product loop, the skip link moved), when the tests run, then each fails at least one test.
- Given the page at 1366 × 768, 320 px, 390 × 844 and 820 × 1180, when it opens for the seed product with the most warning rows, then the quantity, the label and the rows are visible without scrolling at 1366 × 768, and nothing scrolls sideways or is cut off from 320 px (checked by hand, QA log).

## Implementation Notes

- 2026-11-27: built in the build session, not by a subagent, because the user approved subagents for the reviews only. The user approved the spec and decisions 1 to 4 of the Design Notes unchanged and kept the spec whole (about 2,100 tokens, over the 1,600 guide). Branch `story/2-7-show-what-to-order-and-whether-to-trust-it-on-the-product-screen` from `0116aaf`.
- New: `src/web/company_data.py` (`load_company_data`, `CompanyData`, `forecast_settings`), `src/explanation/decision.py` (`decision_texts`), `web/product.html`, `web/_product_list.html`, `web/_trust_label.html`, and `tests/test_company_data.py`, `tests/test_decision_text.py`, `tests/test_product_screen.py`. Changed: `web/queries.py` (`settings_for_company`, `sales_weeks_for_company`), `forecasting/display.py` (`MISSING`, `weeks_of_cover`, `suggested_quantity`), the template filters, `web/views.py` (`product_screen`, `header_context` takes the week), `prognose/urls.py` (the route is in `prognose/urls.py`, not `web/urls.py` as the Code Map said), `base.html` (skip-link block, body attributes), `products.html`, `app.css`, and the existing tests for the list, the touch targets, the sample address and the two-account test. The `seeded` fixture moved to `tests/conftest.py`. No model, migration, seed, dependency, catalogue or script change.
- The loader reads four queries (settings, products, sales weeks, latest week), the page six with the login; `test_the_page_makes_the_same_number_of_queries_for_50_products_of_104_weeks` compares 3 and 50 products and allows at most 6. A company without a settings row has the FR-20 defaults (decision 4). `load_company_data` calls `forecast_product` and `build_overview` for the whole company, as AD-2 says.
- Checks in the browser: the seed pages were rendered to static HTML with the test client and measured in headless Chrome 120 (old headless mode, because the new one crashes on this Mac) at 1366 × 640, 1180 × 820, 901 × 900, 900 × 900, 820 × 1180, 390 × 844, 360 × 800 and 320 × 640, for six seed products, with the app's own stylesheet. These are checks in a browser engine with a layout probe, not tests in Safari and not tests on a real phone; those are the user's, recorded apart in the QA log.
- Mutations applied to the new code and restored (compared by hash): 50 before the review (the first run left four alive and one that did not apply; the tests were added and the pattern fixed, and one is an equivalent mutant: the skip link placed first inside the header is still the first focusable element) and 54 after the review patches, all caught except that equivalent one. The script ran with bytecode off and `__pycache__` cleared before each mutation.
- Model: Sonnet 5.5 for the build (the session confirms `claude-sonnet-5-5`; the level the user asked for is not shown). The four reviewers were started as subagents without a model or level set, so the model they ran on is not confirmed here. The epic context was used as valid, as in Story 2.6: `EXPERIENCE.md` is newer than `epic-2-context.md` by modification time, but both were committed together.
- Process notes: the build workflow lists three review layers, and the user asked for four, so the Acceptance Auditor was launched from the `bmad-code-review` skill's layer definition, with the spec as its claims file. The reviewers changed nothing: the hash of all tracked and untracked files was identical before and after. The Blind Hunter and the Verification Gap Reviewer never saw the spec.

## Spec Change Log

## Review Triage Log

BMAD Code Review (2026-11-27): Blind Hunter (BH, N = 9), Edge Case Hunter (EC), Verification Gap (VG) and Acceptance Auditor (AA), as four independent read-only subagents, on the diff of `src` and `tests` from `0116aaf` (68.5 kB). The spec went to the Edge Case Hunter as the claims file and to the Acceptance Auditor. 29 findings (BH 11, EC 11, VG 0, AA 7), in 21 groups: 6 patched, 1 deferred and 14 rejected. None was an intent gap or a bad spec.

| ID | Finding | Verdict | Route |
|---|---|---|---|
| BH-3, EC-6, AA-3 | The header reads the latest week again after the loader has read it | low | patch: `header_context` takes the week from the loader, and `product_screen` passes it |
| EC-8, BH-10 | The query-count test pins the page at exactly 7 | low | patch: the count must be equal for 3 and 50 products and at most 6 |
| AA-4 | «Produktoversikt» is not marked as the current page on the product screen, which the mockup's screen 2 does | low | patch: the product screen passes `products`, and a test checks the mark and the week |
| BH-6, EC-7, AA-6 | `tabindex="0"` on the list and on the product leaves two stops with nothing to scroll up to 900 px | low | patch: the list loses it (it scrolls through its links); the product keeps it as the skip link's target and, with later stories, as its scroll frame. Fixing the rest needs a script outside AD-11's list |
| BH-11 | The edit that added `CompanySettings` to the import in `test_isolation.py` also changed a sample source of the AD-7 scan test | medium | patch: the sample is `from web.models import Product as P` again. The guard test was weakened by the build, not by the design |
| AA-1 | The documents task is not done, and the build marked it done | low | patch for the checkbox, which is open again; the documents come after the review, as in Stories 2.2 to 2.6 (done below) |
| AA-2 | The 1366 × 768 check and the small-screen checks have no record | low | reject: they follow the build and go in the QA log (headless Chrome by Claude, Safari and the real iPhone by the user) |
| BH-1, BH-2, EC-10 | Every page calculates every product and the overview, and a missing number costs the same | low | reject: AD-2 says the product screen computes the whole overview for its list and its neighbours, the criterion names it, and the user approved decision 3 |
| BH-4 | `next(...)` without a default could raise `StopIteration` | false | reject: `results` and `product_list` are built from the same products, so a number in one is in the other |
| BH-5, AA-7 | The trust label is shown twice, and the small variant is unused | low | reject: UX-DR20 puts the large label next to the name and in the trust panel; the small one is for the list rows of Story 2.8 |
| BH-7 | Contrast is only checked by token name | false | reject: the pairs are DESIGN.md's measured ones (the mockup lists 5.3 to 6.6:1); a computed check is Story 4.2's finish review |
| BH-8 | The «0 or – is ink» rule is in the template | low | reject: AD-4 is about sentences; the colour is a presentation rule, tested in the CSS and the HTML |
| BH-9, AA-5 | Pixel values in the new CSS | low | reject: DESIGN.md has no token for 6, 10 and 14 px; `app.css` already has `10px var(--space-5)` and `2px 0`; colours, fonts and radii are tokens and tested |
| BH-10, EC-5 | A number the converter cannot reverse; fragile regexes; the 404 with variants | false | reject: `load_seed` refuses a number that is not 5 digits, a number without a trailing slash is redirected, and the regexes read the page this story writes |
| BH-11 | Stale comment in `products.html` and in `ROUTES` | low | reject: both are still true until Story 2.8 |
| EC-1 | A settings row outside the FR-20 ranges gives a 500 on every page of the company | medium | defer: no form or seed writes one; Story 3.1 builds the validation, as `deferred-work.md` already says for the model (story 1.7) |
| EC-2 | One product that the core refuses breaks every product screen of the company | low | reject: stock is a `PositiveIntegerField`, and the failure would be loud |
| EC-3 | A product whose last week is older than the company's gives wrong week numbers | low | reject: AD-8 says every history ends at the company's latest data week, and the seed reader and `load_seed` write it so |
| EC-4 | An invalid ISO year and week in the data gives a `ValueError` | false | reject: the weeks are derived from real dates by the seed reader |
| EC-9 | The E23 test checks one stock | low | reject: the weeks of cover without a forecast of 0 is Story 2.6's rule, and the same E23 case is checked there |
| EC-11 | An unknown label is a bare `KeyError` | false | reject: the core has three labels, and a missing key is meant to be loud |

**Open points** (`issues.md`): Story 2.8 replaces the list and the loader gets `build_overview` results from here; Story 2.9 writes the column label «Uke 1 · uke 46»; Story 2.11 adds the progress bar and the neighbours; the settings row validation stays with Story 3.1.

## Design Notes

Decisions made without the user, to confirm at the checkpoint: (1) the list rows link through the product name, with the number as plain text, and `/produkter/` uses the same list; (2) the progress bar, neighbours and the settings bar stay with Stories 2.11 and 3.x, and the column label «Uke 1 · uke 46» with Story 2.9, which first shows it; (3) the loader computes the overview (AC) though this page only joins results; (4) a company without a settings row uses the FR-20 defaults.

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check` -- expected: clean
- `uv run python src/manage.py makemigrations --check` -- expected: no changes

**Manual checks:**
- The page in Safari at 1366 × 768, 820 × 1180, 390 × 844 and 320 px, and on the real iPhone 13; the user reports the result in chat.
- Reported by the user on 27 November 2026 (details and gaps in `docs/qa-logg.md`): Safari on the Mac, products 10012, 10040 and 20015, mobile view at 390 and 320 px, 820 × 1180, skip link, focus ring and the 404 between companies (also as Testbedrift B against product 10012); real iPhone 13, login as Testbedrift A, 10012 as on the Mac, 10040 «Lav» without a quantity, and 404 for 20015. Not reported: Safari at 1366 × 768, and the Safari, macOS and iOS versions.
