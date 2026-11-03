# PRD Quality Review — Prognose (G40-lyamouri)

## Overall verdict

This is a strong, unusually precise PRD for a graded forecasting tool. The transparency thesis is explicit, scope and every project-defined rule are disclosed rather than hidden, the bilingual glossary is binding, and all fourteen reference examples recompute correctly by hand, including E5's floating-point case and E14's seasonal indices. Three gaps put this at risk:
- **Confidence labels:** "active warning", which decides every confidence label, has no full definition. The warning and label rules also sit outside the §5 rule set that NFR-2 and AG-1 bind.
- **Must gate:** the Must gate (SM-1, applied through DR-6 and SM-C2) includes E14, which tests a Should feature, so it cannot pass as written.
- **Check by hand:** this promise stops at the order line. No FR shows the inputs behind a base forecast, and no seeded product has a worked example.

Closing these three gaps and the five medium Done-ness items before UX and architecture start would make the PRD safe to hand to AI-assisted story creation.

## Decision-readiness — strong

The PRD states its decisions as decisions and says what each one gave up:
- R-4 picks the first observation as the smoothing start value "because it can be checked by hand".
- R-12 records that "a user-set weeks-of-cover threshold, which research report B suggested, was considered and not chosen, to keep the settings simple".
- §5.4 keeps the brief's 2 × median rule and names Tukey fences and the Hampel filter as the established alternatives.
- The R-14 limitations say what the simple index gives up: trend, and more than two values per week number.
- §7 gives reasons, not just exclusions ("each new signal would need its own rules and test data").

A reviewer who objects to the missing lead time, statistical safety stock or prediction intervals finds the objection acknowledged in §7 or the glossary and answered in addendum §4.

The single `[NOTE FOR PM]` (§8.2) sits at the real tension, the deadline. OQ1 has an owner and a stated consequence ("FR-28 moves from Should to Must"). Two things are missing. The deadline risk is assigned only to Should items. Two open questions are not open in a useful way: one is already answered and the other has no pass criterion.

### Findings
- **medium** Deadline risk is assigned only to Should items (§8.2 NOTE FOR PM; DR-6; §10 OQ1) — The PRD is dated 2026-11-02 and DR-6 sets submission on 1 December 2026. That leaves 29 days for UX, architecture, epics, 23 Must FRs, the DR-3 spreadsheet and README tests on two operating systems. The note only says "the Should items are at risk". It names no Must build order and no checkpoint, and OQ1 can move FR-28 into Must without saying what gives way. *Fix:* Extend the note, or DR-6, with three things: the Must critical path (calculation module and E1–E13 first, then login and isolation, then screens and explanation); a date by which OQ1 must be answered; and which Should item drops if FR-28 becomes Must.
- **low** OQ5 is already answered (§10 OQ5) — "Current answer: no, in version 1." This is a decision written as a question, and it is the kind of omission §7 exists to make explicit. *Fix:* Move it to §7 ("No flagging of unusually low sales in v1; R-10 flags high sales only") and drop it from §10.
- **low** OQ6 has no pass criterion and no fallback (§10 OQ6; FR-17 assumption) — OQ6 asks "Do R-10, R-11 and R-14 behave as expected on the test products?" and is to be answered "before the rules are relied on". The PRD never writes down what "as expected" means, and nothing says what happens if the rules misbehave in the last weeks before the deadline. *Fix:* State which weeks the level-shift and seasonal test products should have classified as unusual weeks or level shifts. Also name a fallback decision, for example: level-shift detection is turned off and runs stay unusual weeks.

## Substance over theater — strong

Nothing here is furniture:
- **Persona:** there is one, and its context drives real choices. Weekly ordering gives R-8 its one-week basis, 10 to 50 products give the sorted overview of R-12, and the need to explain decisions gives the template explanation.
- **Non-users:** the list excludes things a reader might otherwise assume, such as approval steps and placing real orders.
- **NFRs:** they carry product-specific bounds instead of adjectives. NFR-7: "differ by more than colour alone ... and a legend explains them". NFR-8: "50 products of 104 weeks ... within 2 seconds". NFR-1: "the internet is needed only to install dependencies".
- **AI guardrails:** each one traces to an FR (AG-2 to FR-26, AG-3 to FR-28, AG-4 to FR-27). FR-28's check on "the label attached to a number" rests on a named error type (context mismatch, addendum §3), not boilerplate.
- **Vision:** it could not be swapped into another forecasting PRD.

