# Reconciliation: teacher's PRD feedback against the updated PRD

- **Input (wins on any difference):** `tilbakemelding-prd.md` in this folder. This is the teacher's formative feedback on the PRD, dated 2026-11-12 and written in Norwegian. The teacher reviewed the PRD at status `final`, last changed on 2026-11-08.
- **Checked:** `prd.md` (now status `draft`, updated 2026-11-15) and `addendum.md` in this folder. The update is the uncommitted diff against HEAD `42cfae9`. The commit field of the new §12 row still reads "(filled in at commit)".
- **Read only to verify claims (nothing changed):** `.memlog.md` in this folder, `_bmad-output/implementation-artifacts/sprint-status.yaml`, `_bmad-output/planning-artifacts/epics.md`, the UX `EXPERIENCE.md` and the architecture `ARCHITECTURE-SPINE.md`.
- **Status key:**
  - **Addressed:** the update meets the point and the concern behind it. "Addressed (kept)" marks praise or an observation that asked for no change, where the update left the praised part intact or changed it without harm.
  - **Partly addressed:** the requested change is made, but part of the concern is still open. A G-number names the gap (section 2).
  - **Not addressed:** neither a change nor any existing text meets the point.
  - **Deferred:** the feedback itself allows the point to wait (section 6, "Kan vente"), and the PRD keeps it open on purpose.
- **Overall:** the update acts on every proposal in section 4 and every mechanical finding in section 5. Of the 41 points:
  - 27 are addressed, 11 of them praise or observations that the update kept intact.
  - 9 are partly addressed.
  - None is unaddressed.
  - 5 are deferred, as the feedback allows.

  Two of the three items the teacher said must be settled before further work ("Må avklares") are still partly open: what the Must screen shows for a level shift (G1), and the set of allowed numbers (G2).

## 1. Point by point

### Section 2: what works well (praise, no change asked)

| # | Point (short) | Status | Evidence (PRD location and quote) | Note |
|---|---|---|---|---|
| 2.1 | Rules R-1 to R-17 and the answer key E1 to E30, including boundary cases (E5, E18 a) | Addressed (kept) | The §5.7 table is unchanged. R-16 was reworded only: "a sales history shorter than 104 weeks (stockout weeks included)" | The meaning is the same as before, and E29 a to g are unchanged. The rewording is the fix for 5.3b. |
| 2.2 | AI kept under control: AG-1 to AG-6 and the FR-28 fallback ("ingen API-nøkkel, betalt tjeneste eller internett") | Addressed (kept), with one change | AG-1 to AG-6 are unchanged. FR-28 still says "It needs no API key, paid service or internet connection", and the fallback bullet is unchanged | The update rewrote the FR-28 number check (4.2b). The new check is mechanical, but it no longer protects the context of a number (G3). |
| 2.3 | Honest scope: §7, the R-14 limitations, seasonal adjustment at Should, SM-C1 to SM-C3, and all eight `[ASSUMPTION]` tags in §11 | Addressed (kept) | §7, the §5.5 limitations and SM-C1 to SM-C3 are unchanged. There are 8 inline tags and 8 entries in §11 | §8.2 replaced the `[NOTE FOR PM]` with the decided order, and it still says "the Should items are at risk". |

### Section 3: assessment per dimension

