---
title: 'Story 2.2: Calculate the base forecast with the moving average or exponential smoothing'
type: 'feature'
created: '2026-11-24'
status: 'done'
route: 'dispatch'
baseline_commit: 'a66efb466f434a03bcbbf0d0c544a55b05269983'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The core classifies weeks (Story 2.1) but cannot turn them into a number, so no screen can show a base forecast, and FR-5, FR-6 and FR-8 have no test against the reference spreadsheet.

**Approach:** Add `forecast_product(weeks, stock_on_hand, settings)` to the pure core. It picks the calculation weeks (R-2), calculates the base forecast by R-3 or R-4, or gives no forecast with a reason (R-6), and returns a frozen `ProductResult`. Test it against every base forecast the spreadsheet states. No screen, model or rounding change.

## Boundaries & Constraints

**Always:**
- Calculation weeks: the valid weeks in time order from `classify_weeks`, minus the unusual weeks when `unusual_weeks_included` is false. Level-shift weeks are never unusual, so they always stay; an excluded unusual week still counts as a valid week for R-6.
- R-3: the sum of the last N calculation weeks divided by N, skipping weeks that are not calculation weeks. R-4: the first calculation week is the start level, then level = α × sales + (1 − α) × previous level; the base forecast is the last level; skipped weeks are not zeros (E17). The result keeps the level of every calculation week (empty for the moving average).
- R-6: fewer than 3 valid weeks gives no forecast (checked first); then too few calculation weeks (fewer than the window, or none for exponential smoothing) gives no forecast. The reason is a code, and the result holds `required_calculation_weeks` (the window, or 1), never a sentence (AD-3, AD-4). With no forecast, `base_forecast` and the levels are empty.
- `ProductResult` is frozen, holds the settings used, the positions of the valid, unusual, level-shift and calculation weeks, the base forecast as a full-precision float or `None`, and the reason. No rounding, no formatted string, no clock, file or environment variable (AD-1, AD-2, AD-3).
- `ForecastSettings` is a frozen dataclass in `forecasting/settings.py` with method, window, smoothing factor and `unusual_weeks_included`, defaulting to the constants there (AD-9). The factor may be a `Decimal`; the core converts it with `float()`.
- The tests read the expected `calculation_weeks`, `levels` and `base_forecast` from `reference/reference-examples.xlsx` through `answer_key_reader`, for every case and rule test product that states one, within `TOLERANCE`. Each test names its E-n and FR-n (AD-17, DR-5).

**Never:**
- No order quantity, week forecast, scenario, warning, label or seasonal adjustment (Stories 2.3 to 2.5, Epic 5): `stock_on_hand` is accepted and not used yet; seasonal cases (E14) are not checked. No expected value copied into code. No model, migration, view, template or dependency. Do not change the spreadsheet or `weeks.py`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Moving average | E1: window 3 | 14.333 | N/A |
| Exponential smoothing | E2: α 0.3; E17: stockouts skipped | levels as stated; 13.790; 21.404 | N/A |
| Stockout weeks skipped | E7: 20, 22, S, S, 21, 23 | (22 + 21 + 23) / 3 = 22.0 | N/A |
| Unusual weeks, both settings | E8, E15, E18 b, E19 | included 41.0 / excluded 21.333, and so on | N/A |
| Level shift always kept | E9, E16 | 51.0 with either setting | N/A |
| Too few valid weeks | E11 a: 2 valid weeks | no forecast, reason fewer than 3 valid weeks | N/A |
| Too few calculation weeks | E11 b: window 12, 10 calculation weeks | no forecast, reason carries window 12 and 10 | N/A |
| Zero sales, trend lag | E23: 0, 0, 0; E28: 10 to 20 | 0.0 and 18.0, both forecasts | N/A |
| Unused input | other stock on hand | same result | N/A |

</frozen-after-approval>

## Code Map

