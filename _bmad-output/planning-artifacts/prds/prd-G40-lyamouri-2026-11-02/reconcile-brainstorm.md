# Reconciliation: Brainstorm vs PRD

**Input:** the pre-PRD brainstorm of 2026-10-31 (`_bmad-output/brainstorming/brainstorm-prognose-pre-prd-2026-10-31/brainstorm-intent.md` and its `.memlog.md`) and the open points in the session-log `issues.md`. **Checked against:** `prd.md`, `addendum.md` and the PRD session log `.memlog.md` in this folder. **Date:** 2026-11-03.

**Citations:** BI = section of brainstorm-intent.md; BS Ln = line n of the brainstorm `.memlog.md` ("by user" = the user's words); PL Ln = line n of the PRD `.memlog.md`; ISS Ln = line n of `issues.md`.

**Verdict:** every brainstorm Must item is in the PRD, and no MoSCoW priority differs. There are no high-severity gaps. The four medium gaps are a warning trigger the user named, a Should item changed without a logged decision, an approved rationale that was never written down, and a risk to the visible calculation.

## 1. User decisions

**Carried unchanged**
- **Job and flow:** the job, including "a clear basis for purchasing decisions" (BS L12 → §2.1); the weekly flow (BS L31 → UJ-1, FR-24, FR-25, FR-29, FR-30); the overview stays a list, with no ordering (BS L36 → FR-30, §7).
- **Period and data:** week, with a 3-week horizon (BS L40 → §3, FR-7); 104 weeks plus short-history products (BS L43 → FR-3); a stock column and a weekly stockout flag (BS L15 → FR-3).
- **Order quantity:** next week only; normal scenario plus margin; never below 0; rounded up; no pack sizes; weeks 2–3 not summed (BS L60, L63, L65 → FR-7, FR-11, R-8, §7). The one-line visible calculation (BS L19 → FR-12). The normal scenario "by default" (BS L63) is fixed and has no scenario setting. This matches the brainstorm's settings list.
- **Data quality:** stockouts excluded, with a warning (BS L28 → FR-15); the moving average skips stockouts (BS L54 → FR-5); 2 × median kept (BI §2 → R-10); 3+ high weeks followed (BS L58 → FR-17, E9); at least 3 valid weeks, the 8-week warning, and confidence at 12/104 weeks with a reason (BS L23, L68, L71 → R-6, FR-8, FR-18, FR-19); no forecast when the window is larger than the data (BS L72 → FR-8, E11).
- **Scope:** manual adjustment (BS L35 → FR-29); seasonality in the calculation, as Should (BS L47, L77 → FR-9, R-14); the template explanation without a paid API, as Must (BS L77 → FR-26, AG-2); process and repo items, as Must (BS L80 A → DR-2, DR-4, DR-5, AG-6); the level-shift split (BS L80 B → FR-17).

**Changed later in the PRD session**

| Brainstorm | PRD | Log |
|---|---|---|
| Outlier median over the 3 preceding valid weeks (BI §2) | Baseline = the 3 latest earlier valid weeks that are not unusual; a baseline of 0 never flags; no check without 3 such weeks (R-10) | PL L44 |
| 3+ consecutive high weeks (BS L58) | 3+ consecutive weeks that each break the outlier rule, counting valid weeks only (R-11) | PL L34, L45 |
| Window compared with valid weeks (BS L72) | Compared with calculation weeks; excluded unusual weeks stay valid (R-2, FR-8) | PL L26 |
| Valid data older than 8 weeks (BS L68) | Counted from the latest data week (FR-18, E12) | PL L35 |
| "Order soon" = stock ÷ forecast (proposal, BI §4) | Suggested quantity above 0; weeks of cover is used only for sorting (R-12) | PL L47 |
| "Uncertain stock level" trigger (BS L24, by user) and a stock as-of date | Dropped: one stock value at the end of the latest data week (R-13, §7) | PL L49 |
| Saving adjustments undecided (BI §4) | Could, with an approval mark (FR-31); «Foreslått»/«Justert av deg» marking is Should (FR-30) | PL L21, L22 |
| Round up (BS L65) | Round to 6 decimals first (R-9, E5) | PL L43 |
| Active notes count toward medium confidence (BI §2) | Unusual weeks count whether included or excluded (FR-16) | PL L36 (coach change) |
| Language-model explanation "when a key is available" (BI §3) | Local model only, no key; hosted AI excluded (FR-28, AG-5, §7) | **No user decision line**; only the research event at PL L9 |
| Accuracy metric MAPE (BI §3) | MAE (FR-34) | **No PL line**; rationale in addendum §4 (B-R5) |

**Missing**
- **Rationale for seasonality as Should** (BS L78 C, approved at BS L80). The PRD shows the cut (FR-9, §8.2), the non-seasonal note (FR-7) and the seasonal test data (FR-3). It does not give the reason: the brief and the teacher suggested seasonality, and it was cut for feasibility.
- **"Seasonal variation" as a warning trigger** (BS L24, by user). BI §3 reduced it to a fallback note. The PRD keeps only the generic sentence in FR-7, which every product shows. Neither the §3 warning list nor FR-19 has a seasonal criterion.
- **Incidental, from the PRD session:** PL L30 made "choosing individual unusual weeks" a Could, but no FR or §8.3 entry exists.

## 2. MoSCoW comparison (mismatches only)

There are no priority mismatches. Every brainstorm Must, Should and Could item has the same priority in PRD §8, and every Won't item is in §7. These items keep their priority but changed in scope or wording:

| Item | Brainstorm | PRD | Issue |
|---|---|---|---|
| Language-model explanation | Should; hosted, with a key | Should; local only (FR-28) | Scope changed without a user decision; may become Must (§10 Q1) |
| Accuracy metric | Could; MAPE | Could; MAE (FR-34) | Justified by zero-sales weeks, but not logged |
| Level-shift message | Should; the rule is Must (BS L80 B) | FR-17 warning is Should | FR-19 (Must) needs the level shift as an active warning, and FR-26 (Must) explains "any level shift". The message is therefore Must in practice |
| Overstock note | Should | FR-14, Should | The UJ-1 edge case shows it with no priority tag, so it reads as Must |

## 3. Open points from issues.md

| ISS | Open point (translated) | Status in PRD |
|---|---|---|
| L3 | Choose the seasonal method through research | Resolved: R-14, FR-9 (PL L48) |
| L4 | Confirm "order soon" as stock coverage | Resolved differently: R-12 (PL L47) |
| L5 | Confirm a stock date as the trigger for "uncertain stock" | Resolved by dropping it: R-13, §7 (PL L49) |
| L6 | Outlier check in the first weeks; median 0 without a stockout flag | Resolved: R-10, E10 (PL L44) |
| L7 | Save adjustments between sessions? | Resolved: Could (FR-31); adjustments last for the current session until then (UJ-1; PL L21) |
| L8 | Template content and the fallback for the model explanation | Resolved: FR-26, FR-28, AG-3 |
| L9 | Tech stack and deadline | Deadline resolved: DR-6 (PL L59). Stack deferred to architecture (NFR-9, addendum §2) and not in §10 |
| L10 | Update the Product Brief with the session decisions | **Missing:** neither resolved nor in §10 |
| L11 | Ask the teacher whether a language model must be visible | Open question: §10 Q1; FR-28 tagged [OPEN] |
| L12 | Outlier rule: 2 × median with a zero guard, or Tukey/Hampel | Resolved: R-10 status, addendum §4 (PL L44) |
| L13 | Weeks 2–3 equal week 1 without seasonality | Resolved: FR-7, R-5 (PL L33) |
| L14 | SES convention and start value; thresholds as assumptions | Resolved: R-4 (PL L42); thresholds listed in §11 |
| L15 | Company isolation and the two-account test | Resolved for the PRD: FR-2, NFR-3, SM-4. The data-layer design goes to architecture (addendum §2) |
| L16 | Write and test the README setup sequence | Required by DR-1 and SM-2; the test itself is §10 Q3 |
| L17 | Textbook sources for report B | Open question: §10 Q4 |
| L18 | Optional polish of the research reports | Outside the PRD's scope; correctly absent |

Housekeeping: L3–L8 and L12–L15 can be ticked off, and L9 can be split.

## 4. Gaps

| # | Gap | Severity | Suggested fix |
|---|---|---|---|
| G1 | Nothing in the PRD carries the user's seasonal-variation warning (BS L24). FR-9 is Should and at risk (§8.2). Without it, a seasonal product with a gradual peak triggers no warning and can be labelled «høy» while its forecast stays flat through the season. This undercuts the differentiator kept at PL L18 | Medium | Add a simple, hand-checkable warning that counts as active for FR-19. For example, compare the base forecast with sales in the same week numbers last year (seasonal naive, addendum §4) and warn above a stated percentage. At minimum, say in FR-19 and the README that the label ignores seasonality until FR-9 is built |
| G2 | "Language-model explanation when a key is available" became a local-only model, with hosted AI excluded. No user decision records this. If §10 Q1 makes it Must, a local model on the examiner's machine is the only option | Medium | Confirm with the user and log the decision. Add to FR-28 that a hosted option with a key was considered and rejected (addendum §4). Note the install effect under §10 Q1 |
| G3 | Approved decision C (BS L78, L80) asked the PRD to say why seasonality is Should. The PRD does not | Medium | Add one sentence to FR-9 or §8.2: the brief and the teacher suggested it; it is the most demanding rule; it was cut for feasibility; the Must forecast is non-seasonal and says so (FR-7) |
| G4 | The brainstorm formula is `max(0, round up(…))`, but FR-12 covers only the simple case. For E6 the line would read «100 + 10 − 150 = 0». With one-decimal display (R-9), the shown numbers do not always give the rounded-up result, though FR-12 says each number "equals the value used". The overstock note that would explain a 0 is Should (FR-14) | Medium | Show the unrounded result and each step, e.g. «… = −40 → 0» and «… = 10,77 → rundet opp til 11». State that shown numbers are rounded per R-9. Add E4 and E6 as display examples |
| G5 | ISS L10 (update the brief) is neither resolved nor listed | Low | Add to §0 that the PRD applies where it differs from the brief, as §3 already does for one term. Close the issue or track it outside the PRD |
| G6 | Choosing individual unusual weeks (Could, PL L30) is missing from the PRD | Low | Add a Could FR next to FR-23, or log that it was dropped |
| G7 | The Should part of the level-shift split is empty in practice (see §2) | Low | Ask the user whether the FR-17 warning should be Must, or state what FR-19 and FR-26 show without it |
| G8 | The confidence levels overlap, as in the brainstorm (BS L71). "Medium: … or any active warning" overlaps "low: fewer than 12 valid weeks", and "insufficient data" is itself a warning (§3) | Low | Add to FR-19: low takes precedence over medium, and medium over high |
| G9 | The user's own worst case (BS L51: 100 a week, then 4 stockout weeks with 0 sales) has no reference example. E7 has a 2-week gap and states no sales values for it | Low | Add E15: 100, 100, 100, four stockout weeks with 0 sales, then 100. Expected: moving average 3 = 100 (not 33.3), and week 8 is not an unusual week |
| G10 | Neither the MAPE → MAE change nor the stack deferral is logged as a decision or listed as an open question | Low | Add one PL line for each, or a §10 line for the stack |

## 5. Qualitative ideas at risk

- **"Warn when the data basis is uncertain" / "the system tells you when not to trust it"** (BS L20, L24, L82; PL L18): strong for stockouts, unusual weeks, level shifts, old data and short history; weak for seasonal products (G1).
- **"Calculation must be visible so the user understands"** (BS L19): FR-12 specifies only the simple case (G4).
- **"Explain any outliers"** (BS L20): FR-26 lists weeks "left out", but unusual weeks are included by default, so the explanation may never mention them. FR-16 marks and counts them, but nothing says why a week is unusual. Add to FR-26 which weeks were unusual and the 2 × baseline test.
- **"A clear basis for purchasing decisions"** (BS L12): strong on the product screen (FR-12, FR-19, FR-26). The combined order overview (FR-30), which UJ-1 takes to the meeting, shows only the quantity and its marking. Consider adding the confidence label to each row.
- **"Avoid both empty shelves and overstock"** (BS L12): the overstock half rests on a suggested quantity of 0, weeks of cover and FR-14 (Should). R-12 says the overview shows weeks of cover, but the column list in FR-24 leaves it out.
- **"Keep rules simple and testable"** (BS L68, L72): carried (NFR-2, §5, §11, SM-C1). However, FR-9 and FR-17 cite "its reference example" for the seasonal and level-shift test products, while §5.6 has only short toy series (E9, and E14 with a 4-week cycle). The tests the user asked for at PL L34 need those answers.
- **"Good forecasts" and the user's priority order** (BI §1, BS L81): the PRD measures correctness (SM-1). Accuracy is a Could (FR-34) and also a counter-metric (SM-C1). This is acceptable, but the order (working site, good forecasts, understandable calculations, honest warnings, simplicity, deadline) is not written down. Adding it to §8 would give sprint planning a tie-breaker (§10 Q2).