### Findings
- **low** The stated difference from a spreadsheet is the wrong one (§1, second paragraph) — "What sets Prognose apart from a spreadsheet or a large ERP system is transparency." A spreadsheet is as transparent as a tool gets. What Prognose adds over one is in the next sentence: stockout weeks left out, unusual weeks and level shifts detected, and a confidence label with a reason. *Fix:* Name the trust signals as the difference from a spreadsheet, and keep transparency as the difference from an ERP system.
- **low** NFR-6 names four browsers that nothing verifies (§6.1 NFR-6) — "current versions of Chrome, Edge, Firefox and Safari" is an assumption that no SM or DR checks. SM-2's clean-machine test names operating systems, not browsers. *Fix:* Name the browser used in each SM-2 run, and list the others as untested.

## Strategic coherence — adequate

The thesis is explicit and the PRD bets on it: transparency plus honesty about trust ("Every number comes from deterministic rules the user can see, adjust and check by hand. The system also says when a forecast should not be trusted."). The priorities follow from it:
- **Must:** the calculation line (FR-12), the data-quality rules and confidence label (FR-15 to FR-19), and the template explanation.
- **Should or Could:** seasonal adjustment, the language model, and the purchase-planning conveniences.

The counter-metrics are pointed rather than decorative. SM-C1 forbids trading hand-checkable rules for accuracy, and SM-C3 forbids weakening warnings to raise the share of «høy» labels. The MVP is a problem-solving scope, and its logic matches.

There are two weaknesses. The thesis is carried all the way through only for the order step. And the Vision promises an AI feature that the Must scope does not contain.

### Findings
- **high** "Check by hand" stops at the order line (§1; UJ-1 climax; FR-12, FR-25, FR-26; DR-3) — §1 says an examiner can "log in as a test company and check each forecast against a worked example". UJ-1's climax promises "how it was calculated". But only part of that is delivered:
  - FR-12 shows only the order step: forecast plus margin minus stock.
  - No FR makes the inputs to the base forecast visible. FR-25 asks for a chart, and FR-26's explanation covers "the number of calculation weeks, which weeks were left out and why", not their values or the formula.
  - No seeded product has a worked example. DR-3's spreadsheet holds E1–E14, which are short synthetic series that never appear in the app.
  - The seed file in the repository (FR-3) lets a determined examiner recompute, but the purchasing manager inside the app cannot. No SM measures whether anyone can reproduce what a screen shows.

  *Fix:*
  - Add a forecast-step line to FR-12 or FR-25. For moving average, for example: «Glidende gjennomsnitt, 3 uker: (16 + 12 + 15) / 3 = 14,3». For exponential smoothing, show the last update with α and the previous level. Add a table of the calculation weeks used.
  - Seed at least one product per reference series (E1–E4, E7–E10), so the spreadsheet and the screen show the same case.
  - Add an SM such as: "for the seeded reference products, a person given only the product screen reproduces the base forecast and the suggested order quantity."
- **medium** The Vision promises AI explanations that the Must scope does not contain (§1, second paragraph; FR-26, FR-28; §10 OQ1) — The Vision says "AI explains the result in plain language but never produces the numbers." In Must scope, though, the explanation is a template (FR-26). The only language model is a Should (FR-28), and OQ1 leaves that decision to the teacher. The teacher and examiner named in §0 will read the Vision first. *Fix:* Reword the Vision: "Plain-language explanations come from fixed templates; an optional local language model may rephrase them but never produces the numbers." Revise it again if OQ1 makes FR-28 Must.

## Done-ness clarity — adequate

