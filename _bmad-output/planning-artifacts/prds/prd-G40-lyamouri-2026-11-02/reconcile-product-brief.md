---
title: 'Reconciliation: Product Brief vs PRD'
created: '2026-11-02'
source: _bmad-output/planning-artifacts/briefs/brief-G40-lyamouri-2026-09-18/brief.md
checked: prd.md and addendum.md in this folder
---

# Reconciliation: Product Brief vs PRD

Every statement in the approved brief (§1 to §11) was checked against `prd.md` and `addendum.md`. Every number in the brief reappears unchanged (window 2 to 12, default 3; factor 0.1 to 0.9, default 0.3; horizon 3; scenario default 10%; 2 × the median of 3; 10 to 50 products). The teacher feedback and brainstorm files cited in PRD §0 were outside this check.

## 1. Covered

- Product idea, course and module 4.1 (brief §1) → PRD §1.
- Login with customer number and password, own data only (§1, §3, §7) → FR-1, FR-2, SM-4.
- Sales history in a local database, kept between sessions (§3, §7, §10) → FR-4, SM-5.
- Moving average and exponential smoothing with the brief's ranges and defaults (§3, §4) → FR-5, FR-6, FR-20, R-3, R-4.
- Horizon of 3 periods; normal = base forecast; optimistic and pessimistic = base ± scenario percentage (default 10%), pessimistic never below 0 (§4) → FR-7, FR-10, R-5, R-7.
- Unusual figures above 2 × the median of 3, with include or exclude (§4) → FR-16, FR-20, R-10.
- Deterministic, hand-checkable rules; no numbers from AI (§1, §4) → §5 intro, AG-1, SM-1, SM-C1.
- Charts (§3) → FR-25. Adjustable method, safety margin and unusual-week handling with a visible effect (§3, §7) → FR-20, FR-21, SM-3.
- Target user, 10 to 50 products, weekly review; synthetic accounts and data with trend and seasonal patterns (§6, §8) → §2, FR-3, NFR-4.
- Every out-of-scope item (§8) → §7, including "actual orders": the order quantity is advice only (§4.4, §4.9). Later integration outside v1 (§9) → §1.
- Simple local stack, separately testable calculations, data with known results, teacher runs it from a README without paid services or keys (§10) → NFR-1, NFR-2, NFR-9, DR-1, DR-3, SM-2, addendum §2.
- AI use in development documented (§1, §7) → AG-6, DR-5, SM-8.
- All nine success criteria (§7) → mapped one by one in §9. Open questions (§11) → DR-6 (deadline), NFR-9 and addendum §2 (stack), §5 intro and §10 Q6 (rule validation), FR-26 to FR-28 (explanations).

## 2. Deliberately changed

| Brief | PRD | Where | Explained? |
|---|---|---|---|
| "Period" | Week (calendar week assumed) | §3, FR-5, FR-7 | Implicitly (weekly review, §2); assumption tagged |
| Suggested planning quantity = selected forecast + safety margin | Suggested order quantity = week-1 normal forecast × (1 + margin) − stock on hand, at least 0, rounded up | §3, R-8, R-9, FR-11 | Rename stated in §3; formula grounded in addendum §4 (order-up-to policy). See G4 |
| Safety margin, no default | Default 10%, range 0% to 100% | FR-20, §11 | Default indexed as project-defined; range not (G6) |
| Scenario percentage, no range | Range 0% to 50% | FR-20 | No (G6) |
| Adjustable settings, scope not stated | One company-wide set; per-product settings are Could | FR-20 to FR-23 | Stated as deliberate (§4.6, addendum §4) |
| Proposed calculation rules | Only calculation weeks count (stockouts and excluded unusual weeks skipped); SES starts at the first observation; at least 3 valid weeks; outlier baseline skips unusual weeks, has a zero guard and flags high sales only; unusual weeks included by default; 3 or more in a row are a level shift and never excluded | §5.1 to §5.4, FR-8, FR-15 to FR-17 | Yes (§5.4, FR-16, addendum §4); project-defined rules indexed in §11 |
| "Established statistical methods" | MA and SES kept; data rules and R-14 labelled project-defined | §5, §11 | Yes |
| AI-based explanations, with an alternative needing no paid API | Template explanation (Must); local model rephrasing (Should, off by default); no hosted AI | FR-26 to FR-28, AG-2 to AG-5 | Yes (addendum §3, §4); visible AI still open (§10 Q1). See G1 |
| Seasonal patterns in the test data | Also a seasonal adjustment method (Should) | FR-9, R-14 | Yes; limitations in §5.5 |
| Forecasting website | Weekly purchase-decision tool: stock on hand, stockout weeks, warnings, confidence label, order-soon status, weeks of cover, adjust, combined overview, export | §1, §3, FR-15 to FR-19, FR-24, FR-29 to FR-34 | Rules sourced or indexed as project-defined (addendum §4, §11); the scope growth itself not explained (G3) |
| Open question: deadline | 1 December 2026 | DR-6 | Resolves brief §11 |

