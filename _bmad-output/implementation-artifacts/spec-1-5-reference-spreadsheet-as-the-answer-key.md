---
title: 'Story 1.5: Reference spreadsheet as the answer key'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'dispatch'
baseline_commit: 'da87fd7f68e4447710c9700ba30cb7be218c7805'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `reference/` holds only `.gitkeep`. No test, seed generator or examiner can check a number against PRD §5.7, and Stories 1.6, 2.1 to 2.6 and 3.2 have no answer key to read (DR-3, AD-17).

**Approach:** One workbook, `reference/reference-examples.xlsx`, written with openpyxl, holds every §5.7 example and the four FR-21 variants as cases, and the rule test products with their series, stock on hand and expected results, all as plain values. A `checks` sheet recalculates every expected value with visible formulas, and `check_log` records the dated hand check. `reference/README.md` documents the schema, `tests/answer_key.py` reads the workbook, and `tests/test_reference_spreadsheet.py` fails when a case, an expected value or a check is missing or wrong.

## Boundaries & Constraints

**Always:**
- Sheets `about`, `cases`, `products`, `checks` and `check_log`, with the columns in Design Notes. Row 1 holds the column names, and `cases` and `products` hold no formulas.
- One row per case. An example whose result depends on a setting, a series or a product has one row per variant, such as «E8 (included)» and «E8 (excluded)». `example` holds the §5.7 ID, `prd_input` and `prd_result` quote its PRD cells verbatim, and every setting is written out in every row.
- Sales are written «12, 15, S, S2»: whole units sold, «S» a stockout week with 0 units sold, «S2» one with 2. Positions count from 1.
- Numbers are numeric cells with the precision of PRD §5.7; a calculated number matches when it differs by less than 0.0005. «none» is an expected absence, such as no forecast; an empty cell is not asserted. Lists are «4, 5»; flags are «yes» or «no».
- The expected values equal PRD §5.7: E1 to E30 with E11 a/b, E18 a/b and E29 a–g. Where a case states a warning or a confidence label, `warnings` lists every active warning of R-15, with item 6 only in Should cases.
- E30, by the user's decision of 2026-11-22: it stays as the PRD has it, and its cases record «lav», which R-16 step 1 gives because E14's data has 8 valid weeks. The open point that E30 cannot show FR-36's effect on the label moves to Story 5.2, and the PRD is not changed.
- `products` holds the rule test products built from E1–E4, E7–E10 and E15–E19, one per distinct series, and the demo product Strøsand 25 kg, with the FR-20 defaults. The company follows UX-DR46: E8 and Strøsand in A, the rest in B.
- `checks` recalculates each expected value, and each R-10, R-11 and R-16 decision, with a visible formula next to the recorded value and a match formula. Claude also recalculates every case with an independent script in the scratchpad. The user opens the workbook in Excel or Numbers without saving and reports the result in chat, and `check_log` records the date, who checked, how and the result. A difference from PRD §5.7 is recalculated by hand, the wrong side is corrected (a PRD correction gets a §12 row), and the QA log records it.
- The tests read the §5.7 table, the FR-3 ranges and the FR-21 table from the PRD, use no database, and name DR-3, AD-17, FR-3, FR-21 or NFR-4 (D-10).

**Never:**
- No expected value in test code, and no committed builder or recalculation script: the workbook is the one answer key (AD-17).
- No forecasting code (Epic 2); no seed generator, product numbers, product names or pattern products such as Snøskuffe aluminium (Story 1.6); no new dependency.
- No save of the workbook in Excel, which writes the local path and the user name into the file (NFR-4).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Complete workbook | as built | every test passes | N/A |
| Missing case | a §5.7 ID without a row | the test fails and names the ID | N/A |
| No expected value | a case whose expected cells are all empty | the test fails and names the case | N/A |
| Schema error | «1O», «s», a position past the series, an unknown setting, warning or label | the schema test fails and names the cell | N/A |
| Formula in the answer key | a formula in `cases` or `products` | the reader raises | N/A |
| Stale check | a recorded value in `checks` that differs from the answer key, or an expected value without a check | the check test fails | N/A |
| Changed PRD | a §5.7 cell that differs from `prd_input` or `prd_result` | the sync test fails | N/A |
| Local path | an Excel save that leaves `absPath` or `/Users/` in the XML | the NFR-4 test fails | N/A |