- `src/forecasting/weeks.py` -- `Week`, `classify_weeks`, `WeekClassification`; reuse as is. Positions run from 1 (AD-8).
- `src/forecasting/settings.py` -- the FR-20 constants and `Range`; gets `ForecastSettings`, built from the same constants.
- `src/forecasting/forecast.py` (new) -- `ProductResult`, `forecast_product`; style of `weeks.py` (module docstring with FR, R and AD, plain functions, frozen dataclass).
- `tests/test_core_imports.py` -- already covers every file in `forecasting/`.
- `reference/answer_key_reader.py` -- `cases()`, `products()`, `Week`, `TOLERANCE`. 25 cases state a `base_forecast` (E11 a and b state «none»), 2 state `levels`, E11 b states `calculation_weeks`; 11 products state `base_forecast`. E14 has seasonal adjustment on and is left out. `tests/test_week_classification.py` shows the import style and the case filter.
- Documents: `docs/statustabell.md` (FR-5, FR-6, FR-8, FR-16, FR-17 rows), `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, `sprint-status.yaml`, `.logs/mounia-03/issues.md`.

## Tasks & Acceptance

**Execution:**
- [x] `src/forecasting/settings.py` -- add `ForecastSettings` -- AD-9
- [x] `src/forecasting/forecast.py` -- `ProductResult`, `forecast_product`, calculation weeks, R-3, R-4, R-6 -- FR-5, FR-6, FR-8, FR-16, FR-17
- [x] `tests/test_forecast.py` -- every matrix row, every stated spreadsheet value for the cases and the rule test products, a guard that the listed examples are covered, input not changed, frozen result -- FR-5, FR-6, FR-8
- [x] documents above, `sprint-status.yaml` to `review` -- DR-7

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check` and `uv run ruff format --check`, when they run locally and in CI, then they pass, and `makemigrations --check` finds no change.
- Given a mutation of `forecast.py` (stockout or unusual weeks counted in the wrong setting, level-shift weeks dropped, a stockout counted as 0 in R-4, α and 1 − α swapped, the first level not the first sales, the window off by one, the 3-valid-weeks check removed or run after the window check), when the tests run, then at least one fails.

## Implementation Notes

- 2026-11-24: built in the build session, not by a subagent, because the user approved subagents for the reviews only. The epic context already existed. Branch `story/2-2-calculate-the-base-forecast-with-the-moving-average-or-exponential-smoothing` from `a66efb4`.
- New: `src/forecasting/forecast.py` (`ProductResult`, `forecast_product`, the two reason codes) and `tests/test_forecast.py`; `ForecastSettings` added to `src/forecasting/settings.py`. `weeks.py` is unchanged.
- Spreadsheet-driven: 24 cases (E14 left out, as it has seasonal adjustment on) and 11 rule test products, plus direct tests for every matrix row. 443 tests after the review and the settings guard, 1 skipped (the Docker check, because Docker is not on the PATH of this shell). `makemigrations --check` finds no change.
- Mutations applied to `forecast.py` and then restored (the file was compared with the copy taken before and was identical), 55 in all after the settings guard, run by the build session and not by the reviewers: the setting inverted, always or never excluding unusual weeks, level-shift weeks dropped, all weeks used, the window off by one either way, the first N weeks, a swapped α, a start level of 0, the first week applied twice, the first level as forecast, stockout weeks as sales, the 3-valid-weeks limit at 2, at 4 or with `<=`, the window check with `<=` or skipped, the exponential smoothing asking for 2 weeks or the window, the reasons swapped, an unknown method taken for exponential smoothing, rounding, integer division, an unconverted `Decimal`, the stock on hand used, the weeks not turned into a tuple, positions from 0, the unusual, level-shift, settings and required-weeks fields left empty, the 3-valid-weeks check removed, levels filled for the moving average, and 19 on the settings guard (not called, called late, the method, window type, either end of the window or the factor moved or made strict, a `Decimal` compared with a float, and the window not checked for exponential smoothing). 54 were caught. The survivor is an equivalent mutant: the 3-valid-weeks check made on the calculation weeks. A history with 3 valid weeks always has at least 3 calculation weeks, because the first 3 valid weeks are never checked (R-10), so no input can tell the two checks apart.

- 2026-11-24, decision after the review: the core refuses a bad setting. Reasons for: `forecast_product` is public and the first caller after the form is the loader, so a window of 0 gave `ZeroDivisionError` and a negative window or a factor outside 0.1 to 0.9 gave a number that looks like a forecast, on a tool that suggests purchases; the ranges are read from `settings.py` (AD-9), so nothing is defined twice; and the guard is 20 lines in the function this story adds. Against: the form of Story 3.1 refuses the same values, which is why the finding was first rejected. The form keeps the user-facing message (Norwegian, previous value kept, AD-9), and the core fails loudly with an English `ValueError` as a guard that the user never meets. Not widened: no check of the number of decimals, of negative units, of `None` weeks or of `stock_on_hand`. Both ends of both ranges are accepted, a `Decimal` or a float factor is compared as a float, and the window is checked for both methods, because the settings belong together. The dead check for a bool was removed after a mutation showed it never matters (0 and 1 are below the smallest window). `ProductResult` is unchanged. The four reviewers were not run again on this change; the build session ran 19 new mutations and 28 new tests instead.

## Spec Change Log

## Review Triage Log

