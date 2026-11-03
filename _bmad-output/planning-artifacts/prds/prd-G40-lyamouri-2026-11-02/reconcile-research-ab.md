---
title: 'Reconciliation: research A and B against the PRD'
created: '2026-11-02'
inputs: 'research A and B'
---

# Reconciliation: research A and B against the PRD

Inputs: report A `_bmad-output/planning-artifacts/research/academic-lit-forecasting-methods-seasonality-outliers-2026-11-01/research.md`, report B `_bmad-output/planning-artifacts/research/domain-safety-stock-and-order-quantity-2026-11-01/research.md`, and `prd.md` and `addendum.md` in this folder. A-R1 is report A's recommendation 1, and [A7] is its source 7. §, FR, R and E refer to `prd.md` unless the addendum is named.

## 1. Recommendations and caveats from A and B

Summary: 19 reflected, 3 partly reflected, 4 decided otherwise (one without a reason), 1 decided or left to §10, 3 missing.

| # | Research item | Status | Where, and note |
|---|---|---|---|
| A1 | MA and SES with the textbook formulas; recursive SES (A-R1) | Reflected | R-3, R-4, FR-5, FR-6. E1 and E2 equal A's worked examples. A calls these fixtures to re-verify, not sourced results, and §5 has the group recalculate every example. |
| A2 | Flat forecast for weeks 1 to 3, stated plainly in the UI (A-R1, cross-insight) | Reflected | R-5, Glossary "Base forecast", FR-7 note, FR-9 last consequence. For the note's wording, see §2 item 5. |
| A3 | Hand-checkable SES start (first valid observation, a NIST option) instead of optimisation; one indexing convention | Reflected | R-4 (first calculation week; FPP3 form written out), addendum §4. |
| A4 | Every threshold and default recorded as an assumption (A-R6) | Reflected, two omissions | §11 lists 3, 8, 12 and 104 weeks, α 0.3 and window 3. Not listed: the window, scenario and margin ranges, and R-14 step 4. |
| A5 | Window and α are usually chosen by best fit on past errors ([A3][A5]) | Missing | FR-20 makes them user settings; the PRD gives no reason for not fitting them. |
| A6 | SES (and, being flat, MA) suits only data without trend or seasonality ([A1][A5]) | Partly | Seasonality: FR-7, FR-9. Trend: not stated for R-3 to R-5. The FR-3 "known trend" product has no expected result. |
| A7 | Seasonal adjustment stays Should (A-R2) | Reflected | FR-9, §8.2. |
| A8 | Ratio-to-moving-average indices (A-R2) | Decided otherwise, explained | R-14 uses a simple week-number index. Addendum §4 gives A's caveats (26 weeks lost at each end, one ratio per week number, "not recommended"). R-14's own rationale misstates A (§2 item 1). |
| A9 | Indices average 1; forecast the adjusted series, then multiply by the index ([A7][A8]) | Reflected | R-14 steps 2 and 3, E14. |
| A10 | Compare any seasonal method with seasonal naive (A-R2, [A2]) | Decided otherwise, no reason given | Addendum §4 only says "the PRD does not require that comparison". |
| A11 | Exclusions remove index values; few values per index (cross-insight) | Reflected | R-14 steps 1 and 4 (calculation weeks only; fallback with a note), limitation "Few values per week number". |
| A12 | Several complete seasonal cycles ([A12], one vendor source) | Missing | R-14 step 4 allows indices built from one value per week number (one year of data). The limitations discuss only 104 weeks. |
| A13 | A year has 52.18 weeks | Reflected | R-14 assumption on week 53, §11. |
| A14 | Brief's outlier rule kept only as a project-defined rule with a zero-median guard; stockout flag against runs of zeros (A-R3, cross-insight) | Reflected | R-10 (no flag at baseline 0), §5.4 status, E10, FR-3, §11. A's "minimum floor" variant was not taken, and no reason is given. |
| A15 | Tukey or Hampel as alternatives; replacing outliers blindly is "a dangerous practice" ([A13]) | Reflected | §5.4 status, FR-16 (included by default), addendum §4. |
| A16 | Leave stockout weeks out as a design decision with partial support; keep the flag (A-R4) | Reflected | FR-15, FR-3, §11, addendum §4. R-1 itself carries no label in §5. |
| A17 | MA over the last N valid weeks is the project's own rule; gap handling unresolved | Decided (project rule) | FR-5 (look further back), FR-8, R-6, §11. SES gap skipping (FR-6, R-4) has no source either, but §11 names only the moving average. |
| A18 | Level shift as a project-defined rule with its own test series (A-R5) | Reflected | FR-17 assumption, R-11, E8, E9, FR-3, §10 Q6. |
| A19 | Croston for many zero weeks is out of scope for v1 | Reflected | Addendum §4. |
| A20 | Evidence comes mostly from FPP3; 4 of 8 claims verified | Reflected | Addendum §5. |
| A21 | Other A open questions (simplest unconstraining method, smoothing indices, sourced level-shift rule, MAPE) | Decided or open | Decided in R-1, R-11 and R-14; behaviour left to §10 Q6; MAPE in addendum §5. Acceptable. |
| B1 | Keep the formula as a simplified weekly order-up-to policy, with an assumptions list: weekly review, lead time 0, no open orders, stock on hand only, at least 0, round up (B headline, B-R1) | Partly | R-8 (at least 0, round up), §7 (no lead time, open orders, pack sizes, MOQ or z × σ). The order-up-to framing and "stock on hand instead of inventory position" appear only in addendum §4. Weekly review is implicit, and DR-1 does not ask for any of these. |
| B2 | Adjustable margin, called a rule of thumb that ignores demand variability and is not a service-level guarantee, in the UI wording; z × σ later (B-R2) | Partly | FR-20, Glossary "Safety margin", §11, §7, addendum §4. No FR puts the wording on screen or in the explanation (FR-11, FR-12, FR-26), as FR-10 does for scenarios. |
| B3 | Scenarios as what-if, not intervals or probabilities; a fixed percentage does not widen with the horizon; any later range from forecast error (B-R3) | Reflected | Glossary "Scenario", FR-10 (testable), addendum §4. §11 uses a different label (§2 item 4). |
| B4 | Order soon from forward weeks of cover against a user-set threshold; say that lead time is not modelled (B-R4) | Decided otherwise, explained; one part missing | R-12, addendum §4 (the same as cover below 1 + margin). Cover is used only for sorting, in line with [B6]. "Lead time is not modelled" is stated only in §7, not at R-12 or on screen. |
| B5 | Weeks of cover assumes constant consumption, so seasonal demand needs an adjusted calculation ([B4]) | Missing | R-12 divides by week 1 only, even when R-14 makes weeks 1 to 3 differ. |
| B6 | Order at least 0, rounded up to whole units; pack sizes out of v1 | Reflected | R-8, R-9, FR-11, E5, E6, §7. |
| B7 | MAE, not MAPE, if accuracy is shown (B-R5) | Reflected | FR-34 (Could), addendum §4. |
| B8 | "No textbook source" recorded as a known limitation (B-R6); open questions on sources and on σ | Reflected | §10 Q4, addendum §4 and §5. Q4 leaves out fixed-percentage scenarios, although addendum §5 says Q4 records that gap. |
| B9 | Do ranges help decisions? Mixed to negative, one 2010 study ([B12]) | Reflected, used one-sidedly | Addendum §4 (§2 item 3). |

