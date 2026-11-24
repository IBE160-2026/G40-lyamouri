---
title: 'Story 2.3: Round and format every number the same way'
type: 'feature'
created: '2026-11-24'
status: 'done'
route: 'dispatch'
baseline_commit: '1e213d4660d08a20d2d815f9049d28e5259e0fb8'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Nothing rounds or formats a number yet, so Story 2.4 and every screen after it would each choose their own rounding and write «14.3» next to «14,3», or 70 next to 71 (E5). The stock on hand in `products.html` is printed raw, and `display.py` has only the header week label.

**Approach:** Add `forecasting/rounding.py` (R-9, `decimal`, never `round()`), extend `forecasting/display.py` with the Norwegian number formats and week labels (NFR-5, UX-DR42), and add one template-filter module that only calls them. The stock column of the product list uses the filter. No model, migration or forecast change.

## Boundaries & Constraints

**Always:**
- Every rounding first rounds to 6 decimals, then either up to whole units (R-8) or half away from zero for display (R-9). Both use `Decimal` built from the float's exact value, so 70.00000000000001 gives 70 and 10.25 gives 10,3. The core still returns numbers only (AD-3).
- Display decimals follow R-9: one decimal for forecasts, scenarios, weeks of cover and the safety margin amount; two for the unrounded order result (E21 «0,07»); none for order quantities and percentages. Seasonal decimals stay for Epic 5, through the generic function.
- Format: decimal comma, minus sign U+2212, no thousands grouping, no-break space (U+00A0) before «%». A value that rounds to zero has no minus sign.
- Week labels take an ISO year and week: «uke 46» in lists, «uke 10/2025» when the list reaches before the recent period, and the year on ISO week 1 in both forms; chart axes use the bare number («46», «1/2027»). `header_week_label` is unchanged.
- The filters live in one module, `web/templatetags/prognose.py`, take a number and call `display` only. `products.html` shows the stock through the whole-number filter.
- Tests read every stated value (`*_shown`, `suggested_order_quantity`) from `reference/reference-examples.xlsx` through `answer_key_reader`, within `TOLERANCE` where numeric, and name their E-n and NFR-5 or AD-3 (AD-17).

**Never:**
- No order quantity, week forecast, scenario or weeks-of-cover calculation (Story 2.4). «–» for a missing value and the column label «Uke 1 · uke 46» come with their values in Stories 2.4 to 2.7. No calendar arithmetic. No `round()`, `floatformat`, `intcomma` or `localize`, in `src` or a template. No new dependency, model or migration.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Round up once | E5: 100 × 1.1 − 40 = 70.00000000000001 | 70, not 71 | N/A |
| Round up, a real remainder | E21: 27.333 × 1.1 − 30 = 0.067 | 1 | N/A |
| Half away from zero | E20: 10.25; 0.285; −0.25 | «10,3»; 2 decimals «0,29»; «−0,3» | N/A |
| Display, stated values | E1 14.333, E2 13.79, E13 0.349 and 1.5, E27 0.455, E21 0.067 | «14,3», «13,8», «0,3», «1,5», «0,5», «0,07» | N/A |
| Sign and zero | −40; −0.04 at one decimal | «−40,00» at two decimals; «0,0» | N/A |
| Percent, whole | 10; 12.5 | «10 %» (U+00A0); «13 %» | N/A |
| Week labels | 2026 w46; 2027 w1; 2025 w10 in a long list | «uke 46»; «uke 1/2027»; «uke 10/2025»; axes «46», «1/2027» | N/A |
| Not a number | NaN, infinity | refused | `ValueError` |
| Stock in the list | stock 5 | `<td class="number">5</td>`, same as before | N/A |

</frozen-after-approval>

## Code Map

