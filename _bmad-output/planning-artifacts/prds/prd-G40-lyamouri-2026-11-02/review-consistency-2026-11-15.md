---
title: 'Consistency review: Prognose PRD update 2026-11-15'
created: '2026-11-15'
---

# Consistency review: Prognose PRD update (2026-11-15)

**Scope.** This review covers the uncommitted update of `prd.md` and `addendum.md` on branch `prd/teacher-feedback` (`git diff` against `42cfae9`). It checks the update against the whole PRD, the whole addendum and the teacher's feedback in `tilbakemelding-prd.md`. Section 3 compares the downstream documents (EXPERIENCE.md, DESIGN.md, ARCHITECTURE-SPINE.md and epics.md) with the updated PRD. `sprint-status.yaml` was read to check the Should order. No other file was edited. Severity levels: **High** blocks the Must scope or a Must test. **Medium** means that a changed Must statement cannot be met as written. **Low** covers wording, cross-references and bookkeeping. "c4" means an FR's fourth testable consequence.

**Verdict.** The update answers every point in the feedback, and its new bookkeeping holds. The IDs and counts agree, and so do the priority of every FR in all five places, the §8.5 table against §9, the Should order, the SM-1 rule lists and the `[ASSUMPTION]` index. Three changed statements need a fix before the PRD goes back to final:
- FR-25's new warning rule pulls Should and Could texts into a Must FR (C-1).
- FR-27's allowed numbers leave out numbers that FR-26 requires (C-2).
- The publishing cut line is not carried into DR-8, FR-4 and DR-1 (C-3).

The other seven findings are Low.

| Check | High | Medium | Low |
|---|---|---|---|
| IDs, counts and cross-references | 0 | 0 | 3 (C-7, C-9, C-10) |
| Priorities | 0 | 1 (C-1) | 0 |
| §8.5 success metrics against §9 | 0 | 0 | 1 (C-5) |
| Cut line | 0 | 1 (C-3) | 0 |
| FR-27, FR-28 and SM-6 against FR-26, AG-1 to AG-5, the glossary and addendum §3 | 0 | 1 (C-2) | 2 (C-4, C-6) |
| Should order; SM-1 rule lists; `[ASSUMPTION]` and `[NOTE FOR PM]` | 0 | 0 | 0 |
| Glossary | 0 | 0 | 1 (C-8) |
| **All** | **0** | **3** | **7** |

## 1. Inconsistencies in the PRD and addendum

### Medium

- **C-1 · FR-25 c4 (new); also §3 Warning, §3 Level shift and FR-26 c1.**
  - Quote: "The screen lists every active warning and every note that R-15 gives the product, each with its Norwegian text, and no warning or note that does not apply."
  - Problem: R-15 gives three texts that are not Must: the level-shift warning (its text is FR-17b, Should), the overstock note (FR-14, Should), and the note that the stock will not last through weeks 2 and 3 (FR-33, Could). As written, the Must FR-25 needs all three, so one FR again spans Must, Should and Could. Feedback point 4.3 asked to remove exactly that. Other Must FRs that touch a Should FR carry a qualifier: "only when FR-9 is built" in FR-20 and "(when FR-28 is built)" in FR-27. This bullet has none. The same gap appears in three more places:
    - §3 Warning ("A message … a level shift in the recent period") presents the level-shift text without the Should tag.
    - §3 Level shift ("reported with a warning") does the same.
    - FR-26 c1 ("every active warning and note (R-15)") has the same gap for the explanation.
  - Fix:
    - In FR-25 c4, write "…that R-15 gives the product and whose FR is built…".
    - Add to FR-25: "Until FR-17b is built, an active level shift is named only in the confidence label's reason (FR-17)."
    - Use the same qualifier in FR-26 c1.
    - In §3 Level shift, write "reported with a warning (text: FR-17b, Should)".

- **C-2 · FR-27 c1 against FR-26 c1, FR-12 and FR-7.**
  - Quote: "The allowed numbers are: the values in the product's calculation result that the product screen shows … the safety margin amount, the stock on hand, the suggested order quantity, …; the fixed thresholds that these texts name: 3 (R-6), 8 (R-15), 12 (R-15, R-16), and 100 and 104 (R-16)."
  - Problem: FR-26 c1 requires the explanation to cover "the order calculation line" and "every active warning and note". Two kinds of number in that content are not allowed numbers:
    - The order calculation line includes the unrounded result (FR-12, R-9): «= 10,77» for E4 and «= −40,00» for E6.
    - The FR-7 note reads «Uke 2 og 3 viser samme tall som uke 1 …». The horizon labels 1 and 2 are not allowed; 3 passes only because R-6's threshold is also 3.

    So the FR-27 test fails on a correct template, unless a value happens to coincide. Addendum §3 (Template approach) also lists "the inputs" and "the order calculation line" as template content.
  - Fix: add "the unrounded result on the order calculation line" to the first list, and "the horizon week labels 1, 2 and 3" to the second.

