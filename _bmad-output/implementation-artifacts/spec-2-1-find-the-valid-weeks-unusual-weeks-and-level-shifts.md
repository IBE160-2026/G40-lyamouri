---
title: 'Story 2.1: Find the valid weeks, unusual weeks and level shifts'
type: 'feature'
created: '2026-11-24'
status: 'done'
route: 'dispatch'
baseline_commit: '1b8927d26b6a4b87b4beffe3bb209c5621fe4acf'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Nothing in `forecasting/` classifies a sales history, so no forecast, warning or chart can know which weeks are valid, unusual or level-shift weeks (FR-15, FR-16, FR-17), and the reference examples have no tests yet.

**Approach:** Add one pure function in the core that classifies a product's weeks by R-1, R-10 and R-11 in a single forward pass, and test it against every classification stated in the reference spreadsheet. No screen changes.

## Boundaries & Constraints

**Always:**
- The function takes a product's weeks, oldest first, each with `units_sold` and `stockout`, and returns the positions (1 to N, AD-8) of the valid weeks, the unusual weeks and the level-shift weeks. It never reads the setting «include unusual weeks» (R-2 and Story 2.2 do) and never uses the units of a stockout week.
- R-10 exactly as the PRD states it: the baseline is the median of the 3 most recent earlier valid weeks that are not unusual (level-shift weeks count); fewer than 3 such weeks means the week is not checked but still enters later baselines; a baseline of 0 never gives an unusual week; unusual means more than 2 × the baseline, so exactly 2 × is not; only high sales are flagged. R-11: when a week becomes unusual and the two previous valid weeks are unusual, the three become level-shift weeks at once; stockout weeks in between do not break the run.
- Integer arithmetic only, so the 2 × comparison is exact. The module imports only the standard library, and reads no clock, file or environment variable (AD-1).
- The tests read the expected `valid_weeks`, `unusual_weeks` and `level_shift_weeks` from `reference/reference-examples.xlsx` through `answer_key_reader`, for the cases and for the rule test products, and compare only the values a row states. Each test names its E-n and FR-n (AD-17, DR-5).

**Never:**
- No expected value copied into code. No calendar arithmetic. No model, migration, view, template or dependency. No calculation weeks, forecast, rounding or warning (Stories 2.2 to 2.5). Do not change the spreadsheet.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Stockout weeks | E7: 20, 22, S, S2, 21, 23 | 4 valid weeks (positions 1, 2, 5, 6), none unusual | N/A |
| Two high weeks | E8: positions 4 and 5 high | unusual 4, 5; no level shift | N/A |
| Three high weeks | E9: positions 4 to 6 high | level shift 4, 5, 6; no unusual week | N/A |
| Spike after a shift | E15 | level shift 4, 5, 6; unusual 7 | N/A |
| Stockout inside a run | E16: position 7 is a stockout | level shift 6, 8, 9; 6 valid weeks | N/A |
| Zero baseline | E10: zeros, then sales | no unusual week | N/A |
| Exactly 2 × / above 2 × | E18 a / E18 b | none / unusual 4 | N/A |
| Fewer than 3 earlier weeks | E19: first weeks high | week 1 to 3 unchecked, unusual 6 | N/A |
| Empty or all-stockout history | no valid week | three empty results | N/A |
| Units of a stockout week | same history, other stockout units | same result | N/A |

</frozen-after-approval>

## Code Map