## 3. Gaps

- **G1 (medium) AI explanations: vision vs Must scope.** Brief §3 and §8 put AI-based explanations in scope. PRD §1 still says "AI explains the result in plain language", but the Must explanation is template-only, and FR-28 is Should, off by default and at risk (§8.2). §9 maps the brief's "AI explanations clearly separated" to SM-6, which measures number integrity, not separation. If FR-28 slips, the brief's in-scope item is gone without a recorded decision. *Fix:* reword §1 (templates explain; an optional local model may rephrase); map the criterion to FR-27 and SM-6; state in §10 Q1 that a Must-only build departs from brief §3 and §8 and needs the teacher's agreement.
- **G2 (medium) "Understand why the forecast changes" (brief §5) is only implicit.** FR-21 makes a change visible and FR-26 explains the current result, but nothing names what changed or shows before and after. Because settings are company-wide, trying an assumption on one product changes every product. *Fix:* add a consequence (Should) to FR-21: after a change, the product screen names the changed setting and shows the previous and new forecast and order quantity.
- **G3 (medium) No record of changes from the approved brief.** Stock on hand, stockout weeks, level shift, old-data warning, confidence label, order-soon status and weeks of cover are new and in the Must scope. Apart from the glossary note on the order quantity and the "from the brief" tags in §11, the PRD does not say which brief items it extends or why; it only cites the teacher feedback and brainstorm files in §0. *Fix:* add a short "Changes from the Product Brief" table to §0 (item, change, reason, source).
- **G4 (low) "Selected forecast" narrowed without a note.** Brief §4 adds the margin to "the selected forecast"; R-8 fixes it to the week-1 normal forecast and subtracts stock on hand. If the brief meant a scenario chosen by the user, that choice is gone; FR-13 (Should) only shows the other scenarios' quantities. *Fix:* one sentence in R-8 giving the reading and why stock on hand is subtracted.
- **G5 (low) Trend has no defined purpose.** Brief §2 names "understand sales trends" and §8 puts trend in the test data. FR-3 includes a trend product, but no rule, reference example or warning uses it. Both methods give flat forecasts that lag a trend, yet §5.5 states "no trend" only for R-14. *Fix:* give the trend product an expected result and add "both methods lag a trend" to the README limitations (DR-1).
- **G6 (low) New ranges without a reason.** The scenario percentage range (0% to 50%) and the safety margin range (0% to 100%) in FR-20 are missing from §11. *Fix:* add both to §11 with a one-line reason.

## 4. Qualitative ideas at risk

- **Simplicity (brief §2 "simpler", §5 "simple and clear") — medium.** The PRD carries simplicity into the architecture (NFR-9) and the settings (R-12) but not into the screens. FR-25, with FR-7, FR-21 and FR-26, puts about a dozen elements on the product screen with no order of importance, and the Must scope adds several data-quality concepts. *Fix:* hand "simple and clear" to the UX step as a design principle (one main number per product, warnings summarised, details on demand).
- **Ease of use (brief §5) — medium.** No NFR or metric measures it (NFR-7 covers only chart markings), and UJ-1's 20 minutes for about 30 products is narrative only. *Fix:* make it a UX acceptance check or a secondary metric (a first-time user completes the SM-3 flow without help).
- **Transparency — carried well** (§1, FR-12, FR-15, FR-16, FR-19, FR-26, §11), with plain-language Norwegian kept by NFR-5 and the glossary. No action.
- **Forecast understanding vs ordering — low.** The brief is about estimating demand and, long term (§9), making forecasting "more accessible and easier to understand". The PRD centres on one order number per product (UJ-1 climax); weeks 2 and 3 repeat week 1 and feed no Must decision, and the brief's vision sentence is not restated. *Fix:* restate it in PRD §1, and let FR-26 explain the forecast before the order quantity.
- **"Easier to keep track of" (brief §2) — low.** Only the product overview (FR-24) serves it. Saved decisions (FR-31) and accuracy (FR-34) are Could, so a Must-only build keeps nothing between weekly reviews except the settings. *Fix:* record this as an accepted limitation in §8.
