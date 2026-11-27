---
title: 'Story 2.8: List the products in R-12 order'
type: 'feature'
created: '2026-11-27'
baseline_commit: 'aa9a90029d91fbf1934b0c0b3ee8e48eb6a5f9dd'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The list on `/produkter/` and beside the product screen is Story 1.8's plain table in product number order. It shows no suggested quantity, forecast, cover or trust label, has no groups, and the loader's `build_overview` result is not used by any screen. There is no settings bar.

**Approach:** Until Story 2.11 builds «Denne uken», `/produkter/` is a tidy one-column page that holds only the grouped list (the user's decision 1); on the product screen the list stays beside the product. One list, built from the loader's results in the order and groups of `build_overview` (R-12), replaces the table on both pages: cards for «Bestill snart» and «Uten prognose», rows for «Øvrige produkter». Every page after login gets the settings bar without its button. The seed-data stand-in for R-8 is replaced by a check against the core.

## Boundaries & Constraints

**Always:**
- Groups, cards and rows follow UX-DR16 to UX-DR18 and UX-DR44 word for word; an empty group is not shown; the whole card or row is one link, the selected one has `aria-current="page"` and wins over the dashed border. The list is the region «Produkter». The heading «Produktoversikt» carries the count («30 produkter», «1 produkt»).
- Every sentence that depends on a result or a count comes ready from `explanation/` in singular and plural (group summaries, the product count, the card reason, the settings texts, the empty text with the exact load command from the README); templates only place them (AD-4). All numbers go through `forecasting/display.py` (AD-3): «–» for a missing quantity or cover. The card reason is the label's reason without the label word and the last full stop, first letter in capital; none for «høy», and none on a card without a forecast, which shows the FR-8 reason in red instead and then only the label «Lav» (the user's decision A after the review, 2026-11-27: the mockup's card, not the acceptance criterion's wording, which would give the same reason twice).
- The loader gives the page its order; it joins the numbers of `build_overview` with the products and results and does no grouping, sorting or rounding of its own (AD-2). The loader also gives the settings in use. The number of queries does not depend on the number of products (NFR-8). The two-account test covers the list.
- The settings bar (UX-DR15) shows «Innstillinger i bruk:», the method with its window or factor, «Scenarioprosent 10 %», «Sikkerhetsmargin 10 %», «Uvanlige uker: tas med» or «holdes utenfor», and «Endringen gjelder alle produkter i bedriften.»; it wraps and is cut off at no width.
- NFR-8 is measured on an isolated test database with 50 products of 104 weeks (pytest-django's own database, or a separate throwaway database on the same server for the user's hand check); existing data in the regular database is never changed, created or deleted (the user's decision 2). The spec stays whole at about 2,000 tokens (decision 3).
- Up to 900 px the list follows the product area with no scroll frame of its own and every card and row is tappable anywhere (UX-DR7, NFR-6).

**Never:**
- No search, keyboard hint, arrow keys, scroll memory, «Denne uken», progress bar, previous and next links or «Endre innstillinger» button (Stories 2.11, 3.1). No model, migration, seed file, dependency or script change; no `round()` or formatting outside `display.py`; no model manager outside `queries.py`; `forecasting/` never imports `explanation/`; nothing is stored.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Testbedrift A | seed company | «Bestill snart» with 4 cards, «4 produkter · 31 enheter foreslått», «Uten prognose» 1 card, «Øvrige produkter» 25 rows, in `build_overview` order | N/A |
| Card, forecast | Strøsand 25 kg | name, «Varenr. 10012», «Foreslått» over «11» in blue, «Lager 5», «Ukeprognose uke 1 14,3», «Uker dekning 0,3», «Middels» and the reason without label and full stop | N/A |
| Card, no forecast | 10040 | dashed red border, the red FR-8 reason in place of the forecast, «–» for quantity and cover, «Lav» and no second reason | N/A |
| Row, label «høy» | ordinary product | the meta line, «Foreslått» over the quantity in ink, the label, no reason | N/A |
| Selected product | product screen | selected style and `aria-current="page"`; a selected no-forecast card has a solid blue border | N/A |
| Singular | 1 product in a group | «1 produkt · du bestemmer selv», «1 produkt · 4 enheter foreslått», «1 · etter varenummer» | N/A |
| Empty group | nothing to order soon | no «Bestill snart» heading | N/A |
| No products | company without products | «Ingen data er lastet inn. Kjør uv run python src/manage.py load_seed som står i README.» | N/A |
| Exponential smoothing | settings row | «Eksponentiell glatting, faktor 0,3» in the bar | N/A |
| Other company | A is logged in | none of B's products | N/A |
| Queries | 3 or 50 products of 104 weeks | the same count | N/A |

</frozen-after-approval>

## Code Map

- `src/web/company_data.py` -- `CompanyData` gets `settings` (the `ForecastSettings` already built by `forecast_settings`); `overview` is already there.
- `src/web/views.py` -- `product_overview` uses the loader; one builder joins `overview.order_soon`, `without_forecast`, `others` with `product_list` and `results` into groups with card or row items; `header_context` takes the loader data (week and settings bar). `LABELS` is reused.
- `src/explanation/trust.py` -- `confidence_reason`, `list_text`, `LABEL_WORDS`; add `card_reason(result)`.
- `src/explanation/product_list.py` (new) -- headings, group summaries, product count, empty text; `src/explanation/settings_bar.py` (new) -- the bar's texts from `ForecastSettings` through `display`.
- `src/web/templates/web/_product_list.html` (rewrite), `_trust_label.html` (small variant exists), `_settings_bar.html` (new), `base.html`, `products.html`, `product.html`; `src/web/static/web/app.css` -- cards, rows, group heading, bar; tokens only; the `.product-table` rules go.
- `tests/` -- `test_product_overview.py`, `test_product_screen.py`, `test_isolation.py`, `test_app_shell.py`, `test_company_data.py` (extended); `test_product_list.py`, `test_settings_bar.py` (new); `tests/test_seed_data.py` loses `suggested_quantity`, `warning_shapes` and `week_1_forecast`, and a core-based test of Testbedrift A's figures, labels and the 21 quiet products replaces `test_denne_uken_for_testbedrift_a_matches_the_mockup_and_the_ux_flow`.
- Documents: `docs/statustabell.md`, `qa-logg.md`, `ki-styringslogg.md`, `arbeidslogg.md`, `sprint-status.yaml`, `deferred-work.md` and `.logs/mounia-03/issues.md` (the stand-in item).

## Tasks & Acceptance

**Execution:**
- [x] `src/explanation/`, `src/web/company_data.py` -- the texts and the settings in the loader -- FR-24, AD-2, AD-4
- [x] `src/web/views.py`, templates, `app.css` -- groups, cards, rows, the bar, the empty state -- FR-24, UX-DR7, UX-DR15 to UX-DR18, UX-DR44
- [x] tests above -- every matrix row, the two-account test, the query count at 3 and 50 products, Testbedrift A against the core and the mockup (E13, E23, E24, FR-24) -- FR-2, NFR-8
- [x] the documents above, `sprint-status.yaml` to `review` -- DR-7

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `makemigrations --check`, when they run, then they pass.
- Given mutations of the new code (groups or the order swapped, a card shown as a row, the reason with the label word, «–» shown as 0, the selected style lost, a settings text unread, the company filter dropped, a query in the product loop), when the tests run, then each fails at least one test.
- Given the pages at 1366 × 768, 320 px, 390 × 844 and 820 × 1180, when they open for Testbedrift A, then nothing scrolls sideways or is cut off, the bar wraps, and the list follows the product up to 900 px (checked by hand, QA log).

## Implementation Notes

- 2026-11-27: built in the build session, not by a subagent, because the user approved subagents for the reviews only. Model: Sonnet 5.5 (`claude-sonnet-5-5`, confirmed by the session; the level «High» that the user asked for is not shown by the session). Branch `story/2-8-list-the-products-in-r-12-order` from `aa9a900`. The user answered the three open questions: (1) `/produkter/` is a tidy one-column page until Story 2.11, (2) NFR-8 is measured with 50 products of 104 weeks on an isolated database and the regular data is never changed, (3) the spec stays whole (about 2,000 tokens, over the 1,600 guide). The user approved the other design decisions (the card reason, the summaries in singular and plural, the count in the heading, the settings texts, the empty text with the load command, search and keyboard to 2.11, and the stand-in test replaced by a check against the core).
- New: `src/explanation/product_list.py` (headings, summaries, count, empty text), `src/explanation/settings_bar.py`, `card_reason` in `src/explanation/trust.py` (with `confidence_reason` built on the same `_reason_parts`), `web/_settings_bar.html`, `tests/test_product_list.py` and `tests/test_settings_bar.py`. Changed: `CompanyData.settings` in `web/company_data.py`; `web/views.py` (`header_context(company, current, data)`, `label_context`, `list_context`, `product_overview` through the loader); `_product_list.html` (rewritten as groups of cards and rows), `base.html`, `products.html`, `product.html`; `app.css` (the `.product-table` rules are gone); `tests/answer_key.py` (the mockup's label); and the existing tests of the list, the touch targets and the two-account test. The stand-in R-8 (`suggested_quantity`, `warning_shapes`, `week_1_forecast`) and its test are removed from `test_seed_data.py`; `test_denne_uken_for_testbedrift_a_matches_the_mockup_and_the_ux_flow` in `test_trust_seed.py` checks the same figures against the core, and also each mockup product's label. The task line for `test_company_data.py` was not needed: the loader gains one field, which the page tests of the bar read.
- The route and the Code Map: the overview is `.page` with `.list-column` (640 px), the product screen keeps the shell. The group heading is `h2` on the overview and `h3` beside a product (the list heading is `h2`).
- Deviation from the acceptance criterion's wording, decided by the user after the review (AA-3): a card without a forecast shows the FR-8 reason in red in place of the forecast and the label «Lav», with no second reason after the label. The criterion says «the trust label and, unless the label is «høy», the reason», which gives «Ingen prognose: færre enn 3 gyldige uker» in red and «Ingen prognose, færre enn 3 gyldige uker» after the label. The mockup's card shows only the label, and so does the spec's matrix. The rule is in `card_reason`, so a row never needs it, and the trust panel on the product screen keeps the full reason.
- Checks in the browser: seed pages (Testbedrift A: overview, 10012, 10040, 10025; Testbedrift B: overview, 20015) were rendered with the test client on pytest's own database, saved as static HTML and measured in headless Chrome 120 (old mode) at 1366 × 640, 1180 × 820, 901 × 900, 900 × 900, 820 × 1180, 390 × 844, 360 × 800 and 320 × 640: 48 measurements, nothing scrolls sideways, the settings bar wraps (38 px at 1366, 62 px at 900, 112 px at 390, 162 px at 360 and 320), and from 900 px the list follows the product. The panels end at 405, 403, 381 and 469 px of 640 at 1366 × 640. This is not Safari and not a phone.
- NFR-8: with 50 products of 104 weeks the overview and a product screen make 6 queries (the login's 2 and the loader's 4), as with 3 products. On pytest's test database the test client took a median of 26 ms (max 48 ms, 12 requests each). On a throwaway database `prognose_nfr8` next to the regular one, real HTTP requests to the development server took 32 to 43 ms (8 requests each); the regular database was unchanged (2 companies, 62 products, 5,016 weeks before and after) and the throwaway one was dropped. These are Claude's measurements; the hand check on the user's laptop is the user's.
- Mutations applied and restored (compared by hash): 41 before the review, all caught; 45 in the final run after the review patches (the four new ones: a card without a forecast repeating the reason, the bar's values run together, the dashed class, and the label and reason run together). 43 were caught; one no longer applied because the code had changed, and one was an equivalent mutant (the template partial of the label already ends with a line break). Both were rewritten against the changed code and caught. A first final run was stopped because a new test failed at its baseline; the file that was mutated at that moment was restored by hand and the full suite was green before the run was repeated.
- Process: four reviewers as `general-purpose` subagents with `model: "sonnet"` (an alias, not confirmed to be 5.5), launched together. The Acceptance Auditor's prompt had a wrong diff path (a placeholder, Claude's mistake), corrected by a message before it reported. The reviewers changed nothing: the hash of all modified and new files was identical before and after. The Blind Hunter and the Verification Gap Reviewer never saw the spec.
- Manual checks, reported by the user in chat on 2026-11-27 (details and gaps in `docs/qa-logg.md`): Safari in its responsive view (not a real device) at 1366 × 768, 820 × 1180, 390 × 844 and 320 × 844 as Testbedrift A and B, with grouping, cards, rows, trust labels, the wrapping settings bar and the placement of the list checked and no visible sideways scrolling; real iPhone 13 as Testbedrift A, where the cards for 10012 and 10040 and the row for Malertape 25 mm opened the right product screen when the card face was tapped; NFR-8 on the isolated database with 50 products of 104 weeks, where Safari showed 123 ms for `/produkter/` and 142 ms in total, the test server stopped, `prognose_nfr8` dropped and the regular database unchanged (Claude checked afterwards, by reading only, that it still holds 2 companies, 62 products and 5,016 weeks). Not reported: the Safari, macOS and iOS versions, the product numbers opened in Safari, Testbedrift B on the iPhone and the tab order.

## Spec Change Log

- 2026-11-27, Acceptance Auditor AA-3 (intent_gap, resolved by the user): a card without a forecast gave the same reason twice. The user chose A: follow the mockup, with only the red FR-8 reason and the label «Lav». The frozen block's card-reason rule and the matrix row were amended by the user's decision, and the code was changed with `card_reason`. Known-bad state avoided: the FR-8 reason repeated in two wordings on one card. KEEP: the full reason in the trust panel, and the card reason for «Middels» and «Lav» products with a forecast.

## Review Triage Log

BMAD Code Review (2026-11-27): Blind Hunter (BH, N = 9), Edge Case Hunter (EC), Verification Gap (VG) and Acceptance Auditor (AA), as four independent read-only subagents, on the diff of `src` and `tests` from `aa9a900` (69 kB). The spec went to the Edge Case Hunter and the Acceptance Auditor as the claims file. 30 findings (BH 12, EC 11, VG 0 and 2 other findings, AA 5), in 23 groups: 5 patched, 1 intent gap (resolved by the user, code changed), 1 deferred and 16 rejected.

| ID | Finding | Verdict | Route |
|---|---|---|---|
| BH-1 | The empty text sends a company without products to `load_seed`, which stops on a database that is not empty | low | defer: the Message Catalogue and the criterion fix the sentence; the README's command refuses a non-empty database (`deferred-work.md`) |
| BH-2, EC-9 | The raw-data oracle of the deleted seed test is replaced by one that reads the core | low | reject: `deferred-work.md` asked for it («checks them with the core and removes the stand-in»), and the PATTERNS table in `test_seed_data.py` still checks the data shapes |
| BH-3 | `assert "quantity" not in inner` can never fail | low | patch: the row test checks `<b>0</b>` without `qty-ink` |
| BH-4 | `<h{{ level }}>` has no default | low | reject: both includers pass it; a guard adds branches for a case nobody reaches |
| BH-5, EC-6, VG-1 | The first group keeps its 24 px top margin on the product screen | low | reject: the mockup's `.grp` has 24 px above every group; cosmetic |
| BH-6, EC-10 | Pixel paddings (11/13, 9/13, 10/14, 6, 640) instead of tokens | low | reject: DESIGN.md has no token for them (as BH-9 of Story 2.7), and the colours, fonts and radii are tokens and tested |
| BH-7 | The link name is the whole card, and the focus ring sits next to the blue border | low | reject: UX-DR17 and UX-DR18 make the whole card one link; the ring is outside the border with a 2 px gap |
| BH-8, EC-4 | The bar's values are adjacent `<b>` elements, so the text runs together | low | patch: a line break between them, and a test reads the text without tags |
| BH-9 | Phone-width behaviour unchecked | false | reject: measured at 8 sizes in headless Chrome, nothing scrolls sideways |
| BH-10 | `selected` is passed to the page and no longer read; texts are built for every item | low | patch for `selected`; reject for the texts (cost is negligible) |
| BH-11 | `removesuffix(".")` is fragile | false | reject: every reason ends with the full stop that `_sentence` or the format adds |
| BH-12 | Plural «selected products»; the decision has no pointer | low | patch: the comments |
| EC-1 | One odd product makes `card_reason` raise and the page fail | low | reject: loud by design, as EC-11 of Story 2.7 |
| EC-2 | A card with no `list_text` and no forecast | low | reject: only two reasons exist, and a third would fail loudly |
| EC-3 | An unknown method in a settings row fails every logged-in page | medium | reject: the core already raises for it on every page; Story 3.1 validates the row (EC-1 of Story 2.7, already deferred) |
| EC-5 | The pill and the reason run together | false | reject: the label partial ends with a line break; a space added in the first patch was removed again, and a test and a mutation guard it |
| EC-7 | `mockup_products` raises on a chunk without a pill | low | reject: the mockup is a fixed file, and a break is loud |
| EC-8, AA-4 | The test docstring says 21 products and the loop checks 26 | low | patch: «the other 26 products» |
| EC-11, AA-1 | The documents are not written | low | reject: they follow the review, as AA-1 of Story 2.7 |
| VG-2 | The list's pills are not checked for shape | low | reject: the list uses the same partial as the product area, which is checked |
| AA-2 | The card quantity is ink for 0 as well as «–» | low | reject: a card holds only products to order soon (above 0) or without a forecast («–») |
| AA-3 | A card without a forecast gives the FR-8 reason twice | medium | intent_gap: the criterion's wording and the mockup disagree; the user chose A, the mockup (see the Spec Change Log) |
| AA-5 | The hand checks cannot be verified from the code | – | reject: not a defect; they are the user's checks, listed under Verification |

**Open points** (`issues.md`): Story 2.11 moves the list into the two-column shell beside «Denne uken», and adds search, the keyboard hint, arrow keys and scroll memory; Story 2.9 writes the column label «Uke 1 · uke 46»; the settings row validation stays with Story 3.1; the empty-state command for a non-empty database is deferred.

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check` -- expected: clean
- `uv run python src/manage.py makemigrations --check` -- expected: no changes

**Manual checks:**
- Safari at 1366 × 768, 820 × 1180, 390 × 844 and 320 px, and the real iPhone 13, for `/produkter/` and a product screen, as Testbedrift A and B; the user reports the result in chat.
- The 2-second check of NFR-8 on an isolated database with 50 products of 104 weeks: the user's laptop, a throwaway database next to the regular one, whose data stays as it is. Done by the user (see Implementation Notes).