- **C-3 · §8.1 cut line against DR-8, FR-4 c3, DR-1 and DR-9.**
  - Quote: "SM-9 then lapses, DR-10 is reported as not built in the status table (DR-8) and the README, and SM-2 and SM-3 count as met on the local version."
  - Problem: the summary's "Done when" line, DR-10, SM-2, SM-3 and SM-9 agree with the cut line. Four statements do not follow it:
    - DR-8: "One table lists every FR with its priority …". DR-10 is not an FR, so the status table has no row to report it in.
    - FR-4 c3 (Must): "The published version keeps the same data in PostgreSQL, loaded with the same load command (DR-4)." It cannot be met once publishing stops, and the cut line does not release it.
    - DR-1 (Must, "needed to deliver the app") still requires "The address of the published version, and for the group the steps to publish it …".
    - DR-9: the final checklist still lists "SM-9" without the lapse.
  - Fix:
    - Cut line: add "FR-4 c3 lapses with it, and FR-4 is reported as partly built".
    - DR-8: "lists every FR, and DR-10, with its priority …".
    - DR-1: "… (DR-10), or, if the cut line in §8.1 applies, that publishing was not built and why."
    - DR-9: "SM-9 (unless the cut line in §8.1 applies)".

### Low

- **C-4 · FR-26 c3 and the §4.8 description against FR-27 c1.**
  - Quote: "Every number in the explanation comes from the calculation result." The §4.8 description says: "so it never contains a number that the calculation did not produce."
  - Problem: FR-27 now also allows the thresholds 3, 8, 12, 100 and 104, which no calculation produces. Two Must FRs in the same feature define the explanation's numbers differently.
  - Fix: FR-26 c3: "Every number in the explanation is an allowed number (FR-27)." §4.8: "… never contains a number other than the allowed numbers in FR-27."

- **C-5 · SM-1 and SM-7 "Validates" lines, copied into §8.5.**
  - Quote: SM-7 says "Validates FR-3 and FR-15 to FR-19, and FR-17b and FR-36 once they are built." §8.5 says "A dash means that no success metric covers the FR."
  - Problem: §8.5 matches §9 row for row, but three FRs are covered by a metric that does not list them:
    - FR-8: its insufficient-data warning is an active warning (R-15 item 5), so "every warning" in SM-7 covers it. SM-7 and the §8.5 row (SM-1 only) leave it out. This was XR-6 in `review-consistency.md` (2026-11-02) and is still open.
    - FR-24: c1 names E13 and E24, which are in SM-1's Must gate. SM-1 and the §8.5 row (SM-3 only) leave it out.
    - FR-14: its only consequence names E23, which is also in SM-1's Must gate. The §8.5 row shows "–".
  - Fix: add FR-8 to SM-7, add FR-24 to SM-1's Must list, add FR-14 to SM-1's "once they are built" list, and update the three §8.5 rows.

- **C-6 · FR-28 c3 and SM-6 against addendum §3.**
  - Quote: "rejects the rephrased text when a placeholder is missing, added, repeated or renamed, or when the text contains a number outside a placeholder."
  - Problem: the rule has two gaps.
    - "Repeated" reads as "appears more than once", but a template can name one value twice by design. For example, the 12 of the recent period can appear in the confidence label's reason and again in a recent-period warning. Addendum §3 states the rule as "placeholders differ from the template's".
    - Two placeholders that swap places pass every check in the list. That is the "real number in the wrong context" error, which addendum §3 ("Why each label and value are checked together") gives as the reason for the check. The previous SM-6 covered it ("attaches a number to a different label").
  - Fix: choose one.
    - In FR-28 and SM-6, write "when its placeholders differ from the template's in name, count or order". A rejected text falls back to the template, so a strict order check is safe.
    - Or keep the set check, and say in addendum §3 that it binds each value to its name but not to the words around it.

- **C-7 · FR-17b c2 against FR-19.**
  - Quote: "It does not change the confidence label, which FR-17 already sets."
  - Problem: FR-19 sets the label (R-16). FR-17 only makes the level shift count for it.
  - Fix: "It does not change the confidence label; FR-17 already counts the level shift for it."