- `src/forecasting/` -- holds `display.py` and `settings.py`; new `weeks.py` follows their style (module docstring naming the AD, plain functions, frozen dataclass as in `settings.Range`).
- `tests/test_core_imports.py` -- already checks every file in `forecasting/` for AD-1, so `weeks.py` is covered without a change.
- `reference/answer_key_reader.py` -- `cases()`, `products()` and `Week(units_sold, stockout)`; unstated columns are absent from a row. `tests/test_reference_spreadsheet.py` shows how tests import it (`pythonpath` has `reference`).
- Spreadsheet rows with the three columns: E7, E8, E9, E10, E15, E16, E18 a and b, E19 per setting, E11, E29 and the 11 rule test products.
- Documents: `docs/statustabell.md` (FR-15 to FR-17 rows), `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, `sprint-status.yaml`, `.logs/mounia-03/issues.md`.

## Tasks & Acceptance

**Execution:**
- [x] `src/forecasting/weeks.py` -- `Week`, `WeekClassification` and `classify_weeks` -- R-1, R-10, R-11, AD-1, AD-8
- [x] `tests/test_week_classification.py` -- every matrix row, every stated spreadsheet value for the cases and the rule test products, a guard that the nine listed examples are covered, input not changed -- FR-15, FR-16, FR-17
- [x] documents above, `sprint-status.yaml` to `review` -- DR-7

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check` and `uv run ruff format --check`, when they run locally and in CI, then they pass, and `makemigrations --check` finds no change.
- Given a mutation of `weeks.py` (`>=` for `>`, a baseline that skips level-shift weeks, a baseline over all earlier weeks, a stockout week counted as valid, a run broken by a stockout), when the tests run, then at least one fails.

## Implementation Notes

- 2026-11-24: built in the build session, not by a subagent, because the user approved subagents for the reviews only. The epic context did not exist; it was compiled inline into `epic-2-context.md`, because the subagent route was not approved for the build.
- Branch `story/2-1-find-the-valid-weeks-unusual-weeks-and-level-shifts` from `1b8927d`. New: `src/forecasting/weeks.py` (`Week`, `WeekClassification`, `classify_weeks`) and `tests/test_week_classification.py`. 362 tests after the review, 1 skipped (the Docker check, because Docker is not on the PATH of this shell). `makemigrations --check` finds no change.
- Spreadsheet-driven: 35 parametrised checks, 24 cases and the 11 rule test products that state a value (the nine listed examples in every variant, E1, E11 and E29 a to g), plus 14 direct tests. The spreadsheet states the valid weeks only as a count, so the positions are also compared with R-1 (every week but the stockout weeks).
- `Week` is a `NamedTuple`, as the reader's own `Week`, while the result is a frozen dataclass as `settings.Range`. The constants of R-10 and R-11 stay in `weeks.py`, because the rules fix them and `settings.py` holds only the FR-20 settings (AD-9).
- Mutations applied to `weeks.py` and then restored, 29 in all, all caught: `>=` for `>`; the factor 3; a baseline of 2 or 4 weeks, or over all earlier weeks; a mean, a maximum or a minimum for the median; a zero baseline or a baseline above 1 left out; a stockout counted as valid or its units used; a baseline that leaves out level-shift weeks or keeps unusual ones; a level-shift run of 2 or 4, without the check that the weeks are unusual, broken by a stockout or by calendar positions, or with the shift weeks left unusual or the first one dropped; weeks checked from 1 or 2 earlier weeks; positions from 0; the input not turned into a tuple. The first set of 20 left 3 gaps that the review and a second set found (`>= 1` and `>= 2` earlier weeks, and a baseline above 1); each now has a test.
- The reviewers changed `weeks.py` for their own mutations in the working tree and restored it. The file was compared with the copy taken before the review and was identical.


## Spec Change Log

## Review Triage Log

BMAD Code Review (2026-11-24): Blind Hunter (BH), Edge Case Hunter (EC), Verification Gap (VG) and Acceptance Auditor (AA), as four independent subagents, on the working-tree diff from `1b8927d` (24.8 kB, 5 files, N = 5 for the Blind Hunter). The spec went to the Edge Case Hunter as the claims file and to the Acceptance Auditor. The first round had the three layers of the build workflow. A first Verification Gap run had a mistyped diff path, found the file anyway and reported no gap; it was repeated with the right path and found VG-1. The Acceptance Auditor, the fourth layer of `bmad-code-review` that the routine for code review and Stories 1.1 to 1.8 use, was added before the commit, on the whole diff with the documents (55.3 kB), and read only. 29 findings: 16 patched, 5 rejected and 8 false. None was deferred, and none needed a decision from the user. The fixes are in the commit `5548f4e`.