Where the PRD is precise, it is exemplary. §5 states every formula, and R-9 even closes the floating-point trap (E5: 100 × 1.1 − 40 must give 70, not 71). Nearly every Must FR has consequences that translate directly into tests. FR-2's two-account test and FR-15's "same forecast as the same history with those weeks removed" are model consequences. All fourteen reference examples were recomputed for this review, and all of them match, including:
- E2's smoothing chain (12 to 13.7904);
- E8's included and excluded results (41.0 and 21.333);
- E14's indices (0.5432, 0.9383, 1.4815, 1.0370) and forecasts (10.982, 18.968, 29.950).

The gaps cluster in three places:
- where the trust signal is decided (warnings and the confidence label);
- at the edges of the project-defined rules, which have the fewest examples;
- in two consequences that an AI story writer would encode literally and wrongly.

### Findings
- **high** "Active warning" has no full definition, yet it decides every confidence label (§3 Confidence label; FR-15, FR-16, FR-19, FR-25) — High needs "no active warning", and Medium is "12 to 103 valid weeks, or any active warning". The glossary lists the warning types, but three questions are left open, and they decide the label for most products:
  1. **Scope.** FR-15 and FR-16 imply that warnings cover the whole history ("The presence of unusual weeks counts as an active warning"). Then one unusual week 90 weeks back keeps a product at Medium, even though it lies outside a 3-week moving-average window. With 104-week histories, High would need two years without a single stockout week or unusual week. FR-3 does not require such a product, although SM-7 needs one. That may be intended, but the PRD never says so.
  2. **Precedence.** A product with 5 valid weeks and a stockout warning matches both Low and Medium. FR-19's rule "A product without a forecast (FR-8) is labelled low" also contradicts the glossary in one case: a product with 12 valid weeks whose calculation weeks fall below the moving-average window.
  3. **Coverage.** SM-1 claims to validate FR-19, but no reference example exercises the label.

  *Fix:*
  - Add a §5 rule for warnings: each type, its trigger, and whether it looks at the whole history or only the calculation weeks.
  - Add a §5 rule for the label: precedence Low over Medium over High, and a definition of "active".
  - Add reference examples for each label and for the precedence case.
  - Require in FR-3 that one product reaches High.
- **medium** The level-shift warning is Should, but a Must label and a Must explanation depend on it (FR-17; FR-19; FR-26; §8.2) — FR-17 is "Must for the calculation; Should for the warning", and §8.2 defers the "Level-shift warning text". Yet the glossary lists a level shift as a warning, FR-19 drops a product to Medium on any active warning, and the Must explanation (FR-26) covers "any level shift". In a Must-only build, the level-shift test product therefore gets High or Medium depending on whether a Should item has been built. *Fix:* State that a detected level shift counts as an active warning in Must scope and that only its warning text is Should. Alternatively, make the whole warning Must.
- **medium** FR-21's consequence is false or untestable as written (FR-21) — It says "Changing any setting visibly changes the affected forecast, scenarios or suggested order quantity on the product screen." This is often false:
  - Changing the smoothing factor while moving average is selected changes nothing.
  - Changing the unusual-week setting on a product with no unusual weeks changes nothing.
  - The scenario percentage never changes the suggested order quantity.

  If "the affected" is read loosely instead, the sentence says nothing testable. FR-21 is the FR behind SM-3, so the end-to-end test inherits the problem. *Fix:* Reword it: "After a settings change, every value on the product screen and the product overview is recalculated with the new settings within NFR-8's 2 seconds, without logging in again." Add one concrete check on a seeded reference product. For example, on the E1 series, switching from moving average 3 to exponential smoothing 0.3 changes the base forecast from 14,3 to 13,8.
- **medium** FR-12's "equals the value used" clashes with R-9's one-decimal display, and the line can visibly fail to add up (FR-12; R-9) — The values used have full precision but are displayed with one decimal, so the line cannot literally show "the value used". Take default settings, sales of 27, 28 and 27 (moving average 27.333) and stock on hand of 10. R-8 rounds 20.067 up to 21, while the line reads «Prognose 27,3 + sikkerhetsmargin 10 % (2,7) − lager 10 = foreslått bestillingsmengde 21». Anyone checking by hand gets 20, at the exact place where the thesis promises checkability. Two display rules are also missing:
  - No rule covers the margin amount in brackets.
  - The rounding mode is unstated. A spreadsheet rounds halves up, while many languages' default formatting rounds exact halves to even. This matters for DR-3's side-by-side comparison.

  *Fix:* Show the unrounded total and the round-up step on the line, for example «… − lager 10 = 20,07 → rundet opp til 21». Define "equals" as "equals after R-9 display rounding". Give the margin amount a display rule, and set the rounding mode to half-up.