- **C-8 · §3 Latest valid week (new) against §3 Latest data week.**
  - Quote: the new row says "The old-data warning counts the weeks from it to the latest data week". The existing row says of the latest data week: "the old-data warning counts from it".
  - Problem: the two rows give different starting points for the same count. FR-18 c1 calls the latest data week "the reference point".
  - Fix: in the new row, write "counts the weeks between it and the latest data week".

- **C-9 · Addendum §1 and the addendum frontmatter.**
  - Quote: "(PRD §0, DR-5, §10 question 6 and §12 → §7)". The frontmatter says `updated: '2026-11-03'`.
  - Problem: PRD §10 question 6 now only says that the task moved to DR-5, and it no longer points to addendum §7. The addendum changed on 2026-11-08 (§2) and on 2026-11-15 (§3 and §6), but its frontmatter still says 2026-11-03.
  - Fix: drop "§10 question 6" from the list, and set `updated: '2026-11-15'`.

- **C-10 · §12, row 2026-11-15.**
  - Quote: "…; §10 question 1 closed and question 6 moved to DR-5." The commit field says "(filled in at commit)".
  - Problem: §12 says that every change to a requirement is recorded. The row leaves out several changed items: DR-6 (Should order now in §8.2), DR-9 (SM-10 added to the checklist), DR-10 (cut-line bullet), SM-9 (lapse clause), the §3 Sales history definition, and the summary at the top (the 2026-11-08 row named the summary). The commit field is still a placeholder.
  - Fix: add those items to the row, and fill in the commit when the update is committed.

## 2. Checks with no inconsistency

- **IDs and counts.** FR-1 to FR-36 plus FR-17b make 37 FRs: 24 Must, 8 Should and 5 Could. They agree in §0, §4, §8.1 to §8.3, §8.5 and the summary.
  - The summary's counts hold: 17 rules, 15 of them Must (all but R-14 and R-17), and 30 reference examples, 24 of them in SM-1's Must gate.
  - Every SM, DR, AG, NFR, R and E reference in the changed text resolves.
  - Not counted: §8.1, SM-1 and SM-7 all use the range "FR-15 to FR-19" to exclude FR-17b, and SM-7 names FR-17b separately, but no sentence says so. One line in the §4 intro would settle it: "A range such as FR-15 to FR-19 does not include FR-17b." This matters downstream (D-3).