| ID | Finding | Verdict | Route |
|---|---|---|---|
| VG-1 | The «fewer than 3 earlier weeks» rule is not pinned: `>= 1` or `>= 2` earlier weeks passed all 46 tests | medium | patch: `test_a_week_with_fewer_than_three_earlier_valid_weeks_is_not_checked`, with a stockout in front and week 4 compared with them |
| BH-6, EC-5 | The valid weeks are compared as a count only, and the one check of positions repeats the function's own rule | medium | patch: every case and product also compares the positions with R-1, and E7 states 1, 2, 5, 6 |
| BH-8 | No direct test of a zero baseline | medium | patch: `test_a_baseline_of_zero_never_gives_an_unusual_week` (all three weeks 0, and a median of 0) |
| EC-4 | No test of a second level shift after the first | low | patch: `test_a_second_level_shift_follows_the_first_at_the_new_level` |
| BH-5, EC-1, VG-2 | The code indexes the weeks, so a generator fails, while the test says «any sequence» | low | patch: `tuple(weeks)` first, and a generator in the test |
| BH-7, EC-6 | The product test could be empty, and the guard covers only the listed examples | low | patch: the number of checked products must equal the products in the workbook; E11 and E29 are checked by the same filter and not listed by the spec |
| BH-9 | Hand-made histories carry E-n names, and FR-3 is not in the spec | low | patch: the docstrings say «as in E8» and so on; FR-3 stays, because the products test is its test |
| BH-10, EC-7 | The import test demands an exact set and repeats the AD-1 test | low | patch: a subset, and the docstring says why it is not a repeat (`test_core_imports.py` allows every standard-library module, the clock included) |
| VG-3 | The `len(run) == 3` check cannot fail | low | patch: removed, with a comment that a flagged week has 3 earlier valid weeks |
| BH-12 | The constants look configurable, and `last_updated` is a made-up time | low | patch: a comment that the rules fix them (AD-9); `last_updated` takes the time of the update. Rejected inside it: `__all__`, which no module of the project uses, and the quadratic rebuild of the baseline (EC-3) |
| BH-3 | `Week` is a `NamedTuple`, not a frozen dataclass, and can be built with swapped fields | low | reject: it is immutable like the reader's `Week`, and a later story builds it by keyword from `SalesWeek` |
| BH-4, EC-2 | No check of floats, `None` or negative units | low | reject: units come from integer columns and the validated seed, so the state cannot be reached, and a check adds a branch for it; the median of 3 whole numbers is a whole number |
| EC-3 | The baseline list is rebuilt for every week | low | reject: at most 104 weeks per product, and the loop reads as R-10 does |
| AA-1 | Not every test names an E-n and an FR-n | low | patch for `test_low_sales_are_never_flagged`, which named only R-10 and now names FR-16. Rejected for the rest: D-10 asks for an FR-n or an E-n, and a test that verifies no FR names its AD-n; the case and product tests carry their E-n in the test id |
| AA-2 | The valid positions are derived in the test, and E7's are written out, though the spreadsheet states a count | low | reject: R-1 defines the valid weeks as all but the stockout weeks, the matrix of the spec states E7's positions, and BH-6 and EC-5 asked for the check |
| AA-3 | The spec says `done` and `sprint-status.yaml` says `review` | false | step 5 of the build sets exactly this, as in Story 1.8: the sprint status reaches `done` with the merge |
| AA-4 | «commit følger» is still in the logs | false | the hashes are filled in with the commits, which is the first open point of the session log |
| BH-1, BH-2, EC-8, EC-9 | The spec says `in-review` and the tasks are open, and the documents and `sprint-status.yaml` are not in the diff | false | the documents are the last task, after the review, as in Story 1.8 (AA-5); the tasks are checked and the status set at the end |
| BH-11 | No evidence of the mutation test | false | the mutations and their results are in the Implementation Notes |
| VG-4 | A reviewer's mutation restore was once wrong | false | `weeks.py` was compared with the copy from before the review and was identical |

**Open points** (`issues.md`): none for this story beyond Stories 2.2 to 2.5, which use the result.

## Design Notes

`Week` is the core's own type, so the shell builds it from `SalesWeek` rows later and the core imports nothing from `reference/`; the tests convert the reader's weeks. The result holds tuples of positions, which Story 2.2 turns into calculation weeks.

## Verification

**Commands:**
- `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` -- expected: pass.
