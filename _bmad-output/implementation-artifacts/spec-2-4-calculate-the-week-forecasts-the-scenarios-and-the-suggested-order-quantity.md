---
title: 'Story 2.4: Calculate the week forecasts, the scenarios and the suggested order quantity'
type: 'feature'
created: '2026-11-24'
status: 'done'
route: 'dispatch'
baseline_commit: 'f30fc3c77aa588c9f7ef643e83bca8e7038ec883'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `forecast_product` stops at the base forecast: it has no week forecasts, no scenarios and no suggested order quantity, and `stock_on_hand` is accepted and ignored. Stories 2.5 to 2.9 have nothing to show or sort on, and the order test in `tests/test_rounding.py` still borrows its own formula.

**Approach:** Extend `ProductResult` with the week forecasts (R-5), the scenarios (R-7), the safety margin amount, the unrounded order result, the suggested order quantity (R-8, R-9) and the stock on hand (R-13), all numbers, and add a pure function that labels horizon weeks 1 to 3 from the latest data week (AD-8). No screen, model or migration change.

## Boundaries & Constraints

**Always:**
- Full float precision; the only rounding is `rounding.round_up_to_units`, once, at the end (AD-3). The order is `F1 × (1 + m/100) − S`, so E5 gives 70.00000000000001 and 70. The floor of 0 is in the core: `max(0, …)`.
- `scenario_percentage` and `safety_margin` are whole percents in `ForecastSettings`, with defaults and ranges read from `settings.py` (AD-9), and checked in `check_settings` like the window.
- Without seasonal adjustment, weeks 1, 2 and 3 equal the base forecast, and the result carries a flag for the FR-7 note. Scenarios are calculated for each of the three weeks; only week 1 feeds the order.
- `stock_on_hand` is a whole number of at least 0 (a bool, a float or a string is a `TypeError`, a negative number a `ValueError`). The result keeps it also when there is no forecast.
- A product without a forecast has `None` for the week forecasts, scenarios, margin amount, unrounded result and quantity, and no FR-7 flag.
- The horizon labels come from a pure function of the latest ISO year and week using `datetime.date.fromisocalendar` and no clock; it is the only calendar arithmetic in the core (AD-8). The labels are written by `display.week_label`.
- Every stated value (`week_forecasts`, `normal`, `optimistic`, `pessimistic`, `order_unrounded`, `suggested_order_quantity`) is read from `reference/reference-examples.xlsx` through `answer_key_reader`, within `TOLERANCE`; each test names its E-n and FR-n (AD-17).

**Never:**
- No seasonal adjustment (Epic 5), no scenario order quantities or weeks of cover (FR-13, FR-14), no warnings, notes or label wording (Story 2.5), no overview or sorting, no loader or view, no «–» or column label in `display.py` (they come with the first screen that shows them), no `round()`, no new dependency, model or migration.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Flat horizon | E1 (14.333), no seasonal adjustment | weeks 1, 2, 3 all 14.333; FR-7 flag set | N/A |
| Trend lag | E28: 10, 12, 14, 16, 18, 20, window 3 | forecast 18.0 in all three weeks, no warning | N/A |
| Scenarios | E3: 14.333, 10 % | 14.333 / 15.767 / 12.900 in each week | N/A |
| Scenario limits | week forecast 14.333 at 0 % and at 50 %; 0 at 50 % (E23) | all three equal at 0 %; pessimistic 7.167; 0, 0, 0 | N/A |
| Order | E4 (stock 5): 10.767; E5: 70.00000000000001; E6: −40; E21: 0.067 | 11; 70; 0; 1 | N/A |
| No forecast | fewer than 3 valid weeks | week forecasts, scenarios, amount, result, quantity `None`; stock kept | N/A |
| Zero forecast | E23: 0, 0, 0 | forecast, scenarios and quantity 0 | N/A |
| Horizon at year end | latest 2026 w52; 2026 w53; 2025 w52 | 2026 w53, 2027 w1, 2027 w2; 2027 w1, w2, w3; 2026 w1, w2, w3 | N/A |
| Bad inputs | stock −1, 2.5, «5», True; week 53 in a 52-week year | refused | `TypeError` or `ValueError`, naming the value |

</frozen-after-approval>

## Code Map