| # | Dimension (rating) | Status | Evidence | Note |
|---|---|---|---|---|
| 3.1 | Decision clarity (strong) | Addressed (kept) | New named decisions: §8.1 "**Cut line for publishing.**" and §8.2 "**Order of the Should items (decided in sprint planning on 2026-11-08):**" | |
| 3.2 | Substance (strong) | Addressed (kept) | The persona, rules and NFRs are unchanged, apart from the wording changes in 4.4 | |
| 3.3 | Strategic coherence (strong) | Addressed (kept) | SM-10 now measures the thesis directly | See I-1. |
| 3.4 | Testability (strong; exceptions in 4.2 and 4.4) | Partly addressed | The exceptions the teacher named (FR-24, FR-25, NFR-6 and FR-27) now have testable wording | Templates that follow FR-26 fail the FR-27 test (G2). |
| 3.5 | Scope and boundaries (good; Must is large and Should is "at risk") | Addressed | The cut line in §8.1 and the ranked Should list in §8.2 | The size of the Must scope is unchanged. The teacher asked for a seam to cut along, not for a smaller Must scope. |
| 3.6 | Usability for the next phase (good; length and mixed priorities make extraction heavy) | Partly addressed | Mixed priorities are gone: FR-17b, the feature headings and the §8.5 table | The documents grew: the PRD from 14,399 to 15,508 words and the addendum from 5,582 to 5,607 (`wc -w`). G1 shows the consistency cost the teacher warned about in section 1. |
| 3.7 | Fit to the product (good; process requirements DR-5, DR-7 and DR-9 take up much space) | Partly addressed | §8.1 labels DR-3, DR-5, DR-7, DR-8 and DR-9 as "Process requirements that the group set itself" | The process requirements are labeled but not shortened. DR-5 gained the brief-update task and DR-9 gained SM-10. |

### Section 4: main improvements

| # | Proposal (short) | Status | Evidence (PRD location and quote) | Note |
|---|---|---|---|---|
| 4.1a | Add a cut line to §8.1: if DR-10 does not work by a given date, SM-9 lapses, and SM-2 and SM-3 count on the local version | Addressed | §8.1: "If the published version (DR-10) does not work by the time the rest of the Must scope passes SM-1 and SM-3 (the milestone in sprint planning), the group stops working on publishing. SM-9 then lapses, … and SM-2 and SM-3 count as met on the local version." The summary at the top, SM-9 ("Lapses if the cut line in §8.1 applies") and DR-10 follow | A deliberate difference: the trigger is a milestone, not a date. The remaining issues are in G5. |
| 4.1b | Mark which DRs are self-set process requirements and which are needed to deliver the app | Addressed | §8.1: "Needed to deliver the app: DR-1, DR-2, DR-4 and DR-6." / "Process requirements that the group set itself, so that the examiner can trace the work: DR-3, DR-5, DR-7, DR-8 and DR-9." / "Publishing (DR-10) is the group's own choice." | Every DR stays Must (G6, I-5). |
| 4.2a | Define the set of numbers allowed in the explanation | Partly addressed | FR-27: "The explanation contains only allowed numbers. A number is any figure in the text, including week numbers." The list ends with "the fixed thresholds that these texts name: 3 (R-6), 8 (R-15), 12 (R-15, R-16), and 100 and 104 (R-16)." The test "fails if one of them is not an allowed number for that product." SM-6 follows | The set is bounded and testable, which was the teacher's concern. But it leaves out two kinds of number that FR-26 makes the explanation contain, and FR-26 and §4.8 contradict it (G2). |
| 4.2b | Placeholders such as `{base_forecast}` that the app fills in; the test rejects a placeholder that is missing, swapped ("byttet") or added | Addressed | FR-28: "The model receives the template explanation with a named placeholder in place of each number, for example `{base_forecast}` …". It "rejects the rephrased text when a placeholder is missing, added, repeated or renamed, or when the text contains a number outside a placeholder. A test sends prepared answers with each of these faults …". SM-6 and the addendum §3 note follow | This goes beyond the teacher's example. Two placeholders that trade places still pass (G3). |
| 4.3a | Split FR-17 into a Must FR (calculation and confidence label) and FR-17b (Should, warning text) | Partly addressed | FR-17: "… and counts it for the confidence label. Priority: Must." FR-17b: "… the product screen shows the warning «Etterspørselen ser ut til å ha endret nivå.» Priority: Should." §8.2: "Level-shift warning text: FR-17b" | The split follows the proposal. But FR-25 and the glossary pull the level-shift message back into Must (G1). |
| 4.3b | Take priorities out of the feature headings, or write "(Should/Could)" | Addressed | §4 intro: "A feature's heading lists the priorities of its FRs, core priority first." Headings such as "4.3 Forecast Calculation (Must/Should)" and "4.9 Purchase Planning (Should/Could)" | All nine headings match the priorities of their FRs. Some Must FRs still contain clauses marked Should (G6). |
| 4.3c | Add a table FR → priority → SM to §8 | Addressed | §8.5: "Each FR has one priority. A dash means that no success metric covers the FR." The table has 37 rows | Every row was checked against the FR's priority line and the SMs' "Validates" lists. No mismatch. |
| 4.4a | FR-24: concrete display for a product without a forecast | Addressed | FR-24: "the week-1 normal forecast, suggested order quantity and weeks of cover columns show no value. Instead, they show the reason from FR-8 in Norwegian across the three columns, for example «Ingen prognose: færre enn 3 gyldige uker»." | A deliberate difference: there is no "–" in the order column. The wording follows the approved UX (section 3). The Norwegian text is only an example (G6). |
| 4.4b | NFR-6: at 800 px no text overlaps, and every control can be reached with the keyboard | Addressed | NFR-6: "At 800 pixels wide, no text overlaps or is cut off, and every control can be reached with the keyboard; wide tables may scroll inside their own frame." DR-9 runs NFR-6 on the final commit | |
| 4.4c | FR-25: "all active warnings" cannot be tested as written | Addressed | FR-25: "The screen lists every active warning and every note that R-15 gives the product, each with its Norwegian text, and no warning or note that does not apply." | The list is now bounded by R-15's closed list. This sentence is the cause of G1, and it lacks "for the FRs built". |
| 4.4d | FR-33 should get testable consequences before it is planned | Deferred | §4 intro: "Could FRs are stated in one sentence and get their consequences when they are planned." FR-33 is unchanged | Section 6 of the feedback allows this ("Konsekvenser for Could-FR-ene, til de planlegges"). |
| 4.5a | Decide question 1 (the order of the Should items) with a one-sentence rationale | Addressed | §10 Q1: "Decided: the order is in §8.2 (sprint planning, 2026-11-08)." §8.2 has the ordered list and the rationale: "Seasonal adjustment comes first because the Product Brief and the teacher asked for it, and the optional language model comes last because the template explanation already meets the need (FR-26)." DR-6, the summary and addendum §6 follow | The order differs from the teacher's example, which the teacher allowed. It matches `sprint-status.yaml`. The rationale explains only the first and last items. |
| 4.5b | Question 6 is a task, not a question | Addressed | §10 Q6: "Moved: this is a task, not a question, and it now stands in DR-5." DR-5: "After this PRD is approved, the group updates the Product Brief …" | |
| 4.5c | Add SM-10: two people outside the group can explain why a product has the confidence label «lav» | Addressed | SM-10: "Two people outside the group see the product screen of a test product with the confidence label «lav», and each can explain in their own words why it has that label. Checked by hand on the final commit and recorded in the QA log (DR-9)." The DR-9 checklist and §8.5 follow | It matches the example word for word, but the intent can still drop out (G4, I-1). |

