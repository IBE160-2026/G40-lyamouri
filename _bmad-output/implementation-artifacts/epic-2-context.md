# Epic 2 Context: See what to order, how it was calculated and whether to trust it

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Build the pure forecasting core and the screens on top of it, so that the purchasing manager sees, per product, the week forecasts, the scenarios, the suggested order quantity, how each number was calculated, the chart, the warnings, the confidence label and a template explanation, with the overview in order-soon order. Every value must match the reference spreadsheet, which is the single answer key for the Must scope (milestone M2: all 24 Must reference examples pass).

## Stories

- Story 2.1: Find the valid weeks, unusual weeks and level shifts
- Story 2.2: Calculate the base forecast with the moving average or exponential smoothing
- Story 2.3: Round and format every number the same way
- Story 2.4: Calculate the week forecasts, the scenarios and the suggested order quantity
- Story 2.5: Give each product its warnings, notes and confidence label
- Story 2.6: Sort the products by what needs ordering first
- Story 2.7: Show what to order and whether to trust it on the product screen
- Story 2.8: List the products in R-12 order
- Story 2.9: Show how the forecast and the order quantity were calculated
- Story 2.10: Show the sales history and the forecast in a chart, also as text
- Story 2.11: Go through the week's products and find a product quickly
- Story 2.12: Explain each forecast in plain Norwegian

## Requirements & Constraints

- **Weeks used:** stockout weeks are never used in any calculation and never count as valid weeks. Unusual weeks are found by one forward pass over the valid weeks (baseline: median of the 3 most recent earlier valid weeks that are not unusual; unusual only above 2 × a non-zero baseline). Three unusual valid weeks in a row become level-shift weeks, which always stay in the calculation. The setting only decides whether unusual weeks are included.
- **Forecast:** moving average (window 2 to 12) or exponential smoothing (factor 0.1 to 0.9) over the calculation weeks; a product with too little data gets no forecast, no order quantity and a warning. Weeks 2 and 3 repeat week 1 without seasonal adjustment, and only week 1 feeds the order quantity.
- **Order quantity:** the larger of 0 and (week-1 forecast × (1 + safety margin) − stock on hand), rounded to 6 decimals and then up to a whole unit once, at the end.
- **Trust:** each product gets its active warnings, notes and one confidence label by fixed rules; stockout weeks, unusual weeks and level shifts count only in the recent period (the last 12 weeks). The label's reason names the deciding condition (first in rule order), then the other active warnings; its phrases, including «gamle data, N uker siden siste gyldige uke» (a guard case that cannot occur under today's rules) and the singular «1 gyldig uke», are fixed in the Message Catalogue.
- **Answer key:** every reference example is read from `reference/reference-examples.xlsx` with openpyxl; no expected value is copied into code. Each test names its E-n and FR-n. A disagreement is recalculated by hand and logged in the QA log.
- **Every story:** own branch; tests, Ruff and `makemigrations --check` pass locally and in CI; the status table, QA log, AI steering log (at least one case per epic) and work log are updated; the pull request names the story, its FRs and what was tested, and records every BMAD Code Review finding with its decision and fix commit. Changed pages are checked at 320 px, 390 × 844 and 820 × 1180.

## Technical Decisions

- **Pure core (AD-1):** `forecasting/` imports only the standard library and reads no clock, file or environment variable; `explanation/` may import `forecasting/`, never the reverse. `tests/test_core_imports.py` enforces it.
- **One compute path (AD-2):** `forecast_product(weeks, stock_on_hand, settings)` returns a frozen `ProductResult`; `build_overview` groups and orders; one loader in `web/company_data.py` reads a company's data through `web/queries.py` and calls the core. Nothing outside the core calculates, rounds, sorts or groups domain values; results are never stored.
- **Rounding and format (AD-3):** the core keeps full float precision and returns numbers; all rounding goes through `forecasting/rounding.py` with `decimal`, never `round()`; all Norwegian display text and week labels come from `forecasting/display.py`.
- **Wording (AD-4, AD-5):** each warning, note and label has its wording in one place; the explanation is template-based with named placeholders, and numbers in it must come from the result.
- **Weeks (AD-8):** a week is identified by its position in the sales history (1 to N, oldest first); every order and distance uses positions, never calendar arithmetic. Histories are gapless and end at the company's latest data week.
- **Settings (AD-9):** the FR-20 defaults and ranges live once in `forecasting/settings.py`.
- **Tests (AD-17):** `uv run pytest` runs everything; the reference examples are read through `reference/answer_key_reader.py`.

## UX & Interaction Patterns

- Screens show texts verbatim from the Message Catalogue in EXPERIENCE.md; all text is Norwegian bokmål; everything works without scripts, by keyboard, and never by color alone (WCAG 2.2 AA).
- The overview groups products with «Denne uken» first and is the only place that sorts them; the product screen shows the decision panel, the trust panel, the calculation lines and the chart with its text alternative.
- Stockout weeks, unusual weeks and level-shift weeks each get their own chart marker, explained in the legend.

## Cross-Story Dependencies

- **Order:** 2.1 (week classification) feeds 2.2 (base forecast), which feeds 2.4 (scenarios and order quantity); 2.3 (rounding and display) is used by 2.4 onward; 2.5 (warnings and label) needs 2.1 and 2.4; 2.6 and 2.8 need 2.4 and 2.5; 2.7 and 2.9 to 2.12 build on the computed `ProductResult`.
- **Replaces Story 1.8's simple product list** and extends `forecasting/display.py` (the header week label from Story 1.8).
- **Isolation:** every new route and list extends the two-account test of Story 1.8, and a direct request for another company's product gives «not found».
- **Seed data:** the rule test products in the seed files carry the series of the reference examples, so later stories check the core against both the examples and the seeded products.