- `src/forecasting/forecast.py` -- `forecast_product` and `ProductResult` get the new fields; `check_settings` gets the two percentages; `stock_on_hand` is validated here.
- `src/forecasting/settings.py` -- `ForecastSettings` gets `scenario_percentage` and `safety_margin` from `SCENARIO_PERCENTAGE` and `SAFETY_MARGIN`.
- `src/forecasting/horizon.py` (new) -- `horizon_weeks(iso_year, iso_week)` gives three `(iso_year, iso_week)` pairs; style of `weeks.py`.
- `src/forecasting/rounding.py`, `display.py` -- used, not changed.
- `tests/test_forecast.py` -- case filter and helpers to reuse; `tests/test_rounding.py:44` -- `unrounded_order` is replaced by the core's `order_unrounded`.
- `tests/test_core_imports.py` -- already covers `horizon.py`.
- Documents: `docs/statustabell.md`, `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, `sprint-status.yaml`, `.logs/mounia-03/issues.md` (the 2.4 point of 2026-11-24 is closed or moved).

## Tasks & Acceptance

**Execution:**
- [x] `src/forecasting/settings.py` -- the two percentages on `ForecastSettings` -- AD-9, FR-20
- [x] `src/forecasting/forecast.py` -- week forecasts, scenarios, margin amount, unrounded result, quantity, stock, FR-7 flag; checks of the percentages and the stock -- R-5, R-7, R-8, R-13
- [x] `src/forecasting/horizon.py` -- the three labelled weeks -- AD-8
- [x] `tests/test_week_forecasts.py`, `tests/test_horizon.py`, `tests/test_rounding.py` -- every matrix row, every stated spreadsheet value, a guard that the listed examples are all checked, the stand-in formula replaced -- FR-7, FR-10, FR-11, FR-12, E3 to E6, E21, E23, E28
- [x] documents above, `sprint-status.yaml` to `review` -- DR-7

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check` and `uv run ruff format --check`, when they run locally and in CI, then they pass, and `makemigrations --check` finds no change.
- Given a mutation of the new code (the floor of 0 on the order removed, `1 − s` for `1 + s`, the margin on the wrong week, rounding before the 6 decimals, a week offset of 0, the year dropped at week 53), when the tests run, then at least one fails.

## Implementation Notes