### Section 5: mechanical findings

| # | Finding | Status | Evidence | Note |
|---|---|---|---|---|
| 5.1 | IDs are continuous, cross-references resolve, and the position of FR-35 and FR-36 is explained | Addressed (kept) | §4 intro: "FR-17b was split from FR-17 after the teacher's feedback (§12)". §0: "FR-1 to FR-36 and FR-17b". SM-10 follows SM-9 | The new references to FR-17b and SM-10 resolve. |
| 5.2 | All eight `[ASSUMPTION]` tags appear in §11, and the reverse | Addressed (kept) | 8 inline tags (§3 Week, FR-17, FR-28, R-12, R-14, R-17, NFR-5, NFR-8) and 8 entries in §11 | The new decisions that await approval are not tagged. The PRD's `draft` status covers them. |
| 5.3a | "Latest valid week" (FR-18, R-15) is missing from the glossary | Addressed | §3, new row "Latest valid week" (Siste gyldige uke): "The most recent valid week in a product's sales history. The old-data warning counts the weeks from it to the latest data week, by position in the sales history (R-15, FR-18)." | |
| 5.3b | R-16 uses "sales history" to mean a number of weeks, stockout weeks included | Addressed | §3, Sales history: "The length of the sales history is its number of weeks, stockout weeks included; R-16 counts it this way." R-16: "a sales history shorter than 104 weeks (stockout weeks included)" | |
| 5.4 | SM-1 says it validates R-1 to R-17, although R-14 and R-17 are Should | Addressed | SM-1: "For the Must scope, it validates … rules R-1 to R-13, R-15 and R-16. Once they are built, it also validates FR-9, FR-13 and FR-36, and rules R-14 and R-17." | This is the teacher's wording, and the FR list is split the same way. |
| 5.5 | The PRD is in English with a Norwegian UI, and the glossary handles this consistently | Addressed (kept) | The new glossary row has its Norwegian label, "Siste gyldige uke" | |
| 5.6 | No sensitive information | Addressed (kept) | The diff adds no names, e-mail addresses or local paths | The SM-10 entry in the QA log should not name the testers (G4). |

