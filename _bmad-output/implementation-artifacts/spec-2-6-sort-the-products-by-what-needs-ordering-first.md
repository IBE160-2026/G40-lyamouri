---
title: 'Story 2.6: Sort the products by what needs ordering first'
type: 'feature'
created: '2026-11-27'
status: 'done'
baseline_commit: '3671ebaed7b03daddba242ac61d1e8cf5372764f'
route: 'dispatch'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `ProductResult` has no weeks of cover and no order-soon status, and nothing sorts or groups the products of a company. Stories 2.7, 2.8 and 2.11 have no order, no week figures, no review sequence and no previous or next product to show, and E13, E23, E24 and the rule test products are not yet checked end to end (SM-1).

**Approach:** `forecast_product` sets `weeks_of_cover` and `order_soon` (R-12). A pure module `forecasting/overview.py` has `build_overview(results, adjustments)`, which gives the three groups, the four week figures, the review sequence and the neighbours. A test that reads the spreadsheet runs every Must reference example and every rule test product through the core. No screen, loader, model or migration change.

## Boundaries & Constraints

**Always:**
- `weeks_of_cover` is the stock on hand ÷ the week-1 normal forecast at full precision, and None when there is no forecast or the week-1 forecast is 0 (E23). `order_soon` is `suggested_order_quantity > 0` and False without a forecast. Nothing is rounded in the core; the sort uses the unrounded value (AD-3).
- `build_overview(results, adjustments)` takes `results` as a mapping from product number (text) to `ProductResult`, and `adjustments` as an empty mapping until FR-29 is built; a non-empty one is a `ValueError`, so an adjustment is never ignored silently. It reads no clock, file or database (AD-1).
- Groups, in this order (R-12): order-soon products by weeks of cover, lowest first, ties by product number (E24); products without a forecast by product number; the other products by product number. Product numbers sort as text, as the five-digit seed numbers and E24's «A» and «B» do.
- The overview also gives the four week figures (order-soon count, the sum of the suggested order quantities, the products without a forecast, the products with at least one active warning, counting a product without a forecast, whose warning is insufficient data), the review sequence (order-soon, then without a forecast), and the previous and next product of each product across all groups, None at the ends (AD-2, UX-DR33, UX-DR35). It gives product numbers; the caller joins them with the results.
- Every stated value (`weeks_of_cover`, `order_soon`, `overview_position`, and for the rule test products the six values of FR-3) is read from `reference/reference-examples.xlsx` through `answer_key_reader`; each test names its E-n and FR-n (AD-17). No expected value is copied into code.
- The Must examples E1 to E13, E15 to E21, E23, E24, E28 and E29 each run through the core in one sweep test that fails if one of them is missing from the sweep (SM-1, NFR-2). The rule test products run from the committed seed files with the FR-20 defaults, as the loader will (PRD §10 question 4).

