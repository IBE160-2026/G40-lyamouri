# PRD Quality Review — Prognose (G40-lyamouri)

*Scope: `prd.md` (status `draft`, updated 2026-11-15, uncommitted working copy after the teacher's feedback) and `addendum.md`. Reviewed 2026-11-15 against the bmad-prd quality rubric. All 30 reference examples were recomputed from the rules as written. The downstream documents were checked only where the PRD's changes touch them.*

## Overall verdict

The PRD is still strong: its thesis (numbers the user can check by hand, plus honest trust signals) drives the priorities, every rule carries a source tag, all 30 reference examples recompute exactly, and the 2026-11-15 update gives every FR one priority (§8.5, FR-17b) and makes FR-24, FR-25 and NFR-6 testable. The risk is in the hand-off rather than the content: the update has not reached the epics and the architecture spine that the build will follow, and FR-27's new allowed-number set rejects numbers that FR-26 and the approved UX put into the explanation. The schedule decisions are softer than the rule decisions, with a cut line that covers only publishing and fires on an event rather than a date, and five changes that the decision log marks as pending approval left untagged.

## Decision-readiness — adequate

At the rule level, the PRD states its decisions as decisions and says what each one gave up:
- R-4 starts from the first calculation week, which addendum §6 chooses because "it can be checked by hand".
- R-7 says it is "not a statistical interval".
- R-8 lists what it assumes away ("weekly review, no lead time, no orders already on the way").
- §7 gives reasons, not just exclusions ("each new signal would need its own rules and test data").
- Addendum §6 records the alternatives considered for the main rules (R-1, R-4, R-7, R-8, R-10 and R-11, R-12, R-14, R-16).

The update closes §10 question 1 by recording the Should order in §8.2. That order matches `sprint-status.yaml` (5.1, 5.2, 5.3, 6.1, 6.2, 7.1).

The schedule-level decisions the teacher asked for (feedback 4.1) are only half made. One cut line exists, for publishing. The DR grouping names which DRs are self-imposed but gives that label no consequence. The only `[NOTE FOR PM]`, at the deadline tension in §8.2, was removed in the same update, although the tension remains. Two other 2026-11-15 changes trade something away without saying so: the FR-28 check and the pass criterion in question 4.

### Findings
- **medium** The cut line covers only publishing, and it fires on an event, not a date (§8.1 "Cut line for publishing" and the DR grouping; DR-6) — The trigger reads "If the published version (DR-10) does not work by the time the rest of the Must scope passes SM-1 and SM-3 (the milestone in sprint planning)". Two problems:
  - **The trigger slips with the work it protects.** The trigger is the same progress the cut is meant to protect. If the Must scope slips, the cut slips too, and publishing keeps using time. The parenthesis leaves open whether the date (2026-11-21 in `sprint-status.yaml`) or the event decides. That file, last updated 2026-11-08, still lists every story as backlog, and its first milestone (2026-11-11, "epic 1 done and published on Vercel") has passed.
  - **The DR grouping is not a seam.** The grouping labels DR-3, DR-5, DR-7, DR-8 and DR-9 as "Process requirements that the group set itself" but attaches no consequence. Read as a cut list, it would be wrong. SM-1, the Must gate, requires results to "match the reference spreadsheet (DR-3)", and the DR-9 QA log holds the evidence for SM-2, SM-9 and SM-10. All 11 NFRs and every DR remain Must, so publishing is still the only part that can be cut.

  *Fix:* Make the trigger a date: "on the SM-3 milestone date in sprint planning, or when SM-1 and SM-3 pass, whichever comes first". Then do one of two things:
  - Name what gives way first among the process DRs, for example DR-5's minimum of five steering-log cases or DR-7's branch-per-story rule, but never DR-3 or DR-9.
  - Or state plainly that nothing else can be cut, and keep that as a `[NOTE FOR PM]`.
- **medium** FR-28's new placeholder check no longer catches the error it exists for, and neither document says so (FR-28; SM-6; addendum §3) — The update replaced "rejects the rephrased text if any number, or the label attached to a number, differs" with a rejection "when a placeholder is missing, added, repeated or renamed, or when the text contains a number outside a placeholder". That is mechanical, as the teacher asked. But it accepts a text that moves a placeholder into the wrong sentence, such as «Lagerbeholdningen er {base_forecast} enheter»: every placeholder is present exactly once, so the text passes.

  This is the "real number in the wrong context" error that addendum §3 calls the most common ("context mismatch 1.59 to 3.28%, against fabrication 0 to 0.81%"). The addendum still says "A check that every number appears somewhere in the input misses that error", and a set-equality check on placeholders is that check. The new addendum note calls the scheme "an exact-equality policy". That is true of the values, not of the context they sit in.

  *Fix:* Add a cheap order rule, for example "the placeholders appear in the same order as in the template", which catches swaps. Then state the remaining risk in FR-28 or addendum §3: a placeholder that keeps its order but sits in a sentence that misdescribes it is not detected, and the «KI-omformulert forklaring» label is the mitigation.
- **medium** Question 4's pass criterion tests the code, not the rule (§10 question 4; FR-17 `[ASSUMPTION]`; FR-3; §5.5) — Q4 asks "Do R-10, R-11, R-14 and R-17 behave as expected on the test products?" Its pass criterion is that "for every rule test product, the app's results equal the expected results in the reference spreadsheet (DR-3)".

  The spreadsheet is a hand calculation of those same rules, because FR-3 builds the rule test products from the E-series. So the criterion repeats SM-1. It can show that the code matches the rule, never that the rule misbehaves. FR-17's assumption promises validation "with the level-shift and seasonal test products". Those are pattern products, which the criterion does not cover, and §5.5 already predicts trouble there: "the seasonal test product can show level-shift markers every season", and trend "is mistaken for season". No fallback is named if a rule fails. This is also the teacher's first reflection question: how did the group decide that a rule was good enough?

  *Fix:* Judge the pattern products against the generator's known truth rather than the rules. That means the week where the level shift was generated, whether a seasonal pattern exists, and whether the trend product gets flagged as seasonal. Write the expected classification next to each pattern product in DR-3, and name one fallback per rule. For example, if R-11 marks seasonal peaks as a level shift, it stays a stated limitation; if R-17 flags the trend product as seasonal, raise the threshold or drop FR-36.
- **low** The Should order says why FR-9 comes first, not what it puts at risk (§8.2 "Order of the Should items"; FR-36; addendum §6) — FR-9 is first "because the Product Brief and the teacher asked for it". In a graded course that is a legitimate reason. But FR-9 is also the costliest item: addendum §6 calls R-14 "the most demanding rule". Sprint planning gives the whole Should list (eight FRs in six steps) 2026-11-22 to 11-27. If FR-9 overruns, two things are at risk:
  - FR-36, the trust signal for seasonal products, which "can be built before FR-9" by its own text;
  - FR-29 and FR-30, which complete UJ-1 steps 5 and 6, where Mounia "leaves the session with an order quantity decided for every product".

  *Fix:* Add one sentence that names this risk and time-boxes FR-9. Alternatively, move FR-36 ahead of FR-9: it is cheap, it serves the thesis directly, and it leaves the rest of the order unchanged.

## Substance over theater — strong

Nothing reads as furniture:
- **Persona.** There is one, and her context drives requirements. Mounia's weekly ordering gives R-8 its one-week basis. The office PC gives NFR-6 its desktop bound. The "20 minutes before the purchasing meeting" gives R-12's sorted overview and FR-25's above-the-fold rule at 1366 × 768.
- **NFRs.** They carry bounds, not adjectives. NFR-6 sets 1024 and 800 px, NFR-7 requires markings that "differ by more than color alone", and NFR-11 requires WCAG 2.2 AA with a table alternative for the chart.
- **Vision.** The differentiator now names the checks, not transparency alone ("transparency with built-in checks ... leaves out stockout weeks, flags unusual sales, notices when demand moves to a new level").
- **Guardrails and claims.** Every AI guardrail traces to an FR. The at-a-glance claim "17 deterministic rules (15 of them in the Must scope) checked by 30 reference examples (24 of them for the Must scope)" is exact.
- **The update's additions.** SM-10 and §8.5 both do real work.

The one remaining adjective is NFR-8's "ordinary laptop". In practice it is bounded only by the machine named in the DR-9 checklist, which is minor.

## Strategic coherence — strong

The thesis is explicit in §1: "transparency with built-in checks", and the system "says when a forecast should not be trusted". The Must line follows from it:
- **Must:** the calculation display (FR-12, FR-35), the data-quality rules and the confidence label (FR-15 to FR-19), and the template explanation (FR-26, FR-27).
- **Should or Could:** seasonal adjustment, the language model and purchase planning.

SM-1 validates the calculation half of the thesis. The new SM-10 is the first metric aimed at the trust half, as the teacher asked. The counter-metrics are pointed: SM-C3 forbids weakening warnings to raise the share of «høy». The MVP is a problem-solving scope, and its logic matches. The Vision promises only what the Must scope holds: templates, with an optional local model. The one place where priority follows requests more than the thesis is the Should order (see Decision-readiness).

### Findings
- **low** SM-10 can pass by reading the reason aloud (§9 SM-10; FR-19) — FR-19 prints the reason with the label: "The reason names the condition that decided the label". «Lav» is also the simplest label, usually "fewer than 12 valid weeks" or "no forecast". A tester who restates «Lav: …» in their own words passes. SM-10 therefore measures whether the reason text is readable, not whether the label would change what a buyer does. *Fix:*
  - Use a «middels» product whose reason lists a warning.
  - Ask two questions: why the product has that label, and whether the tester would order the suggested quantity as it stands.
  - Optionally, ask the tester to reproduce the base forecast from the forecast calculation (FR-35). That one step tests the "check by hand" half of the thesis too.
  - Write down the passing answer before the test.

## Done-ness clarity — adequate

Where the PRD is precise, it is exemplary, and its answer key is correct. All 30 reference examples were recomputed for this review from the rules as written: the single forward pass in R-10 and R-11, R-9's 6-decimal step, and R-14 at full precision. Every result matches, including:
- E5's 70.00000000000001 → 70;
- E15's 70.333 and 51.0;
- E17's 21.404 (16.256 with zeros);
- E27's 7.080 → 8 and its "wrongly give 18".

The update fixes the teacher's adjective items:
- FR-24 names the three columns and the text.
- FR-25 lists exactly the R-15 warnings and notes.
- NFR-6 is testable at 800 px.

The gaps cluster around the explanation and the hand-check display. That is where the thesis lives, and where an AI story writer would encode the text literally.

### Findings
- **medium** FR-27's allowed numbers exclude numbers that FR-26 and the approved UX put in the explanation (FR-26; FR-27; FR-7; FR-12; UX `EXPERIENCE.md` "Calculation display rules") — FR-26 requires the explanation to cover "every active warning and note (R-15) … and the order calculation line". FR-27 counts "any figure in the text, including week numbers", and its test "fails if one of them is not an allowed number for that product". The allowed set misses:
  - **The unrounded order result.** FR-12 makes it part of the line ("10,77", "−40,00", "0,07").
  - **The figures in the fixed FR-7 note.** The note reads «Uke 2 og 3 viser samme tall som uke 1 …». Only 3 is allowed, as R-6's threshold, so 2 and 1 fail for any product where no count happens to equal them.
  - **The horizon's calendar week numbers.** The UX shows them as «Uke 1 · uke 46».
  - **Other listed week numbers.** The week numbers of included unusual weeks and of level-shift weeks are not allowed; only "the week numbers of the weeks left out" are.
  - **The sales figure in the UX warning.** The format is «1 uvanlig uke (uke 39: 31 stk)».
  - **A year,** if weeks are shown with the year that §3 makes part of their identity.

  The test therefore fails on correct template text, unless template writers follow word-avoidance rules that nobody wrote down. *Fix:*
  - Define the allowed set as "every number the product screen renders for this product, taken from the same result object, plus the fixed thresholds". That is mechanical and matches the original intent.
  - Require the FR-7 note and the full order calculation line in the snapshot tests, so the set is proven against real templates.
  - State how the test parses numbers: decimal comma, and any thousands grouping.
- **low** FR-35's line can disagree with a hand check from the numbers it shows (FR-35; R-9; FR-12) — FR-12 warns «Tallene er avrundet for visning.», but FR-35 does not. For exponential smoothing, the line shows the previous level with one decimal. With a previous level of 13.24 and sales of 15, the screen shows «0,3 × 15 + 0,7 × 13,2 = 13,8», from the true 13.768. Computed from the shown numbers, the result is 13,74, which rounds to 13,7. E2 and E17 happen not to expose this. R-9 also has no display rule for the seasonal indices and adjusted values that FR-35 shows when seasonal adjustment is on. E14 uses 4 and 3 decimals, and the UX rounding rule is silent too. *Fix:* Add FR-12's rounding sentence to FR-35, or show the previous level with two decimals. Then give seasonal indices 4 decimals and adjusted values 1 decimal in R-9.
- **low** E30 cannot show that the seasonal-pattern warning affects the label (FR-36; E30; R-16) — FR-36's first consequence is that the warning "counts as an active warning for the confidence label". E30 checks it as "label at most «middels»". But E14's data has 8 valid weeks, so R-16 step 1 gives «lav» whether or not the warning exists. *Fix:* Add an E29-style row: 104 weeks, all valid, a seasonal pattern by R-17 with no peak in the recent period, and no other active warning. With seasonal adjustment off the label is «middels»; with it on, «høy».
- **low** Weeks listed by week number are ambiguous over a 104-week history (FR-15; FR-16; FR-35; R-15; §3 Week) — §3 identifies a week "by year and week number". Yet FR-15 lists stockout weeks "by week number", and FR-16 does the same for excluded unusual weeks. FR-35's exponential-smoothing table covers every calculation week. Over 104 weeks, every week number occurs twice, and R-15 keeps listing weeks from before the recent period. A tester cannot tell which «uke 10» is meant, and neither can a user checking by hand. *Fix:* Show weeks with their year (for example «uke 10/2025») wherever a list can reach past the recent period. Add the year to FR-27's allowed numbers.
- **low** Smaller behaviors are left to the implementer (FR-25; R-12; FR-21; NFR-8; "Version 1 at a glance") — Five gaps:
  - **Warning texts.** FR-25 checks every warning "with its Norwegian text", but no text is fixed for the stockout, unusual-week and old-data warnings or the FR-9 note. `EXPERIENCE.md` only describes the old-data warning, as "A warning with the number of weeks since the latest valid week".
  - **Sorting.** R-12 gives no order inside group 2, the products without a forecast.
  - **FR-21 expected values.** Four of FR-21's seven rows give no expected new value (for example "E1 with window 4 instead of 3"). The SM-3 test therefore passes on any change, including a wrong one. The values are 14.0, 14.133, 17.2/11.467 and 17.
  - **Timeouts.** NFR-8's 2-second update target conflicts with FR-28's 10-second timeout `[ASSUMPTION]` when the local model is on.
  - **Definition of done.** "Done when" names only SM-1, SM-2, SM-3 and SM-9, so it omits SM-4 (isolation) and SM-6 (explanation integrity). §4 defines Must as "version 1 is not done without it".

  *Fix:*
  - Add a table of the Must warning texts to R-15, or name `EXPERIENCE.md` as the copy source.
  - Sort group 2 by product number.
  - Add the four expected values to FR-21.
  - Exempt the model path from NFR-8, or set its timeout below 2 seconds.
  - Make "Done when" read "every Must FR passes its consequences, and SM-1 to SM-10 hold as they apply".

## Scope honesty — adequate

§7 is a real non-goals list. The read-only data, the absence of low-sales flagging, and the missing lead time and statistical safety stock are all explicit. §8.2 says plainly that the Should items "are at risk", and DR-1 and DR-8 require every unbuilt Should item to be listed with its reason. All 8 inline `[ASSUMPTION]` tags appear in §11, which also indexes every project-defined rule by source status.

Open-items density is moderate for a PRD about to drive a build with 16 days left: 4 open questions (Q2 to Q5) and 8 assumptions, none of which can reshape scope. The gap is the status of the update itself.

### Findings
- **medium** Five changes awaiting approval are presented as settled, and the document's status contradicts itself (frontmatter; §12 opening line; §8.1; §8.2; SM-10; FR-28) — The decision log (`.memlog.md`, 2026-11-15) records five items as "Pending user approval", and the PRD tags none of them:
  - the cut line tied to the milestone rather than a fixed date;
  - the DR grouping;
  - the one-sentence rationale for the Should order, which the log says was "not documented before";
  - SM-10;
  - the FR-28 placeholder rule.

  The only `[NOTE FOR PM]` was removed in the same update. The frontmatter says `status: draft`, while §12 opens with "This PRD was approved and set to final on 2026-11-03", and nothing in the PRD explains the difference. The teacher, a downstream agent or any other reader cannot tell which of the 2026-11-15 changes are confirmed. *Fix:* Either approve the five items, return the status to `final` and fill in the §12 commit, or tag each one `[ASSUMPTION: pending approval]` and index it in §11. In both cases, add one sentence after §12's first line: "Set to draft on 2026-11-15 while the changes below await approval."

## Downstream usability — adequate

Inside the document, extraction is clean:
- The binding bilingual glossary gained "latest valid week" and a precise "length of the sales history".
- All ID sets are contiguous, and every FR reference resolves.
- The new §8.5 FR → priority → SM table agrees, row for row, with every SM's "Validates" line.
- Cross-references use § numbers and IDs, never "see above".

The PRD no longer sits at the top of an unbuilt chain, though. UX (2026-11-06), the architecture spine (2026-11-08), `epics.md` and `sprint-status.yaml` were all derived from the 2026-11-08 version, and this update changes requirements they already encode.

### Findings
- **high** The update does not say which downstream documents it changes, and those documents now contradict it (§12, row 2026-11-15; DR-5 "The change-log rule in §12 also applies to the architecture, UX and epics documents") — Checked against the current files:
  - **FR-17.** `epics.md` still gives it "Must for the calculation and the confidence label; Should for the warning text" and maps "FR-17 (warning text)" to Epic 5 (stories 2.4 and 5.2). FR-17b does not exist there.
  - **Story 3.3** still tests the superseded FR-27: "every number in the text is also shown among the calculated numbers on the product screen".
  - **Story 7.1** still rejects text in which "a number, or the label attached to a number, differs".
  - **SM-10.** The requirements inventory lists "SM-1 to SM-9", and both the DR-9 summary and Story 4.4's manual checklist omit SM-10, so no story owns the new two-person check.
  - **Open questions.** `epics.md` still lists "the order of the Should items" and "the Product Brief update" as open.
  - **Architecture.** AD-10 in `ARCHITECTURE-SPINE.md` still names "the number-and-label check".

  The build works from the stories, so these PRD fixes will not reach the code unless someone carries them over. The §12 row lists what changed in the PRD, not what it affects downstream. *Fix:* Add an "Affects" column to §12, or one line under the 2026-11-15 row, naming:
  - the `epics.md` FR inventory and coverage map;
  - stories 2.4, 3.3, 4.4, 5.2 and 7.1;
  - AD-10.

  Update those documents under DR-5's change-log rule before any of those stories starts.

## Shape fit — strong

The shape matches a single-operator planning tool whose correctness is graded:
- one journey with a named protagonist, which now includes the settings change that SM-3 tests (UJ-1 step 4);
- a capability spec with testable consequences;
- a calculation chapter with an answer key;
- the course-delivery requirements in their own section (§6.3);
- research and stack rationale in the addendum, which yields to the PRD on any conflict.

The examiner's path runs through DR-1's «Prøv selv» section, SM-2 and SM-9 instead of a second UJ, which is proportionate. The length, about 950 lines plus the addendum, is the user's own choice: the decision log overrides the 5–8 page target. Its cost is maintenance rather than readability, and it surfaces as the downstream drift above.

## Mechanical notes

- **IDs.**
  - The sets are contiguous and unique: FR-1 to FR-36 plus FR-17b; R-1 to R-17; E1 to E30 (with E11 a/b, E18 a/b and E29 a–g); NFR-1 to NFR-11; AG-1 to AG-6; DR-1 to DR-10; SM-1 to SM-10; SM-C1 to SM-C3; UJ-1.
  - FR-17b, FR-35 and FR-36 sit out of numeric order, as §4 explains.
  - "FR-17b" breaks the `FR-n` pattern that DR-5's traceability and any pattern-based coverage check assume, so give it its own row in the DR-8 status table.
- **Assumptions Index roundtrip.** All 8 inline tags are indexed in §11, and every index entry appears inline. The FR-17 tag states that a rule is project-defined rather than an unconfirmed inference, so it duplicates §11's second list.
- **§10.** Questions 1 and 6 remain as closed entries. That keeps them traceable, but a reader counting open items sees 6 instead of 4. Consider a short "Closed" list.
- **Cut line wording.** "SM-2 and SM-3 count as met on the local version" adds nothing, because both are measured locally by definition. Only SM-9 lapses.
- **E23.** It is in the Must set but asserts "no overstock note", which is FR-14 (Should), so it passes trivially in a Must-only build. This is harmless, but its "Rule (priority)" column could say so.
- **Glossary drift.** §3 says "no synonyms in either language", yet the FR-12 line (and the UX template) uses «Prognose» and «lager» where the glossary binds «Ukeprognose» and «Lagerbeholdning». Either list these short forms in the glossary as line labels, or note the exception.
- **Stale statements.**
  - §0 "This PRD feeds" still describes the UX and architecture steps in the future tense.
  - Addendum §1 says "The technology stack, the local model runtime and the model itself are still open", and the §2 heading says "not decided". The spine, which addendum §2 itself cites (AD-13, AD-15, AD-16), has chosen Django.
  - The addendum frontmatter still says `updated: '2026-11-03'`, although the addendum was edited on 2026-11-08 and 2026-11-15.
- **Implicit data rule.** On the short rule test products, recent-period warnings (for example E29 a's listed stockout warning) appear only if every product's history ends at the latest data week. FR-3 and the glossary never say so.
- **§12.** "(filled in at commit)" in the 2026-11-15 row is expected for a working copy.
- **Required sections and paths.** All the expected sections are present for the stakes: Vision, user and UJ, glossary, FRs with consequences, rules and answer key, NFRs, non-goals, MVP scope, SMs with counter-metrics, open questions, the assumptions index and the change log. Every file cited in §0 exists.
