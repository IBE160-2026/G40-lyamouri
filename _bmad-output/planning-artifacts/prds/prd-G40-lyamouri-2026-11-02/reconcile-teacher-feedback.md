# Reconciliation: teacher feedback against the PRD

- **Source (wins on any difference):** `_bmad-output/planning-artifacts/briefs/brief-G40-lyamouri-2026-09-18/tilbakemelding-product-brief.md` (IBE160 teacher, 2026-10-06).
- **Checklist:** `extract-teacher-feedback.md` in this folder (29 expectations, 7 criteria). No material difference from the source was found.
- **Checked:** `prd.md` and `addendum.md` in this folder (both dated 2026-11-02).
- **Status key:** Covered, Partly, Missing, or Deferred (an explicit hand-off to a later BMAD step stated in the PRD, counted as covered). G-numbers refer to the gaps in section 3.
- **Overall:** the PRD answers all three of the teacher's "most important changes". 22 expectations are covered, 1 is deferred, 6 are partly covered and none is missing. The remaining risk is in the AI feature, season and trend, the dataset answer key, the schedule and the trace convention.

## 1. The 29 expectations

| # | Expectation (short) | Status | PRD location and note |
|---|---|---|---|
| 1 | Numbers from known methods in code, never from an LLM | Covered | §1, §5 intro, R-3, R-4, AG-1, §7 |
| 2 | Two to three methods in v1 | Covered | FR-5, FR-6 (Must); FR-9 seasonal adjustment (Should): the teacher's three examples |
| 3 | Rules for scenarios, safety margin and outliers | Covered | R-7 to R-11, FR-16, FR-17; E3 to E6, E8 to E10 |
| 4 | Rules settled in the PRD, not left to AI | Covered | §5 (R-1 to R-14, E1 to E14), §11; small leftovers in section 4 below |
| 5 | AI role decided and limited (plain-language explanation) | Partly | FR-26 to FR-28, AG-1 to AG-5: tightly limited, but the only AI feature (FR-28) is Should, off by default, and §10 Q1 is open (G1) |
| 6 | Method and AI-role decisions with rationale | Covered | R-4, §5.4 status, §5.5 limits, §11, addendum §3 and §4; the method rationale is spread out (G7) |
| 7 | Correctness criterion against a hand calculation | Covered | SM-1, DR-3; E1 is the teacher's own example (moving average over 3 weeks) |
| 8 | Small dataset with known trend and season, hand-calculated answers | Partly | E1 to E14, FR-3, DR-3; no trend example (G2); the 104-week test products have no expected values of their own (G3) |
| 9 | Keep the functional criteria (own data, persistence, visible change) | Covered | FR-2/SM-4, FR-4/FR-22/SM-5, FR-21/SM-3, §9 mapping |
| 10 | Core flow first, finished and stable | Covered | SM-3 (the teacher's flow), SM-C2, DR-6, FR-21 |
| 11 | Method, margin and outliers as adjustable controls | Covered | FR-20, FR-21 (changed from the product screen) |
| 12 | What the planner sees: chart, key screens, sketches | Covered | FR-24, FR-25, FR-12, NFR-7, UJ-1; sketches are not in the PRD and are not explicitly handed to the UX step (G8) |
| 13 | Concrete primary user and the decision they take | Covered | §2, §2.1, UJ-1 (small business, 10 to 50 products, weekly, order quantity) |
| 14 | Honest difference from a spreadsheet or ERP | Covered | §1 paragraph 2; names no limits against a spreadsheet or ERP (G10) |
| 15 | Vision: later feed to S&OP or MPS, not in v1 | Covered | §1 paragraph 3, §7 |
| 16 | Deadline stated, work planned backwards | Partly | DR-6 (1 December 2026), §8.2 note; no dated milestones (G4) |
| 17 | One simple, justified stack with one database | Deferred | NFR-9 hands the choice to the architecture step; addendum §2 recommends Django + SQLite (83) over Flask (80) |
| 18 | Calculation logic in its own testable module | Covered | NFR-2, §5 intro, §4.3 |
| 19 | Runs locally without keys, paid accounts or own infrastructure | Covered | NFR-1, FR-4, DR-1, SM-2 |
| 20 | README gives a test company's customer number and password | Covered | FR-3, §4.1, DR-1 |
| 21 | LLM fallback without a key, documented in the README | Covered | FR-28, AG-2, AG-3, DR-1 |
| 22 | Cost, test-mode or mock plan for paid APIs | Covered | Not needed: no paid or hosted APIs (NFR-1, AG-5, §7, addendum §3) |
| 23 | Where secrets, test data, docs, dataset and generator script live | Partly | DR-2 and FR-3 require "documented places" but name none (G6) |
| 24 | `.env.example` for keys | Covered | NFR-3, DR-2 |
| 25 | Seed data; CSV import optional | Covered | FR-3, DR-4; import out (§7); CSV export is Could (FR-32) |
| 26 | Login, isolation, one role, password hashing | Covered | FR-1, FR-2, §2, NFR-3 |
| 27 | Data model entities | Covered | §3 Glossary (company, product, week, sales history, stock on hand, settings as forecast parameters); campaigns and customer orders out (§7); physical model left to architecture (implicit) |
| 28 | Traceable from brief to PRD, stories and code | Partly | §0, §9 mapping, "Realizes UJ-1" links, DR-5, SM-8; no trace convention and no FR-to-brief back-trace (G5) |
| 29 | Scope: season and trend in v1; campaigns and orders later; BOM etc. out | Partly | §7 and §8 cover the deferrals and exclusions; season is Should (FR-9), trend is not modelled (G2) |

## 2. The 7 grading criteria for part 1

Risk = how likely the PRD as written is to hold back a high score on that criterion.

| # | Criterion (weight) | How the PRD supports it | Risk | What would strengthen it |
|---|---|---|---|---|
| 1 | Process and AI governance (30 %) | Core rules settled with their source status (§5, §11) and `[ASSUMPTION]` tags; inputs listed (§0); brief success criteria mapped to SMs (§9); guardrails AG-1 to AG-6; DR-5 and SM-8 require a decision record and FR-to-story-to-test tracing; rationale and rejected alternatives in addendum §2 to §4 | Medium | Trace convention (G5); one decision table (G7); settle §10 Q1 now (G1); commit the hand-check spreadsheet before the calculation module |
| 2 | Functionality and scope (20 %) | Module 4.1 only; every FR prioritised; the teacher's core flow is SM-3; SM-C2 and DR-6 hold back Should and Could until Must passes; real domain content (two methods, scenarios, margin, stockout weeks, outliers, level shift, confidence labels) | Medium | Dated backward plan (G4); decide the AI feature (G1) and FR-9's priority (G2) early, since both decide what v1 shows |
| 3 | Quality assurance and testing (15 %) | Testable consequences on every FR; hand-calculated answer key E1 to E14; SM-1 at 100 %; DR-3 spreadsheet; one-command tests (NFR-2); end-to-end (SM-3), isolation (SM-4), explanation integrity (SM-6) and rule coverage (SM-7); snapshot tests (FR-26) | Low | Trend example (G2); expected values for every FR-3 test product (G3) |
| 4 | Design and user experience (10 %) | Concrete persona and journey with edge cases and priorities (UJ-1); screens defined (FR-1, FR-24, FR-25, FR-30); chart content and markings that do not rely on colour alone (FR-25, NFR-7); fixed Norwegian labels (§3) and example UI text | Low | Hand the sketches to the UX step explicitly (G8); optionally an examiner journey (clone, log in, check E1 against the spreadsheet) |
| 5 | Code quality and architecture (10 %) | One web app with one local database (NFR-9); calculation module isolated from UI and database (NFR-2); stack explicitly deferred, with a scored recommendation and a reversibility hedge (addendum §2) | Low | Decide early and answer the teacher's "no more complex than needed" test in the decision: the Django-Flask margin is within the scoring uncertainty (addendum §5), and addendum §2 names Django's extra concepts as the case against it |
| 6 | README and runnability (10 %) | No keys, paid services or internet when running (NFR-1); README for macOS and Windows tested from a fresh clone (DR-1); test logins (FR-3); one-command seed (DR-4); optional model off by default with fallback (FR-28); SM-2 | Low | Schedule the clean-machine tests on both systems (G4); if Chart.js is chosen, vendor it, the only option that meets NFR-1 offline (addendum §2); check the SQLite version (addendum §5) |
| 7 | Repository tidiness (5 %) | Documented places and `.env.example` (DR-2); no secrets (NFR-3); no personal data or local paths (NFR-4); spreadsheet in the repo (DR-3) | Low | Name the folders (G6) |

## 3. Gaps

| # | Gap | Severity | Suggested fix |
|---|---|---|---|
| G1 | No AI feature in the Must scope (#5). The Must explanation is template-only (AG-2); FR-28 is Should, off by default and flagged at risk (§8.2 note); §10 Q1 goes to the teacher only "before sprint planning", after the architecture step. The teacher's scope suggestion 1 assumes "a limited AI function" in the app, and addendum §3 notes the hybrid design wins if a visible AI feature counts. | High | Ask the teacher now, before the architecture step. If the answer is yes or unclear, make a minimal FR-28 Must (local model, template fallback, number check) so the architecture plans for it, and record the decision with rationale. |
| G2 | Season and trend are thin (#8, #29). The teacher names "season and trend" as core domain logic and suggests both for v1. No method handles trend and no hand-calculated example has one. The lag of the flat MA and ES forecasts under a trend is not stated as a limitation, and seasonal adjustment (FR-9) is Should and at risk. | Medium | Add a known-trend reference example (for example sales 10, 12, 14, 16, 18, 20: MA-3 gives 18 while the trend continues to 22). State the lag in §5.5 and the README, record why no trend method (such as Holt's) is in v1, and decide now whether FR-9 (E14 is ready) becomes Must. |
| G3 | The answer key stops short of the dataset (#8). FR-9 and FR-17 point the 104-week seasonal and level-shift test products to "its reference example", but §5.6 has only short series: E9, and E14 with a 4-week cycle while R-14 assumes 52 week numbers. DR-3 covers only E1 to E14. | Medium | Build the FR-3 test products from the E-series inputs, or extend DR-3 so the spreadsheet holds hand-calculated outputs for every FR-3 test product. State whether R-14 takes the cycle length as a parameter, so that E14 can run as a test. |
| G4 | Deadline stated, no backward plan (#16). About four weeks remain for UX, architecture, epics, 23 Must FRs, and the teacher's "testing, fixing and README at the end", including README tests on two clean machines. | Medium | Add dated milestones to DR-6 (architecture, epics, Must passing SM-1 and SM-3, SM-2 tests on macOS and Windows, code freeze) and a cut order in case Must slips. |
| G5 | No trace convention (#28). DR-5 and SM-8 require FR-to-story-to-test tracing but do not say how; the back-trace to the brief covers only its success criteria (§9). | Medium | Add to DR-5: each story names its FR-n, each test names its FR-n or E-n, and each commit names its story. Link this file from §0 as the trace of the teacher's feedback. |
| G6 | Repo layout not named (#23). DR-2 and FR-3 promise "documented places" for the data, generator script, spreadsheet and docs, but name none. | Low | Name the folders in DR-2, or hand them explicitly to the architecture step. |
| G7 | Decisions and plan changes are spread out (#6, closing note). There is no single decision record, and the teacher's optional "AI suggests parameters" idea is not addressed. | Low | Add a short decision table (decision, alternatives, rationale, source) that includes AI parameter suggestions, plus a "changed since the brief" list. |
| G8 | Screen sketches are not handed over (#12). | Low | Add one sentence to §0 or §4.7: the UX step sketches the login, product overview, product screen (chart and settings) and combined order overview. |
| G9 | Must-only gap in FR-19. The level-shift calculation is Must but its warning is Should, so it is unclear whether a level shift lowers the confidence label in a Must-only build. | Low | State the rule in FR-17 or FR-19. |
| G10 | The differentiation (#14) lists only strengths. | Low | Add one sentence on what a spreadsheet or ERP does better (flexibility; lead times and statistical safety stock, which §7 excludes). |

## 4. The teacher's qualitative points at risk

- **"A traceable path from plan to finished app" (WHY, C1).** The ID scheme (FR, R, E, NFR, AG, DR, SM) is a good base, and DR-5 and SM-8 promise FR-to-story-to-test tracing. Nothing yet fixes how the IDs travel into stories, tests and commits, so this point stays at risk until the epics step sets that (G5).
- **"Not left to AI during implementation" (feasibility, BMAD flow).** The PRD keeps this promise for methods, scenarios, margin and outliers. An implementing agent would still decide four things alone:
  - the expected values for the 104-week test products, which would then come from the code under test (G3);
  - how E14's 4-week cycle fits R-14 (G3);
  - the confidence label for a level shift in a Must-only build (G9);
  - the Norwegian template wording (FR-26), which the snapshot tests would freeze as written. Review the wording before the first snapshot.

  R-4 is protected: an implementation that estimates the start level, as FPP3 does (addendum §4), would fail E2.
- **Control over the AI's work (feasibility).** The PRD asks the group to recalculate E1 to E14 by hand before implementation (§5 intro, DR-3). The examiner sees this only if the spreadsheet is committed before the calculation module. This check recalculated E1 to E14 and found them consistent, but that does not replace the group's own calculation.
- **"Professionally correct numbers" (difficulty, domain logic).** The PRD states openly that R-10, R-11, R-14, the thresholds, and the percentage margin and scenarios have no research source (§5.4, §11, §10 Q4, addendum §5). That openness helps the grade. The weak spot is "season and trend", which the teacher names as core domain logic (G2).
- **"A limited AI function" in the app (scope suggestion 1; dependencies row).** The PRD describes the AI part carefully (AG-1 to AG-5), but a delivery with only the Must scope has no AI in the app at all (G1).
- **"Finish and stabilise the core flow first" (difficulty).** This is built in (SM-3, SM-C2, DR-6). The only threat is a four-week schedule without milestones, which includes the two clean-machine README tests (SM-2, G4).
- **"History shows how the plan developed" (closing note).** The PRD lists its inputs (§0) and notes a few changes from the brief (for example the §3 entry that replaces "suggested planning quantity"), but it has no single list of what changed since the brief (G7).