- `src/forecasting/display.py` -- holds `header_week_label` only; gets the number formats and week labels. Tests: `tests/test_forecasting_display.py`.
- `src/forecasting/rounding.py` (new) -- `round_up_to_units`, `round_for_display`; style of `weeks.py` (module docstring with R, AD).
- `src/web/templatetags/prognose.py` (new, with `__init__.py`) -- the filters; `web` is already in `INSTALLED_APPS`.
- `src/web/templates/web/products.html:20` -- `{{ product.stock_on_hand }}` becomes the filter; `tests/test_product_overview.py` must still pass.
- `reference/answer_key_reader.py` -- `cases()`; stated shown values: E1, E2, E13 (two), E20, E21, E27; E23 states «–» and is left for Story 2.4. E5, E21 and the other cases that state both a base forecast and `suggested_order_quantity` give the round-up values. `tests/test_forecast.py` shows the import and case-filter style; Story 2.2's `forecast_product` supplies the base forecasts.
- `tests/test_core_imports.py` -- already covers every file in `forecasting/`.
- Documents: `docs/statustabell.md`, `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, `sprint-status.yaml`, `.logs/mounia-03/issues.md` (the 2026-11-23 point on Story 2.3 is closed).

## Tasks & Acceptance

**Execution:**
- [x] `src/forecasting/rounding.py` -- both roundings with `decimal` -- AD-3, R-9
- [x] `src/forecasting/display.py` -- `format_number`, one and two decimals, whole number, percent, week and axis labels -- NFR-5, UX-DR42
- [x] `src/web/templatetags/prognose.py`, `products.html` -- number filters, stock through the filter -- AD-3
- [x] `tests/test_rounding.py`, `tests/test_forecasting_display.py`, `tests/test_number_filters.py` -- every matrix row, the stated spreadsheet values, a guard that they are all checked -- R-9, NFR-5
- [x] `tests/test_no_formatting_outside_the_core.py` -- no `round()` call or Django number filter in `src` or the templates, `quantize` only in `rounding.py` -- AD-2, AD-3
- [x] documents above, `sprint-status.yaml` to `review` -- DR-7

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check` and `uv run ruff format --check`, when they run locally and in CI, then they pass, and `makemigrations --check` finds no change.
- Given a mutation of the new code (the 6-decimal step removed, `ROUND_HALF_EVEN`, the round-up before the 6 decimals, a hyphen for U+2212, a point for the comma, a normal space before «%», the year dropped at week 1), when the tests run, then at least one fails.

## Implementation Notes

- 2026-11-24: built in the build session, not by a subagent, because the user approved subagents for the reviews only. The epic context already existed. Branch `story/2-3-round-and-format-every-number-the-same-way` from `1e213d4`.
- New: `src/forecasting/rounding.py`, `src/web/templatetags/prognose.py` (with `__init__.py`), `tests/test_rounding.py`, `tests/test_number_filters.py`, `tests/test_no_formatting_outside_the_core.py`; changed: `src/forecasting/display.py`, `src/web/templates/web/products.html`, `tests/test_forecasting_display.py`. No model, migration, dependency or forecast change. 641 tests, 1 skipped (the Docker check, because Docker is not on the PATH of this shell). `makemigrations --check` finds no change.
- Spreadsheet-driven: every case that states `suggested_order_quantity` with seasonal adjustment off (E4, E5, E6, E21, E23, E24 A and B, FR-21 d) and every stated `*_shown` value (E1, E2, E13 a and b, E20, E21, E27) are read through `answer_key_reader`; E23's «–» is left for Story 2.4. The core's own full-precision base forecast gives E1, E2 and E20 their shown values. The stand-in order formula in the test reproduces E5's 70.00000000000001 and is checked against the stated `order_unrounded` where there is one.
- Mutations applied to the new files and then restored (compared byte for byte with the copies taken before), run by the build session and not by the reviewers: 54 before the review (18 in `rounding.py`, 28 in `display.py`, 5 in the filters, 3 in `products.html`) and 5 on the input checks plus 6 injected violations for the guard after it. All 65 were caught.
- Decision after the review: `rounding.py` refuses what is no number: `None`, a string or a bool is a `TypeError`, and NaN, infinity or a value too large for `decimal` is a `ValueError`, both naming the value. This follows the matrix row «Not a number», and a string «70» would otherwise print unrounded through a filter.

## Spec Change Log

## Review Triage Log

BMAD Code Review (2026-11-24): Blind Hunter (BH), Edge Case Hunter (EC), Verification Gap (VG) and Acceptance Auditor (AA), as four independent read-only subagents, on the working-tree diff of `src` and `tests` from `1e213d4` (24.1 kB, 9 files, N = 5 for the Blind Hunter). The spec went to the Edge Case Hunter as the claims file and to the Acceptance Auditor, and the other two never saw it. The reviewers changed no file: the hashes of `src`, `tests`, `reference`, `docs`, `.logs` and the implementation artifacts were identical before and after. 34 findings (BH 8, EC 18, VG 3 other findings and no gap, AA 5), in 14 groups: 7 patched and 7 rejected. None was deferred, and none went to the user. The fixes are in commit `92da6bf`, in PR #31.