### Section 6: before you go further

| # | Point | Status | Evidence | Note |
|---|---|---|---|---|
| 6.M1 | Must be settled before UX, architecture and epics: the cut line and the order of the Should items | Addressed | See 4.1a and 4.5a | The epics, made on 2026-11-08, do not have either one yet (section 5). |
| 6.M2 | Must be settled: the definition of the allowed numbers in the explanation | Partly addressed | See 4.2a | G2. |
| 6.M3 | Must be settled: the split priorities in FR-17 | Partly addressed | See 4.3a | G1. |
| 6.K1 | Can wait: sources for the inventory rules (question 3) | Deferred | §10 Q3 is unchanged: "Textbook references are added if found; otherwise the gap is stated in the process documentation." | |
| 6.K2 | Can wait: the choice of language model (question 5) | Deferred | §10 Q5 and the "Model candidates" section of addendum §3 are unchanged | FR-28 is last in the Should order, so waiting fits the plan. |
| 6.K3 | Can wait: updating the brief (question 6) | Deferred | DR-5: "After this PRD is approved, the group updates the Product Brief …" | This is now a task, triggered by approval. |
| 6.K4 | Can wait: consequences for the Could FRs until they are planned | Deferred | §4 intro: "Could FRs … get their consequences when they are planned." | |
| 6.B | The brief feedback has been followed up; only the update of the brief itself is still open | Addressed (kept) | AG-1, R-7, R-8, R-10, E1 to E30, DR-6 and §7 are unchanged | The open part is 6.K3. |

### Section 7: reflection questions

| # | Question | Status | Evidence | Note |
|---|---|---|---|---|
| 7.1 | How did you decide that a project-defined rule (R-10, R-11, R-14, R-17) was good enough, and what would make you reject a rule the AI proposed? | Partly addressed | Text the update did not change: addendum §6, "Each rule entry gives why the PRD has the rule, the alternatives considered, and the PRD reference examples that test it."; the pass criterion in §10 Q4; and the DR-5 steering log of cases "where the group clarified, rejected or corrected AI output" | This is a reflection question, so no PRD change was needed. No document says when the group rejects a rule the AI proposed. The answer belongs in the process documentation (DR-5). |
| 7.2 | If the app and the spreadsheet disagree, who is right, and how do you find out why? | Partly addressed | Text the update did not change: §5, "those examples are the answer key (fasit) for the tests (DR-3)"; DR-3, "The automated tests use the same inputs and expected results"; and DR-9, which records defects found by "the reference spreadsheet" | The spreadsheet is the answer key, but no rule covers the case where the spreadsheet itself is wrong, and no rule says how a disagreement is traced. E5's rounding case shows that settling one can need a rule of its own (R-9). One sentence in DR-3 would settle it: the rule text in §5 decides; the group recalculates the case by hand, fixes whichever side is wrong and records it in the QA log (DR-9); an unclear rule is changed through §12. |

## 2. Gaps

**G1. The PRD does not define what the Must product screen shows for a level shift** (4.3a, 4.4c, 6.M3).
- FR-17 is now Must, and FR-17b holds "the warning «Etterspørselen ser ut til å ha endret nivå.»" as Should.
- But the new FR-25 consequence, which is Must, says that "The screen lists every active warning and every note that R-15 gives the product, each with its Norwegian text".
- R-15 item 3 makes "A level shift with at least one level-shift week in the recent period (FR-17)" an active warning.
- The glossary defines a warning as "A message about the data behind a forecast …" and marks only the seasonal pattern "(Should)". Its Level shift row also says "reported with a warning".