- 2026-11-24: built in the build session, not by a subagent, because the user approved subagents for the reviews only. The epic context was valid. Branch `story/2-4-calculate-the-week-forecasts-the-scenarios-and-the-suggested-order-quantity` from `f30fc3c`.
- New: `src/forecasting/horizon.py`, `tests/test_week_forecasts.py`, `tests/test_horizon.py`; changed: `src/forecasting/forecast.py` (`ProductResult`, `WeekScenarios`, `scenarios_of`, `check_stock_on_hand`, the percentage checks), `src/forecasting/settings.py`, `tests/test_forecast.py` (the stock test no longer compares whole results), `tests/test_rounding.py` (the borrowed order formula is replaced by the core's `order_unrounded`). No model, migration, dependency, template or display change. 714 tests, 1 skipped (the Docker check). `makemigrations --check` finds no change.
- Spreadsheet-driven: every case without seasonal adjustment that states `normal`, `optimistic`, `pessimistic`, `order_unrounded` or `suggested_order_quantity` (E3, E4, E5, E6, E21, E23, E24 A and B, FR-21 c and d), and E1 and E28 for the flat horizon, the scenario limits and the trend lag. The spreadsheet states `week_forecasts` only for the seasonal E14, E25 and E26, which are Epic 5.
- Mutations applied to the new files and restored (compared byte for byte): 33 before the review and 36 after it (the second run replaced the check of the horizon types and added the error paths), all caught by the tests. The mutation «the margin on the wrong week» of the acceptance criteria is an equivalent mutant until Epic 5: without seasonal adjustment the three week forecasts are equal, so the code cannot tell week 1 from week 3. The test that was named for it now says what it shows.
- Decisions as in the Design Notes, confirmed by the user when approving the spec. `horizon_weeks` is called by no screen yet; the loader (Story 2.6 on) passes the latest ISO year and week from the sales weeks, and Stories 2.7 to 2.9 write the labels through `display.week_label`.
- Process slip, found by the review: a scripted edit of `tests/test_rounding.py` removed the guard `test_the_spreadsheet_examples_for_rounding_are_all_checked` together with the old formula. Four reviewers found it; it is restored.

## Spec Change Log

## Review Triage Log

BMAD Code Review (2026-11-24): Blind Hunter (BH), Edge Case Hunter (EC), Verification Gap (VG) and Acceptance Auditor (AA), as four independent read-only subagents, on the working-tree diff of `src` and `tests` from `f30fc3c` (31.0 kB, 7 files, N = 6 for the Blind Hunter). The spec went to the Edge Case Hunter as the claims file and to the Acceptance Auditor, and the other two never saw it. The reviewers changed no file: the hash of `src`, `tests`, `reference`, `docs`, `.logs` and the implementation artifacts was identical before and after. 36 findings (BH 10, EC 13, VG 1 gap and 3 other findings, AA 9), in 18 groups: 8 patched and 10 rejected. None was deferred, and none went to the user.

| ID | Finding | Verdict | Route |
|---|---|---|---|
| BH-1, EC-9, VG-1 (and its dead constants), AA-1 | `test_the_spreadsheet_examples_for_rounding_are_all_checked` was deleted by the scripted edit, and nothing guards the shown-value cases (E1, E2, E13, E20, E27) | medium | patch: the test is restored |
| BH-8, EC-6, EC-7, AA-5 | `horizon_weeks` names no value in the stdlib errors, leans on `fromisocalendar` for the type check, and raises `OverflowError` at 9999 week 52 | medium | patch: an explicit type check, one `ValueError` that names the year and week, tests with `match` and 9999 |
| EC-12, AA-3, AA-4 | The matrix rows «Flat horizon» and «Scenario limits» use hand-made sales and not E1 and its 14.333, 7.167 at 50 % | medium | patch: both tests read E1 from the spreadsheet |
| AA-6 | The second way to no forecast (too few calculation weeks) has no test of the new fields | low | patch: a test with window 12 |
| BH-9 (two parts) | A bad percentage for a product without a forecast is untested, and the no-clock test asserts `HORIZON_WEEKS == 3` | low | patch: a test for both percentages, the unrelated assertion removed |
| BH-7 | `check_stock_on_hand` says «positive integer» although 0 is accepted, and its message reads «not below 0» | low | patch: «at least 0» |
| EC-11, AA-2, VG (other) | The mutation «the margin on the wrong week» cannot fail a test, and `test_only_week_1_feeds_the_order...` proves only a zero forecast | low | patch: the test is renamed to what it shows; the criterion is an equivalent mutant until Epic 5 (Implementation Notes) |
| BH-10 (readability) | Two chained comparisons are hard to read | low | patch: plain asserts |
| BH-2 | `test_rounding.py` no longer rounds an order it calculates itself | low | reject: Story 2.3 left it to this story («Story 2.4 replaces it»); the spreadsheet's `order_unrounded` and quantities still check the core |
| BH-3, EC-5 | Percentages raise `ValueError` and the stock `TypeError` | low | reject: the settings follow the window's convention (`ValueError`, Story 2.2 tests), and the stock follows `rounding.py` (`TypeError` for a wrong type); both name the value |
| BH-4 | `horizon_weeks` is not called by the result | low | reject: decision 1 of the spec, confirmed at the checkpoint (AD-2 fixes the signature, the weeks carry no dates) |
| BH-5, EC-8 | `weeks_repeat_week_1` is true whenever there is a forecast | low | reject: there is no seasonal setting before Epic 5, and the code comment says so; Epic 5 changes this line |
| BH-6, EC-4 | The percentages and the stock refuse a `Decimal` | low | reject: the model fields are integer columns (`PositiveSmallIntegerField`, `PositiveIntegerField`), so the loader gets `int` |
| EC-1, EC-2, EC-3 | Negative units, a stock above 2**53 and sales so large that the order is infinite | low | reject: the columns and the seed check (AD-8, Story 1.7) keep units and stock to whole numbers within 32 bits, and the case cannot be reached |
| EC-10 | `week_forecasts` is not among the compared columns | low | reject: the spreadsheet states it only for seasonal cases, which are Epic 5 (checked by listing the columns) |
| EC-13, AA-9 | The documents and `sprint-status.yaml` are not in the diff | low | reject: the documents task comes after the review, as in Stories 2.2 and 2.3, and `sprint-status.yaml` is the build step's sync |
| BH-10 (helpers), AA-7, AA-8, VG (ast observation) | Test helpers are copied, `scenarios_of` and `check_stock_on_hand` are public, `forecast.py` imports `HORIZON_WEEKS`, and the no-clock test reads the source | low | reject: each test file keeps its own helpers as the others do, the checks sit beside `check_settings`, the import stays inside the core, and the source check is the convention guard of Story 2.3 |

**Open points** (`issues.md`): Story 2.5 replaces the flag by the note and the warnings; Stories 2.6 to 2.9 pass the latest ISO year and week to `horizon_weeks`; Story 2.7 defines «–» and the column label «Uke 1 · uke 46» in `display.py` (moved from Story 2.4); Epic 5 changes `weeks_repeat_week_1` and the week-1-only order, so that the mutation of the wrong week can be tested.

## Design Notes

Decisions made without the user, to confirm at the checkpoint: (1) the horizon labels are a separate function and not a new parameter of `forecast_product`, because AD-2 fixes its signature and the weeks carry no dates; the loader (Story 2.6 on) passes the latest ISO year and week; (2) «–» and the column label «Uke 1 · uke 46» wait for the first screen, not this story, which moves the 2.4 point of `issues.md`; (3) the FR-7 marker is one boolean on the result, the sentence is Story 2.5's; (4) the unrounded order result keeps its sign, so E6 gives −40 and shows «−40,00».