- **Priorities.** Each FR's own priority line matches its feature heading (Must, Must/Should, Must/Could or Should/Could), §8.1 to §8.3, §8.5, and the summary's Must, Should and Could lines. Within each feature, the Should and Could FRs follow the Must FRs, FR-17b included.
- **§8.5 against §9.** All 37 rows match the Validates lines of SM-1 to SM-10. C-5 lists the three gaps that §8.5 copies.
- **Cut line.** "Done when", DR-10, SM-2, SM-3 and SM-9 agree with §8.1. DR-10 says "If publishing does not work in time, the cut line in §8.1 applies", and SM-9 says "Lapses if the cut line in §8.1 applies". The milestone that the cut line points to exists in `sprint-status.yaml`: SM-3 and the Must scope are due by 2026-11-21. C-3 lists what the cut line misses.
- **Should order.** The §8.2 order is FR-9; FR-36 and FR-17b; FR-13 and FR-14; FR-29; FR-30; FR-28. It agrees with DR-6, §10 question 1, the summary, addendum §6 ("Sprint planning put it last") and the sprint-planning record (stories 5.1, 5.2, 5.3, 6.1, 6.2 and 7.1). Its rationale agrees with addendum §3 and §6.
- **SM-1 rule lists.** In §5, R-1 to R-13, R-15 and R-16 carry no Should tag, and R-14 and R-17 carry one. R-15's Should item 6 is tagged inside the rule. SM-1's Must examples match the "(Must)" tags in §5.7.
- **AG-1 to AG-5 and the glossary against FR-27, FR-28 and SM-6.** The placeholders enforce AG-1, and AG-3 points to FR-28's fallback list. AG-4 and §3 Explanation point to FR-27's label. Addendum §3 (Model's role, and the updated addendum note) describes the same placeholder design.
- **`[ASSUMPTION]` and `[NOTE FOR PM]`.** The eight tags (§3 Week, FR-17, FR-28, R-12, R-14, R-17, NFR-5 and NFR-8) match the eight §11 entries one to one, and the update added or removed none. No `[NOTE FOR PM]` is left.
  - Not counted: `.memlog.md` records five items of this update as pending user approval: the cut-line timing, the DR grouping, the Should-order rationale, SM-10 and the FR-28 placeholder rule. They are untagged in the PRD, which fits `status: draft`. Log their approval before the status goes back to final.
- **Glossary.** The changed text uses the §3 terms as defined: latest valid week, sales history and its length, valid week, recent period, active warning, note, confidence label, week-1 normal forecast, weeks of cover and calculation week.
  - Not counted: the summary and the cut line say "the local version", while NFR-1, NFR-8 and DR-10 say "the local app". Neither is a §3 term.
- **Outside this update (not counted).** Addendum §2 still says "one web application with one local file database (NFR-9, FR-4)" and "no … third-party accounts or internet connection when running (NFR-1)". Both statements are older than the 2026-11-08 Vercel change.

## 3. Downstream documents that now disagree with the PRD (not edited)

Eleven statements in three documents disagree with the PRD. DESIGN.md has none, and the Should order in `sprint-status.yaml` agrees with §8.2.

**EXPERIENCE.md**
- **D-1 · State Patterns, Level shift.** "The text «Etterspørselen ser ut til å ha endret nivå.» is added when that Should item is built (FR-17)." The text is now FR-17b.
- **D-2 · Component Patterns, Forklaring.** "It contains only numbers that are also shown above (FR-26, FR-27)." FR-27 now gives a closed list plus the thresholds 3, 8, 12, 100 and 104. Several numbers that this spine shows above the Forklaring are not on that list:
  - the horizon week «uke 46» (Voice and Tone says "Write «uke 46» in running text");
  - «uke 39: 31 stk» in the warning line;
  - «10,77» on the calculation line.

  Fix C-2 first, then align this line.

**ARCHITECTURE-SPINE.md**
- **D-3 · Frontmatter `binds` and the Capability map.** Neither `binds: [FR-1, …, FR-36, …]` nor "Warnings and confidence (FR-14 to FR-19, FR-36)" includes FR-17b.
- **D-4 · AD-10.** "Prevents: a number in the explanation that the calculation did not produce" and "with a 10 s timeout and the number-and-label check". FR-27 now also allows fixed thresholds. FR-28 now checks placeholders: a missing, added, repeated or renamed placeholder, or a number outside a placeholder.

**epics.md**
- **D-5 · FR-17 split.** FR-17 is now Must only, and its warning text is FR-17b (Should). The epics still treat the text as part of FR-17:
  - Requirements Inventory: "FR-17: … [Must for the calculation and the confidence label; Should for the warning text]".
  - FR Coverage Map: "Epic 5 (warning text)".
  - Epic 5: "FR-17 (warning text)".
  - Story 5.2: "(FR-17, warning text)".
- **D-6 · §10 references.** The order is now decided in §8.2, and the Brief update is a DR-5 task. Four places still cite the old §10 questions:
  - Epic List: "their order is set in sprint planning (PRD §10, question 1)".
  - Requirements Inventory: "Open questions to close during the build (PRD §10): the order of the Should items (sprint planning); … the Product Brief update".
  - DR-5 line: "(PRD §10, question 6)".
  - Story 4.3: "(PRD §10, questions 3 and 6)".
- **D-7 · SM-10.** The DR-9 line and Story 4.4 list a "manual checklist for NFR-6, NFR-7, NFR-8, NFR-11, SM-2 and SM-9", and the inventory says "SM-1 to SM-9 (targets)". DR-9 now includes SM-10, and no story covers SM-10.
- **D-8 · NFR-6.** The NFR-6 line says "no horizontal page scrolling from 1024 px; FR-25 content visible at 1366 × 768", and Story 4.2 checks "at 1024 px, 1366 × 768 and 1440 px". NFR-6 now also requires a check at 800 px.
- **D-9 · Story 3.3.** "it uses only values from the result" and "a number check confirms that every number in the text is also shown among the calculated numbers on the product screen (FR-27, SM-6)". FR-27 now defines the allowed numbers, thresholds included, and tests every template explanation against them.
- **D-10 · AR-8 and Story 7.1.** AR-8 says "the number-and-label check", and Story 7.1 says "Given a rephrased text in which a number, or the label attached to a number, differs from the template explanation". FR-28 now rejects a missing, added, repeated or renamed placeholder, or a number outside a placeholder. It also requires a test with a prepared answer for each fault, while Story 7.1 tests only the server failures.
- **D-11 · Cut line.** Under the cut line, SM-9 lapses and DR-10 is reported as not built, but the epics have no path for that case:
  - Story 4.1: "… and the published address".
  - Story 4.4: "verified on the final commit, both locally and published", and its SM-9 criterion.
  - Epic 4: "Requirements covered: … SM-9".

Not counted: Story 2.5 ("a product without a forecast shows the reason instead of a number") and Story 2.6 ("all active warnings and notes") keep the wording that the PRD replaced. They do not contradict the new FR-24 and FR-25 consequences, but they should adopt them.
