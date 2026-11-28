---
title: 'Story 2.9: Show how the forecast and the order quantity were calculated'
type: 'feature'
created: '2026-11-28'
baseline_commit: '9aec086f3a2a8f9255a70b7a279c24e81de28413'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The product screen shows the decision and trust panels and nothing of how the numbers came about. The examiner cannot check the forecast, the scenarios or the order quantity by hand against the reference spreadsheet. `ProductResult` holds no sales figures, and `display.py` has no horizon column label.

**Approach:** One panel «Slik er tallene regnet ut» below the two panels: the sales of the last 12 weeks with status tags, «Prognoseutregning», «Ukeprognoser og scenarioer» and «Utregning av bestillingsmengde». Sentences come from a new `explanation/worksheet.py`, numbers from `display.py` (AD-3, AD-4); a product without a forecast gets only the sales table.

## Boundaries & Constraints

**Always:**
- Decisions by the user (2026-11-28): (1) `ProductResult` gets `sales` (units sold per position, 1 to N) and `stockout_weeks`; the texts read only the result (AD-4). (2) A left-out unusual week reads «Holdt utenfor: uke 38 og 39 (utsolgt), uke 42 (uvanlig).», stockout weeks first, each kind in time order; «[3] uker brukt i beregningen» is stated when the setting excludes unusual weeks and one is excluded; N is the number of weeks tagged «brukt». These rows go into the Message Catalogue in `EXPERIENCE.md` with a change-log row. (3) A list that holds any week before the last 12 weeks writes every week with its year («uke 10/2025 og 11/2025»); the first week of a new year always carries it.
- Tags (UX-DR30): «utsolgt» red hollow square, «uvanlig» amber solid triangle on amber-tint for an unusual week that is taken into the calculation, «uvanlig, holdt utenfor» amber hollow triangle with a dashed border on the surface for one that the setting leaves out (the user's instruction 2026-11-28: the two must be told apart by words and shape, never by colour alone), «nytt nivå» ink diamond, «brukt» turquoise without icon; a week may have «brukt» beside «uvanlig» or «nytt nivå». «Brukt» = the last N calculation weeks for the moving average, every calculation week for exponential smoothing. The sentence below the table follows the mockup, with its other variants worded in the same style (exponential smoothing, singular, level shift, setting «holdes utenfor»).
- Lines: moving average «Glidende gjennomsnitt, 3 uker: (16 + 12 + 15) / 3 = 14,3», then «Uker brukt: uke 43, 44 og 45.»; exponential smoothing «Eksponentiell glatting, faktor 0,3: 0,3 × 15 + 0,7 × 13,3 = 13,8» (the last update, from the previous level), «Tallene er avrundet for visning.» inside the box, and a table of every calculation week with sales and level in its own scroll frame. Order line (E4, E6, E21): «Prognose 14,3 + sikkerhetsmargin 10 % (1,4) − lager 5 = 10,77 → foreslått bestillingsmengde 11»; «(lageret dekker behovet)» ends the line when the quantity is 0 and the stock is above 0 (the FR-14 rule, so E23 has none); the box holds the rounding note; the tommelfingerregel sentence always follows below. Scenario table: columns «Uke 1 · uke 46» from `display.py`, rows Optimistisk, **Normal**, Pessimistisk, the scenario sentence with the actual percentage, then the FR-7 note as «Merknad: …».
- Every number through `display.py` («−» U+2212, decimal comma, «10 %» with a no-break space); no `round()` or formatting elsewhere; the core imports nothing from `explanation/`. The loader's query count stays fixed (NFR-8); a product of another company gives the not-found page (FR-2).
- From 320 px: a table wider than the panel scrolls in its own frame, calculation lines wrap between terms and never inside a number, the page never scrolls sideways (NFR-6, UX-DR7). Headings `h2` «Slik er tallene regnet ut», `h3` per subsection; tables have `th scope`.

**Never:**
- No chart, legend or unusual-weeks switch (Story 2.10), no «Forklaring» panel (2.12), no seasonal values (FR-9), no per-scenario order quantities (FR-13), no progress bar or previous and next links (2.11), no settings form (Epic 3). No model, migration, seed file or dependency change; no expected value copied into code (AD-17); nothing stored.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| E1 / E3 / E4 | 12, 15, 11, 14, 13, 16, 12, 15; MA 3; stock 5 | «(16 + 12 + 15) / 3 = 14,3», «Uker brukt» names the ISO weeks of positions 6 to 8, scenarios 15,8 · 14,3 · 12,9, line «… = 10,77 → … 11» | N/A |
| E2 | same series, ES 0,3 | «0,3 × 15 + 0,7 × 13,3 = 13,8», level table 12 … 13,8, rounding note | N/A |
| E6 / E21 | 100, 100, 100 stock 150 / 27, 27, 28 stock 30 | «= −40,00 → … 0 (lageret dekker behovet)» / «= 0,07 → … 1» | N/A |
| E23 | 0, 0, 0 stock 0 | line ends «… 0» with no cover phrase | N/A |
| Strøsand 25 kg | seed, 104 weeks | last 12 weeks, tags for 38 and 39 (utsolgt), 42 (uvanlig), 43 to 45 (brukt); «Holdt utenfor: uke 38 og 39 (utsolgt).» | N/A |
| Unusual excluded | E8 or E15, setting «holdes utenfor» | each excluded week listed with «(uvanlig)», «[3] uker brukt i beregningen» | N/A |
| Level shift | E9 | «nytt nivå» on weeks 4 to 6, which stay used | N/A |
| Short history | 12 weeks or fewer | heading «Salgshistorikk, alle ukene» | N/A |
| Old left-out week | stockout before the last 12 weeks | list carries the year on every week | N/A |
| No forecast | E11 a | only the sales table | no calculation, scenario or order text |
| No sales weeks | empty history | no table, «Produktet har ingen salgsuker.» | N/A |
| Narrow screen | 320 px | tables scroll inside their frames, no sideways page scroll | N/A |

</frozen-after-approval>

## Code Map

- `src/forecasting/forecast.py` -- `ProductResult` gets `sales` and `stockout_weeks`, filled in `forecast_product`.
- `src/forecasting/display.py` -- column label «Uke 1 · uke 46», the week list with the year rule, the smoothing factor with one decimal.
- `src/explanation/worksheet.py` (new) -- the sales rows and tags, the tag sentence, the calculation lines, the left-out lists, the scenario texts, the order line.
- `src/web/views.py`, `templates/web/product.html`, `_worksheet.html` (new), `static/web/app.css` -- the panel after `.decide`; tokens only.
- `_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/EXPERIENCE.md` -- the new catalogue rows and the change-log row.
- `tests/` -- `test_worksheet.py` (new), `test_forecast.py`, `test_forecasting_display.py`, `test_product_screen.py`, `test_isolation.py`, `test_core_imports.py` (extended); the expected values are read with `tests/answer_key.py` and the workbook.
- Documents: `docs/statustabell.md`, `qa-logg.md`, `ki-styringslogg.md`, `arbeidslogg.md`, `sprint-status.yaml`, `deferred-work.md`, `.logs/mounia-03/issues.md` (the column label and the FR-7 note items).

## Tasks & Acceptance

**Execution:**
- [ ] `src/forecasting/` -- result fields and display helpers -- FR-7, FR-15, FR-16, UX-DR42, AD-3
- [ ] `src/explanation/worksheet.py` -- all worksheet sentences and rows -- FR-10, FR-12, FR-35, UX-DR28 to UX-DR30, AD-4
- [ ] `src/web/` templates, view, CSS -- the panel, tables in scroll frames, tags, calculation boxes -- NFR-6, UX-DR7
- [ ] `EXPERIENCE.md` -- catalogue rows and change log -- the user's decision 2
- [ ] tests above -- every matrix row against the workbook (E1 to E4, E6, E8, E9, E11 a, E15, E21, E23), the two-account test, the query count at 50 products of 104 weeks -- FR-2, NFR-8; exponential smoothing and «holdes utenfor» through a `CompanySettings` row in the test database
- [ ] the documents above, `sprint-status.yaml` to `review` -- DR-7

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` and `makemigrations --check`, when they run, then they pass.
- Given mutations of the new code (a stockout week counted as used, the last update on the wrong level, the margin on week 2, «(lageret dekker behovet)» without a condition, the year rule dropped, a number formatted outside `display.py`, the company filter dropped, a query in the product loop), when the tests run, then each fails at least one test.
- Given Strøsand 25 kg and the test products E1 and E8, when the pages open at 1366 × 768, 320 px, 390 × 844 and 820 × 1180, then nothing scrolls sideways or is cut off, and the lines match the workbook and the mockup (checked by hand, QA log).

## Implementation Notes

- 2026-11-28: built in the build session, not by a subagent, because the user approved subagents for the reviews only. Model: Sonnet 5.5 (`claude-sonnet-5-5`, confirmed by the session; the effort level is not shown by the session). Branch `story/2-9-show-how-the-forecast-and-the-order-quantity-were-calculated` from `9aec086`. The user approved the three proposals and the six clarifications, and added that an unusual week that is used must be clearly told from one that is held out (see the Spec Change Log).
- New: `src/explanation/worksheet.py` (the sales rows and tags, the tag sentence, the calculation lines, the left-out list, the scenarios and the order line), `web/_worksheet.html`, `tests/test_worksheet.py`. Changed: `ProductResult.sales` and `.stockout_weeks` in `forecasting/forecast.py`; `horizon_column_label`, `week_item`, `week_list` and `factor` in `forecasting/display.py`; `web/views.py` (`sheet` in the context), `product.html`, `app.css`; the Message Catalogue and change log of `EXPERIENCE.md`; the tests of the product screen, the forecast and the display.
- Deviations from the frozen block, both because R-10 never checks the first three valid weeks, so a forecast always has at least three calculation weeks: the matrix row «One calculation week» (a «startnivå» line) and the singular «1 uke brukt i beregningen» cannot occur, so no code was written for them (AA-1, EC-3, EC-4). The user chose option A on 2026-11-28 and the row and the singular were taken out of the frozen block (see the Spec Change Log).
- Interpretations: «[N] uker brukt i beregningen» counts the weeks used in the forecast (the weeks that «Uker brukt» names, or every calculation week for exponential smoothing). The tag «uvanlig» (taken in) and «uvanlig, holdt utenfor» (left out) differ in words, shape (solid or hollow triangle) and border (solid or dashed).
- Checks run: `uv run pytest` 1191 passed and 1 skipped (Docker), against 1099 and 1 after Story 2.8; `ruff check` and `ruff format --check` clean; `makemigrations --check` no changes. 28 mutations before the review (21) and after it (7), all caught; the files were restored and compared by hash.
- Layout in headless Chrome 120 (old mode), six saved pages (Strøsand 25 kg, 10040 without a forecast, E8, and E15 and E7 of Testbedrift B, and Strøsand with exponential smoothing and unusual weeks left out) at 1366 × 640, 1180 × 820, 901 × 900, 820 × 1180, 390 × 844 and 320 × 640: 36 measurements, the page never scrolls sideways and no element outside a scroll frame is wider than the screen. At 320 px the sales table (up to 705 px) and the scenario table (418 px) scroll inside their frames of 246 px; the calculation lines wrap (77 and 141 px high). The table of levels with 104 weeks scrolls in its own frame. This is not Safari and not a phone; the hand checks are the user's.
- Process: four reviewers as `general-purpose` subagents with `model: "sonnet"` (an alias, not confirmed to be 5.5), launched together. The Verification Gap reviewer's prompt had a wrong diff path (a missing hyphen, Claude's mistake), corrected by a message before it reported. The reviewers changed nothing: the hash of the whole tree was identical before and after. The Blind Hunter and the Verification Gap reviewer never saw the spec.
- Manual checks, reported by the user in chat on 2026-11-28 (details and gaps in `docs/qa-logg.md`): Safari on the Mac for Strøsand 25 kg (10012) at 1366 × 768, 820 × 1180, 390 × 844 and 320 × 844, and for 10025, 10040, 20005 and 20002, with the worksheet, tags, formula, scenarios and order quantity agreeing and the table's own horizontal scroll checked; the real iPhone 13 (iOS 27.0.1, as the user gave it) for all five products, with the horizontal scroll of 10012's sales table confirmed. Claude read macOS 15.6.1 and the installed Safari 18.6 from the system; the Safari version that ran the checks was not given. Gaps: the Safari view type, the widths for the other four products, the scenario table's scroll, the Tab order and focus rings of the frames, and the iPhone screenshots (not seen by Claude). Exponential smoothing and the left-out tag cannot be tried in the app before Epic 3.
- Committed with the user's approval on 2026-11-28: the code, the tests and the catalogue in `019114c`; the spec and the documents in the next commit, and the session log in the last. Pushed over SSH with the user's approval and merged as PR #50 on 2026-11-28 (merge commit `0fb5391`, parents `9aec086` and `8ffa2af`); CI run #94 on the branch and Windows run #24 passed, and CI run #95 on `main` passed with 1192 tests (the Docker check runs in CI). The session export is masked and kept in `.logs/mounia-03/sessions/2-9-2026-11-28.txt`.

## Spec Change Log

- 2026-11-28, the user's instruction when approving the spec (not a review finding): the status tags must clearly tell an unusual week that is used from one that is held out. The tag rule in the frozen block was amended with the user's approval: «uvanlig» (taken into the calculation) and «uvanlig, holdt utenfor» (left out by the setting) differ in words, shape (solid or hollow triangle) and border (solid or dashed). Known-bad state avoided: one «uvanlig» tag for both, leaving the reader to guess from the sentence below the table. KEEP: the mockup's «uvanlig» for an included week.
- 2026-11-28, Acceptance Auditor AA-1 and Edge Case Hunter EC-3 and EC-4 (intent_gap, resolved by the user): the I/O matrix row «One calculation week» (ES, one week left, a «startnivå» line) and the singular «1 uke» in «[N] uker brukt i beregningen» have no code. R-10 never checks the first three valid weeks, so a forecast has at least three calculation weeks and a moving average at least two; the cases cannot occur. The user chose option A on 2026-11-28: no dead branch, and a comment in `_formula` explains why. The reason given: the cases cannot occur under R-10, and a branch for them could be tested only with a `ProductResult` built by hand, which no reachable input produces. Option B (a defensive branch with such a test) was declined. Amended in the frozen block with the user's decision: the matrix row «One calculation week» is removed and the «(«1 uke»)» is taken out of decision 2. Known-bad state avoided: untestable dead code and a «startnivå» sentence that no reachable input produces. KEEP: the update line from the previous level and the plural count, and the comment in `_formula` that names R-10 as the reason.
- 2026-11-28, review of Story 2.9 (patches inside the frozen block's rules, no amendment): the sentence below the sales table explains only the tags on the table («Brukt» only when a used week is shown) and, without a forecast, makes no claim about a calculation (BH-1, VG-1, AA-2, AA-3, EC-1, EC-2, EC-13). Known-bad state avoided: a sentence about a «brukt» tag that is not on the table, and «tatt med» for a calculation that does not exist.

## Review Triage Log

BMAD Code Review (2026-11-28): Blind Hunter (BH, 13), Edge Case Hunter (EC, 13), Verification Gap (VG, 2 gaps and 2 other findings) and Acceptance Auditor (AA, 7), as four independent read-only subagents, on the diff of `src`, `tests` and `EXPERIENCE.md` from `9aec086` (79 kB). The spec went to the Edge Case Hunter and the Acceptance Auditor only. 37 findings in 22 groups: 8 patched, 1 intent gap (resolved by the user: option A), 0 deferred and 13 rejected.

| ID | Finding | Verdict | Route |
|---|---|---|---|
| BH-1, VG-1, AA-2, EC-1, EC-13 | The sentence below the table explains «brukt» from all used weeks, also when none is on the table, and no test has a flagged week before the shown 12 | medium | patch: «Brukt» only when a used week is shown; tests with a stockout before the shown weeks and with no used week shown |
| EC-2, AA-3 | Without a forecast the sentence says unusual weeks are «tatt med» or level shifts «alltid tatt med i beregningen» | medium | patch: no claim about a calculation without a forecast; tests for E11 b and a level shift without a forecast; catalogue row updated |
| AA-1, EC-3, EC-4, EC-11 | No «startnivå» line and no «1 uke» singular, as the matrix and decision 2 say | low | intent_gap, resolved by the user on 2026-11-28 with option A: R-10 makes both cases unreachable (at least three calculation weeks), so no code is written, the frozen block's matrix row and the singular are taken out, and the Spec Change Log records it; option B (a defensive branch tested with a hand-built `ProductResult`) was declined |
| BH-6, EC-7 | `week_list([])` gives «uke » | low | patch: `ValueError`, with a test |
| BH-7, EC-6 | The `used_weeks` docstring says None, the code returns `()`; `shown` is computed before the early return | low | patch: the docstring, and `shown` moved |
| BH-2 | Three new catalogue rows with four cells sit in the component table of three | medium | patch: moved into the Message Catalogue table, and the name made «Weeks left out (text)» because a row with that name exists in the display rules |
| BH-4 | The catalogue says «at least one left out», the code needs an unusual week | low | patch: «at least one unusual week left out» |
| BH-11 | A test docstring names weeks 38 and 39 where the assertion has 42 and 43; one test is duplicated in `test_forecast.py` | low | patch: the docstring, and the duplicate removed (the raw-SVG assertion is kept, see the rejects) |
| VG-2, BH-12 (part), VG other | The levels table with a long history, its year labels and the page-level frame attributes are untested; the frame test runs on a moving-average page only | medium | patch: unit tests for the year rule in the table, for excluded unusual weeks with exponential smoothing and one on the page for the frame's role, tabindex and label |
| BH-12 (rest) | A week that is both a stockout and unusual; narrow-viewport checks; gaps in the weeks | low | reject: stockout weeks are never classified (R-1), so the combination cannot occur; the viewports are measured in headless Chrome (Implementation Notes); weeks are gapless (AD-8) |
| EC-8 | The heading «alle ukene» stands above «Produktet har ingen salgsuker.» | low | reject: reads naturally, and a conditional heading adds a branch for a case the page already explains |
| BH-5 | The «Holdt utenfor» list has no cap | low | reject: the criterion lists every week left out; a cap would hide a week from the examiner |
| BH-8 | No sticky first column in the sales table | low | reject: UX-DR28 and the mockup have none; the frame scrolls, and the 12 weeks fit from 900 px |
| BH-9 | No captions, a literal `aria-label` on the levels frame, no `:focus-visible` rule for the frames | low | reject: each frame has a name, the global `:focus-visible` rule (UX-DR4) covers every focusable element, and the extra tab stops are expected and tested |
| BH-10 | The contrast of the new tags is not verified | false | reject: computed ratios 5.55 (utsolgt), 6.64 (uvanlig), 7.41 (uvanlig, holdt utenfor), 14.33 (nytt nivå) and 5.19 (brukt), all above 4.5; each tag also has its words |
| EC-9 | A line can wrap between «lager» and «5» | low | reject: the criterion asks for wrapping between terms and never inside a number |
| EC-5 | `week_at_position` raises when the latest week is missing | low | reject: loud by design, as EC-11 of Story 2.7; a company with sales weeks always has a latest week |
| EC-10, AA-4 | `test_isolation.py` and `test_core_imports.py` are not changed | low | reject: `ROUTES` already holds the product page, which now shows the stock; `test_core_imports.py` scans every file of `explanation/` |
| BH-3, EC-12, AA-5, AA-6 | The documents are not in the diff, and the change-log row says «hash følger» | low | reject: the documents follow the review (AA-1 of Story 2.7), and the hash is filled in after the commit |
| BH-13 | The spec and `sprint-status.yaml` are not in the diff | low | reject: the spec goes to two reviewers as the claims file by design |
| AA-7 | «The margin on week 2» cannot make a test fail | low | reject: an equivalent mutant while the weeks repeat (the open point for Epic 5); the mutation list used the margin percentage instead |
| BH-11 (rest) | The test of the mockup uses regexes, and the hollow-triangle assertion matches a raw SVG string | low | reject: the mockup is one fixed file and a break is loud; the string is the only check that the two triangles are drawn differently |

**Decision by the user (2026-11-28):** AA-1 is resolved with option A. No open point remains from the review.

## Design Notes

The seed companies use the defaults (moving average, unusual weeks included), and no screen changes settings before Epic 3. Exponential smoothing and «holdes utenfor» are therefore checked with a `CompanySettings` row on pytest's own database and with `forecast_product` directly; the hand checks in the browser cover the moving average only. Where the mockup and `EXPERIENCE.md` word a line differently, `EXPERIENCE.md` wins (UX-DR28).

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check` -- expected: clean
- `uv run python src/manage.py makemigrations --check` -- expected: no changes

**Manual checks:**
- Safari at 1366 × 768, 820 × 1180, 390 × 844 and 320 px, and the real iPhone 13, for Strøsand 25 kg and the test products as Testbedrift A and B; the user reports the result in chat. The calculation lines are compared with the workbook by hand.