A story for FR-25 must therefore either build the FR-17b text, which pulls a Should item into Must, or use a text the PRD does not define. That is the disagreement about "what counts as done" that 4.3 set out to remove. The epics already assume that the Must screen shows no level-shift message ("a level shift counts for the label even though its dedicated warning text comes in Epic 5", story 2.4), and FR-25 now contradicts that.

There are two ways to fix it:
- Add "for the FRs built" to FR-25 and say that, until FR-17b is built, a level shift shows only as its chart markers and in the confidence label's reason. Mark the same in the glossary rows.
- Or make the one-sentence warning text Must and drop FR-17b.

"For the FRs built" would also fix FR-25's notes, because R-15 also lists notes from FR-9 and FR-14 (Should) and FR-33 (Could).

**G2. The allowed-number set in FR-27 is incomplete against FR-26, and FR-26 contradicts it** (4.2a, 6.M2, 3.4). FR-26 requires the explanation to cover "every active warning and note (R-15) … and the order calculation line". Two kinds of number that this content naturally contains are not in the FR-27 list:
- **The unrounded result on the order calculation line.** FR-12 shows it, and R-9 sets "the unrounded result on the order calculation line with two decimals". Examples are «10,77» in the E4 line, «−40,00» in the E6 line and «0,07» in the E21 line. The opening clause of FR-27 ("the values in the product's calculation result that the product screen shows") could be read to include it, but the list after the colon leaves it out, so whoever writes the test has to guess.
- **The forecast-horizon positions in the FR-7 note**, «Uke 2 og 3 viser samme tall som uke 1 …». The 3 passes only by coincidence, through R-6's threshold. The 1 and the 2 pass only for products that happen to have a count of 1 or 2, so the test result would depend on the data.

A template that repeats the order line or the FR-7 note fails the FR-27 test. The same goes for R-10's factor 2, if a template explains why a week is unusual.

FR-26 is also inconsistent with FR-27:
- FR-26 still says "Every number in the explanation comes from the calculation result".
- §4.8 says the explanation "never contains a number that the calculation did not produce".
- FR-27 allows the fixed thresholds 3, 8, 12, 100 and 104, which the calculation does not produce.

A possible fix:
- Add "the unrounded result on the order calculation line" and "the positions 1 to 3 of the forecast horizon" to FR-27, or state that the templates leave them out.
- Change the FR-26 bullet to "Every number in the explanation is an allowed number (FR-27)".

**G3. The placeholder check no longer protects the context of a number** (4.2b, 2.2).
- **Before the update:** FR-28 rejected text "if any number, or the label attached to a number, differs from the template explanation", and SM-6 rejected text that "attaches a number to a different label".
- **Now:** FR-28 and SM-6 reject only text where a placeholder is "missing, added, repeated or renamed", or text that has "a number outside a placeholder".
- **The hole:** if the model moves `{stock_on_hand}` into the sentence about the forecast, or swaps two placeholders, every check passes, and the app inserts the right value under the wrong words.

Addendum §3 names this as the most common error ("a real number in the wrong context" [D2]), and its bullet still starts with "Why each label and value are checked together (FR-28)". FR-28's rule that "each placeholder's name is the label of its number" ties a name to its value, but not the name to the words around it.

A possible fix: require each placeholder to stay in the sentence it had in the template, with the sentence order kept. Or state the limit openly in FR-28 and the addendum. Separately, "repeated" should mean "more often than in the template". The addendum's phrase "placeholders differ from the template's" says this better.

**G4. The check that users understand the label (SM-10) can drop out of the build** (4.5c, I-1). SM-10 adopts the teacher's example, but nothing makes it drive any work:
- **Timing:** it is "Checked by hand on the final commit", when a failure can no longer change anything.
- **Coverage:** it covers only «lav», although «middels» is the label with the most possible reasons (R-16 step 2).
- **No pass rule:** nothing says what counts as a correct explanation, for example that each person names the deciding condition in R-16.
- **No story:** no FR consequence carries it, and the epics take their acceptance criteria from FR consequences (§0), so no story fails if users do not understand the label.

A possible fix:
- Also run SM-10 at the Must milestone.
- Define a pass as "names the deciding condition".
- Consider adding a product with «middels».
- Record the result without the testers' names (NFR-4).