</frozen-after-approval>

## Code Map

- `reference/.gitkeep` -- delete once the workbook exists.
- `pyproject.toml` -- openpyxl 3.1.5 is already a dev dependency. pytest's default import mode puts `tests/` on `sys.path`, so test modules can import `answer_key`.
- `_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md` -- the §5.7 table (lines 665–704, rows start with `| E`), the FR-3 ranges (line 208) and the FR-21 table (lines 428–436); the tests parse them.
- `…/prds/prd-G40-lyamouri-2026-11-02/review-calculations.md` -- the planning-phase recalculation of E1–E14 and M1–M16, the source of E15–E30, in double precision.
- `…/ux-designs/ux-G40-lyamouri-2026-11-15/mockups/konsept-d-kombinert.html` lines 267–303 and 543, `EXPERIENCE.md` lines 301–305 and 347 -- Strøsand's weeks 34–45, stock 5 and the «Denne uken» figures.
- `tests/test_app_shell.py` lines 16–22 -- how a test reads a planning document by its real path.
- `docs/statustabell.md` (status paragraph, FR-3 and FR-21), `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, `README.md` («Tester»), `sprint-status.yaml`, `.logs/mounia-03/issues.md` (lines 20, 98 and 99) -- documents to update.

## Tasks & Acceptance

**Execution:**
- [x] Scratchpad, not committed -- an independent recalculation of R-1 to R-17, and a builder that writes the workbook from the PRD values and generates the `checks` formulas from a small expression tree, evaluated in Python with Excel's rounding -- finds differences before the user's check.
- [x] `reference/reference-examples.xlsx` -- create the five sheets; delete `reference/.gitkeep`.
- [x] `reference/README.md` -- create, in Norwegian: the sheets, every column, the notation, the comparison rule, the products, how the check was made and how to edit the workbook safely.
- [x] `tests/answer_key.py` -- create the reader (typed values, the sales parser, «none», flags and lists; it raises on a formula) and the PRD parsers.
- [x] `tests/test_reference_spreadsheet.py` -- create one test per matrix row.
- [x] `README.md` -- one sentence in «Tester» that links `reference/README.md`.
- [ ] `docs/statustabell.md`, `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, `sprint-status.yaml`, `.logs/mounia-03/issues.md` -- the tests in the FR-3 and FR-21 rows and the status paragraph; the hand check and any difference; a case if AI output is corrected; the work log; the story status; the open points.

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check` and `uv run ruff format --check`, when they run locally and in CI, then they pass.
- Given the workbook opened in Excel or Numbers without saving, when the user reads the summary beside the table in `checks`, then every check matches, and `check_log` and the QA log record the date and the result.

## Implementation Notes

- 2026-11-23: built in the build session, not by a subagent, because the user approved subagents for the reviews only. The epic context was used as it was, as in Story 1.4: the spine change from Story 1.3 that made it formally stale touches nothing here.
- The builder in the scratchpad typed the expected values from PRD §5.7 and the hand calculations, recalculated every case and product with its own implementation of R-1 to R-17, and evaluated the `checks` formulas with Excel's rounding (half away from zero, `ROUNDUP` away from zero). Every typed value equals the independent recalculation, so no value differs from PRD §5.7.
- Found by the builder's comparison before the workbook was written: the check formulas for the three recent-period warnings compared the last such week with «N − 12», which is true for a history shorter than 12 weeks without such a week; 33 checks failed. They now compare with `MAX(1, N − 11)`, the first week of the recent period, and all 376 checks match (QA log).
- The workbook: 52 cases, 11 products, 628 check rows, of which 376 hold a recorded value and 252 are steps such as `r10_flag`. Long series (more than 30 weeks) get a flag row for each flagged week and one bound row for the others instead of 104 flag rows. A stockout week with 0 units sold is written «S», so Strøsand's weeks 97 and 98 are «S, S2» (the Design Notes' «S0» means the same).
- Strøsand 25 kg, with position 104 at ISO week 45 of 2026: positions 93, 97, 98 and 101 are weeks 34, 38, 39 and 42, as in the mockup. R-17 (Should) gives week number 42 the index 1.5735 because of the unusual week, so FR-36 would add a seasonal-pattern warning; an open point for Story 5.2.
- Mutations, each applied to a copy of the workbook or the PRD and then restored by a scratchpad script that is not committed: a case deleted, a case without expected values, «1O» and «s» in a series, a position past the series, an unknown setting, warning and label, warnings out of R-15 order, a flag that is not «yes» or «no», a formula in `cases` and in `products`, a changed value in `cases` and in `products`, a check row removed, a product without a required result, a product series that differs from its example, an FR-21 variant without its value, a check log without a date, an `absPath` in the workbook XML, and a changed §5.7 example in the PRD. All 21 were caught. The first run missed two, because the script's `ws.cell(..., value=None)` leaves a cell unchanged in openpyxl; the script was fixed, not the tests.
- 142 tests pass (132 earlier and 10 new), with `~/.docker/bin` on PATH; Ruff passes after `ruff format` of the two new test files.
- 2026-11-23, the second acceptance criterion: the user opened the workbook in Excel for Mac 16.78 (23100802), read K1 = 376, K2 = 376 and K3 = TRUE in `checks`, and closed it without saving; the file's hash was unchanged afterwards. The builder then wrote the workbook again with the user's row in `check_log`, and every other sheet is identical to the checked version. The QA log records the check.

## Spec Change Log

## Review Triage Log

Review pass 1 (2026-11-23): Blind Hunter, run inline by the build session as in Stories 1.2 to 1.4, on the diff from `da87fd7` with a text dump of the workbook (163.8 kB, so at least 10 findings). Edge Case Hunter and Verification Gap were skipped here, because BMAD Code Review runs them as independent subagents on the pull request (D-8).

| ID | Finding | Verdict | Evidence | Route |
|---|---|---|---|---|
| BH-1 | openpyxl's `insert_rows` and `delete_rows` do not move formula references, and the README tells editors to use openpyxl, so a row inserted or deleted in `checks` silently points formulas at the wrong rows | medium | Real: openpyxl leaves formula strings unchanged, and the tests read no formula results, so nothing would fail | patch: the README says to append rows at the end of `checks` and to read the summary in Excel or Numbers after every edit |
| BH-2 | No test evaluates the formulas in `checks`, so a wrong reference or literal passes every test | low | Real, but the builder evaluated every formula with Excel's rounding before writing, and the manual check in Excel reads the results; an evaluator in the tests would add a formula interpreter | reject; the patch for BH-1 makes the check in Excel part of every edit |
| BH-3 | The schema test does not check the FR-20 ranges of the settings | low | Real: a window of 30 would pass. AD-9 defines the ranges once, in `forecasting/settings.py`, which Story 1.7 creates, so copying them into the test would duplicate them | reject; open point for Story 1.7 in `issues.md` |
| BH-4 | `LOCAL_PATH` misses Linux home paths | low | `/home/` was not in the pattern | patch: `/home/` added |
| BH-5 | `read_rows` raises `StopIteration` on an empty sheet | low | A loud failure on a malformed workbook, not a wrong result | reject |
| BH-6 | The README says `recorded` is the answer-key value, but display checks record the number 14.3 for «14,3», and week and warning checks record TRUE or FALSE | low | Real gap in the wording | patch: the README explains both |
| BH-7 | The README and the logs state counts (52 cases, 11 products, 376 checks) that can drift | low | They describe the state at the check, which `check_log` also records | reject |
| BH-8 | The warning names only Excel, but another program could also write metadata into the file | maybe-false | Numbers exports a copy instead of saving the xlsx, and whatever writes a local path fails the NFR-4 test | reject |
| BH-9 | `FR21_COLUMNS` in the test maps the text of the FR-21 table, so a new row raises `KeyError` | false | The `KeyError` is the intended loud failure when the PRD adds a variant | reject |
| BH-10 | Strøsand's stockout week with 0 units sold is «S» in the workbook and «S0» in the Design Notes | low | The notation gives both the same meaning, and the Implementation Notes record it | reject: the fix would edit this build's spec |
| BH-11 | The products sheet has no settings columns, so its expected values depend on the FR-20 defaults that only the README states | low | The defaults are the PRD's (FR-20) and the seed state; changing them is a PRD change that recalculates the answer key anyway | reject |
| BH-12 | `tests/answer_key.py` is imported through pytest's default import mode, which puts `tests/` on `sys.path`; `--import-mode=importlib` would break it | low | The project sets no import mode, and the Code Map records the dependency | reject |
| BH-13 | The README says that Numbers shows the function names in the program's language, which was not checked | low | An unchecked claim | patch: the sentence names Excel only |

## Design Notes

**Columns.**
- `cases`: `case`, `example`, `rule`, `priority`, `prd_input`, `prd_result`; inputs `sales`, `method` (`moving_average`, `exponential_smoothing`), `window`, `smoothing_factor`, `scenario_percentage` and `safety_margin` (whole percent), `unusual_weeks_setting` (`included`, `excluded`), `seasonal_adjustment` (`on`, `off`), `cycle_length` (52, or 4 where §5.7 says so), `stock_on_hand` (0 where the example gives none), `product_number` (E24 only); expected `valid_weeks`, `unusual_weeks`, `level_shift_weeks`, `calculation_weeks`, `levels`, `week_number_means`, `mean_of_means`, `seasonal_indices`, `adjusted_sales_used`, `base_forecast`, `base_forecast_shown`, `week_forecasts`, `normal`, `optimistic` and `pessimistic` (week 1), `order_unrounded`, `order_unrounded_shown`, `suggested_order_quantity`, `optimistic_order_unrounded`, `optimistic_order_quantity`, `pessimistic_order_unrounded`, `pessimistic_order_quantity`, `weeks_of_cover`, `weeks_of_cover_shown`, `order_soon`, `overview_position`, `overstock_note`, `weeks_since_latest_valid`, `seasonal_adjustment_used`, `seasonal_pattern`, `warnings` (`stockout_weeks`, `unusual_weeks`, `level_shift`, `old_data`, `insufficient_data`, `seasonal_pattern`, in R-15 order) and `confidence_label` (`lav`, `middels`, `høy`).
- `products`: `product` (the example whose series it uses, or the demo name), `company` (`A`, `B`), `examples`, `sales`, `stock_on_hand`, `base_forecast`, `suggested_order_quantity`, `unusual_weeks`, `level_shift_weeks`, `warnings`, `confidence_label`.
- `checks`: `sheet`, `key`, `value` (an answer-key column, or a step such as `r10_flag`), `item` (a list index, a position, a warning or «other»), `recorded`, `recalculated` (formula), `match` (formula), `note`; the summary «N of N match» stands beside the table. `check_log`: `date` (ISO), `checked_by`, `scope`, `method`, `result`.

**Concrete series** for examples that give none: E5 and E6 «100, 100, 100»; E11 b «10, 10, 10, 30, 10, 10, 10, 30, 10, 10, 10, 10» (weeks 4 and 8 unusual); E12 95 × 10 and 9 × S, then 96 × 10 and 8 × S; E29 b 12 × 10; E29 c 53 × 10, 30, 50 × 10; E29 d 98 × 10, 30, 5 × 10; E29 f 50 × 10, 3 × S, 51 × 10; E29 g 50 × 10, 5 × S, 49 × 10; E24 A «10, 10, 10» and B «20, 20, 20», stock 0.

**FR-21 variants**, hand-calculated: a) E1 with window 4: (13 + 16 + 12 + 15) / 4 = 14.0; b) E2 with α 0.5: levels 12, 13.5, 12.25, 13.125, 13.0625, 14.53125, 13.265625, 14.1328125, so 14.133; c) E3 with 20 %: 17.2 and 11.467; d) E4 with 50 %: 14.333 × 1.5 − 5 = 16.5, rounded up to 17.

**Products.** E1 (E1–E4; B; stock 5); E7 (E7, E17, E29 a), E9, E10, E15, E16, E18 a, E18 b and E19 (B; stock 0); E8 (A; stock 50, so the need of 45.1 is covered and «Denne uken» keeps 4 products to order soon); Strøsand 25 kg (E1, E3, E4, E13; A; stock 5): positions 1–92 repeat the E1 series, and 93–104 are the mockup's «11, 13, 12, 14, S0, S2, 13, 15, 31, 16, 12, 15», so position 101 (week 42 of 2026) is unusual, 97 and 98 are stockout weeks, the base forecast is 14.333, and the label is «middels».

## Verification

**Commands:**
- `uv run pytest` -- expected: every test passes, the 132 earlier ones included.
- `uv run ruff check` and `uv run ruff format --check` -- expected: no findings.

**Manual checks:**
- The user's check in Excel or Numbers, without saving.
- `unzip -p reference/reference-examples.xlsx | grep -c absPath` -- expected: 0.