BMAD Code Review (2026-11-24): Blind Hunter (BH), Edge Case Hunter (EC), Verification Gap (VG) and Acceptance Auditor (AA), as four independent read-only subagents, on the working-tree diff from `a66efb4` (18.4 kB, 3 files, N = 5 for the Blind Hunter). The spec went to the Edge Case Hunter as the claims file and to the Acceptance Auditor. The first Verification Gap run had a mistyped diff path in its prompt, found the file through the fallback path and reported no gap in 40 seconds; it was repeated with the right path, read the 450-line diff, ran the tests and again found no gap, and made one observation (VG-1). The reviewers changed no file: the hashes of `src`, `tests`, `reference`, `docs` and the implementation artifacts were identical before and after. 23 findings: 14 patched, 7 rejected and 2 false. None was deferred. One decision went to the user: whether the core should refuse a bad window or factor (BH-1, EC-1 to EC-4, first rejected). The user asked for an assessment, and the answer was to patch it (see the Implementation Notes). The fixes are in the working tree and not yet committed.

| ID | Finding | Verdict | Route |
|---|---|---|---|
| BH-2, EC-7, EC-8, EC-10 | The count guards compare the reader with itself (`len(PRODUCTS) == len(<same filter>)`), so a dropped case or product goes unnoticed, though the docstring says it cannot | medium | patch: the only case left out must be E14, and every rule test product must be checked (`len(PRODUCTS) == len(reader.products())`) |
| BH-3, AA-2 | `LISTED_EXAMPLES` lacks E23 and the FR-21 variants that the docstring and the matrix name | low | patch: E23, FR-21 a and FR-21 b added |
| BH-6 | R-6 is tested at 3 valid weeks only for the moving average with window 3, and 2 valid weeks are not tested with a window that they would fill | medium | patch: window 2 in the 2-valid-weeks test, and exactly 3 valid weeks for window 2, window 3 and exponential smoothing. Rejected inside it: a mixed level-shift and excluded-unusual forecast, which E15 (excluded) already states |
| VG-1 | No test says that the moving average has no levels | low | patch: `levels == ()` in the 3-valid-weeks test |
| AA-1 | Not every test names an E-n and an FR-n | low | patch for the five tests that could name both. Rejected for `test_the_forecast_settings_start_at_the_fr_20_defaults`, which has no E-n, as in Story 2.1 |
| BH-1, EC-1, EC-2, EC-3, EC-4 | No check of window or smoothing factor against the FR-20 ranges, a non-integer window, or a bad setting that stays hidden when there is no forecast | medium | first rejected (the settings form of Story 3.1 refuses them); after the user asked for an assessment, patch: `check_settings` refuses a method, window or factor outside the definitions in `settings.py` before anything is calculated, for both methods and also when there is no forecast |
| EC-5, EC-6 | Negative units, `None` weeks or `None` settings | low | reject: units come from integer columns and the validated seed, and `None` settings is a programming error that fails loudly with a TypeError (as Story 2.1, EC-2) |
| BH-4 | Calculation weeks are compared by count only | low | reject: the base forecast and levels pin which weeks were used (a wrong selection of the right size changes the value in E8, E15 and E19), and the E8 and E16 tests state the positions |
| BH-5 | The reason of a no-forecast row is not checked in the spreadsheet helper | low | reject: the spreadsheet states no reason; E11 a and E11 b have their own tests for the reason and the numbers |
| BH-7 | A negative or `None` `stock_on_hand` is not defined | low | reject: it is not used until Story 2.4, which defines it |
| BH-8 | The reason is a bare string, not an Enum, and no invariant ties it to `base_forecast` | low | reject: `settings.py` and the reader use strings for methods and warnings, and a `__post_init__` adds a branch for a state the function cannot produce |
| BH-9 | O(n²) membership test, no annotations, method checked after the classification | low | reject: at most 104 weeks per product, `weeks.py` has no annotations either, and the early check changes nothing |
| EC-9 | Taking the last N valid weeks instead of calculation weeks is caught only by E8 and E19 | false | caught is not a gap: mutation «all weeks used» and the E8, E15 and E19 excluded cases fail |
| EC-11 | The «level-shift weeks dropped» mutation cannot be made in the filter | false | it was made (`and position not in classification.level_shift`) and caught by E9, E15 and E16 (excluded) |

**Open points** (`issues.md`): the settings form of Story 3.1 must give the user a Norwegian message before a bad value reaches the core, which now refuses it with a ValueError; the stock on hand is defined in Story 2.4.

## Design Notes

The result names its reason with a code and the numbers a sentence needs (`required_calculation_weeks`), so `explanation/` can write E11 a and E11 b without a calculation of its own (AD-4). It holds the settings used because AD-5 fills explanations from `ProductResult` alone.

## Verification

**Commands:**
- `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` -- expected: pass.