- **medium** The level-shift rule has two readings that give different forecasts (R-10; R-11; E9) — R-11 says level-shift weeks "stop being unusual weeks, are always kept in the calculation, and count in later baselines". It does not say when the relabelling happens. E9 stops at the third high week, so it cannot tell the two readings apart. Add one week: 20, 22, 21, 50, 52, 51, 110, with unusual weeks excluded.
  - **Relabel as soon as the third week is found:** week 7's baseline is median(50, 52, 51) = 51. So 110 is a lone unusual week and is excluded, and the moving average over 3 weeks is 51.0.
  - **Flag all weeks first, then group runs:** weeks 4 to 7 form one level shift, which is always kept. The moving average is (52 + 51 + 110) / 3 = 71.0.

  *Fix:* State that a run is relabelled as soon as its third week is found, and that later weeks are checked against the updated baseline. Add this series as a reference example. Also add a run that stays high, such as 20, 22, 21, 50, 52, 51, 53, to fix which weeks the chart marks as level shift.
- **medium** Seeded test products have no expected values, and E14 cannot run against a 52-week rule (FR-9; FR-17; §5.6 E14; NFR-2; DR-3) — FR-9 says the seasonal test product "matches its reference example in §5". FR-17 says "The level-shift test product (FR-3) gives the forecast in its reference example". But §5.6 holds only short synthetic series: E9 has 6 weeks and E14 uses a 4-week cycle. Neither reference resolves. Separately, R-14 fixes week numbers 1 to 52, while NFR-2 and SM-1 require E14 as an automated test. That only works if the season length is a parameter of the calculation module, and no rule says it is. *Fix:* Add expected results for each named test product to §5.6 and the DR-3 spreadsheet, or seed products whose histories are the reference series (as in the Strategic coherence fix). State in R-14 that the season length is a module parameter: 52 in the app, 4 in E14.
- **low** R-14 can divide by zero (R-14 steps 2 and 3) — A seasonal item with no sales in a given week number in both years gets index 0, and step 3 then divides that week's sales by it. This is common for garden or winter goods in a hardware store. A history of all zeros also makes the step-2 denominator 0. §5 guards every other zero (R-10's zero baseline, R-12's «–»). *Fix:* Extend step 4: seasonal adjustment is used only when every week-number mean is above 0. Otherwise, the forecast is shown without it, with the existing note.
- **low** Adjectives where bounds belong (FR-10; FR-16; FR-27; FR-28; NFR-8) — Five phrases have no measurable bound:
  - FR-10's "presented as what-if alternatives, not as probabilities" has no observable form.
  - FR-16's "marked clearly" and FR-27's "its own clearly marked area" are bounded by NFR-7 only for the chart.
  - FR-28's "does not answer in time" has no timeout.
  - NFR-8's "ordinary laptop" names no reference machine, and NFR-8 does not say whether the 2 seconds include the optional model (addendum §3 raises this).

  *Fix:* Give FR-10 a fixed heading text and FR-27 a heading for the template area. Give FR-28 a timeout. Give NFR-8 a reference machine and limit it to the template path.
- **low** Small behaviours are left to the implementer (FR-20; FR-24; R-9; R-12; FR-29) — Four details are unspecified:
  - whether percentages accept only whole numbers (NFR-5 implies it; FR-20 does not say), and what step the smoothing factor takes;
  - how the remaining products are ordered after the R-12 groups;
  - how many decimals weeks of cover shows (E13 uses 0.35, but R-9 covers only forecasts, scenarios and order quantities);
  - what happens to an adjusted order quantity when a settings change moves the suggestion under it.

  *Fix:* Add one sentence each to FR-20, FR-24, R-9 and FR-29.

## Scope honesty — adequate