## 2. Misrepresentations of the research

1. **R-14 limitation "Not a textbook method" (§5.5).** It says "the research found no source for this simplified index", and that the textbook alternatives, including ratio-to-moving-average, are "much harder to check by hand". Report A does not discuss a week-number average index, so the index is unresearched, not unsourced. A does not call ratio-to-moving-average hard to check by hand. It recommends that method (A-R2) and names only STL and Fourier terms as not hand-checkable. A's caveats about it are the 26 weeks lost at each end, one ratio per week number, FPP3's "not recommended" and poor robustness. So the stated reason for not following A-R2 is not A's, and "no source" claims more than the research shows.
2. **Addendum §4, Tukey fences.** "Used as intended, they need a decomposition that cannot be checked by hand" turns FPP3's practice (fences on an STL remainder [A13]) into a requirement. A-R3 offers Tukey 1.5 × IQR or Hampel as a direct switch. The decision still stands on simplicity; only the reason is overstated.
3. **Addendum §4, prediction intervals.** [B12] is cited as a reason to prefer fixed-percentage scenarios. B rates it as one abstract-level lab study from 2010 with "mixed to negative" evidence, in which a simple 85%-interval heuristic came close to optimal. The study compared intervals with point forecasts, not with fixed-percentage scenarios, so it does not support that choice.
4. **§11, last bullet.** It calls fixed plus-or-minus scenarios "simple rules of thumb". B found no practice source for a fixed percentage (only an unfetched template snippet) and asks for the label "what-if" (B-R3). B uses "rule of thumb" for the safety margin only. The Glossary and FR-10 use the right label.
5. **FR-7 note.** «... fordi metoden ikke tar hensyn til sesong» gives only one of two reasons. Per [A1], the forecast equals the last level, and both methods assume neither trend nor seasonality.
6. **Checked and accurate:** R-4 (start value, no standard α), R-5 (flatness, verified high), the §5.4 status, the FR-17 assumption, §11 on R-1 ("only partly supported"), R-12 on B-R4, §10 Q4 on vendor sources, FR-34, and the evidence table and list of inferences in addendum §5.

