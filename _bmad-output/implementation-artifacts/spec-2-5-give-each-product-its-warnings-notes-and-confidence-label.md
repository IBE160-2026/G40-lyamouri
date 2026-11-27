---
title: 'Story 2.5: Give each product its warnings, notes and confidence label'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: 'b27a277a7d4d78527269fe998c9d17dd9fd92f86'
route: 'dispatch'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `ProductResult` has the weeks, the forecast and the order quantity, but no active warnings, no notes and no confidence label, and only a boolean flag for the FR-7 note. Stories 2.6 to 2.9 have nothing to sort, show or explain trust with, and SM-7 and SM-10 cannot be checked.

**Approach:** A pure module `forecasting/trust.py` finds the active warnings (R-15), the notes and the confidence label with its deciding condition (R-16), and `forecast_product` puts them on `ProductResult` as codes and numbers. `explanation/` writes every text from the Message Catalogue (AD-4). No screen, model or migration change.

## Boundaries & Constraints

**Always:**
- Codes, not text, in the core: warnings are `stockout_weeks`, `unusual_weeks`, `level_shift`, `old_data`, `insufficient_data` in R-15 order (the names of the spreadsheet); the label is `lav`, `middels` or `høy`; the deciding condition is a code of its own. Counts and positions come from the result (AD-5).
- The recent period is the last 12 positions of the sales history, stockout weeks included, or the whole history when it is shorter. Stockout, unusual and level-shift weeks count only in it; the unusual-weeks warning does not read `unusual_weeks_included` (FR-16).
- Old data: the latest valid week is more than 8 positions before the last position (E12: 9 gives it, 8 does not). A product with no valid week has no latest valid week and no old-data warning. Insufficient data is active whenever there is no forecast, whatever the reason.
- R-16, first condition wins: no forecast or fewer than 12 valid weeks gives «lav»; an active warning, a history shorter than 104 weeks (stockout weeks counted) or fewer than 100 valid weeks gives «middels»; else «høy». The no-forecast reasons are told apart (few weeks, window).
- `weeks_repeat_week_1` is replaced by `notes`, holding the FR-7 code when there is a forecast; the other notes belong to Stories 5.1, 6.x and 8.x.
- The reason is «[Label]: [deciding condition].» followed by one sentence for each other active warning, in R-15 order. The warning that a condition names (insufficient data for «lav» without a forecast) is not repeated. The texts for stockout, unusual, old-data and insufficient-data warnings, the list texts, the FR-7 note and the reason are written by `explanation/` and follow the Message Catalogue word for word; week numbers and numbers go through `display.py`, and week labels come from the latest ISO year and week through one pure function in `horizon.py`, the only calendar arithmetic (AD-8).
- Decided by the user on 2026-11-27: old data in the reason is «gamle data, 9 uker siden siste gyldige uke» (alone: «Middels: gamle data, 9 uker siden siste gyldige uke.»; after another warning the sentence «Gamle data, 9 uker siden siste gyldige uke.»); recent-period warnings are one phrase before «de siste 12 ukene», in R-15 order, joined by commas and «og» («2 utsolgte uker, 1 uvanlig uke og nytt nivå de siste 12 ukene»). The phrase is in the Message Catalogue (`EXPERIENCE.md` reason row and change-log row of 2026-11-27, `hash følger`), so the catalogue and `explanation/` agree.
- Every stated value (`warnings`, `confidence_label`, `weeks_since_latest_valid`) is read from `reference/reference-examples.xlsx` through `answer_key_reader`, for the cases and the rule test products; each test names its E-n and FR-n (AD-17). Seed products are run through the core for SM-7 and SM-10.