The defaults are honest:
- §7 is a real non-goals list with reasons.
- The UJ-1 priority note says what the Must-only version lacks ("adjustments last for the current session only").
- All seven inline assumptions appear in the §11 index.
- §11 also lists every project-defined rule and threshold that has no research source, which most PRDs would leave implicit.

The number of open items is reasonable for a medium-rigor course PRD: 7 open questions, 7 assumptions, 1 NOTE FOR PM and 1 OPEN tag. Only OQ1 could reshape scope.

Three omissions are still left for the reader to infer, and one of them is a logic error in the scope gate itself.

### Findings
- **high** The Must gate includes a Should test, so it cannot pass as written (SM-1; DR-6; SM-C2; §5.6 E14) — DR-6 and SM-C2 say no Should or Could item starts before "the Must scope passes SM-1 and SM-3". §4's intro words the gate differently: "if the core flow is finished and stable". SM-1 requires "100% of the reference examples E1 to E14" and lists FR-9 among what it validates. But E14 tests R-14, the Should seasonal adjustment. Read literally, no Should item can ever start. In practice, R-14 gets built inside the Must scope to make SM-1 pass, which is exactly the silent scope growth SM-C2 exists to prevent. *Fix:* Define the Must gate as E1–E13 plus SM-3, let E14 pass together with FR-9, and use the same wording for the gate in §4, DR-6 and SM-C2.
- **medium** Editing company data is neither required nor excluded (FR-2; FR-4; §2.1; §7) — FR-2 says a company can "see and change only its own products, sales history, settings and order quantities". Its test "tries to read and change test company B's products, sales history and settings". Yet no FR lets anyone change products, sales history or stock on hand. Without data entry, the weekly routine in §2.1 and UJ-1 can only run once, on a frozen dataset, and §7 excludes only "import of real company data". Two things can go wrong: UX may design an entry screen nobody asked for, or the isolation test may target endpoints that do not exist. *Fix:* Add to §7: "No entry or editing of products, sales history or stock on hand in v1; the seed data is read-only, and the weekly cycle is shown on it." Narrow FR-2 to what can be changed: settings and adjusted order quantities.
- **medium** The known limitations miss two interactions between the outlier rules and R-14 (§5.5 known limitations; FR-17 assumption; OQ6) — The list says "Seasonal peaks can look like unusual weeks" and that the default setting leaves the forecast unchanged. It does not say two things:
  1. A peak that stays above 2 × the pre-peak baseline for three weeks or more becomes a level shift. The seasonal test product would then carry level-shift markings in the chart (Must, FR-25), and once the Should text exists, a "demand seems to have moved to a new level" warning every season.
  2. With unusual weeks excluded, a one- or two-week spike flagged in both years leaves its week number with no calculation week. R-14 step 4 then switches seasonal adjustment off for the whole product.

  This list goes into the README (DR-1) as the project's stated limits. *Fix:* Add both points to the limitations. Give the seasonal test product an expected R-10/R-11 classification, which also answers OQ6.

## Downstream usability — strong

The PRD is built for extraction:
- The glossary is binding in both languages, so UX gets its copy and stories get stable nouns.
- IDs are contiguous and unique across FR-1 to FR-34, R-1 to R-14, E1 to E14, NFR, AG, DR and SM.
- Every FR carries a priority, and most feature sections name the UJ-1 steps they realise.
- Cross-references use § numbers and IDs, never "see above", and each SM names the requirements it validates.
- `addendum.md` holds the research and the stack rationale, and says the PRD wins on any conflict. That keeps the architecture step from treating a research recommendation as a requirement.

### Findings
- **medium** The warning, confidence and old-data rules sit outside the §5 rule set that NFR-2, AG-1 and SM-1 bind (FR-18; FR-19; §5; NFR-2; AG-1) — AG-1 says warnings and confidence labels "come only from the rules in §5", and NFR-2 puts "All rules in §5" into the calculation module. But the confidence thresholds exist only in FR-19 and the glossary, and the 8-week old-data rule exists only in FR-18. An architecture step that takes §5 as the module's contract could put the label and the old-data check in the web layer. They would then sit outside the unit-tested module and outside the answer key. *Fix:* Move them into §5 as numbered rules, together with the Done-ness fix for "active warning". Keep FR-18 and FR-19 as the user-facing consequences.