| ID | Finding | Verdict | Route |
|---|---|---|---|
| BH-5, EC-1, EC-2, EC-17, VG-2, VG-3, AA-5 | Bad input fails in uneven ways: `None` is a `TypeError`, a string «70» is rounded silently, a bool is taken as 0 or 1, and a value above about 1e22 is an `InvalidOperation`, not the `ValueError` of NaN | medium | patch: a non-number type is a `TypeError`, a non-finite or too large value a `ValueError`, with tests for each and for the four filters |
| BH-1, BH-2, BH-3, EC-8, EC-9, EC-10, VG-1, AA-2 | The guard is narrower than its text: `decimal.ROUND_UP` as an attribute, other modes, `math.trunc`, Django number functions in a `.py` file, `.txt` templates and scripts are not looked at, the template regex matches «localize» inside a class name, and Django's grouping setting is not asserted off | medium | patch: any `ROUND_` name, `trunc`, the Django formatting names and modules, `.txt` templates, `toFixed` and the like in scripts, a tightened regex with its own snippet tests, and `USE_THOUSAND_SEPARATOR` off. Rejected inside it: a check of every f-string format spec, `format()` and `%`, because `models.py` and `seed.py` write week identifiers with `:02d` (the guard text now says what it does not look at); `add`, `pluralize` and `yesno`, which format no number; chart values through `json_script`, which is Story 2.10 (AD-11) |
| BH-6, EC-13 | `test_a_filter_refuses_what_is_not_a_number` accepts any `Exception` and tries only `None` | low | patch: each filter against `None`, «», «70», a bool, NaN and infinity, with the named error |
| BH-8, EC-15 | The test of forbidden characters does not check that U+2212 and U+00A0 are present, and tries few values | low | patch: negative, tiny and large values, and the presence of the two characters |
| AA-4 | `test_e21_...` repeats the literals «0,07» and 1 beside the spreadsheet values | low | patch: the literals are removed |
| EC-12, EC-16 | The stand-in order formula is not checked against the stated `order_unrounded`, and `reader.TOLERANCE` is not used | low | patch: the test compares it with `order_unrounded` within `TOLERANCE` where the case states it |
| EC-18, AA-1 | `display.py` says it imports only the standard library; the documents task was open during the review | low | patch: the docstring names `forecasting/rounding.py`; the documents were written after the review, as in Story 2.2 |
| BH-7, EC-14, VG (observation) | `products.html` is checked by reading its source, not by rendering | low | reject: an integer prints the same with or without the filter, a removed `{% load %}` fails `test_product_overview.py`, and a mutation that removes the filter is caught by the source test |
| BH-4, EC-5, EC-6, EC-7 | No week label filters, no range check of the week, and `with_year` is left to the caller | low | reject: no week filters is decision 4 of the spec; weeks come from integer columns checked at the seed (AD-8); a list that knows its own year boundary is the design of Story 2.9, and the spec fixed `with_year` as the caller's flag |
| BH-5 (last bullet), BH-8 (last bullet), EC-3 | `round_up_to_units` does not clamp at 0, so the floor of R-8 is only in the test | low | reject: «the larger of 0 and …» is the order calculation of Story 2.4, which the spec leaves out; the rounding of −0.4 is 0 by itself (point in `issues.md`) |
| EC-4 | `format_number` does not check the type of `decimals` | low | reject: only the module's own constants call it, and the range is checked |
| EC-11 | A spreadsheet row without a column would break the collection of `test_rounding.py` | low | reject: the reader and `test_reference_spreadsheet.py` guarantee every settings column in every case |
| AA-3 | The stand-in order formula repeats Story 2.4's | low | reject: it lives in the test only, says so, and Story 2.4 replaces it |
| BH-5 (context) | `Decimal` reads the global context | low | reject: nothing in the app changes it |

**Open points** (`issues.md`): Story 2.4 applies the floor of 0 in code, replaces the stand-in formula and defines «–» and the column label «Uke 1 · uke 46» in `display.py`; Stories 2.7 to 2.9 decide whether the templates need week label filters.

## Design Notes

Decisions made without the user, to confirm at the checkpoint: (1) the 6-decimal step runs before display rounding too, as AD-3 words it, so 10.249999999999998 shows «10,3»; (2) week 1 carries its year in lists too, «uke 1/2027»; (3) «–» and the horizon column label wait for the story that has the value; (4) the Django filters call `display` and take no week arguments.