**Never:**
- No screen, loader, overview, sorting or chart; no FR-17b, FR-36 or seasonal wording (Should); no overstock or stock-not-lasting note; no change to the seed files, models or dependencies; no `round()` and no formatting outside `display.py`; `forecasting/` never imports `explanation/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Old data | E12: latest valid week 9 vs 8 positions back | `old_data` with 9, none with 8; stockout warning in both | N/A |
| Old period | stockout or unusual week before the recent period | not a warning | N/A |
| Setting flip | E8 included vs excluded | same `unusual_weeks` warning in both | N/A |
| No forecast, few weeks | E11 a (2 valid weeks) | `stockout_weeks`, `insufficient_data`; «lav» | N/A |
| No forecast, window | E11 b = E29 e | `unusual_weeks`, `insufficient_data`; «lav»; «Lav: ingen prognose, færre uker enn vinduet.» then the unusual-weeks sentence | N/A |
| Labels | E29 a to g | lav, middels, høy, middels, lav, høy, middels | N/A |
| Short history, warning | warning and history under 104 weeks | the warning decides; the short history is not named | N/A |
| Level shift | E9 | `level_shift`, reason «nytt nivå de siste 12 ukene», no warning text (FR-17b) | N/A |
| Empty history | no weeks | `insufficient_data`, «lav», no old-data warning | N/A |

</frozen-after-approval>

## Code Map

- `src/forecasting/forecast.py` -- `ProductResult` gets `history_length`, `warnings`, `notes`, `confidence_label`, `confidence_condition`, `weeks_since_latest_valid`, `recent_stockout_weeks`, `recent_unusual_weeks`, `recent_unusual_units`, `recent_level_shift_weeks`; `weeks_repeat_week_1` goes. Reuse `classification`, `calculation_weeks`, `reason`.
- `src/forecasting/trust.py` (new) -- `RECENT_WEEKS = 12`, `OLD_DATA_WEEKS = 8`, `HISTORY_WEEKS = 104`, `VALID_WEEKS_HIGH = 100`, `VALID_WEEKS_MIDDELS = 12`; `recent_positions`, `active_warnings`, `confidence`; style of `weeks.py`.
- `src/forecasting/horizon.py` -- add `week_at_position(position, history_length, iso_year, iso_week)` beside `horizon_weeks`, with the same checks.
- `src/explanation/trust.py` (new) -- `warning_texts`, `list_text`, `note_texts`, `confidence_reason`; imports `forecasting.display` and `forecasting.horizon`.
- `src/forecasting/display.py` -- used (`axis_week_label`, `whole_number`), not changed; `rounding.py`, `weeks.py`, `settings.py` unchanged.
- `tests/test_trust.py`, `tests/test_trust_texts.py`, `tests/test_trust_seed.py` (new); `tests/test_week_forecasts.py` -- the flag assertions; `tests/test_core_imports.py` already covers the new modules.
- `data/seed/*` -- read only; products 10040 (few weeks), 20015 (old data), 10001 (høy) already cover SM-7 and SM-10.
- `_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/EXPERIENCE.md` -- changed before the build (reason row, change-log row); `epic-2-context.md` recompiled. Fill in the commit hash of the change-log row after the commit.
- Documents: `docs/statustabell.md`, `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, `sprint-status.yaml`, `.logs/mounia-03/issues.md` (the 2.2 and 2.4 points for Story 2.5 are closed).

## Tasks & Acceptance

**Execution:**
- [x] `src/forecasting/trust.py`, `src/forecasting/forecast.py`, `src/forecasting/horizon.py` -- the warnings, the notes, the label and its condition, `week_at_position`; the flag replaced -- R-15, R-16, FR-7, FR-8, FR-15 to FR-19
- [x] `src/explanation/trust.py` -- the Message Catalogue texts, the snapshots for the window case and for a warning with a short history -- AD-4, UX-DR40
- [x] `tests/test_trust.py`, `tests/test_trust_texts.py`, `tests/test_trust_seed.py`, `tests/test_week_forecasts.py` -- every matrix row, E11, E12, E28, E29 a to g and the rule test products from the spreadsheet, every warning and label from the seed products -- E11, E12, E29, SM-7, SM-10
- [x] documents above, `sprint-status.yaml` to `review` -- DR-7

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check` and `uv run ruff format --check`, when they run locally and in CI, then they pass, and `makemigrations --check` finds no change.
- Given mutations of the new code (the recent period 11 or 13 weeks, old data at 8 or 10, the condition order of R-16 swapped, 104 or 100 off by one, the unusual-weeks warning reading the setting), when the tests run, then each one fails at least one test.

## Implementation Notes

- 2026-11-27: built in the build session, not by a subagent, because the user approved subagents for the reviews only. The epic context was recompiled after the user approved the catalogue change (`EXPERIENCE.md` reason row and change-log row of 2026-11-27; the hash of that row follows the commit). Branch `story/2-5-give-each-product-its-warnings-notes-and-confidence-label` from `b27a277`.
- New: `src/forecasting/trust.py`, `src/explanation/trust.py`, `tests/test_trust.py`, `tests/test_trust_texts.py`, `tests/test_trust_seed.py`; changed: `src/forecasting/forecast.py` (`ProductResult` has `history_length`, `warnings`, `notes`, `confidence_label`, `confidence_condition`, `weeks_since_latest_valid` and the `recent_` fields; `weeks_repeat_week_1` is replaced by `notes`), `src/forecasting/horizon.py` (`week_at_position`), `tests/test_horizon.py`, `tests/test_week_forecasts.py`. No model, migration, dependency, template, seed or display change. 877 tests, 1 skipped (the Docker check). `makemigrations --check` finds no change.
- Spreadsheet-driven: every case that states `warnings`, `confidence_label` or `weeks_since_latest_valid` without the Should seasonal pattern (E11 a and b, E12, E28, E29 a to g; E30 is Should) and every rule test product (11). The seed products give all five warnings and all three labels (SM-7) and the «lav» for too few valid weeks (SM-10); no seed product has the conditions «fewer calculation weeks than the window» or «fewer than 100 valid weeks without a warning», which E11 b and E29 g cover.
- Mutations applied to the new files and restored (compared byte for byte): 42 before the review and 45 after it, all caught. The first run left one alive (R-16 counting calculation weeks and not valid weeks); `test_excluded_unusual_weeks_still_count_as_valid_weeks_for_the_label` catches it.
- Decisions as in the Design Notes and the frozen block. Two review findings went to the user, who decided on 2026-11-27: the stand-alone phrase «Middels: gamle data, 9 uker siden siste gyldige uke.» cannot occur, because old data means at least 9 of the last 12 weeks are sold out and the stockout phrase comes first, so `EXPERIENCE.md` marks it as a guard case and the code keeps it, tested on a built result; and the singular «Produktet har 1 gyldig uke.» (and the zero case) is now in the catalogue. `test_the_catalogue_has_the_singular_and_marks_the_old_data_phrase_as_a_guard_case` reads the catalogue, so the two cannot drift apart.
- The mutation script first left a stale `.pyc` (a same-length mutation and its restore within one second), found when a plain test run failed after the review; all 45 mutations were rerun with bytecode off and `__pycache__` cleared, and all were caught.
- Process notes: one of four reviewer prompts had a typo in the diff path; it was corrected by a message before the reviewer reported. The reviewers changed nothing: the hash of all tracked and untracked files was identical before and after.

## Spec Change Log

## Review Triage Log

BMAD Code Review (2026-11-27): Blind Hunter (BH, N = 9), Edge Case Hunter (EC), Verification Gap (VG) and Acceptance Auditor (AA), as four independent read-only subagents, on the diff of `src`, `tests` and the `EXPERIENCE.md` change from `b27a277` (65.5 kB). The spec went to the Edge Case Hunter as the claims file and to the Acceptance Auditor, and the other two never saw it. 26 findings (BH 12, EC 6, VG 0, AA 8), in 20 groups: 8 patched, 2 decided by the user and made into changes of the catalogue (BH-1, AA-5) and 10 rejected. None was deferred, and none was an intent gap that stopped the build.

| ID | Finding | Verdict | Route |
|---|---|---|---|
| BH-3, EC-4 | `warning_texts` and `note_texts` skip any code without a text, so a new warning or note is left out silently | low | patch: only the level shift is skipped; any other code is a `KeyError`; tested |
| BH-4, EC-1 | `_condition_phrase` falls through to the «Høy» text for an unknown condition | low | patch: `ALL_CLEAR` is explicit and any other code is a `ValueError`; tested |
| BH-6, EC-3 | `_insufficient_data_text` falls through to the «Glidende gjennomsnitt» text for any other reason | low | patch: the window text needs `TOO_FEW_CALCULATION_WEEKS`, any other reason is a `ValueError`; tested |
| BH-7, AA-8 (part) | The seed test says every deciding condition is covered, but asserts five of seven | low | patch: the docstring says which two the spreadsheet covers |
| BH-8, AA-4 | E7 is loaded as «E29 a» with 22.0 and 25 written in the test, and E8's weeks and units are typed in | low | patch: the tests read E7's `base_forecast` and E8's `unusual_weeks` from the spreadsheet, and compare the order with the same history without the stockout weeks. The constant asserts that restate 8, 12, 104 and 100 stay: they pin the numbers of the rules |
| BH-9 | The short-history test shows no warning inside a history of fewer than 12 weeks | low | patch: a stockout in a 5-week history is an active warning; `recent_positions(0)` is empty |
| BH-10 | Gaps: 0 weeks since the latest valid week, the sentence «Nytt nivå …» after another condition | low | patch: two tests. Rejected parts: the `ValueError` of `week_at_position` through the texts (the horizon tests cover it), a year-crossing list of unusual weeks (the same helper as for stockout weeks), and old data with unusual weeks and a level shift (each phrase has its own test) |
| BH-12 | Two long docstring lines and a badly wrapped paragraph | low | patch: reflowed. Rejected parts: the seed test reads the files at import like the spreadsheet tests, ids that repeat get a suffix from pytest, and `generate_seed.monday_of` is used by `test_seed_data.py` too |
| BH-1 | The stand-alone old-data example in the catalogue cannot occur, since old data means at least 9 sold-out weeks among the last 12 | low | decided by the user (2026-11-27): the catalogue marks the phrase as a guard case, and the code keeps it; a test reads the catalogue |
| BH-2, AA-2 | The change-log row has `hash følger` | low | reject: the Code Map says to fill it in after the commit, as for Story 1.8 |
| BH-5, EC-2 | `warning_phrases[0]` is an `IndexError` if the condition is an active warning with no phrase | low | reject: `confidence()` gives that condition only with a recent or old-data warning, and every seed product builds its reason in `test_every_product_has_its_texts_and_they_match_its_result` |
| BH-11 | `weeks_repeat_week_1` is replaced by `notes` without a note | low | reject: the 2.4 open point asks for it, nothing else reads the flag, and `ProductResult` is built only in `forecast_product` |
| AA-1 | The document task is not done | low | reject: it comes after the review, as in Stories 2.2 to 2.4 (done below) |
| AA-3 | The constant names differ from the Code Map | low | reject: the fix edits this spec; the values are right |
| AA-5 | «1 gyldig uke» is not in the catalogue | low | decided by the user (2026-11-27): the singular «Produktet har [1] gyldig uke.» and the zero case are in the catalogue; a test reads the catalogue |
| AA-6 | The «snapshots» are string assertions | false | the epic's criterion is met by exact strings, as in Story 2.4 |
| AA-7 | The mutations are not in the diff | low | reject: they are run by the build session and recorded in the Implementation Notes and the QA log |
| AA-8 (part) | The seed coverage cannot be verified | false | `test_every_warning_is_triggered_by_at_least_one_test_product` passes: level shift 10004, 20003, old data 20015 |
| EC-5 | `list_text` has no text for an unknown reason | low | reject: only two reasons exist (`forecast.py`), and a forecast is `None` only with one |
| EC-6 | «de siste 12 ukene» for a history shorter than 12 weeks | false | the recent period is the last 12 weeks, so the weeks of a short history are among them, and the catalogue fixes the phrase |

**Open points** (`issues.md`): Story 2.7 shows the texts and the notes; Stories 2.6 to 2.9 pass the latest ISO year and week to `warning_texts`; FR-17b and FR-36 add their texts, and `warning_texts` fails until they do; Epic 5 changes the note; the hash of the change-log row.

## Design Notes

Decisions made without the user, to confirm at the checkpoint: (1) the rules sit in `forecasting/trust.py` and run inside `forecast_product`, because AD-2 has one compute path and nothing is stored; (2) the result carries the recent positions and the units of the recent unusual weeks, so no text needs the sales history; (3) the notes are a tuple of codes with one entry today; (4) lists of 3 or more weeks read «38, 39 og 40»; (5) the «lav» reason by a window or few weeks wins over «færre enn 12 gyldige uker» when there is no forecast; (6) a week list at New Year shows «52 og 1/2027» through `axis_week_label`.

Golden reasons: «Middels: 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene.» · «Lav: ingen prognose, færre uker enn vinduet. 2 uvanlige uker de siste 12 ukene.» · «Høy: minst 104 uker salgshistorikk, minst 100 gyldige uker og ingen varsler.»

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check` -- expected: clean
- `uv run python src/manage.py makemigrations --check` -- expected: no changes