**G5. The cut line is weaker than the teacher's date, and it is not carried through to FR-4** (4.1a, I-4).
- **The trigger:** "by the time the rest of the Must scope passes SM-1 and SM-3 (the milestone in sprint planning)" can mean the planned date of that milestone or the moment the Must scope actually passes. Read the second way, the cut slips whenever the Must scope slips, and publishing keeps competing with the core flow. That is the risk the teacher's "[dato]" closed. `sprint-status.yaml` gives the planned date: "by 11-21-2026: epic 3 done; SM-3 passes (Must scope complete)".
- **The status table:** the cut line says "DR-10 is reported as not built in the status table (DR-8)", but the DR-8 table "lists every FR", not the DRs.
- **FR-4:** this Must FR, mapped to SM-9 in §8.5, still requires "The published version keeps the same data in PostgreSQL". The cut line does not release that requirement.

A possible fix: write "by the planned date of that milestone", and have the status table report FR-4 as "changed" (local database only).

**G6. Minor points.**
- **FR-24:** the text is "for example «Ingen prognose: færre enn 3 gyldige uker»", and FR-8 fixes no Norwegian wording. A test can check the three columns and that no number appears, but not an exact string.
- **FR-25:** in "each with its Norwegian text", the PRD fixes no text for the stockout, unusual-week, old-data and insufficient-data warnings, so the UX documents supply them.
- **NFR-6:** only 800 px is named. That the rule also holds between 800 and 1024 px is implied, not stated.
- **Should clauses inside Must FRs:** examples are FR-35, "With seasonal adjustment on (Should) …", the seasonal rows in FR-20 and FR-21, and "(when FR-28 is built)" in FR-27. They are clearly marked, but every story must leave them out.
- **DR labels:** the §8.1 labels change nothing in practice, because every DR stays Must. DR-3 is labeled self-set, but SM-1 ("match the reference spreadsheet (DR-3)") and FR-3 depend on it, so it cannot be cut.
- **Addendum metadata:** the addendum's frontmatter still says `updated: '2026-11-03'`, although it was edited on 2026-11-08 and on 2026-11-15.

## 3. Deliberate differences from the teacher's examples

| Point | Teacher's example | PRD wording | Underlying concern met? |
|---|---|---|---|
| 4.1a | "ikke fungerer innen [dato]" | "does not work by the time the rest of the Must scope passes SM-1 and SM-3 (the milestone in sprint planning)" | Yes, if the milestone's planned date is meant (2026-11-21 in `sprint-status.yaml`). The memlog records that dates stay in sprint planning on purpose. See G5. |
| 4.2a | The fields of `CalculationResult`, plus 12 and 8 | The values of the calculation result that the screen shows, listed by meaning, plus 3, 8, 12, 100 and 104, with no code name | The set is bounded, which was the concern. Keeping code names out of the PRD is consistent with the rest of it (the architecture calls the object `ProductResult`). The set leaves out two kinds of number (G2). |
| 4.2b | Reject a placeholder that is missing, swapped ("byttet") or added | Missing, added, repeated or renamed, or a number outside a placeholder, plus a test with prepared faulty answers | Yes for the teacher's list. Two placeholders that trade places are not caught (G3). |
| 4.3a | "FR-17 Nivåskifte i beregning og tillitsmerke (Must)" and "FR-17b Eget varsel for nivåskifte (Should)" | "FR-17: Level shift" (Must) and "FR-17b: Level-shift warning text" (Should) | The split, yes. FR-25 reopens the question (G1). |
| 4.3b | Take priorities out of the headings, or write "(Should/Could)" | The second option: "(Must/Should)", "(Must/Could)" and "(Should/Could)" | Yes. All nine headings match their FRs. |
| 4.4a | The forecast column shows «Ingen prognose: færre enn 3 gyldige uker», and the order column shows "–" | The three number columns show no value, and the FR-8 reason spans all three | Yes. This follows the approved UX (`EXPERIENCE.md`, product table: "A product without a forecast shows its reason across the three number columns (FR-24)") and covers both reasons in FR-8. |
| 4.4b | At 800 px: no overlap, and every control can be reached with the keyboard | The same, plus "or is cut off" and "wide tables may scroll inside their own frame" | Yes. |
| 4.5a | "FR-29/30 → FR-9/36 → FR-28", or another order | FR-9; FR-36 and FR-17b; FR-13 and FR-14; FR-29; FR-30; FR-28 | Yes (the teacher allowed another order). The order matches `sprint-status.yaml` and puts the seasonal adjustment the brief asked for first. |
| 4.5c | SM-10 as in the example | The same, plus "in their own words", "on the final commit" and the QA log | Yes, word for word. See G4. |