## 3. Gaps, severity and suggested fixes

- **High: the order-quantity caveats are not shown to the user (B1, B2, B4).** B's caveats on the order rule appear only in the Glossary, §7, §11 and the addendum, never in an FR or DR. They are: the margin is a rule of thumb that ignores demand variability and promises no service level; lead time and orders on the way are not modelled, so stock on hand stands in for inventory position; and R-8 is a simplified weekly order-up-to policy. The suggested order quantity is the product's key number, and the PRD already makes this kind of wording testable for scenarios (FR-10) and flat forecasts (FR-7). *Fix:* add an "Assumptions" line to R-8 (weekly review, lead time 0, no open orders, stock on hand only, at least 0, round up; see addendum §4). Add an FR-12 or FR-26 consequence with one fixed Norwegian sentence on the margin, lead time and open orders. List both under the known limitations in DR-1.
- **Medium: the "project-defined" labels in §5 do not match §11 (A4, A16, A17).** §5 says the rules it marks are listed in §11, which implies that unmarked rules have a source. Only R-10, R-11 and R-14 are marked. Several unmarked rules have no source or only partial support: R-1, the gap skipping in R-2 to R-4, R-6, the percentages in R-7 and R-8, and R-12's trigger, plus FR-18's 8 weeks and FR-19's 12 and 104 in §4. Conversely, R-14 step 3 has a source [A8]. *Fix:* tag each rule as sourced (with the report key), partly supported or project-defined, and make §11 match the tags, including the setting ranges and R-14 step 4.
- **Medium: the trend caveat is missing (A6).** A product with a steady trend and 104 clean weeks gets «høy» and no warning, although both methods assume no trend [A1] and so lag behind one. *Fix:* state the no-trend assumption in R-5, and name trend as well as season in the FR-7 note. Give the FR-3 trend product a reference example that shows the lag, and list the limitation in DR-1. Add an open question on whether a trend should lower the confidence label.
- **Medium: R-14 drops two parts of A-R2 without a reason (A10, A12; FR-9 is Should).** It has no seasonal-naive comparison, although A names seasonal naive as the benchmark and it is trivial to check by hand. It also lets an index rest on a single value per week number. *Fix:* add an FR-9 consequence that compares the seasonal test product with seasonal naive, or say why not. Require two values per week number, or record the one-value case as a limitation and as a threshold in §11. Correct the R-14 rationale (§2 item 1).
- **Low: FR-12 conflicts with R-9 on rounding.** FR-12 says every number on the line "equals the value used in the calculation". But R-9 shows forecasts with one decimal, and the line has no rounding step (E4 shows 14,3 + 1,4 − 5, then 11). Take a forecast of 18.24, a 10% margin shown to one decimal and stock of 0: the screen shows 18,2 + 1,8 = 20,0, but the result is 21. *Fix:* say that the line shows rounded values, show the total before rounding with «rundet opp», set the display precision of the margin amount, and add this case as a reference example.
- **Low: weeks of cover (B4, B5).** Under R-14, stock ÷ week-1 forecast no longer counts weeks, because weeks 1 to 3 differ. R-9 sets no display precision for it (E13 shows 0.35 and 1.5), and FR-24's column list leaves it out, although R-12 says the overview shows it. *Fix:* define it for flat forecasts only, or use the cumulative forecast for weeks 1 to 3. Add its precision to R-9 and the column to FR-24.
- **Low: smaller unexplained choices (A5, A14, B8).** The settings are not fitted to past errors (this could use FR-34's MAE). The R-10 guard covers only a baseline of exactly 0, so with a baseline of 1, any week of 3 units or more is flagged. §10 Q4 leaves out fixed-percentage scenarios. *Fix:* add one sentence for each in addendum §4 or §10.
- **Low: wording corrections** for §2 items 2 to 4 (the Tukey reason, the use of [B12] and the §11 label for scenarios).