## Shape fit — strong

The shape matches a single-operator tool with real UX whose correctness is graded:
- one UJ with a named protagonist;
- a capability spec with testable consequences;
- a calculation chapter with an answer key;
- course-delivery requirements in their own section (§6.3).

Research and stack detail live in the addendum instead of the PRD. The length the user accepted is spent on rules and examples, not ceremony. For a PRD at the top of the chain, feeding UX, architecture and stories, the traceability is at the right level.

### Findings
- **medium** The graded flow has no journey (§2.3 UJ-1; §4 intro; §4.6; FR-21; SM-3; §1) — UJ-1 never changes a setting. Yet the primary metric SM-3 is to "change the forecasting method, safety margin or unusual-week setting, and see the result change". FR-21 "Realizes the teacher's core flow", and "core flow" also gates the Should items in §4's intro. The term is defined only in the teacher feedback, which the PRD "builds on, and does not repeat". The person who will actually run v1 has no journey either: the examiner of §1, who installs from the README and checks forecasts against worked examples. UX will design from UJ-1 and may treat settings as an afterthought. *Fix:* Add a UJ-2 with a named protagonist: the examiner, or the purchasing manager trying out a setting. Path: clone, follow the README, log in, open a seeded reference product, compare it with the spreadsheet, change the method, the margin and the unusual-week setting, and see every number update. Define "core flow" inline as SM-3's sequence.

## Mechanical notes

- **IDs.** All ID sets are contiguous and unique: FR-1 to FR-34, R-1 to R-14, E1 to E14, NFR-1 to NFR-9, AG-1 to AG-6, DR-1 to DR-6, SM-1 to SM-8 and SM-C1 to SM-C3. UJ-1 is the only journey.
- **Assumptions Index roundtrip.** All 7 inline `[ASSUMPTION]` tags appear in §11, and every index entry appears inline. The FR-17 tag says the rule is project-defined; it is not an unconfirmed inference, and it duplicates §11's second list. The `[OPEN: …]` tag in FR-28 is an extra tag type. It resolves to OQ1, which is fine, but it is not indexed.
- **Cross-references.**
  - FR-9's and FR-17's "its reference example" do not resolve (see Done-ness).
  - SM-1 lists FR-12 and FR-19 as validated, but no reference example exercises the calculation line or the label.
  - The "(§6)" in the §5 intro means NFR-2.
- **Glossary drift.**
  - The FR-12 line uses «Prognose», which is also the product name, and «lager», where the glossary binds «Grunnprognose» and «Lagerbeholdning». It shows «Prognose 100» where R-9 would display «100,0».
  - FR-24 says "week-1 base forecast" where FR-11, R-8 and R-12 say "week-1 normal forecast" (the same value).
  - §7 says "stock figure" for stock on hand.
  - The glossary defines a level shift as "Three or more consecutive high weeks", while R-11 counts "unusual weeks in a row (counting valid weeks only)".
  - FR-24's column list omits weeks of cover, which R-12 says the overview shows.
- **Glossary gaps.** "Product overview" and "product screen" are used throughout §4 but have no glossary row or Norwegian label, unlike "combined order overview". "The seasonal test product" and "the level-shift test product" are used as named entities, although FR-3 asks only for "at least one product" per pattern.
- **Week identity.** The glossary identifies a week by year and week number, but E12 uses a running index ("Latest data week 104"). FR-18 does not say how week differences are counted across a year boundary. ISO 2026 has 53 weeks, and R-14's week-53 assumption covers only the seasonal index.
- **Required sections.** All are present for the stakes: Vision, user, UJ, glossary, FRs with consequences, NFRs, non-goals, MVP scope, SMs with counter-metrics, open questions and an assumptions index.
- **Addendum.** It keeps to its "no new requirements" rule, and its arithmetic checks out:
  - Report C's weighted totals: 83, 80, 65 and 50.
  - The Flask re-weighting note: 83 against 81, which holds only if testability drops to 15.
  - R-12's equivalence to a weeks-of-cover threshold of 1.1.