**Never:**
- No loader, view, template, overview screen or chart; no search, no FR-29 adjustment logic, no combined order overview (FR-30); no overstock note or stock-not-lasting note; no text in the overview (AD-4); no change to the seed files, models, migrations or dependencies; no `round()` and no formatting outside `display.py`; `forecasting/` never imports `explanation/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Cover and status | E13 (E4): stock 5, week 1 14.333; E13 (E6): stock 150, week 1 100 | 0.349 and order-soon; 1.5 and not order-soon | N/A |
| Zero forecast | E23: sales 0, 0, 0, stock 0 | weeks of cover None, not order-soon, quantity 0 | N/A |
| Tie | E24 A and B, both cover 0.0 | A before B in group 1, positions 1 and 2 | N/A |
| Three groups | order-soon, no forecast, other products mixed | the order of R-12, each group by its own key | N/A |
| Stock covers the need | stock above week 1 × (1 + margin) | the product is in group 3, with cover | N/A |
| Week figures | Testbedrift A defaults | 4 order-soon, 31 units, 1 without forecast, 4 with a warning (UX-DR46, the mockup) | N/A |
| Neighbours | first, middle and last product | first has no previous, last has no next; across group borders | N/A |
| Review sequence | order-soon, then without forecast | group 1 order, then group 2 order; group 3 not in it | N/A |
| No products | empty mapping | empty groups, figures 0, empty sequence | N/A |
| Adjustments | non-empty mapping | `ValueError` naming FR-29 | ValueError |

</frozen-after-approval>

## Code Map

- `src/forecasting/forecast.py` -- `ProductResult` gets `weeks_of_cover` and `order_soon`; `forecast_product` sets them after the order quantity. Reuse `suggested_order_quantity`, `week_forecasts`, `stock_on_hand`; nothing else changes.
- `src/forecasting/overview.py` (new) -- `Overview`, `WeekFigures`, `Neighbours` (frozen dataclasses) and `build_overview`; style of `trust.py`; imports only `forecasting.forecast` types it needs.
- `tests/test_overview.py` (new) -- the matrix rows with reader values (E13, E23, E24), the groups, figures, sequence, neighbours, the `ValueError`, and mutations of the sort keys.
- `tests/test_reference_examples.py` (new) -- the SM-1 sweep over the Must examples and the rule test products from the seed files; reuses `answer_key_reader`, `answer_key.settings_of`-style helpers from `tests/test_trust.py` and `tests/test_week_forecasts.py` (`core_weeks`, `settings_of`).
- `tests/test_week_forecasts.py`, `tests/test_trust.py` -- read only unless a new field breaks them; `tests/test_core_imports.py` already covers the new module.
- `data/seed/*`, `reference/*` -- read only.
- Documents: `docs/statustabell.md`, `docs/qa-logg.md`, `docs/ki-styringslogg.md`, `docs/arbeidslogg.md`, `sprint-status.yaml`, `.logs/mounia-03/issues.md` (the 2.4 and 2.5 points for the loader stay open for Stories 2.7 to 2.9; the §10 question 4 point is closed for the rule test products only).

## Tasks & Acceptance

**Execution:**
- [x] `src/forecasting/forecast.py` -- `weeks_of_cover`, `order_soon` on `ProductResult` and in `forecast_product` -- R-12, E13, E23
- [x] `src/forecasting/overview.py` -- `build_overview` with the groups, the figures, the sequence and the neighbours -- R-12, FR-24, AD-2, UX-DR33, UX-DR35
- [x] `tests/test_overview.py` -- every matrix row; E13, E23, E24 from the spreadsheet; Testbedrift A and B from the seed files -- E13, E23, E24, FR-24
- [x] `tests/test_reference_examples.py` -- the sweep over the Must examples and the 11 rule test products -- SM-1, NFR-2, FR-3, DR-3
- [x] the documents above, `sprint-status.yaml` to `review` -- DR-7

**Acceptance Criteria:**
- Given `uv run pytest`, `uv run ruff check` and `uv run ruff format --check`, when they run locally and in CI, then they pass, and `makemigrations --check` finds no change.
- Given mutations of the new code (the sort by displayed cover, the tie key dropped, group 2 and group 3 swapped, order-soon as `>= 0`, cover with a zero forecast, a figure that counts the wrong set, a neighbour off by one), when the tests run, then each one fails at least one test.

## Implementation Notes

- 2026-11-27: built in the build session, not by a subagent, because the user approved subagents for the reviews only. The user approved the spec and decisions 1 to 6 of the Design Notes unchanged and kept the spec whole (about 2,150 tokens, over the 1,600 guide). Branch `story/2-6-sort-the-products-by-what-needs-ordering-first` from `3671eba`.
- New: `src/forecasting/overview.py` (`build_overview`, `Overview`, `WeekFigures`, `Neighbours`), `tests/test_overview.py`, `tests/test_reference_examples.py`; changed: `src/forecasting/forecast.py` (`ProductResult` has `weeks_of_cover` and `order_soon`). No model, migration, dependency, template, seed, display or catalogue change. 960 tests pass, 1 skipped (the Docker check); Ruff is clean and `makemigrations --check` finds no change.
- The sweep runs all 45 Must cases of the spreadsheet (E1 to E13, E15 to E21, E23, E24, E28, E29 and FR-21 a to d) and the 11 rule test products from the committed seed files with the FR-20 defaults. It reads the spreadsheet through `answer_key_reader`. The spreadsheet states `valid_weeks` and `calculation_weeks` as counts, so the sweep compares counts. Left out and named: the Should-have seasonal columns and the optimistic and pessimistic order quantities, which only E22 (Should, FR-13) states. E23's `overstock_note` is checked as absent.
- Testbedrift A gives the figures 4, 31, 1 and 4: the first three are the approved mockup's, read through `answer_key.mockup_overview()`, and the 4 warnings are the UX-DR46 figure (the E8 product adds one to the mockup's 3).
- Mutations applied to the new code and restored (compared by hash): 23 before and after the review, all caught. The first run left four alive: a tie key that reverses the product number (the tests had only the one-character numbers «A» and «B», so the numbers «10021» and «10012» were added), a no-forecast set that was an equivalent mutant (replaced by «a forecast of 0 is a forecast»), and two that did not apply because Ruff had wrapped the line (the patterns were fixed). The one that survived the second run, order-soon taken from the unrounded order, is caught by `steady(50, 55)`, where 50 × 1.1 is 55.00000000000001 and the suggested quantity is 0. The script ran with bytecode off and `__pycache__` cleared before each mutation, as in Story 2.5.
- Model: Sonnet 5.5 (High) for the build and for the four reviewers. The epic context was used as valid: by modification time `EXPERIENCE.md` is newer than `epic-2-context.md`, but both were committed together in `0dac0f7` and the context already holds the guard-case and singular phrases of the catalogue change.
- Process notes: the build workflow lists three review layers, and the user asked for four, so the Acceptance Auditor was launched from the `bmad-code-review` skill's layer definition, with the spec as its claims file as in Story 2.5. The reviewers changed nothing: the hash of all tracked and untracked files was identical before and after.

## Spec Change Log

## Review Triage Log

BMAD Code Review (2026-11-27): Blind Hunter (BH, N = 6), Edge Case Hunter (EC), Verification Gap (VG) and Acceptance Auditor (AA), as four independent read-only subagents, on the diff of `src` and `tests` from `3671eba` (29.4 kB). The spec went to the Edge Case Hunter as the claims file and to the Acceptance Auditor, and the other two never saw it. 19 findings (BH 9, EC 7, VG 0, AA 3), in 13 groups: 6 patched and 7 rejected. None was deferred, and none was an intent gap or a bad spec.

| ID | Finding | Verdict | Route |
|---|---|---|---|
| BH-3, EC-6 | The test hard-codes 4 products with a warning, and its module docstring says no expected value is copied | low | patch: the docstring says that the first three figures are the mockup's and the 4 is the UX-DR46 figure |
| BH-4, AA-2 | The sweep leaves out the optimistic and pessimistic order quantities and the overstock note, and only names them | low | patch for the overstock note, which E23 (Must) states: it is checked as absent. The order quantities are false: only E22 (Should, FR-13) states them, and the sweep's comment now says so |
| BH-5 | The seed-company test does not check ties, the figures, the sequence or the neighbours, and its docstring says more than it checks | low | patch: it checks that the groups are disjoint and equal the order, the ties, the figures, the review sequence and the neighbours from the results |
| BH-9 | No test combines a warning with the group, so grouping by warning is not isolated from grouping by status | low | patch: `test_a_warning_does_not_decide_the_group_the_status_does`. Rejected parts: stock 0 with a forecast is E24, negative stock is refused by `check_stock_on_hand`, and the display of «–» belongs to the screens of Stories 2.7 and 2.8 |
| EC-4 | The sweep would raise `TypeError` for a case that states `week_forecasts` as none for a product without a forecast | low | patch: `same_numbers` compares None with None. No Must case states it today |
| EC-5 | The overview-position test drops a duplicate product number silently | low | patch: it asserts that every case has its own product number |
| BH-1, EC-2 | Two covers that are equal in theory can differ by float noise, so the product-number tie-break would not fire | low | reject: equal fractions of exactly represented numbers give the same float, as E24 does, and a tolerance would make the sort order not transitive |
| BH-2, EC-1, AA-3 | An order-soon product with no cover would make the sort raise `TypeError` | false | reject: `check_stock_on_hand` refuses a stock below 0, so a week-1 forecast of 0 or less gives an order of at most 0 and no order-soon status; a failure there would be loud, not silent |
| BH-6, EC-3 | The overview does not validate its inputs: an int key, `adjustments=None` | low | reject: the loader of Story 2.8 gives text keys and an empty mapping, and a guard is more than a direct correction |
| BH-7 | The frozen `Overview` holds a dict in `neighbours` | low | reject: no caller changes it, the overview is built again for each request, and the fix adds a wrapper |
| BH-8 | The two new fields on `ProductResult` break other constructors and are undocumented | false | reject: only `forecast_product` builds a `ProductResult`, and its docstring describes both fields |
| EC-7 | A negative week-1 forecast gives no cover, which the spec does not say | low | reject: negative sales are not data of this product, and the fix edits the spec |
| AA-1 | The document task is not done | low | reject: it comes after the review, as in Stories 2.2 to 2.5 (done below) |

**Open points** (`issues.md`): Stories 2.7 and 2.8 show «–» for a missing cover and join the product numbers of `build_overview` with the results; the loader of Story 2.8 gives `build_overview` its results; the pattern products of PRD §10 question 4 stay with Story 5.2.

## Design Notes

Decisions made without the user, to confirm at the checkpoint: (1) the overview is its own module `forecasting/overview.py`, since AD-2 puts `build_overview` in the core, and it is built from results only; (2) it sorts by the unrounded cover, so two products that both show «0,3» can still be ordered by their real value (AD-3); (3) product numbers sort as text; (4) a product without a forecast counts in «produkter med varsel» because its insufficient-data warning is active, which gives 4 for Testbedrift A as UX-DR46 states; (5) the PRD §10 question 4 point in `issues.md` is closed for the rule test products, and the pattern products stay with Story 5.2.

Golden overview, Testbedrift A with the defaults: group 1 has 4 products, group 2 has Snøskuffe aluminium (10040), group 3 the rest; figures 4, 31, 1, 4.

## Verification

**Commands:**
- `uv run pytest` -- expected: all pass
- `uv run ruff check && uv run ruff format --check` -- expected: clean
- `uv run python src/manage.py makemigrations --check` -- expected: no changes