## 4. Qualitative intents the FR structure could silently drop

- **I-1. Users understand the confidence label (the thesis, 4.5).** The thesis is that the numbers say when they should not be trusted, and that only helps if the reader understands the label. Only SM-10 carries this intent, and SM-10 sits outside every FR and story. At risk through G4.
- **I-2. Each number stays tied to what it describes (4.2, addendum §3).** The old FR-28 and SM-6 wording carried this intent. The new mechanical check keeps only the link between a placeholder's name and its value. At risk through G3.
- **I-3. The explanation lets the user follow the order calculation by hand (the thesis, FR-26).** If the templates are trimmed until the FR-27 test passes, the unrounded result and the references to weeks 1 to 3 drop out of the explanation without anyone deciding it. At risk through G2.
- **I-4. Publishing has a time limit, so it cannot crowd out the core flow (4.1).** At risk through G5, if the milestone is read as the event rather than its date.
- **I-5. The self-set process requirements are where the group can cut under time pressure (4.1).** The labels exist, but no rule says what may be reduced, for example the "at least five cases" in DR-5. If keeping every DR is intended, nothing is lost. If not, the labels are information only.

## 5. Downstream documents still on the old wording (not edited)

PRD §12 applies the change-log rule to these documents too.

- **`epics.md`:**
  - FR-17 is still split inside one FR ("[Must for the calculation and the confidence label; Should for the warning text]", and "FR-17 (warning text)" in Epic 5 and story 5.2) instead of naming FR-17b.
  - Story 2.5 still says the FR-24 product "shows the reason instead of a number".
  - Story 3.3 still has the old FR-27 check, that "every number in the text is also shown among the calculated numbers on the product screen".
  - The requirements list stops at "SM-1 to SM-9", and the DR-9 checklist in story 4.4 has no SM-10.
  - The Epic List still says the Should order "is set in sprint planning (PRD §10, question 1)".
  - There is no cut line.
- **`ARCHITECTURE-SPINE.md`, AD-10:**
  - "Prevents: a number in the explanation that the calculation did not produce" conflicts with the thresholds that FR-27 allows.
  - "the number-and-label check" is the old FR-28 wording.
  - The binds list has no FR-17b.
- **`sprint-status.yaml`:** the Should order already matches §8.2, so no change is needed.
- **Pending approval:** the memlog lists the cut line, the DR grouping, the rationale for the Should order, SM-10 and the placeholder rule as awaiting the user's approval. The PRD stays `draft` until then.

## 6. How the checks were made

- Every claim was read in the working-tree PRD and addendum. The text before the update comes from `git diff` against HEAD `42cfae9`.
- **`[ASSUMPTION]` tags:** the search found 9 matches. One is the reference line in §0, which leaves 8 inline tags, and §11 lists 8.
- **§8.5 table:** each of the 37 rows was checked against the FR's priority line and the SMs' "Validates" lists. There is no mismatch.
- **Feature headings:** all nine were checked against the priorities of their FRs.
- **Should order:** compared with the milestone comment in `sprint-status.yaml`. Stories 5.1, 5.2, 5.3, 6.1, 6.2 and 7.1 map to FR-9; FR-36 and FR-17b; FR-13 and FR-14; FR-29; FR-30; and FR-28.
- **FR-24:** compared with the product-table row in `EXPERIENCE.md`.
- **FR-27:** checked by hand against the order calculation lines of E4, E6 and E21, and against the FR-7 note.
- **Word counts:** measured with `wc -w`.
- **Sensitive data:** the diff was searched for names, e-mail addresses and local paths. None were found.
