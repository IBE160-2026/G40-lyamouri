---
title: 'Epics and Stories: Prognose (G40-lyamouri)'
status: final
created: '2026-11-18'
updated: '2026-11-21'
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md'
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/addendum.md'
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/tilbakemelding-prd.md'
  - '_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-17/ARCHITECTURE-SPINE.md'
  - '_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-17/teknologinotat.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/DESIGN.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/EXPERIENCE.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/mockups/konsept-d-kombinert.html'
  - '.logs/mounia-03/issues.md'
---

# Prognose (G40-lyamouri) - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Prognose (G40-lyamouri), decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

- **Sources:** the PRD with its addendum, the teacher's PRD feedback of 2026-11-12, the architecture spine of 2026-11-17 with its technology note, the UX spine pair `DESIGN.md` and `EXPERIENCE.md`, and the open points in `.logs/mounia-03/issues.md`. The approved mockup is used only for copy that the spines leave open.
- **IDs:** FR-n, NFR-n, AG-n, DR-n, SM-n, R-n and E-n are the PRD's; AD-n are the architecture spine's; UX-DRn are defined here from the UX spines.
- **Precedence:** if this document disagrees with a source, the source wins: the PRD for requirements and priorities, the spine for technical decisions, and `DESIGN.md` and `EXPERIENCE.md` for the interface, over the mockup.
- **Change log:** once this document is approved, every change is recorded with its date, reason and commit, as PRD §12 and DR-5 require.

## Deviations From the Sources

### D-1 Publishing removed from v1 (decided 2026-11-19; PRD and spine aligned)

- **The teacher's clarification** (Canvas, 2026-11-19, as reported by the user; summarized, not quoted, in `prds/prd-G40-lyamouri-2026-11-02/avklaring-publisering-2026-11-19.md`): publishing is not mandatory. The application may run locally, but the README must explain how to start it and which API keys are needed.
- **These epics do:** no story publishes Prognose. Story 1.9, publishing on Vercel with Neon, is removed, so Epic 1 has 8 stories and the plan 38. The real iPhone 13 test runs over the local network (AD-13), first in Story 1.8 and finally in Story 4.4. Stories 1.1 and 4.1 require the README to explain how to start Prognose and that no API key, paid service or account is needed.
- **Why:** the user's decision of 2026-11-19, after the teacher's clarification. It removes the external risks, such as the organization's approval of the Vercel app, and the work on a second run mode.
- **History, before 2026-11-19** (kept as written then):
  - **The architecture spine said,** until it was aligned on 2026-11-18: under Consistency Conventions, «Delivery order»: "The first story proves the whole path: the project skeleton with `compose.yaml` and CI, and the first deploy to Vercel with Neon." Under Deferred, «Checks in the first story»: the Vercel GitHub app in the IBE160-2026 organization, Vercel Hobby's commit-author rule, Vercel's detection of `src/manage.py` and its run of the build script with `DATABASE_URL_UNPOOLED`, Neon with Postgres 18 in AWS Frankfurt, and GitHub Actions. The open point in `issues.md` of 2026-11-08 also puts publishing in the first story.
  - **These epics do:** Stories 1.1 and 1.2 prove the local path and CI, and Story 1.2 checks that GitHub Actions is allowed. The last story of Epic 1, Story 1.9, publishes on Vercel with Neon and makes the other checks. No other story depends on it. Sprint planning schedules it right after Story 1.8, before any Epic 2 story, so that the examiner gets a working website; it is postponed only while it waits on something outside the group's control, and cut only under the cut line (PRD §8.1; the user's decision of 2026-11-18).
  - **Why:** the user's decision of 2026-11-18, so that publishing can be cut as the cut line requires without holding back the rest of the Must scope.
  - **Risk:** problems with Vercel or Neon, or a wait for the organization's approval of the Vercel app, can delay the first deploy. Scheduling Story 1.9 right after Story 1.8, and asking about the Vercel app when Epic 1 starts, leaves time to solve them before the cut-line date that sprint planning sets.
  - **Resolved:** on 2026-11-18 the user confirmed that publishing is Story 1.9 and blocks no other development. The spine's «Delivery order» row and its Deferred items were aligned the same day, with a row in its change log that also states the risk above. The point in `issues.md` gets a note when this session is logged.
- **Recorded in, on 2026-11-19:** PRD DR-10, SM-9, §8.1 and §12; the spine's AD-13, AD-14, AD-16 and change log; and this document's change log.

### D-2 DR-5 counts the epics that are implemented (decided)

DR-5 asks for at least one AI steering log case per epic. By the user's decision of 2026-11-18, this applies to the epics that are implemented; an epic that is not built is marked as not built in the status table (DR-8). The PRD text is unchanged.

### D-3 The setup test on Windows and offline is a story of its own (decided; spine aligned)

- **The architecture spine said,** until it was aligned on 2026-11-18: under Deferred, the offline start with Docker Desktop and the whole README setup on Windows x64 "run in the first story and again on the final commit".
- **These epics do:** Story 1.3 runs both, on a Windows x64 PC that the user has at work, if installing uv and Docker Desktop is allowed there. Any limitation is recorded in the QA log and, if Windows cannot be tested, in the README and the status table. No other story depends on Story 1.3, so it does not block other development. The final checks in Epic 4 run both again.
- **Why:** the user's decision of 2026-11-18.
- **Resolved:** the spine's Deferred line was aligned on 2026-11-18, together with D-1, and it states the limitation that Windows stays untested if no Windows x64 computer can be used.

### D-4 Innstillinger: the method and its setting change in one save (decided; spine and UX updated)

- **Before:** EXPERIENCE.md disabled the window under exponential smoothing and the smoothing factor under the moving average, by the saved method, and AD-11 did not let `app.js` change that. A method change and the setting it uses took two saves.
- **Now:** AD-11 lets `app.js` enable, before saving, the setting that the chosen method uses, and the settings form accepts both in one POST, which the tests check. Without the script, a second save is still needed (Story 3.1).
- **Why:** the user's decision of 2026-11-18, with the solution kept simple and testable.
- **Recorded in:** the change logs of the architecture spine and EXPERIENCE.md, both dated 2026-11-18.

### D-5 A button next to the unusual-weeks switch when scripts are off (decided; UX updated)

- **The UX spines said:** the switch is a real checkbox with `role="switch"`. They did not say how it sends the change without a script, and DESIGN.md shows no button next to it.
- **Now:** without the script, the small secondary button «Lagre» next to the switch sends the change, and `app.js` hides the button and sends the change on toggle (Story 3.3).
- **Why:** the user's approval of 2026-11-18, so that the switch works without JavaScript (AD-11, UX-DR43).
- **Recorded in:** the change logs of EXPERIENCE.md and the architecture spine, both dated 2026-11-18. DESIGN.md is unchanged, because the button is its small secondary button.

### D-6 The overstock note stands in the decision panel (decided; UX updated)

- **The UX spines said:** the product row shows the FR-14 note once it is built, but they did not say where the note stands on Produktside.
- **Now:** on Produktside, the note stands in the decision panel, below the suggested order quantity, and in the list it stands on the product's row (Story 6.1).
- **Why:** the user's approval of 2026-11-18.
- **Recorded in:** the change log of EXPERIENCE.md, dated 2026-11-18. DESIGN.md is unchanged, because the note uses the existing text styles.

### D-7 NFR-8 with the optional language model (decided; spine updated)

- **The sources said:** NFR-8 asks for 2 seconds, and FR-28 waits up to 10 seconds for the model; both are marked `[ASSUMPTION]`. Addendum §3 says that how the timeout fits NFR-8 is an architecture choice, and the spine deferred it to when FR-28 is scheduled.
- **The check:** the PRD leaves the fit to the architecture, and the model is off by default and outside the basic setup (SM-2). The teacher's feedback on the brief and on the PRD sets no response-time requirement and asks only that the language model stays under control, which FR-28 already ensures. The exception therefore fits the PRD and the teacher's requirements. Checked again in the review of 2026-11-18: FR-28 itself sets the 10-second timeout, and addendum §3 makes both the timeout and its fit with NFR-8 architecture choices, so NFR-8's text is not changed.
- **Now:** every page meets NFR-8 with the model off. With the model switched on locally, a product screen may wait up to the 10-second timeout, and the README states this exception. No caching or background loading is added (Story 7.1).
- **Why:** the user's decision of 2026-11-18. If the exception turns out not to fit when Story 7.1 is scheduled, the story is postponed rather than the architecture made more complex.
- **Recorded in:** the spine's Deferred item on the local language model and its change log, both dated 2026-11-18.

### D-8 Code review in a one-person group (decided)

- **The PRD says:** DR-7's Definition of Done asks that a story's pull request has been reviewed, with the review comments kept in it, and SM-8 that every story was merged through a reviewed pull request. Neither says who reviews. The examiner guidelines look for traces of code review in pull requests (criterion 3).
- **These epics do:** the user, who works alone, reviews each finished story with BMAD Code Review, and documents the findings, the decisions and the fixes, with their commits, in the pull request (the routine for code review). No second person is required.
- **Why:** the user's decision of 2026-11-18: the user works alone, so no second reviewer is available. The PRD text is unchanged, because it does not ask for one.

### D-9 Story 1.1 is merged before CI exists (decided 2026-11-21; spine aligned)

- **The PRD says:** DR-7's Definition of Done asks that a story's tests and the linter pass. It does not ask for CI.
- **These epics did:** the rule for every story and step 5 of the routine for code review asked that the tests and Ruff pass locally and in CI before a story is merged, and AD-17 in the spine merges a pull request only when GitHub Actions passes. CI is built in Story 1.2, after Story 1.1, so Story 1.1 could not meet that rule.
- **These epics do:** Story 1.1 may be merged when `uv run pytest`, `uv run ruff check` and `uv run ruff format --check` pass locally on the branch's final commit, and its pull request names this decision and the results with that commit. The first CI run comes with the pull request for Story 1.2 and runs every test on Linux, including those from Story 1.1. Every later story follows the rule as written.
- **Why:** the user's decision of 2026-11-21: Story 1.1 is finished before Story 1.2 starts, as the order of the stories and the sprint plan say. The PRD text is unchanged, because DR-7 does not ask for CI.

### D-10 Tests that verify no FR name their NFR, DR or AD IDs (decided 2026-11-21; spine aligned)

- **The PRD says:** DR-5 asks that every test names the FR-n or E-n it verifies, so that each FR can be traced from the PRD to code and tests.
- **These epics do:** a test that verifies an FR or a reference example names its FR-n or E-n. A test that verifies no FR, such as a test of the setup, the settings, the secret file or the repository, names the NFR-n, DR-n or AD-n it verifies instead, and Story 4.3's check accepts that.
- **Why:** the user's decision of 2026-11-21, in the BMAD Code Review of Story 1.1: 34 of its 37 test functions at that review verified no FR, because the story builds none, and many tests in Stories 1.2 to 1.8 are of the same kind. The PRD text is unchanged, because its aim, tracing every FR to its tests, still holds.

## Requirements Inventory

### Functional Requirements

37 functional requirements: 24 Must, 8 Should and 5 Could (PRD §8.5). Each FR has one priority, and a story takes its priority from its FRs.

- **FR-1 (Must) — Log in with customer number and password.** A correct customer number and password open the product overview. A wrong one shows one general message, «Feil kundenummer eller passord.», that does not reveal which of the two was wrong. Passwords are hashed with an established salted hasher (Django's PBKDF2, AD-6); no plain-text password exists in the database, the seed data or the logs. Every page except the login page sends a logged-out user to the login page, and logging out ends the session. *UJ-1 entry state; SM-3.*
- **FR-2 (Must) — Company data isolation.** A logged-in company sees and changes only its own products, sales history, stock on hand, settings and order quantities. The server checks the company on every request; a direct request for another company's product (for example a changed identifier in the address) returns "not found" and shows none of its data; lists (the product overview and the combined order overview) hold only the company's products. An automated test logs in as test company A and tries to read B's products, sales history, stock on hand and settings, and to change B's settings and order quantities, directly and through lists. It passes only if every attempt is refused and no list shows B's data. *SM-4.*
- **FR-3 (Must) — Synthetic dataset with known patterns.** A deterministic generator script creates two test companies with 10 to 50 products each. Each product has a product number, a name, a weekly sales history, a stockout flag per week and a stock on hand.
  - Most products have 104 weeks; at least one has fewer than 3 valid weeks, one has 3 to 11, and one has 12 to 103.
  - At least one product per pattern: a known trend; a seasonal pattern without trend; stockout weeks; unusual weeks; a level shift; a long run of stockout weeks at the end; stock on hand that covers next week; a history that reaches «høy».
  - The rule test products are built from the series of E1–E4, E7–E10 and E15–E19, and the reference spreadsheet holds their expected base forecast, suggested order quantity, unusual and level-shift weeks, warnings and confidence label (DR-3).
  - The script gives identical data on every run, the script and its output live in documented places (DR-2), and the README gives each company's customer number and password. *SM-7.*
- **FR-4 (Must) — Data stored between sessions.** Products, sales history, stock on hand and settings are stored in PostgreSQL: locally a server on the same computer, started with one documented command and needing no online service. After the app and the database are stopped and started again, all data and settings are unchanged. *SM-5.*
- **FR-5 (Must) — Moving average.** The base forecast is the mean of the last N calculation weeks, with the window N from 2 to 12 (default 3). Stockout weeks and excluded unusual weeks are skipped, looking further back until N calculation weeks are found. Matches E1, E7, E8, E15–E20 and E28. *R-3.*
- **FR-6 (Must) — Exponential smoothing.** Smoothing over the calculation weeks in time order with a factor from 0.1 to 0.9 (default 0.3). The first calculation week's sales are the start level (R-4), and skipped weeks are not treated as zero sales. Matches E2 and E17.
- **FR-7 (Must) — Three-week forecast horizon.** The product shows the week forecasts for weeks 1, 2 and 3 after the latest data week. Without seasonal adjustment they are equal, and the product screen shows «Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar hensyn til trend eller sesong.» Only week 1 feeds the suggested order quantity. The trend lag (E28) is a stated limitation (DR-1). *R-5.*
- **FR-8 (Must) — Insufficient data.** A product with fewer than 3 valid weeks gets no forecast and a warning about insufficient data. With the moving average, a product with fewer calculation weeks than the window gets no forecast and a warning that names the window and the number of calculation weeks. A product without a forecast has no suggested order quantity, and the user decides by hand. Matches E11 a and E11 b. *R-6; UJ-1 edge case.*
- **FR-9 (Should) — Seasonal adjustment.** R-14 applies when the company setting «Sesongjustering» is on; it is off by default.
  - When it is on, the week forecasts are seasonally adjusted, and the scenarios, the suggested order quantity and the weeks of cover use them (E27).
  - When adjustment is not possible for a product (a week number without calculation weeks, or a week-number mean of 0), the product gets week forecasts without adjustment and a note (E25, E26).
  - The cycle length is a parameter: 52 in the app and 4 in E14 and E25–E27.
  - With the setting off, the seasonal test product stays flat and shows the FR-7 note.
  - The README states the limitations in PRD §5.5. *Should item 1.*
- **FR-10 (Must) — Three scenarios.** For each horizon week: normal is the week forecast, optimistic is the week forecast × (1 + scenario percentage), and pessimistic is the larger of 0 and the week forecast × (1 − scenario percentage). E3 gives normal 14.333, optimistic 15.767 and pessimistic 12.900. Next to the scenarios: «Scenarioene viser hva som skjer hvis salget blir 10 % høyere eller lavere. De er ikke sannsynligheter.», with the actual percentage. *R-7; SM-3.*
- **FR-11 (Must) — Suggested order quantity.** The larger of 0 and (week-1 normal forecast × (1 + safety margin) − stock on hand), rounded to 6 decimals and then up to a whole unit, once, at the end. Matches E4, E5 (70, not 71), E6 and E21. It is never negative, and a product without a forecast has none. *R-8, R-9; UJ-1 climax.*
- **FR-12 (Must) — Order calculation line.** One line with the week-1 normal forecast, the safety margin as a percentage and an amount, the stock on hand, the unrounded result and the suggested order quantity:
  - E4: «Prognose 14,3 + sikkerhetsmargin 10 % (1,4) − lager 5 = 10,77 → foreslått bestillingsmengde 11»;
  - E6: «… = −40,00 → foreslått bestillingsmengde 0 (lageret dekker behovet)»;
  - E21: «… = 0,07 → foreslått bestillingsmengde 1».

  The line says «Tallene er avrundet for visning.», and below it the product screen always shows «Sikkerhetsmarginen er en enkel tommelfingerregel. Leveringstid og varer som allerede er bestilt, er ikke tatt med.»
- **FR-13 (Should) — Order quantity per scenario.** The product screen also shows the order quantity for the optimistic and the pessimistic scenario, each calculated by R-8 with the safety margin and the scenario's week-1 value. Matches E22 (13 and 10). *Should item 3.*
- **FR-14 (Should) — Overstock note.** When the suggested order quantity is 0 and the stock on hand is above 0, the product screen and the product overview show «Lagerbeholdningen dekker forventet behov neste uke.» It is not shown when the week-1 normal forecast and the stock on hand are both 0 (E23). *Should item 3.*
- **FR-15 (Must) — Stockout weeks left out.** Stockout weeks are never used in any calculation and do not count as valid weeks. Each has its own chart marker, and the product screen lists the stockout weeks left out by week number. A stockout week in the recent period is an active warning (R-15). A history with stockout weeks gets the same forecast as the same history without them (E7, E16, E17). *R-1.*
- **FR-16 (Must) — Unusual weeks.** R-10 finds the unusual weeks. Whatever the setting, each has its own chart marker, different from the stockout and level-shift markers and explained in the legend.
  - Unusual weeks are included by default.
  - When the setting excludes them, they leave the calculation but still count as valid weeks, and the product screen lists each excluded week and the number of calculation weeks used.
  - Unusual weeks in the recent period trigger a warning whether they are included or excluded.

  Matches E8, E15, E18 and E19. *R-10.*
- **FR-17 (Must) — Level shift.** Three or more unusual weeks in a row, counting valid weeks only, become level-shift weeks (R-11), which stay in the calculation whatever the setting.
  - Detection is one forward pass: two high weeks are unusual weeks (E8), three are a level shift (E9), a later spike is compared with the new level (E15), and stockout weeks in between do not break the run (E16).
  - Each level-shift week has its own chart marker.
  - A level shift in the recent period is an active warning, and the confidence label's reason names it. The warning text is FR-17b.

  `[ASSUMPTION: the rule is project-defined and is validated with the level-shift and seasonal test products.]`
- **FR-17b (Should) — Level-shift warning text.** When a level shift counts as an active warning, the product screen shows «Etterspørselen ser ut til å ha endret nivå.», for every product with at least one level-shift week in the recent period and for no other product. It does not change the confidence label. *Should item 2.*
- **FR-18 (Must) — Old-data warning.** A warning when the latest valid week is more than 8 weeks before the latest data week, counted by position. A long run of stockout weeks at the end triggers it, and the warning states how many weeks have passed since the latest valid week. Matches E12 (9 weeks: warning; 8 weeks: no warning).
- **FR-19 (Must) — Confidence label.** Every product gets «høy», «middels» or «lav» by R-16, with a Norwegian reason that names the deciding condition and lists the active warnings, for example «Middels: 1 uvanlig uke de siste 12 ukene.» Matches E29 a–g. *UJ-1 step 1; SM-10.*
- **FR-20 (Must) — Company-wide settings.** Each company has one set of settings:
  - forecasting method: moving average (default) or exponential smoothing;
  - window: 3 weeks (2 to 12);
  - smoothing factor: 0.3 (0.1 to 0.9);
  - scenario percentage: 10% (0% to 50%);
  - safety margin: 10% (0% to 100%);
  - unusual weeks: included (default) or excluded;
  - seasonal adjustment: off (only when FR-9 is built).

  A value outside its range is refused with a Norwegian message, and the previous value stays. A setting that does not apply to the chosen method is shown as not in use. *SM-3.*
- **FR-21 (Must) — Changes apply to all products at once.** A settings change takes effect immediately for every product and can be made from the product screen. The settings area always shows «Endringen gjelder alle produkter i bedriften.» After a change, the screen confirms it in Norwegian with the previous and the new affected value, for example «Grunnprognose: 14,3 → 13,8». A test changes each setting for a test product that the setting affects and checks the change:
  - method: E1 → E2, 14.333 → 13.790;
  - window: E1 with 4 instead of 3;
  - smoothing factor: E2 with 0.5 instead of 0.3;
  - scenario percentage: E3 with 20%;
  - safety margin: E4 with 50%;
  - unusual weeks: E8, 41.0 → 21.333;
  - seasonal adjustment (Should): E14, flat → seasonal.

  *UJ-1 step 4; SM-3.*
- **FR-22 (Must) — Settings saved between sessions.** The settings are saved per company and are the same after logging out and in again, or after a restart. *SM-5.*
- **FR-23 (Could) — Settings per product.** A product can have its own settings that override the company settings. Its testable consequences are written when it is planned, and it needs an amendment to AD-9.
- **FR-24 (Must) — Product overview.** After login, the product overview lists every product with its product number, name, stock on hand, week-1 normal forecast, suggested order quantity, weeks of cover, confidence label and order-soon status, sorted by R-12 (E13, E24).
  - For a product without a forecast, the forecast column shows the FR-8 reason, for example «Ingen prognose: færre enn 3 gyldige uker», and the quantity and weeks-of-cover columns show «–».
  - When the company has no products, the overview says that no data is loaded and names the load command from the README.

  *UJ-1 step 1; SM-1, SM-3.*
- **FR-25 (Must) — Product screen.**
  - A chart shows the sales history and the week forecasts with the three scenarios. Stockout, unusual and level-shift weeks each have their own marker, which differs by more than color, and a legend explains them (NFR-7).
  - The screen shows the stock on hand, the safety margin, the forecast calculation (FR-35), the order calculation line (FR-12), the confidence label with its reason, and the explanation (FR-26).
  - It lists every active warning and note that R-15 gives the product and whose FR is built, each with its Norwegian text, and nothing that does not apply. Until FR-17b is built, a level shift is named only in the reason.
  - On a 1366 × 768 screen, the suggested order quantity, the confidence label and the active warnings are visible without scrolling.
  - The settings can be changed from the screen (FR-21).

  *UJ-1 steps 2–4; SM-3, SM-10.*
- **FR-26 (Must) — Template explanation in Norwegian.** Written from the calculation result only. It covers the method and settings used, the number of calculation weeks, the weeks left out and why, every active warning and note whose FR is built, the confidence label and its reason, and the order calculation line. The same result always gives the same text, snapshot tests cover each template, and every number is an allowed number (FR-27). *SM-6.*
- **FR-27 (Must) — Explanation kept apart from calculated numbers.** The explanation has its own area headed «Forklaring», below the calculated numbers, and contains only allowed numbers:
  - the product's values as shown on the screen: the settings used, the base forecast, the week forecasts and scenarios for weeks 1–3, the safety margin amount, the stock on hand, the unrounded order result, the suggested order quantity, the weeks of cover, the number of calculation weeks, the week numbers and years of weeks 1–3 and of the weeks left out, and the counts in the active warnings, notes and reason;
  - the fixed numbers named in them: the horizon labels 1, 2 and 3, and the thresholds 3, 8, 12, 100 and 104.

  A test takes every number from each template explanation and fails on any number that is not allowed for that product. Text from a language model is labeled «KI-omformulert forklaring» (when FR-28 is built). *SM-6.*
- **FR-28 (Should) — Optional local language model.** A local model rephrases the template explanation in Norwegian.
  - It is off by default and is switched on in the local configuration listed in `.env.example`, not in the company settings. It needs no API key, paid service or internet connection, and no hosted AI is used (AG-5).
  - The model receives the template with named placeholders, for example `{base_forecast}`, and the app inserts every number.
  - The text is rejected when its placeholders differ in name, count or order, when the Norwegian §3 label nearest before a placeholder differs, or when a number appears outside a placeholder. A test sends prepared answers with each fault.
  - The template text is shown, without an error, when the model server is not running, the model is missing, no answer arrives within 10 seconds `[ASSUMPTION]`, the response contains an error, or the text is rejected.
  - The README names the model and its license obligations and describes it as a separate, optional step with its download size and time. It is never part of the basic setup (SM-2).

  *SM-6; Should item 6, the last.*
- **FR-29 (Should) — Adjust an order quantity.** The user replaces the suggested order quantity with an adjusted whole number of 0 or more; other input is refused with a Norwegian message. The suggestion stays visible next to the adjusted quantity, and the user can reset to it. Example: 70 changed to 80 marks the product «Justert av deg». *UJ-1 step 5; Should item 4.*
- **FR-30 (Should) — Combined order overview.** Every product with its suggested or adjusted order quantity, marked «Foreslått» or «Justert av deg». A product without a forecast and without an adjusted quantity shows «–» and is marked «Uten prognose». The products follow the R-12 order. *UJ-1 step 6; Should item 5.*
- **FR-31 (Could) — Save adjustments and mark products as approved.** Adjusted quantities are saved between sessions, and the user can mark a product as approved. It replaces only the storage behind `web/adjustments.py` (AD-10).
- **FR-32 (Could) — CSV export.** The combined order overview can be exported as a CSV file.
- **FR-33 (Could) — Stock not lasting through weeks 2 and 3.** A note when the stock on hand plus the suggested order quantity is less than the sum of the week forecasts for weeks 1–3; the Message Catalogue text is «Lageret og bestillingen dekker ikke uke 2 og 3.» The teacher asked for its testable consequences before it is planned.
- **FR-34 (Could) — Forecast accuracy.** The product screen shows the mean absolute error (MAE) of past one-week forecasts. MAPE is not used.
- **FR-35 (Must) — Forecast calculation.** The product screen shows how the base forecast and the week forecasts were calculated:
  - for the moving average, one line with the values used, for example «Glidende gjennomsnitt, 3 uker: (16 + 12 + 15) / 3 = 14,3» (E1), and the week numbers of the calculation weeks used;
  - for exponential smoothing, the last update, for example «Eksponentiell glatting, faktor 0,3: 0,3 × 15 + 0,7 × 13,3 = 13,8» (E2), and a table of every calculation week with its sales and level;
  - a list of the weeks left out and why (stockout week or excluded unusual week);
  - with seasonal adjustment (Should), the seasonal indices, the adjusted values and the week forecasts (E14).

  Numbers are rounded for display by R-9, and «Tallene er avrundet for visning.» stands below the exponential-smoothing line and the seasonal values. *SM-1, SM-3.*
- **FR-36 (Should) — Seasonal-pattern warning.** When a product has a seasonal pattern by R-17 (an index of 1.3 or more, or 0.7 or less `[ASSUMPTION]`) that the forecast does not use, because seasonal adjustment is off or not possible: «Produktet har tydelig sesongvariasjon som prognosen ikke tar hensyn til.» It counts as an active warning for the confidence label. It needs only R-14 steps 1 and 2, so it can be built before FR-9. Matches E30. *Should item 2.*

**Calculation rules and reference examples (PRD §5).** The rules apply per product in this order: R-1; R-10 and R-11; R-2 and R-6; R-3 or R-4 (on seasonally adjusted values with R-14); R-5 (R-14 step 3); R-7; R-8 and R-9 with R-13; R-12; R-15 to R-17.

| Rule | FRs | Reference examples | Priority |
|---|---|---|---|
| R-1 Valid weeks | FR-15 | E7, E16, E17 | Must |
| R-2 Calculation weeks | FR-5, FR-6, FR-16 | E8 | Must |
| R-3 Moving average | FR-5 | E1, E7, E8, E15–E20, E28 | Must |
| R-4 Exponential smoothing | FR-6 | E2, E17 | Must |
| R-5 Week forecasts | FR-7 | E28 | Must |
| R-6 Minimum data | FR-8 | E11 a, E11 b | Must |
| R-7 Scenarios | FR-10 | E3 | Must |
| R-8 Suggested order quantity | FR-11, FR-12; FR-13 (Should) | E4, E5, E6, E21; E22 (Should) | Must |
| R-9 Rounding and display | FR-11, FR-12, FR-35 | E5, E20, E21 | Must |
| R-10 Outlier rule | FR-16 | E8, E10, E15, E18, E19 | Must |
| R-11 Level shift | FR-17 | E9, E15, E16 | Must |
| R-12 Order-soon status and sorting | FR-24; FR-30 (Should) | E13, E23, E24 | Must |
| R-13 Stock on hand | FR-3, FR-11 | – | Must |
| R-14 Seasonal adjustment | FR-9; steps 1 and 2 also FR-36 | E14, E25, E26, E27 | Should |
| R-15 Warnings and notes | FR-8, FR-15 to FR-18; the notes of FR-7, FR-9, FR-14 and FR-33 | E12 | Must; item 6 (FR-36) Should |
| R-16 Confidence label | FR-19 | E29 a–g | Must |
| R-17 Seasonal-pattern check | FR-36 | E30 | Should |

The Must gate in SM-1 is E1–E13, E15–E21, E23, E24, E28 and E29 (24 examples). E14, E22, E25–E27 and E30 (6 examples) pass once FR-9, FR-13 and FR-36 are built.

### NonFunctional Requirements

All NFRs, AI guardrails and delivery requirements are Must (PRD §8.1), except DR-10, which is not in version 1 (D-1).

**Cross-cutting (PRD §6.1)**

- **NFR-1 Local and free to run.** The app and every Must feature run on one computer without paid services, API keys or third-party accounts, and every tool the README asks for is free for personal and educational use. After installation, the local app and its database run without an internet connection, with every asset served locally and none from a CDN. The README covers macOS and Windows.
- **NFR-2 Correct, testable calculations.** All §5 rules live in one calculation module with no dependency on the user interface or the database. Automated unit tests check every rule and every reference example for the features built (SM-1). All tests run with one documented command that needs nothing beyond the README installation and the started local database, and the README shows the expected result.
- **NFR-3 Security.** Passwords are hashed as FR-1 describes, and the logged-in company is checked on the server on every request (FR-2). The session-signing secret is created by the load command (DR-4) when it is missing, stored in a local file that `.gitignore` excludes, and never committed; setup needs no manual file editing. The repository holds no secrets, and `.env.example` lists the optional configuration. The local database has no stored password and accepts connections only from the same computer.
- **NFR-4 Privacy.** Only synthetic data is used. Files in the repository contain no personal data and no local file paths. Saved AI sessions are cleaned before they are committed. Before submission, the group scans the whole repository history for secrets, personal data and local paths and records the result in the QA log (DR-9).
- **NFR-5 Language and number format.** All screens, messages, warnings, notes and explanations are in Norwegian `[ASSUMPTION: bokmål]`. Numbers use a decimal comma; percentages are whole numbers with «%».
- **NFR-6 Platform and screen size.** Prognose is a responsive website with the same functions on a PC or laptop (the main case, UJ-1), an iPad and a phone. From 320 px wide there is no horizontal page scrolling, no text overlaps or is cut off, and every control can be reached with the keyboard and used by touch; wide tables and the chart may scroll inside their own frame. In one column the product comes first and the product list below it. On touch screens every control has a target of at least 44 × 44 px, form fields use 16 px text, and nothing depends on hover. FR-25 sets what must be visible at 1366 × 768, and on smaller screens the same content comes first in the product area. The README lists the screen sizes, devices and browsers tested, with at least one current browser per desktop operating system, each marked as a real device or the browser's responsive view; the phone sizes are also tested on a real phone that reaches the local app over the local network, only during the test.
- **NFR-7 Readable markings.** In the chart, stockout, unusual and level-shift weeks differ by more than color, for example by shape, and a legend explains them.
- **NFR-8 Responsiveness `[ASSUMPTION]`.** With 50 products of 104 weeks each, the product overview and the product screen open within 2 seconds on an ordinary laptop, and results update within 2 seconds after a settings change. The target applies to the local app.
- **NFR-9 Simple architecture.** One web application with one PostgreSQL database and no more parts than it needs: a local PostgreSQL server. The binding choices are in the architecture spine.
- **NFR-10 Robustness.** Numeric fields accept a decimal comma or a decimal point. Empty or non-numeric input is refused with a Norwegian message, and the previous value stays. No address or input shows a stack trace or a debug page. An unknown address shows a Norwegian "not found" page with a link to the product overview. Submitting the same change twice, reloading a page or going back gives the same result without errors.
- **NFR-11 Basic accessibility.** Text contrast meets WCAG 2.2 AA. Every function works with the keyboard alone, with a visible focus. Every form field has a visible label. Pages declare Norwegian as their language. The chart has a text alternative: a short summary and a table with the plotted values, and its markings follow NFR-7.

**AI guardrails (PRD §6.2)**

- **AG-1 No numbers from AI.** Forecasts, scenarios, order quantities, weeks of cover, warnings, notes and confidence labels come only from the §5 rules.
- **AG-2 Explanation without a language model.** The Must explanation is template-based (FR-26).
- **AG-3 Optional local model under control.** It runs locally, is off by default, only rephrases, and falls back to the template explanation in every case that FR-28 lists.
- **AG-4 Labeled AI text.** Text written or rephrased by a language model is labeled and kept apart from the calculated numbers (FR-27).
- **AG-5 No external AI services.** Version 1 sends no data to external AI services.
- **AG-6 AI in development is documented** (DR-5).

**Delivery and repository (PRD §6.3)**

- **DR-1 README.** It covers:
  - what Prognose does and for whom, with screenshots of at least the login page, the product overview and the product screen (a screen recording of UJ-1 steps 1–4, at most 2 minutes, is optional);
  - the prerequisites with minimum versions;
  - setup on macOS and Windows, tested from a fresh clone: exact commands for macOS Terminal and Windows PowerShell run in the project's environment, how to start and stop Prognose and its local database, how the session secret is created, fixes for the likely errors (a database that is not started, a port in use), and the setup time once SM-2 is confirmed;
  - the two test companies' customer numbers and passwords, how to generate and load the data, and how an explicit reset restores the seed state and also resets the settings and adjustments (DR-4);
  - at the top, how to start Prognose locally, and that version 1 is not published, with the reason (DR-10);
  - a section on keys and secrets: no API key, paid service or third-party account is needed, the session secret is created automatically and kept out of Git, the local database has no password, and `.env.example` lists only optional variables (NFR-1, NFR-3);
  - «Prøv selv» in 5–10 steps that follow UJ-1, and a table of the test products naming the rule, warning or confidence label each shows and its reference example. For UJ-1 step 4 it uses the rule test product built from E8, so switching unusual weeks changes the base forecast (41.0 → 21.333);
  - how to run the tests with the expected result (NFR-2), and the screen sizes, devices and browsers tested, each marked as a real device or the browser's responsive view (NFR-6);
  - how to switch on the optional language model as a separate step: the model, its download size and time, its license obligations, and what happens without it (FR-28);
  - an overview of the folders and links to the PRD, the architecture, the epics and stories, the decision logs, the AI steering log (DR-5), the QA log (DR-9) and the status table (DR-8);
  - the known limitations: the trend lag (FR-7), the limitations of R-14, the assumptions behind R-8 and the project-defined rules;
  - every Should item that was not built, with the reason.
- **DR-2 Repository layout.** The synthetic data, the generator script, the reference spreadsheet, the documentation, the saved AI sessions and the planning artifacts each have a documented place (fixed in the architecture, see the Structural Seed). The README explains every top-level folder, including the BMAD and Claude Code folders. The root holds no loose files other than the README, a license and configuration files. `.gitignore` keeps out the virtual environment, caches, test and coverage output, the local database data, `.env`, the session-secret file, and operating-system and editor files. The generated seed data is versioned, and the database is not. `.env.example` lists the optional configuration. One formatter and one linter run with a documented command and pass on the submitted commit, and dependencies are pinned to exact versions in one file.
- **DR-3 Reference spreadsheet.** A spreadsheet in the repository holds the hand-calculated E1–E30 and the expected results for every rule test product (FR-3). The automated tests use the same inputs and expected results.
- **DR-4 Seed data.** The deterministic generator script creates the data, and one documented command loads it into an empty database. The load command never deletes or overwrites data on its own: when the database already holds data, it stops and changes nothing. Only an explicit reset that the user confirms deletes the data and reloads the seed state, without duplicates or errors, and the README says that it also resets the settings and adjustments.
- **DR-5 Process documentation, AI use and traceability.**
  - Decisions are recorded with their rationale.
  - The prompts and AI sessions for each story are saved in the documented folder, cleaned as NFR-4 requires.
  - An AI steering log records at least five cases, at least one per epic, where the group clarified, rejected or corrected AI output: what the AI proposed, what was wrong, what the group decided, and the commit or pull request. The planning phase gives the first entries (the rounding error in E5, the processing order of R-10 and R-11).
  - Every story names the FR-n it implements, every test names the FR-n or E-n it verifies, and every commit names its story.
  - The change-log rule in PRD §12 applies to the architecture, UX and epics documents.
  - The group updates the Product Brief with the changes in addendum §7.
- **DR-6 Deadline.** The submission deadline is 8 December 2026 at 23:59 (earlier 1 December 2026), and the work is planned backwards from it. Sprint planning sets the milestone dates; PRD §8.2 gives the order of the Should items. Should and Could items start only after the Must scope passes SM-1 and SM-3.
- **DR-7 Workflow.** Each story is built on its own branch and merged through a pull request that names the story and its FR-n and says what was tested; review comments stay in the pull request. Defects and open points are tracked as issues. Commits are small and pushed as the work happens. **Definition of Done:** the story's tests and the linter pass; there is no commented-out, unused or duplicated code; the status table and the affected documents are updated; and the pull request has been reviewed.
- **DR-8 Status table.** One table lists every FR, and DR-10, with its priority, its status at submission (built, partly built, not built or changed), its stories and tests, and the reason for any deviation. The README links it.
- **DR-9 QA log.** Every defect in AI-generated code or text found by a test, the reference spreadsheet, a review or a manual test is recorded with how it was found, the fix, and the commit or pull request. A manual test checklist for NFR-6, NFR-7, NFR-8, NFR-11 and SM-2 (with the offline start) runs on the final commit and is recorded with the date, operating system, browser and result, and for NFR-6 also the screen size and whether it ran on a real device or in the browser's responsive view.
- **DR-10 Publishing (not in version 1).** Version 1 is not published: on Canvas on 2026-11-19 the teacher clarified that publishing is not mandatory, so publishing on Vercel with Neon was removed together with Story 1.9 (D-1). The status table lists DR-10 as not built, with this reason (DR-8).

**Success metrics that shape stories (PRD §9)**

- **SM-1 Correct calculations.** 100% of the Must reference examples pass as automated tests and match the reference spreadsheet (the Must gate above); the Should examples pass once their FRs are built.
- **SM-2 Runnable by the examiner.** From a fresh clone, following only the README, a person logs in and sees the product overview on macOS and on Windows, without paid services or keys, and after installation also with the network switched off. Target: at most 15 minutes from the clone to logged in, once the README's prerequisites are installed, confirmed by testing (PRD §10 question 2).
- **SM-3 Core flow works.** Log in; select a product; see the sales history, the forecast calculation and the scenarios; change the forecasting method, the safety margin or the unusual-weeks setting; and see the affected value change. At least one automated test runs this flow through the web application.
- **SM-4 Isolation.** The two-account test passes, including lists.
- **SM-5 Persistence.** Data and settings are unchanged after a restart of the app and the database.
- **SM-6 Explanation integrity.** Every number in every template explanation is allowed, and no rephrased text that fails an FR-28 check is accepted.
- **SM-7 Rule coverage.** Every warning and every confidence label, including «høy», is triggered by at least one test product (FR-17b and FR-36 once built).
- **SM-8 Traceable process.** Decisions and AI use are documented, the AI steering log has at least five cases linked to commits or pull requests, every story was merged through a reviewed pull request, and the status table traces every FR to its stories and tests.
- **SM-9 Published version works (not in version 1).** Removed with DR-10 on 2026-11-19 (D-1); SM-2 and SM-3 check the local version.
- **SM-10 Confidence label understood.** Two people outside the group see the product screen of a test product labeled «lav», and each explains, without reading the reason aloud, why it has that label. It passes when both name the deciding condition (R-16). It is checked by hand when the Must scope passes SM-3 and recorded in the QA log.
- **Counter-metrics.** SM-C1: no accuracy gains through models that cannot be checked by hand. SM-C2: no Should or Could item starts before the Must scope passes SM-1 and SM-3. SM-C3: warnings are never weakened to get more «høy» labels.

### Additional Requirements

**Starter template: none. The first story builds the skeleton by hand (affects Epic 1 Story 1).** The architecture names no third-party starter template. Its delivery order, aligned on 2026-11-18 (D-1, D-3), says that the first stories prove the local path (Story 1.1) and CI (Story 1.2), and that the setup test on Windows and offline (Story 1.3) is a story of its own; version 1 is not published (D-1):
- the Structural Seed: `src/` with `manage.py`, the Django project `prognose/` and the packages `forecasting/`, `explanation/` and `web/`; `tests/`, `data/`, `reference/` and `docs/`;
- `pyproject.toml` with exact pins, `uv.lock`, `.python-version` (3.13), `compose.yaml`, `.env.example` and `.gitignore`;
- the custom user model `web.Company` in the first migration (AD-6), so it exists before the first `migrate`;
- GitHub Actions that run the tests and Ruff on Linux, with the database from `compose.yaml` (AD-17).

**Architecture decisions (spine of 2026-11-17)**

- **AD-1 Functional core, imperative shell.** `forecasting/` and `explanation/` import only the Python standard library; `explanation/` may import `forecasting/`, never the reverse. Neither imports Django, a database driver or an HTTP library, and neither reads the clock, files or environment variables. An import test enforces this (AD-17).
- **AD-2 One compute path per company.**
  - The core computes from inputs only: `forecast_product(weeks, stock_on_hand, settings)` returns a frozen `ProductResult`; `build_overview(results, adjustments)` applies R-12 and gives the groups, the week figures, the previous and next product and the combined order overview; `describe_settings_change(before, after)` gives the FR-21 confirmation lines.
  - One loader, `web/company_data.py`, reads a company's settings, products, sales weeks and adjustments through `web/queries.py` in a fixed number of queries, whatever the number of products. Every page uses it, and the product screen computes the whole overview for its list and its previous and next links.
  - The FR-21 confirmation compares the product the user came from, before and after the change. From a page without a product, it shows only the line naming the new setting.
  - Search hides products from the computed overview and never changes their order, their results or the week figures.
  - The database stores inputs only; results are computed on every request and never stored. Nothing outside the core calculates, rounds, sorts or groups domain values.
- **AD-3 One rounding and one Norwegian number format.** The core keeps full float precision and returns numbers, never formatted strings. Every rounding goes through `forecasting/rounding.py`: first to 6 decimals, then up to whole units (R-8) or half away from zero for display (R-9), with the `decimal` module, never `round()`. Norwegian display text comes only from `forecasting/display.py`: a decimal comma, the minus sign U+2212, no thousands grouping, a no-break space before «%», and week labels with the year at New Year and in lists that reach before the recent period. The template filters, the explanation and the chart all call it.
- **AD-4 Result wording in one place.** Every Norwegian sentence that depends on a result comes from `explanation/`, with the EXPERIENCE.md Message Catalogue as its copy source: warnings, notes, confidence reasons, the forecast and order calculation lines, the FR-21 confirmation, the chart summary and the template explanation. Templates place these strings and never compose them; fixed interface text lives in the templates.
- **AD-5 Explanation guardrails.** Explanation templates use named placeholders, filled from `ProductResult` through `forecasting/display.py`. `ProductResult` exposes the FR-27 allowed numbers as display strings, and a test checks every number in every template explanation against them. The FR-28 checks are pure functions in `explanation/`. The only network call in the app is `web/rephrase.py`: standard library only, a 10-second timeout, off unless the local `.env` names a model URL, and the template text on any failure.
- **AD-6 The company is the authenticated principal.** The custom user model `web.Company` has `customer_number` as its login field and is created in the first migration. Passwords use Django's default PBKDF2 hasher. `LoginRequiredMiddleware` denies by default; only the login page at the app root and the error pages are exempt. Logging out is a POST.
- **AD-7 Company isolation in one data-access module.** Every read or write of company data goes through functions in `web/queries.py` that take the logged-in company as their first argument and filter by it. Views, forms and the chart never use model managers for company data; only `load_seed` and the migrations touch the tables directly. A lookup outside the company raises `Http404` and renders the same page as an unknown address. The two-account test covers every route in the URL map and every list.
- **AD-8 Weeks by ISO week and position.** A week is an ISO 8601 week (ISO year and week number). A sales week is identified by its product and its position, 1 to N, which orders every calculation and measures every distance. Each product's history is a run of consecutive weeks without gaps that ends at the company's latest data week, and `load_seed` refuses seed files that break this. The latest data week is derived, never stored. Calendar arithmetic only labels weeks 1–3, and no domain code reads today's date.
- **AD-9 Settings defined once.** Each company has one `CompanySettings` row. The FR-20 defaults and ranges are defined once, in `forecasting/settings.py`, and the model defaults, the form validation and `load_seed` read them. The window and both percentages are whole numbers; the smoothing factor has one decimal, from 0,1 to 0,9. Number fields accept a decimal comma or a decimal point; other input is refused in Norwegian, and the previous value stays.
- **AD-10 Server-side state and Post/Redirect/Get.** Every change (login, logout, settings, the unusual-weeks switch and adjusted quantities) is an HTML form POST with CSRF protection, followed by a redirect. Navigation and search are GET requests. There are no fetch or XHR calls and no client-side state. Adjusted quantities live in the server-side session (Django's database backend), keyed by product number and latest data week, are reached only through `web/adjustments.py`, and enter the core as an input. Only the explicit reset deletes sessions.
- **AD-11 Rendering, URLs and the chart.**
  - Pages are Django templates. One stylesheet defines the DESIGN.md tokens as CSS custom properties, and components use only those variables. Fonts are the DESIGN.md system stacks. There is no front-end framework, UI library, web font or CDN.
  - The forecast chart is inline SVG rendered on the server. A pure function in `web/chart.py` computes its geometry from `ProductResult` and display strings only, and its summary text comes from AD-4.
  - One optional script, `web/static/web/app.js`, only enhances: arrow keys, scroll positions, submitting the switch, filtering while typing, reloading a page that the browser restores from its back/forward cache (so that Back after «Logg ut» does not show a company's page), and enabling on Innstillinger the setting that the chosen forecasting method uses, so that the method and that setting change in one save. Every function works without it: a button next to the switch sends the change, and a field disabled for the saved method is changed in a second save. The settings form accepts the method and the setting it uses in one POST, which the tests check (amended 2026-11-18, D-4 and D-5).
  - URL map: `/` login (GET and POST); `/logg-ut/` log out (POST); `/produkter/` the product overview, with `?sok=` for search; `/produkter/<varenummer>/` the product screen; `/produkter/<varenummer>/mengde/` set or reset an adjusted quantity (POST, FR-29); `/innstillinger/` the settings (GET and POST), returning to the in-app path it came from; `/innstillinger/uvanlige-uker/` the unusual-weeks switch (POST); `/bestillingsoversikt/` the combined order overview (FR-30).
  - DESIGN.md and EXPERIENCE.md win over the mockup.
- **AD-12 Norwegian error pages.** DEBUG is off unless the local `.env` turns it on. The responses 400, 403 (including a failed CSRF check), 404, 405 and 500 render Norwegian pages with the Message Catalogue texts in the not-found panel. A database connection error renders the «Database unavailable» page with status 503 wherever it is raised, also in middleware, and that page reads nothing from the database (amended 2026-11-18). Errors are logged to the console without request bodies, passwords, secrets or database URLs.
- **AD-13 Local run mode and configuration.** One run mode, the local one. Settings read only environment variables, after loading an optional local `.env`, and neither `.env` nor an API key is needed for the basic setup.
  - `DATABASE_URL` defaults to `postgresql://prognose@127.0.0.1:15432/prognose`. The session secret comes from the git-ignored file `.secret_key`, which `load_seed` creates when it is missing and never overwrites. The app runs with `uv run python src/manage.py runserver --insecure` on 127.0.0.1.
  - Phone test over the local network (NFR-6): only for the manual test on a real phone, the optional local variable `PROGNOSE_LAN_HOST` names the computer's address on a private network, and the app is started with `runserver --insecure 0.0.0.0:8000`. That address is added to `ALLOWED_HOSTS`; without the variable only `127.0.0.1` and `localhost` are allowed. DEBUG stays off, and the database port stays on `127.0.0.1`.
  - `LANGUAGE_CODE` is `nb` and `TIME_ZONE` is `Europe/Oslo`.
- **AD-14 PostgreSQL locally and in CI.** PostgreSQL 18 everywhere: the image `postgres:18.7` in `compose.yaml` locally and in CI. Data access goes through the Django ORM and migrations with psycopg 3, without raw SQL.
  - `compose.yaml` holds only the database: user and database `prognose`, trust authentication, the port `127.0.0.1:15432`, a named volume at `/var/lib/postgresql`, `restart: unless-stopped` and a `pg_isready` health check. It is started with `docker compose up -d --wait`.
  - The tests run against the local PostgreSQL, and the app writes no files at request time.
- **AD-15 Seed data and the explicit reset.** `data/generate_seed.py` writes the versioned JSON files in `data/seed/` and gives identical output on every run. The files hold inputs and password hashes made with Django's hasher and a fixed salt per company. The rule test products take their series from the reference spreadsheet, and the two test companies have disjoint product numbers. `load_seed` without options loads into an empty database only; when any company exists, it stops with a Norwegian message and changes nothing. `load_seed --reset` is the only command that deletes data: it asks for typed confirmation, then, in one transaction, deletes the companies with their data and all sessions and loads the seed. Nothing runs it automatically.
- **AD-16 Publishing on Vercel (removed from v1).** Removed on 2026-11-19 together with Story 1.9 (D-1); the spine keeps the decision as history.
- **AD-17 One test command and one answer key.** `uv run pytest` runs every test against the local PostgreSQL: the core rules, a snapshot of each explanation template, the FR-27 number test, web tests through Django's test client (including the SM-3 core flow and the SM-4 two-account test), the AD-1 import test, and `makemigrations --check`. The reference spreadsheet in `reference/` is the single answer key: the tests and the seed generator read its inputs and expected values with openpyxl, and no expected value is copied into test code. When a test and the spreadsheet disagree, the case is calculated again by hand, whichever was wrong is corrected, and the finding goes into the QA log. Every test names the FR-n or E-n it verifies, or its NFR-n, DR-n or AD-n when it verifies no FR (D-10). `uv run ruff check` and `uv run ruff format --check` cover Python files only. GitHub Actions runs the tests and Ruff on every pull request on Linux, and a pull request is merged only when they pass.

**Consistency conventions**

- **Naming:** code in English with the PRD §3 terms (`base_forecast`, `week_forecasts`, `calculation_weeks`, `safety_margin`, `stock_on_hand`, `weeks_of_cover`, `order_soon`, `confidence_label`); UI text in Norwegian with the glossary labels and fixed strings verbatim; Norwegian URL slugs.
- **Data and formats:** the product number (`varenummer`) is a string of 5 digits, unique within a company. Units sold, stock on hand and quantities are integers; forecasts are floats. Percentages are stored as whole numbers (10 means 10 %), and the smoothing factor with one decimal. Enum values: `moving_average`, `exponential_smoothing`, `included`, `excluded`.
- **Errors:** Norwegian messages name the problem and the fix; validation keeps the previous value; unknown addresses and other companies' objects give the same not-found page.
- **Logging:** console only, never passwords, the session secret, database URLs or request bodies.
- **Configuration:** environment variables only. `.env.example` lists `PROGNOSE_DEBUG`, `DATABASE_URL` and `PROGNOSE_LAN_HOST` (the phone test, AD-13), and `PROGNOSE_LLM_URL` and `PROGNOSE_LLM_MODEL` once FR-28 is built, each marked as optional or secret (aligned in the spine on 2026-11-18 and 2026-11-19). None of them is needed for the basic setup, and no API key is needed.
- **Dependencies:** `pyproject.toml` declares the direct dependencies with exact pins; `uv.lock` is the one lock file; installs use `uv sync --locked`. A new package needs an update to the Stack table in the spine.
- **Commands,** the same on macOS and Windows and run through `uv run` without activating a virtual environment: `docker compose up -d --wait`, `uv sync --locked`, `uv run python src/manage.py migrate`, `uv run python src/manage.py load_seed`, `uv run python src/manage.py runserver --insecure` and `uv run pytest`.
- **Platforms:** macOS on Apple silicon or Intel, and Windows 10 22H2 or Windows 11 23H2 on x64, each with Docker Desktop; on Windows, Docker Desktop needs WSL 2 and hardware virtualization switched on. Windows on ARM is not supported in v1, because psycopg has no wheel for it.
- **Optional features:** Should and Could items exist in code only once they are built, with no runtime feature flags except the FR-28 switch. A story that builds an item updates every place EXPERIENCE.md ties to it, for example the header link, step 3 of the week path and the last-product button for FR-30.
- **Checks before a pull request:** `uv run pytest`, `uv run ruff check` and `uv run ruff format --check` pass locally and in CI; Story 1.1 comes before CI and passes them locally (D-9).
- **Documents:** `docs/` holds `PRODUCT.md`, the `DESIGN.md` link, `arbeidslogg.md`, `qa-logg.md` (DR-9), `ki-styringslogg.md` (DR-5) and `statustabell.md` (DR-8). Session logs are in `.logs/<bruker>/`, exported AI sessions in `.logs/<bruker>/sessions/` (the routine for AI sessions), and story specifications in `_bmad-output/implementation-artifacts/`.
- **Delivery order** (aligned on 2026-11-18 and 2026-11-19, D-1 and D-3): the first stories prove the local path and CI (Stories 1.1 and 1.2); the setup test on Windows and offline (Story 1.3) is a story of its own and blocks no other development; version 1 is not published; then the Must items; Should and Could items only after the Must scope passes SM-1 and SM-3.

**Stack (exact versions):** Python 3.13 (from `.python-version`, installed by uv); Django 5.2.19 LTS; psycopg[binary] 3.3.9; PostgreSQL 18.7 (`postgres:18.7`) locally and in CI; Docker Desktop 4.99.0 with Docker Compose v5.7.0 as the local prerequisite; uv 0.13.9 at authoring (0.12.13 tested); pytest 9.2.0; pytest-django 4.14.0; Ruff 0.17.5; openpyxl 3.1.5 (development only).

**Deferred in the spine, settled in stories**

- **Publishing (removed from v1, D-1).** Vercel with Neon was planned as Story 1.9 until 2026-11-19. Story 1.2 still checks that GitHub Actions is allowed in the organization.
- **Tests not run yet** (`docs/qa-logg.md`): the offline start with Docker Desktop, and the whole README setup on Windows x64. Both run in Story 1.3, which blocks no other story, and again on the final commit (DR-9, SM-2, D-3).
- **Schemas** of the seed JSON and of the spreadsheet's answer-key sheet: set in the data story.
- **Validation messages the Message Catalogue lacks,** for a percentage with decimals or a smoothing factor with two decimals: settled in the settings story under the UX copy rules.
- **FR-28:** the runtime and the model are chosen when FR-28 is scheduled, as the last Should item. How the 10-second timeout fits NFR-8's 2 seconds was decided on 2026-11-18 (D-7).
- **Could items:** FR-31 replaces only the storage behind `web/adjustments.py`; FR-23 needs an amendment to AD-9; FR-32 to FR-34 are decided when scheduled.
- **Caching** only if the NFR-8 check fails, with an amendment to AD-2.
- **Not in v1:** a Content Security Policy, browser end-to-end tests (Playwright), rate limiting, and monitoring, backup or alerting services.
- **Docker Desktop's terms** are checked again before submission: it is free for personal use and education.

**Planning constraints (PRD §8, DR-6 and the teacher's feedback)**

- **One priority per story.** A story takes its priority from its FRs and never mixes Must with Should or Could (teacher's feedback 4.3).
- **Order.** The Must scope comes first. Should and Could items start only after the Must scope passes SM-1 and SM-3 (DR-6, SM-C2). The Should order is fixed (PRD §8.2): 1. FR-9; 2. FR-36 and FR-17b; 3. FR-13 and FR-14; 4. FR-29; 5. FR-30; 6. FR-28. The Could items (FR-23, FR-31 to FR-34) follow only if time allows. The teacher asked that the epics build on this order and on the cut line; the cut line no longer applies, because publishing is not in version 1 (D-1).
- **Publishing (not in version 1).** Until 2026-11-19 the PRD's cut line applied to publishing on Vercel with Neon, planned as Story 1.9 right after Story 1.8 (the user's decisions of 2026-11-18). On 2026-11-19 the teacher clarified on Canvas that publishing is not mandatory, and the user removed it from version 1 together with Story 1.9; the cut line no longer applies (D-1).
- **Done when** the Must scope passes SM-1 and SM-3, and SM-2 holds on the final commit.
- **If time runs short in the Must scope:** sprint planning sets the order in which the remaining Must stories are finished, with the stories needed for SM-1, SM-2, SM-3 and DR-1 first. A Must story that is not built is marked as not built in the status table and the README, with the reason (DR-8). No priority changes (the teacher's feedback, 4.1).
- **Deadline.** 8 December 2026 at 23:59 (DR-6; earlier 1 December 2026), 20 days after this document was started. Sprint planning sets the milestone dates in `_bmad-output/implementation-artifacts/sprint-plan.md`.
- **Could items** get testable consequences when they are planned (PRD §4).
- **Every epic** gives at least one case for the AI steering log (DR-5), and every story meets the DR-7 Definition of Done.

**Open points from `issues.md` that become story work**

- The reference spreadsheet with the hand-calculated E1–E30 (DR-3) does not exist yet (open since 2026-11-03). It is the single answer key that the tests and the seed generator read (AD-15, AD-17), so it comes before the rule tests and the seed data.
- The README setup sequence has to be written and tested (open since 2026-11-01): the database starts with Docker Compose, the commands run with `uv run` without activating a virtual environment, and the README says that Windows on ARM is not supported.
- The setup-time test: at most 15 minutes from the clone with the prerequisites installed, on clean macOS and Windows machines, including the offline start, and again on the final commit (SM-2, PRD §10 question 2). The database part is tested on macOS; Windows and the offline start remain.
- No publishing in version 1 (D-1). Vercel with Neon, first placed in the first story by `issues.md` and made Story 1.9 on 2026-11-18, was removed on 2026-11-19.
- `.gitignore`: the Next.js part and `db.sqlite3*` can be removed in the first story.
- The README links to the QA log (DR-1).
- The final check before submission: repeat the privacy scan of the whole Git history on the final commit and record the result in `docs/qa-logg.md` (NFR-4, DR-9).
- The Impeccable finish review and documentation run on the real build, against the new `DESIGN.md`.
- Impeccable commands that write `DESIGN.md` (for example `document`, or the end of a build) go through the link `docs/DESIGN.md` to the approved design, or replace the link. They run only with approval and with a row in the UX change log. On Windows without symbolic-link support in git, the link becomes a text file.
- If FR-28 is built: choose the local model and clarify its license (PRD §10 question 5).
- Update the Product Brief with the changes listed in addendum §7 (DR-5).
- Textbook sources for the inventory rules (research report B), or a note in the process documentation that they are missing (PRD §10 question 3).

Not story work: confirming Docker's terms in Docker Desktop; GitHub's «Keep my email addresses private» setting and the Git identity in other clones; the Impeccable settings file in the home folder; the relative links inside `DESIGN.md` when read through `docs/DESIGN.md`, which cannot be fixed without changing the approved design; and the optional polishing of the research reports.

### UX Design Requirements

From `DESIGN.md` (how it looks) and `EXPERIENCE.md` (how it works), with copy from the approved mockup where the spines leave it open. Component names match across both spines. Each UX-DR is Must unless marked otherwise; a part marked «Should, FR-n» is built by the story that builds FR-n (Optional features convention).

**Design system**

- **UX-DR1 Design tokens.** One stylesheet defines every token in the DESIGN.md frontmatter as a CSS custom property, with the values copied verbatim: 26 colors, 17 typography roles, 5 radii (xs 3, sm 4, md 6, lg 10 px, full) and the spacing scale (4, 8, 12, 16, 20, 24, 32 and 40 px; list width 392 px; narrow list width 340 px; card padding 12 × 14 px; panel padding 16/20/20 px; text measure 72ch). Components use only these variables (AD-11).
- **UX-DR2 Typography.** One system UI stack and the system monospace stack for formulas, with no web font (NFR-1). Every number uses tabular numerals. No text is below 12 px (chart labels only), and no UI text is below 13 px. No letter-spacing and no uppercase labels. Headings have more space above than below, and paragraphs stop at 72ch. The roles follow the DESIGN.md table, for example the page title for the product name and «Denne uken», and the 44 px order number for the suggested order quantity on the product screen.
- **UX-DR3 Color roles and contrast.** Each color has one job:
  - blue for actions and the decision: buttons, links, the selected product, the focus ring, the switch when on, and the suggested order quantity in large type;
  - turquoise for the forecast: the forecast line and dots, the forecast week labels in the chart, the «brukt» tag, the shading of the forecast weeks, the «Forklaring» panel and the scenario band;
  - green for trust and completion only («høy», completed steps and segments), never for buttons or warnings;
  - amber for unusual demand: «middels», unusual weeks, level shifts and seasonal patterns;
  - red for data that cannot be trusted: «lav», stockout weeks, old data, missing forecasts and errors.

  Text on a tint uses that tint's dark tone or ink, never muted gray, and turquoise text is never placed on the band. Every text pair is at least 4.5:1 (the DESIGN.md contrast table), and field borders and the switch when off are at least 3:1. Light mode only.
- **UX-DR4 Flat depth, radii, selection and focus.** No shadows, gradients, glows, cream backgrounds or side stripes on cards. Depth comes from the three tonal layers (canvas, pane, surface) and 1 px hairlines, and the header bar is the only dark surface. Nothing floats: no modals, popovers or sticky overlays. Radii: lg for cards and panels; md for buttons, fields, warning rows and messages; sm for status tags, the calculation line and keyboard keys; xs for progress segments; full for trust labels and the switch. Selection is a blue-tint fill with a 2 px blue border. Focus is a 3 px blue outline 2 px outside every focusable element, white in the app header (UX change log, 2026-11-23).
- **UX-DR5 Shapes that carry meaning (NFR-7).** Høy, Middels and Lav are a filled circle, a filled triangle and a filled square, always with the word. A stockout week is a hollow square (white fill, red outline), an unusual week a filled amber triangle, and a level shift a filled ink diamond. Old data, insufficient data, a seasonal pattern and an error are a ring with «!» in the row's color. No signal relies on color alone.

**Layout**

- **UX-DR6 App shell and product-screen layout.** Top to bottom: the app header, the settings bar and the work area. The work area has two columns that scroll separately: the product list (392 px) on the left, and the selected product filling the rest, with 16 px top and 24 px side padding. On the product screen, the decision panel and the trust panel sit side by side in two equal columns, the forecast chart spans the full width right below them, and the worksheet and the explanation follow at full width. Panels are 16 px apart, and sections 24–40 px.
- **UX-DR7 Responsive behavior.**
  - From 1181 px: as UX-DR6.
  - 901–1180 px: the list narrows to 340 px, and the two panels stack, decision first.
  - Up to 900 px, also on an iPad held upright and on a phone: one column, with the product area first (the product, or «Denne uken» on Produktoversikt) and the list below it, neither with a scroll frame of its own; the HTML and keyboard order stay as on a wide screen, and the skip link «Gå til produktet» stays first on Produktside.
  - From 320 px there is no horizontal page scrolling, no text overlaps or is cut off, and every control is reachable with the keyboard and by touch (NFR-6). Only wide tables and the chart scroll sideways, inside their own frame; the chart's labels never shrink below 12 and 13 px, and calculation lines wrap between terms. The app header and the settings bar wrap onto more lines.
  - At 1366 × 768 (1366 × 640 px of content), the suggested order quantity, the confidence label and the active warnings are visible without scrolling, and the chart's heading and top edge show (FR-25). On smaller screens they come first in the product area, right after the product header.
  - Touch screens: every control has a target of at least 44 × 44 px, form fields use 16 px text, and the keyboard hint is hidden (UX-DR36).
  - Test sizes: 1366 × 768 in the desktop browsers; 820 × 1180 and 1180 × 820 (iPad), 360 × 800 (Android) and 320 px wide in the browser's responsive view; and 390 × 844 (iPhone 13) in the responsive view and on the real phone over the local network. A test on a real device and a test in the browser's responsive view are recorded apart.
  - Dark mode and print are not designed.

**Screens**

- **UX-DR8 Innlogging (wireframe in EXPERIENCE.md).** The header shows only the wordmark. One login panel, at most 420 px wide, is centered on the canvas: the title «Logg inn», the line «Prognose foreslår hvor mye du bør bestille neste uke, og viser hvordan tallene er regnet.», the fields «Kundenummer» and «Passord» with visible labels, and the primary button «Logg inn». Enter submits. After a failed try, «Feil kundenummer eller passord.» stands above the fields, the customer number is kept and the password is cleared. The panel ends with «Innloggingen for testbedriftene står i README.»
- **UX-DR9 Produktoversikt with «Denne uken» (mockup, screen 1).** The product list on the left, and «Denne uken» on the right:
  - the page title «Denne uken» and the line «Bestillingsforslag for neste uke, uke [46]. Tallene bygger på salget til og med uke [45].»;
  - the week path (UX-DR32) and the week figures (UX-DR33);
  - the primary button «Start med [first product in the review sequence]»;
  - «Slik leser du tillitsmerket» with the three labels and their conditions: «Minst 104 uker salgshistorikk, minst 100 gyldige uker og ingen varsler.», «Minst ett varsel, kortere salgshistorikk enn 104 uker eller færre enn 100 gyldige uker.» and «Ingen prognose, eller færre enn 12 gyldige uker.» This block came from the mockup; the user decided on 2026-11-18 to include it, and EXPERIENCE.md now describes it as the Trust legend.

  With no products, the list shows the «No products» message and «Denne uken» is not shown. With nothing to order soon, the «Bestill snart» group is not shown and the first week figure is 0. The spines do not say what «Start med …» does when the review sequence is empty; the story settles it.
- **UX-DR10 Produktside (mockup, screen 2 and the no-forecast frame).** In order:
  - the skip link «Gå til produktet» as the first focusable element;
  - the product header: the product name as the page title, the large trust label, «Varenr. [10012] · Lagerbeholdning [5] · Uker dekning [0,3]», the progress bar (UX-DR34), and the previous and next links (UX-DR35);
  - the confirmation message at the top of the product area after a settings change;
  - the decision panel and the trust panel, then the forecast chart with the legend and the unusual-weeks switch, then the calculation worksheet, and the explanation panel last.

  Without a forecast: «–» and «Ingen foreslått bestillingsmengde», the «No decision» sentence, «Lav» with its reason and warning, the chart with the weeks that exist and no forecast region, and only the sales table in the worksheet.
- **UX-DR11 Innstillinger (a page of its own, not a modal).** It starts with «Endringen gjelder alle produkter i bedriften.» and has one field per FR-20 setting, each with a visible label:
  - «Prognosemetode»: radio buttons «Glidende gjennomsnitt» and «Eksponentiell glatting»;
  - «Vindu»: a number field with the unit «uker», 2–12, disabled with exponential smoothing with «Ikke i bruk med eksponentiell glatting.»;
  - «Glattingsfaktor»: a number field, 0,1–0,9, disabled with the moving average with «Ikke i bruk med glidende gjennomsnitt.»;
  - «Scenarioprosent» (0–50) and «Sikkerhetsmargin» (0–100): number fields with the unit «%»;
  - «Uvanlige uker»: radio buttons «Tas med» and «Holdes utenfor»;
  - «Sesongjustering»: a checkbox (Should, FR-9).

  «Lagre» (primary) applies the change to every product and returns to the page the user came from, with the confirmation message. «Avbryt» (secondary) returns without changes. Number fields accept a decimal comma or a decimal point, and an error stands at its field while the previous value stays. With the script, the setting that the chosen method uses is enabled before saving, so that the method and its setting change in one save; without it, a second save is needed (D-4).
- **UX-DR12 Samlet bestillingsoversikt (Should, FR-30; wireframe in EXPERIENCE.md).** The page title «Samlet bestillingsoversikt»; the line «Bestillingene for neste uke, uke [46]. Prognose bestiller ingenting: ta listen med til innkjøpsmøtet.»; the week path with steps 1 and 2 done and step 3 current; the combined order table (UX-DR39); and «Tilbake til produktoversikten». The story also adds the header link, step 3 of the week path and the last-product button.
- **UX-DR13 Ikke funnet and the error pages.** The not-found panel has the page title «Siden finnes ikke» and the link «Til produktoversikten». It is shown for unknown addresses and for other companies' products, with none of their data (FR-2). The error pages (Database unavailable with status 503, Server error, Expired form) use the same panel, with the first sentence of their Message Catalogue text as the page title. No page shows data or technical details.

**Components**

- **UX-DR14 App header.** On every page, a navy bar with 10 × 20 px padding. Left: the wordmark «Prognose» (17 px, 700, white) and «[Testbedrift A] · siste registrerte uke: uke [45], [2026]» in header-meta. Right: «Produktoversikt», «Samlet bestillingsoversikt» (Should, FR-30) and «Logg ut» (a POST form, AD-6) in white, 14 px. The current page has weight 600 and a 2 px white underline. Logged out, the bar shows only the wordmark. No logo mark, and no blue or turquoise text on navy.
- **UX-DR15 Settings bar.** On every page after login, a white strip with a bottom hairline and 8 × 20 px padding: «Innstillinger i bruk:» in muted, then the values in ink, weight 600: the method with its window or factor («Glidende gjennomsnitt, 3 uker»), «Scenarioprosent 10 %», «Sikkerhetsmargin 10 %», «Uvanlige uker: tas med», and seasonal adjustment (Should, FR-9). Then the small secondary button «Endre innstillinger», which opens Innstillinger, and «Endringen gjelder alle produkter i bedriften.» in meta muted, pushed to the right. The bar wraps to two lines when narrow.
- **UX-DR16 Product list and group headings.** A pane background with a right hairline. «Produktoversikt» with the product count («[30] produkter»), the search field, and the groups in R-12 order: «Bestill snart» (weeks of cover, lowest first; ties by product number), «Uten prognose» (by product number) and «Øvrige produkter» (by product number). Each group heading has a right-aligned summary: «[4] produkter · [31] enheter foreslått», «[1] produkt · du bestemmer selv» or «[25] · etter varenummer». An empty group is not shown. The list keeps its scroll position when a product is selected, is a labeled scroll region «Produkter», and ends with the keyboard hint (UX-DR36).
- **UX-DR17 Product card («Bestill snart», «Uten prognose»).** White, a 1 px border, radius lg, 12 × 14 px padding, 8 px apart; the whole card is one link.
  - Top left: the name and «Varenr. [10012]». Top right: «Foreslått» over the quantity (28 px, blue).
  - A facts line: «Lager», «Ukeprognose uke 1» and «Uker dekning», with the labels in muted and the values in ink, weight 600.
  - Last: the trust label and, unless it is «høy», the reason without the label word and the full stop, as in the mockup («Nytt nivå de siste 12 ukene»).
  - Selected: a blue-tint fill, a 2 px blue border, secondary text in blue-ink, and `aria-current="page"`.
  - Without a forecast: a 2 px dashed red border, the reason in red, weight 600, in place of the week-1 forecast, and «–» in ink for the quantity and the weeks of cover. When selected, selection wins (a solid blue border), and the red reason stays.
  - Should, FR-29: an adjusted quantity shows «Justert av deg» in place of «Foreslått».
- **UX-DR18 Product row («Øvrige produkter»).** Rows inside one white bordered box (radius lg), separated by hairlines, with 10 × 14 px padding; the whole row is one link. The name in 15 px, weight 600; one meta line «Varenr. [10001] · Lager [40] · Ukeprognose uke 1: [9,3] · Uker dekning [4,3]»; «Foreslått» over the quantity in 18 px ink, not blue, because 0 is not an order; the trust label below, with the reason unless it is «høy». Should, FR-14: the overstock note.
- **UX-DR19 Search field.** The visible label «Søk i produktene» above a white input with a 1 px field border, radius md, 7 × 10 px padding and 14 px text, or 16 px on touch screens (UX-DR7). It is a plain GET form that always goes to Produktoversikt (`/produkter/?sok=`), also from Produktside. It filters by product number or name, ignoring case, and works on Enter. The previous and next links ignore the filter. The groups keep their order, and the results and week figures do not change (AD-2). Filtering while typing is an `app.js` enhancement. With no match: «Ingen produkter passer søket.» and the link «Vis alle produkter».
- **UX-DR20 Trust label.** A pill (radius full, 2 × 10 px padding, 8 px before the icon) with a 12 px shape icon in the text color and the word: «Høy» green on green-tint, «Middels» amber on amber-tint, «Lav» red on red-tint. The large variant (15 px label, 14 px icon) stands next to the product name and in the trust panel. The word is always text; the shape is decoration and is hidden from screen readers.
- **UX-DR21 Panel.** White, a 1 px border, radius lg, 16/20/20 px padding, 16 px apart, with a section-title heading (`h2`). A panel holds one question or one task and never contains another panel; inside it, structure comes from headings, tables and hairlines.
- **UX-DR22 Decision panel «Hva bør du bestille?» (FR-11).** The suggested order quantity in 44 px blue (in ink when it is 0, because 0 is not an order), the largest number on the screen, with «Foreslått bestillingsmengde for neste uke, uke [46]» in 16 px, weight 600, on the same baseline. Without a forecast: «–» in ink, «Ingen foreslått bestillingsmengde», and «Prognose foreslår ingen mengde for dette produktet. Du bestemmer bestillingen selv.» In the Must scope the panel has no buttons, and the previous and next links do the job. Should, FR-14: the overstock note stands below the suggested order quantity (D-6).
- **UX-DR23 Decision buttons (Should, FR-29).** The primary «Behold [11] og gå videre» keeps the suggestion and opens the next product in the review sequence. The secondary «Juster mengden» opens a whole-number field labeled «Justert bestillingsmengde», with «Lagre» and «Tilbake til forslaget», and the suggestion stays visible next to the adjusted quantity. For a product outside the review sequence, the primary button opens the next product in R-12 order. Without a forecast, «Sett mengden selv» opens the same field. On the last product reviewed, or the last product in R-12 order, the primary button becomes «Gå til samlet bestillingsoversikt» (with FR-30) or «Tilbake til produktoversikten». An invalid quantity shows «Skriv et helt tall fra 0 og oppover.» The adjustment lasts for the session (FR-31 is Could).
- **UX-DR24 Trust panel and warning list «Kan du stole på prognosen?» (FR-19, FR-25).** The same height as the decision panel: the large trust label, the reason in body text («Middels: 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene.»), then one row per active warning (R-15) whose FR is built, in R-15 order and worded as in the Message Catalogue, and nothing that does not apply. Stockout and unusual weeks before the recent period are not warnings; the forecast calculation lists them. Rows: 8 × 10 px padding, radius md, 8 px apart, 14 px ink text and a 16 px icon (UX-DR5). Data problems (stockout weeks, old data, insufficient data) use red-tint; demand patterns (unusual weeks, level shift, seasonal pattern) use amber-tint.
- **UX-DR25 Unusual-weeks switch (UJ-1 step 4; FR-16, FR-21).** Below the chart legend, after a hairline with 12 px above. A real checkbox with `role="switch"` in a POST form to `/innstillinger/uvanlige-uker/`, so Space toggles it; without the script, the small secondary button «Lagre» next to it submits the form, and `app.js` hides the button and submits the form on toggle (D-5). A 40 × 22 px track with a 16 px white knob: blue with the knob on the right when unusual weeks are included, field gray with the knob on the left when they are excluded. Beside it, in 14 px: the state in bold («Uvanlige uker tas med.»), what switching does («Slå av for å holde dem utenfor.»), and «Endringen gjelder alle produkter i bedriften.»; the excluded state mirrors this wording. The page reloads with the confirmation message. The switch keeps its size; only the chart is full width.
- **UX-DR26 Forecast chart «Hva skjer med salget?» (FR-15 to FR-17, FR-25, NFR-7).** Inline SVG rendered on the server (AD-11), in a panel with a one-line subtitle and the chart at full width, about 3:1. It shows the whole sales history (up to 104 weeks) and the three forecast weeks; the mockup shows 12 weeks, and its subtitle must change to match.
  - Sales: a 2.5 px ink line with 4.5 px dots where weeks are at least 12 px apart.
  - Stockout weeks: the line breaks, a 1.5 px dashed ink connector bridges the gap, and each week gets a 12 px hollow red square at its sales value.
  - Unusual weeks: an amber triangle of about 20 × 17 px with the sales value in 12 px ink. Level-shift weeks: a 14 px ink diamond.
  - Forecast: the three forecast weeks on a turquoise-tint area labeled «De neste tre ukene», with a 3 px turquoise line and dots, joined to the last sales week by a 2 px dashed turquoise line.
  - Scenarios: the band in the band color with 1.5 px dashed turquoise edges, and the captions «Optimistisk», «Normal» (bold) and «Pessimistisk» with their values.
  - The recent period: a dashed line where the last 12 weeks begin, labeled «Siste 12 uker»; there is no line when the whole history lies in the last 12 weeks.
  - Axes: gridlines in border, the baseline in axis, 12 px muted labels, the forecast week numbers in turquoise, weight 700, and the year on the first week of a new year («1/2027»).
  - Legend: 13 px ink items with 14 px markers (24 px for lines and the band), explaining every marker type whether or not this product has one: «Solgt», «Utsolgt uke, ikke brukt», «Uvanlig uke, tatt med» (with «holdt utenfor» when the setting excludes them), «Nytt nivå», «Prognose» and «Optimistisk og pessimistisk scenario».
  - Without a forecast: the weeks that exist and no forecast region.
  - The chart's `width: 100%` rule must not reach the legend icons or any other SVG; the mockup has this defect.
- **UX-DR27 Chart text alternative (NFR-11).** The chart has a title and a short summary (the weeks shown; the stockout, unusual and level-shift weeks; the forecast and the scenario range), whose text comes from `explanation/` (AD-4). The plotted values are in the worksheet tables: the panel says «Tallene i diagrammet står i tabellene under «Slik er tallene regnet ut».», and a disclosure «Tabell med alle ukene i grafen» lists every plotted week.
- **UX-DR28 Calculation worksheet «Slik er tallene regnet ut».** Subsections in this order:
  - «Salgshistorikk, siste 12 uker», or «Salgshistorikk, alle ukene» when the history has 12 weeks or fewer: week, units sold and a status tag per flagged week, followed by a sentence that explains the tags, as in the mockup.
  - «Prognoseutregning» (FR-35): the formula in a calculation line, then «Uker brukt: uke 43, 44 og 45.» and «Holdt utenfor: uke 38 og 39 (utsolgt).». With unusual weeks excluded, each excluded week and «[3] uker brukt i beregningen» (FR-16). Every week left out in the whole history is listed with its reason, with the year in lists that reach before the recent period («uke 10/2025»). For exponential smoothing, a table of every calculation week with its sales and level, in its own scroll frame. Should, FR-9: the seasonal indices (four decimals) and adjusted values (one decimal) for the weeks used and for weeks 1–3, and the week forecasts.
  - «Ukeprognoser og scenarioer»: the columns «Uke 1 · uke 46», «Uke 2 · uke 47» and «Uke 3 · uke 48»; the rows «Optimistisk», «Normal» (bold) and «Pessimistisk»; the FR-10 text; and the FR-7 note «Merknad: Uke 2 og 3 …», or the FR-9 note when seasonal adjustment could not be used (Should, FR-9). Should, FR-13: a «Bestillingsmengde» column, with the normal quantity in blue and «Bestillingsmengden per scenario er regnet ut fra uke 1, med sikkerhetsmargin.»
  - «Utregning av bestillingsmengde» (FR-12).

  Tables: 14 px, a 13 px muted header row with a 1 px ink rule below, hairlines between rows, numbers right-aligned and the first column left-aligned. Where the mockup and EXPERIENCE.md word a line differently, EXPERIENCE.md wins.
- **UX-DR29 Calculation line.** A sunken box, radius sm, 8 × 10 px padding, with the exact FR-12 or FR-35 format in the 13.5 px monospace formula style. «Tallene er avrundet for visning.» stands on its own line inside the box in 13 px muted system UI, on the order calculation line and below the exponential-smoothing line and the seasonal values. The FR-12 safety-margin sentence follows below the box in meta muted.
- **UX-DR30 Status tag.** In the sales table: radius sm, 1 × 6 px padding, 13 px, with a 10 px icon. «utsolgt» red on red-tint (hollow square), «uvanlig» amber on amber-tint (triangle), «nytt nivå» ink on canvas (diamond), and «brukt» turquoise on turquoise-tint without an icon, for a week used in the forecast: the last N calculation weeks for the moving average, and every calculation week for exponential smoothing.
- **UX-DR31 Explanation panel «Forklaring» (FR-26, FR-27).** Last on the product screen, below every calculated number, on turquoise-tint with a turquoise-border border, in ink body text at most 72ch wide.
  - Content, in order: the method and settings; the number of calculation weeks and the week forecasts; the weeks left out and why; every active warning and note; the order calculation; the weeks of cover; the confidence label and its reason; the scenarios.
  - Numbers: only those FR-27 allows. Templates leave out sales figures and the week numbers of calculation weeks, included unusual weeks and level-shift weeks. A year appears only next to a week left out or a horizon week that lies in another year than the latest data week.
  - The Strøsand 25 kg example in EXPERIENCE.md is the reference text.
  - Should, FR-28: «KI-omformulert forklaring» above the text; on any failure the template text, without an error.
- **UX-DR32 Week path («Denne uken» and Samlet bestillingsoversikt).** Three steps in a row, each a 30 px circle with the number (2 px field border, muted number), a 16 px title (weight 600, ink) and a meta muted line:
  1. «Se hva som haster»: «Produktene som bør bestilles snart, står øverst i listen, med lavest uker dekning først.»
  2. «Gå gjennom produktene»: «Sjekk forslaget, tilliten og utregningen for hvert produkt.»
  3. «Ta med den samlede bestillingsoversikten til møtet»: «Alle produkter med foreslått eller justert mengde.» (Should, FR-30.)

  The current step has a blue circle with a white number, and a done step a green one. Step 1 is current on Produktoversikt, step 2 opens the first product in the review sequence, and step 3 opens Samlet bestillingsoversikt. Without FR-30, the path has two steps.
- **UX-DR33 Week figures («Denne uken»).** Four plain figures, not links, in a row between two hairlines with 16 px padding and no boxes: the number in 30 px ink and the label below in 14 px muted. They are the products with order-soon status («produkter bør bestilles snart»), the units suggested in total, which is the sum of the suggested order quantities («enheter foreslått totalt»), the products without a forecast («produkt uten prognose») and the products with at least one active warning («produkter med varsel»). `build_overview` computes them (AD-2).
- **UX-DR34 Progress bar.** In the product header, 28 × 6 px segments (radius xs, 4 px apart): green for done, blue for the current product and border for the rest. The mockup shows four, one per product to order soon, and the story settles the count for longer groups. It is always followed by its text: «Gå gjennom produktene: produkt [2] av [4] som bør bestilles snart», then «produkt [1] av [1] uten prognose». It is not shown for «Øvrige produkter».
- **UX-DR35 Previous and next links.** Plain blue links with arrows («← Isskrape», «Lyspære LED E27 9 W →»), right-aligned in the product header, in a navigation landmark labeled «Forrige og neste produkt». They go to the previous and next product in R-12 order, across all groups.
- **UX-DR36 Keyboard hint and arrow keys.** At the end of the list: «↑ ↓ forrige og neste produkt · Enter åpner produktet», with keyboard keys in 13 px, 0 × 6 px padding, white, a 1 px field border and radius sm. `app.js` adds ↑ and ↓ to move between products and Enter to open one; Tab and Enter always work. The hint is hidden on touch screens (UX-DR7).
- **UX-DR37 Confirmation message (FR-21).** At the top of the product area after a settings change: blue-tint with blue-ink text, radius md, 8 × 12 px padding, `role="status"`, shown once. «Innstillingen er endret: [sikkerhetsmargin] er nå [50] %.», then one line per affected value, «[Foreslått bestillingsmengde]: [11] → [17]», with «(uendret)» when the value did not change. It compares the product the user came from; from a page without a product, it shows only the line naming the new setting (AD-2).
- **UX-DR38 Error message.** A red-tint row with the red «!» ring and ink text, radius md, above the field or form it concerns, with `role="alert"` and linked to its field with `aria-describedby`. The previous value stays.
- **UX-DR39 Combined order table (Should, FR-30).** A panel with the worksheet's table style and the columns «Varenr.», «Produkt», «Bestillingsmengde» and «Merking». Every product in R-12 order. An adjusted row shows the adjusted quantity in blue with the suggestion in brackets («13 (foreslått 11)») and «Justert av deg» as a blue-tint tag in blue-ink. «Foreslått» is plain muted text. A product without a forecast and without an adjusted quantity shows «–» in ink and «Uten prognose» in plain red. A bold total row («Totalt») ends the table, and each product name links to its product screen.

**Copy, interaction and accessibility**

- **UX-DR40 Message Catalogue as the copy source.** Every warning, note, confirmation and error uses its text in the EXPERIENCE.md Message Catalogue verbatim, with the bracketed parts filled from the result (AD-4). The catalogue has 32 rows: the login error; stockout weeks; unusual weeks (included, excluded and several); level shift (the reason, and the Should warning); old data; insufficient data with few weeks (list and warning); insufficient data with the window (list and warning); seasonal pattern (Should); flat weeks 2 and 3; seasonal adjustment not possible (Should); overstock (Should); stock not lasting (Could); the scenario text; the order calculation line; the safety-margin text; the forecast calculation; the confidence label reason (with its example reasons, the reason when the window prevents a forecast, and which condition comes first); no decision; the settings area; the settings confirmation (with «–» when a change removes or gives a forecast); a value out of range; not a number; a setting not in use; an invalid adjusted quantity (Should); the markings (Should); no products; no search match; not found; database unavailable; server error; expired form; and the AI label (Should).
- **UX-DR41 Voice and tone.** The glossary labels verbatim, with no synonyms: «Lagerbeholdning», «Uker dekning», «Tillitsmerke» and «Grunnprognose», never «beholdning», «dekningsgrad», «score» or «basisprognose». Prognose speaks in the third person («Prognose foreslår …») and calls the user «du», never «vi», «systemet» or «KI-en». Short, complete sentences with a full stop; no exclamation marks, emojis or urgency words beyond «Se hva som haster».
- **UX-DR42 Calculation display rules.** Rounding as R-9 through AD-3. A decimal comma, «%» after a space («10 %»), the minus sign «−» and no thousands grouping. Horizon columns read «Uke 1 · uke 46»; chart axes use week numbers, with the year on the first week of a new year («1/2027»); lists that reach before the recent period show the year («uke 10/2025»). «–» for the suggested order quantity and the weeks of cover without a forecast, and for the weeks of cover when the week-1 forecast is 0 (E23).
- **UX-DR43 Interaction primitives and banned patterns.** Every action is a link or a form submission, so everything works without scripts. Tab follows the order of the page: header, settings bar, list, product, also in the one-column layout. Space toggles the switch, and there are no shortcuts without a visible hint. A click or tap anywhere on a card or row opens the product; nothing depends on hover, nothing is dragged, and a swipe only scrolls. The review sequence is «Bestill snart», then «Uten prognose»; previous and next cover every product. Banned: modals, popovers, tooltips as the only home of information, auto-refresh, animation, infinite scroll, drag, hover-only controls, color-only signals and celebratory feedback. Left out on purpose: sparklines, key-figure tiles, filter chips, letter-box labels and numbered question circles.
- **UX-DR44 Accessibility floor (NFR-11).**
  - WCAG 2.2 AA on every surface, and `lang="nb"` on every page.
  - Every function works with the keyboard alone, with the visible focus ring.
  - The product list and the product area are labeled regions («Produkter», «Valgt produkt»), which keyboard users can scroll where they scroll on their own, and the main navigation is labeled «Hovedmeny» (mockup).
  - Every field has a visible label, the search field included.
  - Headings: one `h1` per page (the product name, «Denne uken» or the page title), `h2` for panels, and `h3` for worksheet subsections and list groups.
  - The selected product has `aria-current="page"`, and the shapes of trust labels are hidden from screen readers.
  - Confirmations use `role="status"` and errors `role="alert"`, and field errors are linked to their field with `aria-describedby`.
  - No timing, no motion, and no content that appears only on hover.
- **UX-DR45 State coverage.** Every state in the EXPERIENCE.md State Patterns table is built on its surface and tested: logged out; login failed; no products loaded; no search match; nothing to order soon; product selected; no forecast with fewer than 3 valid weeks; no forecast with a window longer than the calculation weeks; suggested order quantity 0; week-1 forecast 0; unusual weeks excluded; level shift in the recent period; old data; seasonal adjustment on (Should); seasonal pattern not used (Should); settings changed; invalid setting; quantity adjusted (Should); last product reviewed (Should); language model on (Should); not found; error; reload, Back and double submit; focus.
- **UX-DR46 Demo content for the key flows.** The seed data matches the products and values that the UX flows and the mockup show, where FR-3 and the reference spreadsheet allow: «Testbedrift A» as a hardware store with about 30 products, such as «Isskrape», «Strøsand 25 kg» (the E1 and E4 case, with stockout weeks 38–39 and an unusual week 42 in the recent period) and «Snøskuffe aluminium» (2 valid weeks, «lav», for SM-10); the rule test product built from E8 for UJ-1 step 4 (DR-1); and a latest data week such as week 45 of 2026. The UX examples do not limit the other products, which follow FR-3 (the user's decision, 2026-11-18). Where a mockup value cannot occur under the rules, the rules win: Skruer's week-1 forecast is 21,3, not 21,5, and Kabelstrips' weeks of cover is 3,8, not 3,7, with the suggested quantities unchanged. Testbedrift A holds the UX demo products and the E8 product, and Testbedrift B the other rule test products and pattern products, so «Denne uken» for Testbedrift A shows 4 products with warnings, not 3, because the E8 product adds one. The data story settles the exact list.

### FR Coverage Map

- FR-1: Epic 1 – log in with customer number and password, and log out
- FR-2: Epic 1 – company isolation; every later story that adds a route or a list extends the two-account test
- FR-3: Epic 1 – the synthetic dataset, built from the reference spreadsheet
- FR-4: Epic 1 – PostgreSQL locally
- FR-5: Epic 2 – moving average
- FR-6: Epic 2 – exponential smoothing
- FR-7: Epic 2 – three-week horizon and the flat-weeks note
- FR-8: Epic 2 – no forecast with insufficient data
- FR-9: Epic 5 – seasonal adjustment (Should)
- FR-10: Epic 2 – three scenarios
- FR-11: Epic 2 – suggested order quantity
- FR-12: Epic 2 – order calculation line
- FR-13: Epic 6 – order quantity per scenario (Should)
- FR-14: Epic 6 – overstock note (Should)
- FR-15: Epic 2 – stockout weeks left out
- FR-16: Epic 2 – unusual weeks; the switch is in Epic 3
- FR-17: Epic 2 – level shift in the calculation and the confidence label
- FR-17b: Epic 5 – level-shift warning text (Should)
- FR-18: Epic 2 – old-data warning
- FR-19: Epic 2 – confidence label with its reason
- FR-20: Epic 3 – company-wide settings with their ranges
- FR-21: Epic 3 – a change applies to every product, with the confirmation
- FR-22: Epic 3 – settings saved between sessions
- FR-23: Epic 8 – settings per product (Could)
- FR-24: Epic 2 – product overview; Epic 1 gives the first product list
- FR-25: Epic 2 – product screen; Epic 3 adds changing the settings from it
- FR-26: Epic 2 – template explanation
- FR-27: Epic 2 – allowed numbers in the explanation
- FR-28: Epic 7 – optional local language model (Should)
- FR-29: Epic 6 – adjust an order quantity (Should)
- FR-30: Epic 6 – combined order overview (Should)
- FR-31: Epic 8 – saved adjustments and approval (Could)
- FR-32: Epic 8 – CSV export (Could)
- FR-33: Epic 8 – stock not lasting through weeks 2 and 3 (Could)
- FR-34: Epic 8 – forecast accuracy (Could)
- FR-35: Epic 2 – forecast calculation
- FR-36: Epic 5 – seasonal-pattern warning (Should)

## Epic List

Eight epics, approved by the user on 2026-11-18. Epics 1 to 4 are Must, 5 to 7 Should and 8 Could, and every story takes one priority from its FRs.
- **Order:** Epic 1, then 2, then 3. Stories 4.1 to 4.3 follow Epic 3 and come before any Should work. Epics 5 to 7 start only after the Must scope passes SM-1 and SM-3 and Stories 4.1 to 4.3 are done, in the order of PRD §8.2. Epic 8 is built only if time allows. Story 4.4 comes last in the sprint plan, after every story that is actually implemented. The MVP comes before extra features (the user's decision, 2026-11-18).
- **Independence:** each epic builds only on the epics before it. No Must story depends on a Should or Could story, and every Should story can be implemented on its own, whether or not the other Should stories are built (the user's decision, 2026-11-18).
- **AI steering log:** every epic that is implemented gives at least one case (D-2).
- **File overlap:** Epics 2, 3, 5 and 6 all change the core and the product screen. Merging them was considered on 2026-11-18 and rejected, because the line between Must and Should and the order of the Should items in PRD §8.2 are real risk boundaries: the work must be able to stop after any of them.

**Rules for every story**
- It is built on its own branch and meets the DR-7 Definition of Done: its tests and Ruff pass locally and in CI (Story 1.1 comes before CI and passes them locally, D-9); it leaves no commented-out, unused or duplicated code; the status table and the affected documents are updated; and its pull request names the story and its FR-n, says what was tested, and has been reviewed with BMAD Code Review by the routine for code review below. Because the user works alone, no second person reviews (D-8).
- Its commits are small and pushed as the work happens, so that the history covers the whole build period, and defects and open points are tracked as issues in `.logs/<bruker>/issues.md`, as CLAUDE.md requires (DR-7). GitHub Issues is not required: the original IBE160 examiner guidelines for part 1 accept «branches, pull requests, issues eller tilsvarende» (criterion 1, «Arbeidsflyt»), and the examiner looks for issues in the history (step 6), so the README links to `issues.md` and explains how it is used (Story 4.1). The full guidelines were pasted by the user on 2026-11-18 and are not stored in the repository.
- Every defect in AI-generated code or text that a test, the reference spreadsheet, a review or a manual test finds is recorded in `docs/qa-logg.md` with how it was found, the fix, and the commit or pull request (DR-9).
- Every test names the FR-n or E-n it verifies (DR-5); a test that verifies no FR names the NFR-n, DR-n or AD-n it verifies (D-10). Calculation tests read their inputs and expected values from the reference spreadsheet, and no expected result is hard-coded in the tests or in the calculation code (AD-17; the user's decision, 2026-11-18).
- Every new route or list extends the two-account test (FR-2, AD-7).
- Every page it adds or changes follows UX-DR7 on a PC, an iPad and a phone, and is checked in the browser's responsive view at least at 320 px, 390 × 844 (iPhone 13) and 820 × 1180 (iPad); the pull request names these as checks in the responsive view, and tests on the real iPhone 13 are recorded apart in the QA log (NFR-6).
- Result-dependent Norwegian text comes from `explanation/`, with the Message Catalogue as its copy source (AD-4), and numbers and week labels are formatted by `forecasting/display.py` (AD-3).
- The story's prompts, relevant AI sessions and AI corrections follow the routine below (DR-5, DR-9, NFR-4).

**Routine for AI sessions and AI corrections** (approved by the user on 2026-11-18)
1. A Claude Code session for a story starts by naming the story, for example «Story 2.3: …».
2. When the session ends, the conversation is exported with Claude Code's `/export` to a file in `.logs/<bruker>/sessions/` named after the story and the date, for example `2-3-2026-11-24.txt`. A session that did not shape the story's code, tests or documents, such as a pure status question, need not be saved.
3. Before the commit, the file gets the same privacy check as every commit: local paths such as `/Users/…`, e-mail addresses, keys and passwords are searched for, and every hit is removed or masked. Nothing else in the export is edited, so the prompts stay original.
4. The export is committed in the story's pull request, and the session log and the pull request link to it.
5. When AI output is rejected, corrected or made more precise, a case goes into `docs/ki-styringslogg.md` at once: what the AI proposed, what was wrong, what was decided, and the commit or pull request. A defect in AI-generated code or text also goes into `docs/qa-logg.md`, as the rule above says.
6. For the planning phase, `docs/arbeidslogg.md`, the memlogs and the session logs are the record. Their examples are copied into the AI steering log and the QA log with their source named. No planning-phase prompt is reconstructed or presented as original.

**Routine for code review** (decided by the user on 2026-11-18)
1. When a story's code and tests are done and pass locally, the user runs BMAD Code Review (`bmad-code-review`) on the story's branch with the story's specification file, before the merge. The skill then also writes its findings into the specification file.
2. A comment in the pull request lists every finding with the user's decision: fixed, rejected with the reason, or postponed as an open point in `.logs/<bruker>/issues.md`.
3. Each fix is a new commit on the same branch, and the comment names the commit for each fixed finding.
4. A finding that is a defect in AI-generated code also goes into the QA log, and a rejected or corrected AI suggestion into the AI steering log (DR-9, the routine for AI sessions).
5. The user merges only when the comment is complete and CI passes; Story 1.1 comes before CI and is merged when the tests and Ruff pass locally on its final commit (D-9). No second reviewer is needed; the documented review in the pull request is the review trace that DR-7, SM-8 and the examiner guidelines (criterion 3) ask for.

### Epic 1: Log in and see only your own company's data (Must)

The examiner sets up Prognose from a fresh clone, starts the database with one command, logs in as either test company and sees only that company's products. The data stays in PostgreSQL between restarts. Version 1 is not published (D-1).

**FRs covered:** FR-1, FR-2, FR-3, FR-4.
**Also covers:** NFR-1, NFR-3, NFR-4, NFR-6 (the viewport and touch rules, and the first test on the real iPhone), NFR-9, NFR-10 (the error pages), DR-2, DR-3, DR-4, DR-5, DR-8, DR-9 (the process documents), DR-10 (as not built, in the status table), SM-4 and SM-5; AD-1, AD-6 to AD-8, AD-12 to AD-15 and AD-17; UX-DR1 to UX-DR5, UX-DR7, UX-DR8, UX-DR13, UX-DR14, UX-DR21, UX-DR38, UX-DR41, UX-DR43, UX-DR44 and UX-DR46.
**Implementation notes:**
- Order: the local start (1.1); CI (1.2); the setup test on Windows and offline (1.3), which blocks nothing; the app shell (1.4); the reference spreadsheet (1.5), which can start alongside 1.1 and must be done before the seed data, because the generator reads it (AD-15, AD-17); the seed data (1.6, 1.7); and login and isolation (1.8).
- There is no starter template. The first story builds the skeleton by hand, with `web.Company` in the first migration, and starts the status table and the AI steering log so that every story can update them.

### Epic 2: See what to order, how it was calculated and whether to trust it (Must)

Mounia sees the product overview with «Denne uken» in R-12 order. For each product she sees the week forecasts, the scenarios, the suggested order quantity, the forecast calculation and the order calculation line, the chart, the warnings, the confidence label and the template explanation, all matching the reference spreadsheet.

**FRs covered:** FR-5, FR-6, FR-7, FR-8, FR-10, FR-11, FR-12, FR-15, FR-16, FR-17, FR-18, FR-19, FR-24, FR-25, FR-26, FR-27, FR-35.
**Also covers:** NFR-2, NFR-5 to NFR-8, NFR-11, AG-1, AG-2, AG-4, SM-1, SM-6 and SM-7; AD-2 to AD-5 and AD-11; UX-DR5 to UX-DR7, UX-DR9, UX-DR10, UX-DR15 to UX-DR20, UX-DR22, UX-DR24, UX-DR26 to UX-DR36, UX-DR40 and UX-DR42 to UX-DR45.
**Implementation notes:**
- The pure core comes first, one small story at a time against the reference spreadsheet, then the pages that show it, then the explanation. Every page uses the one compute path (AD-2).
- The stories are small and testable, as the user asked: each one checks a named set of reference examples or screen states. Three pairs of screen stories were merged on 2026-11-18 to reduce the number of pull requests, with all their criteria kept.
- The Must examples in SM-1 pass by the end of this epic.
- Settings are changed in Epic 3; until then the settings bar only shows the settings in use.

### Epic 3: Change the settings and see every product update at once (Must)

Mounia changes the forecasting method, the window, the smoothing factor, the scenario percentage, the safety margin or the handling of unusual weeks from the product screen or the settings page. Every product updates at once, the screen confirms the previous and the new value, and the settings stay after logging out and after a restart.

**FRs covered:** FR-20, FR-21, FR-22, and the part of FR-25 that changes the settings from the product screen.
**Also covers:** NFR-6 (touch on Innstillinger and the switch), NFR-10, SM-3 and SM-5; AD-9 and AD-10; UX-DR7, UX-DR11, UX-DR15, UX-DR25, UX-DR37, UX-DR38 and UX-DR40.
**Implementation notes:** the automated SM-3 core-flow test runs at the end of this epic. When SM-1 and SM-3 pass, the Must scope has passed its gate, and Should work may start (DR-6, SM-C2).

### Epic 4: Ready for the examiner (Must)

The examiner installs Prognose from the README on macOS or Windows within 15 minutes once the prerequisites are installed, follows «Prøv selv», compares the results with the reference spreadsheet and traces every FR to its stories and tests. The final commit passes every check.

**FRs covered:** none directly; the README parts of other FRs belong to DR-1.
**Also covers:** DR-1, DR-2, DR-5, DR-8 and DR-9; NFR-4, and the manual checks of NFR-6, NFR-7, NFR-8 and NFR-11; SM-2, SM-8 and SM-10; UX-DR7 (the test sizes) and UX-DR45 (the state checks); the `issues.md` points on the README, the Product Brief, the textbook sources, the Impeccable finish review and the final privacy scan.
**Implementation notes:** Stories 4.1 to 4.3 come right after Epic 3 and before any Should work, so the Must scope can be submitted even if no Should item is built, and a failed SM-10 can still be fixed. Story 4.4 comes last in the sprint plan, on the final commit, after every story that is actually implemented.

### Epic 5: Seasonal products and clearer warnings (Should, items 1 and 2)

Mounia can switch on seasonal adjustment so that the week forecasts follow the season. A product with a seasonal pattern that the forecast does not use, or with a level shift, gets its own warning text.

**FRs covered:** FR-9, FR-36, FR-17b.
**Also covers:** SM-1 (E14, E25 to E27 and E30) and SM-7; UX-DR40 and UX-DR42, and the parts of UX-DR11, UX-DR15, UX-DR24 and UX-DR28 marked FR-9, FR-36 or FR-17b.
**Implementation notes:** FR-9 first (Should item 1), then FR-36 and FR-17b (item 2). Each story delivers one complete Should item of PRD §8.2, so the work can stop after any of them with nothing half built. Story 5.2 does not depend on Story 5.1: if 5.1 is cut, 5.2 builds R-14 steps 1 and 2 itself.

### Epic 6: Plan the order for the Monday meeting (Should, items 3 to 5)

Mounia sees the order quantity per scenario and the overstock note, adjusts a suggested quantity when she knows better, and takes one combined order overview to the meeting.

**FRs covered:** FR-13, FR-14, FR-29, FR-30.
**Also covers:** AD-10 (adjustments in the session); UX-DR12, UX-DR23, UX-DR38, UX-DR39, UX-DR40 and UX-DR45, and the parts of UX-DR14, UX-DR17, UX-DR18, UX-DR22, UX-DR28, UX-DR32 and UX-DR33 marked FR-13, FR-14, FR-29 or FR-30.
**Implementation notes:** the order of PRD §8.2: FR-13 and FR-14, then FR-29, then FR-30, one story per Should item, so the work can stop after any of them with nothing half built. The FR-2 two-account test is extended to the quantity route and the combined order overview.

### Epic 7: Optional local language model (Should, item 6)

A group member can switch on a local language model that rephrases the explanation, under the FR-28 checks. Prognose works fully without it.

**FRs covered:** FR-28.
**Also covers:** AG-3, AG-5 and SM-6; AD-5; the AI label in UX-DR31; PRD §10 question 5.
**Implementation notes:** the last Should item, kept optional and local. The runtime, the model and its license are decided when it is scheduled, and the timeout's fit with NFR-8 is decided in D-7. If that exception turns out not to fit, the story is postponed rather than the architecture made more complex.

### Epic 8: Extras if time allows (Could)

Small additions to the weekly routine: settings per product, saved and approved adjustments, CSV export, a note when the stock will not last through weeks 2 and 3, and forecast accuracy.

**FRs covered:** FR-23, FR-31, FR-32, FR-33, FR-34.
**Implementation notes:** each story gets its testable consequences when it is planned (PRD §4). FR-23 needs an amendment to AD-9, FR-31 replaces only the storage behind `web/adjustments.py`, and FR-31 and FR-32 build on Epic 6.

## Epic 1: Log in and see only your own company's data

The examiner sets up Prognose from a fresh clone, starts the database with one command, logs in as either test company and sees only that company's products. The data stays in PostgreSQL between restarts. Version 1 is not published (D-1).

### Story 1.1: Start Prognose locally from a fresh clone

As an examiner,
I want to start Prognose from a fresh clone with one command for the database and the documented `uv run` commands,
So that I can run it on my own computer without paid services, keys or file editing.

**Priority:** Must. **Requirements:** NFR-1, NFR-3, NFR-4, NFR-6 (the setting for the phone test), NFR-9, DR-1 (the setup part), DR-2, DR-5, DR-8, DR-9; AD-6, AD-13, AD-14, AD-17; the Consistency Conventions; the routine for AI sessions.

**Tasks,** each with the check that proves it:
1. The repository layout from the Structural Seed, with `pyproject.toml`, `uv.lock` and `.python-version`: `uv sync --locked` installs the pinned versions.
2. `compose.yaml` with only the database: `docker compose up -d --wait` reports the database as healthy.
3. The settings for the local run mode: a test checks the default `DATABASE_URL`, `LANGUAGE_CODE`, `TIME_ZONE` and `ALLOWED_HOSTS`, with and without `PROGNOSE_LAN_HOST`.
4. The custom user model `web.Company` in the first migration: `migrate` runs on an empty database, and `makemigrations --check` finds nothing missing.
5. `load_seed`, which creates `.secret_key` and never overwrites it: a test with and without an existing file.
6. The first page at `/`: a test of the response.
7. pytest with pytest-django against the local PostgreSQL, and Ruff: `uv run pytest`, `uv run ruff check` and `uv run ruff format --check` pass.
8. `.gitignore`, `.env.example`, the README's setup section and the process documents: checked in the review.
9. The planning-phase record in the AI steering log and the QA log, and this story's own exported session: checked against their sources and the privacy check.

**Acceptance Criteria:**

**Given** a fresh clone on macOS with the prerequisites that the README lists (uv and Docker Desktop)
**When** the group runs `docker compose up -d --wait`, `uv sync --locked`, `uv run python src/manage.py migrate`, `uv run python src/manage.py load_seed` and `uv run python src/manage.py runserver --insecure`
**Then** Prognose answers at `http://127.0.0.1:8000/` with a page that declares `lang="nb"` and shows the wordmark «Prognose»
**And** no step activates a virtual environment, needs an `.env` file or a key, or asks for a file to be edited (NFR-1, NFR-3)

**Given** `compose.yaml`
**When** it is read
**Then** it holds only the database: the image `postgres:18.7`, user and database `prognose`, trust authentication, the port `127.0.0.1:15432`, a named volume at `/var/lib/postgresql`, `restart: unless-stopped` and a `pg_isready` health check (AD-14)
**And** the database has no stored password and accepts connections only from the same computer (NFR-3)

**Given** the Structural Seed in the architecture spine
**When** the repository is inspected
**Then** it has `src/manage.py`, the project `src/prognose/`, the packages `src/forecasting/`, `src/explanation/` and `src/web/`, and the folders `tests/`, `data/`, `reference/` and `docs/`
**And** the first migration creates the custom user model `web.Company`, with `customer_number` as its login field and the company name (AD-6)

**Given** no `.secret_key` file
**When** `load_seed` runs
**Then** it creates `.secret_key`, which `.gitignore` excludes (AD-13)
**And** when `.secret_key` already exists, `load_seed` never overwrites it and leaves its content unchanged; a test covers both cases, and in this story the command loads no data (Story 1.7 adds the loading)

**Given** the settings
**When** `PROGNOSE_LAN_HOST` is not set
**Then** `ALLOWED_HOSTS` holds only `127.0.0.1` and `localhost`, and the documented start command listens only on `127.0.0.1` (AD-13)
**And** when the variable names an address, that address is added for the phone test over the local network while DEBUG stays off, and a test covers both cases (NFR-6)

**Given** `pyproject.toml` and `uv.lock`
**When** the dependencies are installed with `uv sync --locked`
**Then** Django 5.2.19 and psycopg[binary] 3.3.9 are pinned exactly, and so are the development tools pytest 9.2.0, pytest-django 4.14.0, Ruff 0.17.5 and openpyxl 3.1.5
**And** `.python-version` names Python 3.13, and `uv.lock` is the only lock file (DR-2)

**Given** the test setup
**When** `uv run pytest` runs
**Then** it runs with pytest-django against the local PostgreSQL from `compose.yaml`, including the tests of the page at `/` and of the secret file (AD-14, AD-17)
**And** `uv run ruff check` and `uv run ruff format --check` pass on the Python files

**Given** `.gitignore` and `.env.example`
**When** they are read
**Then** `.gitignore` keeps out the virtual environment, caches, test and coverage output, the local database data, `.env`, `.secret_key`, and operating-system and editor files, and its Next.js part and `db.sqlite3*` are gone (DR-2)
**And** `.env.example` lists `PROGNOSE_DEBUG`, `DATABASE_URL` and `PROGNOSE_LAN_HOST`, each marked as optional or secret; the language-model variables are added only with FR-28 (Optional features convention)

**Given** the process documents
**When** this story is done
**Then** `docs/statustabell.md` lists every FR and DR-10 with its priority and status (DR-8)
**And** `docs/ki-styringslogg.md` holds the planning-phase cases taken from the examples of AI steering in `docs/arbeidslogg.md`, with the memlogs where needed, each with what the AI proposed, what was wrong, what the group decided, the commit or pull request where the source names one, and the source (DR-5)

**Given** the planning phase
**When** its AI defects and prompts are documented
**Then** `docs/qa-logg.md` records the defects in AI-generated text and code that the work log and the review files describe, such as the rounding error in E5, the processing order of R-10 and R-11, the CSS rule that also hit the legend icons and the wrong breakpoint, each with how it was found, the fix and its commit where the source names one (DR-9)
**And** no planning-phase prompt is reconstructed: where no original prompt is saved, the entry names the work log, a memlog or a session log as its source, and the process documentation says that the planning phase is documented this way (DR-5)
**And** this story's own Claude Code session is exported, checked for privacy and committed by the routine for AI sessions (DR-5, NFR-4)

**Given** the README
**When** this story is done
**Then** its setup section lists the commands above, which are the same in macOS Terminal and Windows PowerShell, and says that Windows on ARM is not supported
**And** it says that no API key, paid service or third-party account is needed, that `load_seed` creates the session secret in `.secret_key`, which Git ignores, and that every variable in `.env.example` is optional (NFR-1, NFR-3)
**And** `docs/qa-logg.md` records the first setup on macOS with the date, the Docker Desktop version, the result and the time taken; the tests on Windows and offline are Story 1.3

### Story 1.2: Check every pull request automatically

As a group member,
I want every pull request tested and linted automatically on Linux,
So that a broken rule, a missing migration or a forbidden import never reaches `main`.

**Priority:** Must. **Requirements:** NFR-2, DR-7; AD-1, AD-17; D-1.

**Tasks,** each with the check that proves it:
1. The GitHub Actions workflow in `.github/workflows/`: a run on a pull request passes.
2. The AD-1 import test: it fails on a forbidden import.
3. The migration check in the test run: `makemigrations --check` fails when a model change has no migration.
4. The organization check: GitHub Actions is allowed in IBE160-2026, recorded in the QA log.

**Acceptance Criteria:**

**Given** a pull request
**When** GitHub Actions runs on Linux
**Then** it installs the locked dependencies with `uv sync --locked`, starts the database from the same `compose.yaml`, and runs `uv run pytest`, `uv run ruff check` and `uv run ruff format --check` (AD-17)

**Given** the packages `forecasting/` and `explanation/`
**When** `uv run pytest` runs
**Then** an import test fails if either imports anything outside the Python standard library, except `explanation/` importing `forecasting/`, or if `forecasting/` imports `explanation/` (AD-1)

**Given** the models
**When** `uv run pytest` runs
**Then** it includes `makemigrations --check`, which fails when a model change has no migration (AD-17)

**Given** a failing run
**When** the group reviews the pull request
**Then** the pull request is not merged until the run passes (AD-17, DR-7)
**And** the group has confirmed that GitHub Actions is allowed in the IBE160-2026 organization, and the QA log records it (D-1)

### Story 1.3: Confirm the setup on Windows and without a network

As an examiner,
I want the setup tested on Windows x64 and with the network switched off,
So that I can trust the README on either operating system, also offline.

**Priority:** Must. **Requirements:** NFR-1, SM-2, DR-1, DR-9; D-3. No other story depends on this one, so it does not block other development. The final checks in Epic 4 run it again on the final commit.

**Tasks,** each with the check that proves it:
1. The setup from a fresh clone on the Windows x64 PC at work, if installing uv and Docker Desktop is allowed there, following the README's setup section in Windows PowerShell: Prognose answers in the browser.
2. The offline start on macOS and on Windows: Prognose answers with the network switched off.
3. Fixes for anything that fails, in the README or the configuration: the step passes when it is run again.
4. The results in `docs/qa-logg.md`: checked in the review.

**Acceptance Criteria:**

**Given** the Windows x64 PC at work
**When** the group checks whether uv and Docker Desktop may be installed on it, under the employer's IT rules and Docker's license terms
**Then** the Windows test runs there if they may (D-3)
**And** if they may not, the QA log records the limitation, the test runs on another Windows x64 computer if one is available, and otherwise the README and the status table say that the setup was not tested on Windows (SM-2, DR-1)

**Given** a Windows 10 22H2 or Windows 11 23H2 computer on x64 with uv, and Docker Desktop with WSL 2 and hardware virtualization switched on, and no earlier Prognose setup
**When** a group member follows the README's setup section from a fresh clone in Windows PowerShell
**Then** Prognose starts and answers at `http://127.0.0.1:8000/` (SM-2)

**Given** a computer where Prognose has been started once
**When** the app and the database are stopped, the network is switched off, and both are started again, on macOS and on Windows
**Then** Prognose starts and answers without a network connection (NFR-1, SM-2)

**Given** a step that fails
**When** its cause is found
**Then** this story fixes the README or the configuration, and the QA log records the finding and the fix (DR-9)

**Given** each test run
**When** it is finished
**Then** `docs/qa-logg.md` records the date, the operating system, the uv and Docker Desktop versions, the result and the time taken (DR-9)
**And** when uv and Docker Desktop are installed for the test, the QA log also records how long the installation took, with WSL 2 and any restart, for the README's expected setup time (Story 4.1)
**And** the time from the clone to logged in (SM-2) is measured in Epic 4, once login exists

### Story 1.4: Norwegian app shell and error pages

As an examiner,
I want every page to share the approved look and every error to show a Norwegian page instead of a debug page,
So that a stopped database or a wrong address tells me what to do next.

**Priority:** Must. **Requirements:** NFR-1, NFR-5, NFR-6, NFR-10, NFR-11; AD-11, AD-12, AD-13; UX-DR1 to UX-DR5, UX-DR7, UX-DR13, UX-DR14 (the logged-out header), UX-DR21, UX-DR41, UX-DR43, UX-DR44.

**Acceptance Criteria:**

**Given** the one stylesheet
**When** it is read
**Then** it defines every token in the DESIGN.md frontmatter as a CSS custom property with the same value: 26 colors, 17 typography roles, 5 radii and the spacing scale (UX-DR1)
**And** components use only these variables, and no page loads a font, script or stylesheet from outside the app (AD-11, NFR-1)

**Given** any page
**When** it renders
**Then** it has `lang="nb"`, the system font stacks with tabular numerals, and the navy app header with only the wordmark «Prognose», as when logged out (UX-DR2, UX-DR14)
**And** every focusable element shows a 3 px blue outline 2 px outside it, and the page has no shadows, gradients or animation (UX-DR4, UX-DR43, UX-DR44)

**Given** any page on a PC, an iPad or a phone
**When** it renders from 320 px wide
**Then** it has the viewport tag `width=device-width, initial-scale=1`, the page does not scroll sideways, and the header wraps instead of being cut off (NFR-6, UX-DR7)
**And** the stylesheet sets the touch rules once for every page: on touch screens every control has a target of at least 44 × 44 px, and form fields use 16 px text (UX-DR7)

**Given** an unknown address
**When** it is requested
**Then** the response is 404 with the not-found panel: the page title «Siden finnes ikke» and the link «Til produktoversikten» (UX-DR13, NFR-10)
**And** no stack trace or debug page is shown

**Given** a stopped database
**When** a page that reads the database is requested
**Then** the response is 503 with the «Database unavailable» text from the Message Catalogue in the not-found panel, with its first sentence as the page title (AD-12)
**And** the 503 handling sits in the outermost middleware, so a database error raised anywhere, also in other middleware, gives this page, and the page itself reads nothing from the database

**Given** a failed CSRF check
**When** a form is submitted
**Then** the response is 403 with the «Expired form» text, «Skjemaet er utløpt. Last siden på nytt og prøv igjen.»
**And** any other 403, and any 400, 405 or 500, shows the «Server error» text with the link «Til produktoversikten», never the expired-form text; every error page is in Norwegian, and tests cover a failed CSRF check, another 403 and a 405 separately (AD-12)

**Given** the run modes
**When** the local `.env` does not set `PROGNOSE_DEBUG`
**Then** DEBUG is off, and only `PROGNOSE_DEBUG` in the local `.env` turns it on (AD-12, AD-13)
**And** errors are logged to the console without request bodies, passwords, secrets or database URLs

### Story 1.5: Reference spreadsheet as the answer key

As an examiner,
I want a spreadsheet in the repository with the hand-calculated reference examples E1–E30 and the expected results of the rule test products,
So that I can check every number in Prognose against the same answer key that the tests use.

**Priority:** Must. **Requirements:** DR-3, FR-3 (the expected results), FR-21 (the variants), SM-1; AD-17; PRD §5.7; UX-DR46. It needs only the repository, so it can start at the same time as Story 1.1 and run alongside Stories 1.1 to 1.4.

**Acceptance Criteria:**

**Given** the spreadsheet in `reference/`
**When** it is opened
**Then** it holds every reference example from PRD §5.7, E1 to E30 with E11 a and b, E18 a and b and E29 a to g, each with its inputs (the sales series with stockout weeks marked, the settings, the stock on hand, and the 4-week cycle where an example uses one) and its expected results
**And** the expected results equal the values in PRD §5.7

**Given** the answer-key sheet
**When** this story is done
**Then** its schema (one row per case, the columns and how a stockout week is marked) is documented in `reference/` (Deferred)
**And** a test reads the spreadsheet with openpyxl and fails if a case from PRD §5.7 is missing or has no expected result (AD-17)

**Given** the rule test products built from E1–E4, E7–E10 and E15–E19, and the demo products that act as rule test products (UX-DR46)
**When** the spreadsheet is complete
**Then** it holds each product's sales series, its stock on hand and its expected base forecast, suggested order quantity, unusual weeks, level-shift weeks, warnings and confidence label (FR-3, DR-3)

**Given** the FR-21 table
**When** the spreadsheet is complete
**Then** it also holds the four variants that FR-21 lists beyond PRD §5.7: E1 with window 4, E2 with smoothing factor 0,5, E3 with scenario percentage 20 % and E4 with safety margin 50 % (FR-21)
**And** each variant has its expected values, calculated by hand and recorded like the other cases, so that Story 3.2 reads them and no test or calculation code holds them (AD-17)

**Given** the hand check
**When** a group member recalculates each expected result by hand or with visible formulas
**Then** the spreadsheet records the check with its date
**And** every difference from PRD §5.7 is calculated again, whichever side was wrong is corrected (a PRD correction gets a row in PRD §12), and the finding goes into the QA log (AD-17, DR-9)

### Story 1.6: Generate the synthetic seed data

As an examiner,
I want a deterministic generator to create two test companies with known products and patterns,
So that every rule and every warning has data with a known answer.

**Priority:** Must. **Requirements:** FR-3, NFR-3, NFR-4; AD-8, AD-15; UX-DR46; SM-7 (the patterns).

**Acceptance Criteria:**

**Given** `data/generate_seed.py` and the reference spreadsheet
**When** the generator runs twice
**Then** both runs write identical JSON files in `data/seed/` (FR-3, AD-15)
**And** the schema of the seed JSON is documented in `data/` (Deferred)

**Given** the seed files
**When** they are read
**Then** they hold two test companies with 10 to 50 products each and disjoint product numbers of 5 digits
**And** each product has a name, a run of consecutive ISO weeks with the units sold and a stockout flag per week, ending at the company's latest data week, and a stock on hand (FR-3, AD-8)

**Given** the products of a test company
**When** their histories are counted
**Then** most have 104 weeks, and at least one has fewer than 3 valid weeks, one 3 to 11 and one 12 to 103 (FR-3)
**And** at least one product is built for each pattern: a known trend, a seasonal pattern without trend, stockout weeks, unusual weeks, a level shift, a long run of stockout weeks at the end, stock on hand that covers next week, and a history meant to reach «høy»; the seed documentation names the product for each pattern (FR-3, SM-7)

**Given** the rule test products
**When** the generator builds them
**Then** their series and stock on hand come from the reference spreadsheet, not from the generator's own code (AD-15)
**And** the demo content matches the products and values in the UX examples where the rules allow: «Testbedrift A» as a hardware store with about 30 products, including «Isskrape», «Strøsand 25 kg» (reproducing the E1 and E4 results in a longer history), «Snøskuffe aluminium» and the E8 product, with week 45 of 2026 as the latest data week; Skruer's week-1 forecast is 21,3 and Kabelstrips' weeks of cover 3,8, because the mockup's 21,5 and 3,7 cannot occur (UX-DR46)

**Given** the two test companies
**When** the products are placed in them
**Then** Testbedrift A holds the UX demo products and the E8 product, with enough stock that the E8 product has no order-soon status, so «Denne uken» shows 4 products to order soon, 31 units, 1 product without a forecast and 4 products with warnings (UX-DR46)
**And** Testbedrift B holds the other rule test products and pattern products, so that every FR-3 pattern is still in the dataset (FR-3, SM-7)

**Given** the logins
**When** the seed files are written
**Then** they hold only password hashes made with Django's PBKDF2 hasher and a fixed salt per company, never a plain-text password (FR-1, AD-15, NFR-3)
**And** the README gives each company's customer number and password (FR-3)

**Given** the seed data
**When** it is reviewed
**Then** it contains no real company, customer or personal data (NFR-4)

### Story 1.7: Load the seed data into an empty database, with an explicit reset

As an examiner,
I want one command that loads the test companies into an empty database and never deletes data unless I confirm a reset,
So that I can set up Prognose safely and restore the demo state when I need to.

**Priority:** Must. **Requirements:** FR-4 (the local part), DR-1, DR-4, SM-5; AD-8, AD-9, AD-15.

**Acceptance Criteria:**

**Given** an empty database after `migrate`
**When** `uv run python src/manage.py load_seed` runs
**Then** it loads both companies with their products and sales weeks, and one `CompanySettings` row per company with the FR-20 defaults
**And** the FR-20 defaults and ranges are defined once, in `forecasting/settings.py`, and the model defaults and `load_seed` read them from there (AD-9)

**Given** a database that already holds a company
**When** `load_seed` runs without options
**Then** it stops with a Norwegian message and changes nothing (DR-4, AD-15)

**Given** a database with data, settings and sessions
**When** `load_seed --reset` runs and the user types the confirmation
**Then** in one transaction it deletes the companies with their data and all sessions and loads the seed state, without duplicates or errors (DR-4, AD-15)
**And** without the typed confirmation it changes nothing, and no other command or build step runs `--reset`

**Given** a seed file where a product's history has a gap or does not end at the company's latest data week, or where units sold or a stock on hand is negative
**When** `load_seed` reads it
**Then** it refuses the file with a Norwegian message and loads nothing (AD-8)
**And** the latest data week is derived from the sales weeks and is never stored separately

**Given** loaded data
**When** the app and the database are stopped and started again
**Then** every product, sales week and setting is unchanged, and the QA log records the check (FR-4, SM-5)

**Given** the README
**When** this story is done
**Then** it says how to generate and load the data, and that an explicit reset restores the seed state and also resets the settings and adjustments (DR-1, DR-4)

### Story 1.8: Log in and see only your own company's products

As a purchasing manager,
I want to log in with my company's customer number and password and see my company's products,
So that I work with my own company's data and nobody else's.

**Priority:** Must. **Requirements:** FR-1, FR-2, NFR-3, NFR-6 (the first test on the real iPhone), NFR-10, SM-4; AD-3, AD-6, AD-7, AD-10, AD-11, AD-13; UX-DR8, UX-DR14, UX-DR38.

**Acceptance Criteria:**

**Given** the login page at `/`
**When** it opens
**Then** it shows the Innlogging wireframe: the page title «Logg inn», the line «Prognose foreslår hvor mye du bør bestille neste uke, og viser hvordan tallene er regnet.», the fields «Kundenummer» and «Passord» with visible labels, the primary button «Logg inn» and «Innloggingen for testbedriftene står i README.» (UX-DR8)
**And** Enter submits the form

**Given** a test company's correct customer number and password
**When** the user logs in
**Then** the product overview at `/produkter/` opens (FR-1)

**Given** a wrong customer number or a wrong password
**When** the form is submitted
**Then** «Feil kundenummer eller passord.» appears above the fields with `role="alert"`, the same in both cases (FR-1)
**And** the customer number is kept and the password field is empty

**Given** a user who is not logged in
**When** any page except the login page and the error pages is requested
**Then** the login page opens, because `LoginRequiredMiddleware` denies by default (FR-1, AD-6)

**Given** a logged-in user
**When** «Logg ut» in the app header is used
**Then** a POST form ends the session and the login page opens, and a GET request to `/logg-ut/` does not end the session (FR-1, AD-6, AD-10)

**Given** a logged-in company
**When** the product overview opens
**Then** it lists only that company's products with the product number, the name and the stock on hand, by product number; Epic 2 replaces this list with the full overview (FR-2)
**And** the app header shows «[Testbedrift A] · siste registrerte uke: uke [45], [2026]», «Produktoversikt» marked as the current page, and «Logg ut», with the week label and the numbers from `forecasting/display.py` (UX-DR14, AD-3)

**Given** the data access
**When** the code is reviewed
**Then** every read of company data goes through functions in `web/queries.py` that take the logged-in company as their first argument and filter by it, and no view uses a model manager for company data (AD-7)

**Given** test company A logged in
**When** it tries to see test company B's products or stock on hand through the product list
**Then** no list shows B's data, and an automated two-account test checks every route and list that exists after this story (FR-2, SM-4)
**And** every later story that adds a route or a list extends this test (AD-7)

**Given** the login
**When** it checks a password
**Then** it uses Django's default PBKDF2 hasher with the hashes from the seed data, and no plain-text password reaches the database or the logs (FR-1, NFR-3)
**And** submitting the login form twice, or reloading after login, gives the same result without errors (NFR-10, AD-10)

**Given** a logged-in user and a stopped database
**When** any page is requested
**Then** the 503 page from Story 1.4 appears, without the parts of the layout that read the database, and a test covers it (AD-12)

**Given** the login on a real phone
**When** a group member starts Prognose for the phone test over the local network (AD-13) and logs in as each test company on the real iPhone 13 in Safari
**Then** the product overview opens with only that company's products, and the QA log records it as a test on a real device, with the date and the iOS version (NFR-6)
**And** after the test the app is stopped and `PROGNOSE_LAN_HOST` is removed

## Epic 2: See what to order, how it was calculated and whether to trust it

Mounia sees the product overview with «Denne uken» in R-12 order. For each product she sees the week forecasts, the scenarios, the suggested order quantity, the forecast calculation and the order calculation line, the chart, the warnings, the confidence label and the template explanation, all matching the reference spreadsheet.

### Story 2.1: Find the valid weeks, unusual weeks and level shifts

As a purchasing manager,
I want Prognose to leave out stockout weeks and to find unusual weeks and level shifts by fixed rules,
So that a forecast never silently rests on weeks that do not show real demand.

**Priority:** Must. **Requirements:** FR-15, FR-16 and FR-17 (finding the weeks); R-1, R-10, R-11; AD-1, AD-8, AD-17; E7, E8, E9, E10, E15, E16, E18 a and b, E19.

**Acceptance Criteria:**

**Given** a sales history with stockout weeks
**When** the core classifies the weeks
**Then** stockout weeks are not valid weeks, are never used in any calculation and do not count toward any valid-week threshold (FR-15, R-1)
**And** E7 has 4 valid weeks

**Given** the valid weeks in time order
**When** the core checks them in one forward pass
**Then** each week's baseline is the median of the 3 most recent earlier valid weeks that are not unusual weeks, with level-shift weeks included (R-10)
**And** a week with fewer than 3 such weeks is not checked but enters later baselines (E19), a baseline of 0 never gives an unusual week (E10), and a week is unusual only when its sales are more than 2 × the baseline, so exactly 2 × is not (E18 a and b)

**Given** the same pass
**When** a week becomes unusual and the two previous valid weeks are unusual too
**Then** the three weeks become level-shift weeks at once (E9), while one or two unusual weeks in a row stay unusual weeks (E8) (R-11)
**And** level-shift weeks are not unusual weeks and count in later baselines, so a later spike is compared with the new level (E15), and stockout weeks between them do not break the run (E16)

**Given** any distance or order between weeks
**When** the core needs it
**Then** it uses the week's position in the sales history, never calendar arithmetic (AD-8)
**And** the core reads no clock, file or environment variable (AD-1)

**Given** the tests
**When** `uv run pytest` runs
**Then** the classification of every example listed above is read from the reference spreadsheet and matches it, and each test names its E-n and FR-n (AD-17, DR-5)

### Story 2.2: Calculate the base forecast with the moving average or exponential smoothing

As a purchasing manager,
I want the base forecast from the chosen method over the calculation weeks only, and no forecast when the data is too thin,
So that I can check the number by hand and know when I have to decide myself.

**Priority:** Must. **Requirements:** FR-5, FR-6, FR-8, FR-16 (included or excluded), FR-17 (level-shift weeks kept); R-2, R-3, R-4, R-6; AD-2, AD-3, AD-9; E1, E2, E7, E8, E9, E11 a and b, E15 to E20, E28.

**Acceptance Criteria:**

**Given** the classified weeks and the setting for unusual weeks
**When** the calculation weeks are chosen
**Then** they are the valid weeks in time order, minus the unusual weeks when the setting excludes them (R-2)
**And** level-shift weeks are always calculation weeks, and an excluded unusual week still counts as a valid week (FR-16, FR-17)

**Given** the moving average with window N
**When** the base forecast is calculated
**Then** it is the sum of the last N calculation weeks divided by N, skipping the weeks that are not calculation weeks and looking further back (FR-5, R-3)
**And** it matches E1, E7, E8 (with unusual weeks included and excluded), E9, E15, E16, E18 a and b, E19, E20 (10.25 before display rounding) and E28

**Given** exponential smoothing with factor α
**When** the base forecast is calculated
**Then** the first calculation week's sales are the start level, each later calculation week gives α × its sales + (1 − α) × the previous level, and the base forecast is the last level (FR-6, R-4)
**And** skipped weeks do not count as zero, so E2 and E17 match (E17 gives 21.404, not 16.256)

**Given** a product with fewer than 3 valid weeks, or the moving average with fewer calculation weeks than the window
**When** the core runs
**Then** it gives no forecast, with the reason: fewer than 3 valid weeks (E11 a), or the window and the number of calculation weeks (E11 b) (FR-8, R-6)
**And** exponential smoothing needs at least one calculation week

**Given** `forecast_product(weeks, stock_on_hand, settings)`
**When** it runs
**Then** it returns a frozen `ProductResult` from its inputs only, with full float precision and no formatted strings (AD-2, AD-3)
**And** the settings it uses follow the definitions in `forecasting/settings.py` (AD-9)

### Story 2.3: Round and format every number the same way

As an examiner,
I want every number rounded by one rule and shown in Norwegian format,
So that the screen, the explanation and the reference spreadsheet always agree.

**Priority:** Must. **Requirements:** R-9, NFR-5; AD-2, AD-3; E5, E20, E21; UX-DR42.

**Acceptance Criteria:**

**Given** a value to be rounded up to whole units
**When** `forecasting/rounding.py` rounds it
**Then** it first rounds to 6 decimals and then up, so the E5 value gives 70, not 71 (R-9)
**And** every rounding uses the `decimal` module, never `round()` (AD-3)

**Given** a value for display
**When** it is rounded
**Then** it is rounded half away from zero: forecasts, scenarios, weeks of cover and the safety margin amount with one decimal (E20 is shown as «10,3»), the unrounded result on the order calculation line with two decimals (E21 is shown as «0,07»), and order quantities and percentages as whole numbers (R-9)
**And** the decimals for seasonal indices and adjusted values come with FR-9 (Epic 5)

**Given** a number to show
**When** `forecasting/display.py` formats it
**Then** it uses a decimal comma, the minus sign U+2212 («−40,00»), no thousands grouping, and a no-break space before «%» («10 %») (AD-3, NFR-5)

**Given** a week to label
**When** `forecasting/display.py` labels it
**Then** the label uses the ISO week («uke 46»), with the year on the first week of a new year («1/2027») and in lists that reach before the recent period («uke 10/2025») (AD-3, UX-DR42)

**Given** the code outside `forecasting/`
**When** it is reviewed
**Then** nothing there rounds or formats a domain number, and the template filters call `forecasting/display.py` (AD-2, AD-3)

### Story 2.4: Calculate the week forecasts, the scenarios and the suggested order quantity

As a purchasing manager,
I want the week forecasts for the next three weeks, the three scenarios and one suggested order quantity for next week,
So that I have one number to order and can see what happens if sales are higher or lower.

**Priority:** Must. **Requirements:** FR-7, FR-10, FR-11, FR-12 (its values); R-5, R-7, R-8, R-13; AD-2, AD-3, AD-8; E3, E4, E5, E6, E21, E28.

**Acceptance Criteria:**

**Given** a base forecast without seasonal adjustment
**When** the week forecasts are calculated
**Then** weeks 1, 2 and 3 after the latest data week all equal the base forecast, and the result marks the product for the FR-7 note (FR-7, R-5)
**And** E28 shows the stated trend lag: the forecast stays at the base forecast while the trend would continue

**Given** the forecast horizon
**When** its weeks are labeled
**Then** week 1 is the ISO week after the latest data week, and only these labels use calendar arithmetic (AD-8)

**Given** a week forecast and the scenario percentage
**When** the scenarios are calculated
**Then** for each horizon week, normal is the week forecast, optimistic is the week forecast × (1 + the percentage), and pessimistic is the larger of 0 and the week forecast × (1 − the percentage) (FR-10, R-7)
**And** E3 matches

**Given** the week-1 normal forecast, the safety margin and the stock on hand
**When** the suggested order quantity is calculated
**Then** it is the larger of 0 and week-1 normal forecast × (1 + safety margin) − stock on hand, rounded up once through `forecasting/rounding.py` (FR-11, R-8, R-9)
**And** E4 gives 11, E5 gives 70, E6 gives 0 and E21 gives 1

**Given** a product without a forecast
**When** the core runs
**Then** it has no week forecasts, no scenarios and no suggested order quantity (FR-8, FR-11)

**Given** `ProductResult`
**When** it is complete
**Then** it also holds the safety margin amount, the unrounded order result and the stock on hand at the end of the latest data week (R-13), so that the order calculation line can be shown (FR-12)

### Story 2.5: Give each product its warnings, notes and confidence label

As a purchasing manager,
I want every product to get its active warnings, its notes and a confidence label with a plain reason in Norwegian,
So that I know when a forecast should not be trusted, and why.

**Priority:** Must. **Requirements:** FR-7 (the note), FR-8 (the warning), FR-15 to FR-19; R-15, R-16; SM-7, SM-10; AD-2, AD-4; E11 a and b, E12, E29 a to g; UX-DR40.

**Acceptance Criteria:**

**Given** a product's classified weeks
**When** its active warnings are found
**Then** they are, in R-15 order: stockout weeks in the recent period of 12 weeks; unusual weeks in the recent period, included or excluded; a level shift with a level-shift week in the recent period; old data, when the latest valid week is more than 8 weeks before the latest data week by position; and insufficient data, when the product has no forecast (R-15, FR-8, FR-15 to FR-18)
**And** E12 gives the old-data warning at 9 weeks and none at 8, and stockout and unusual weeks before the recent period are not active warnings

**Given** a change of the unusual-weeks setting
**When** the warnings are found again
**Then** the unusual-weeks warning neither appears nor disappears (FR-16)

**Given** the conditions of R-16
**When** the confidence label is set
**Then** the first condition that applies decides: no forecast or fewer than 12 valid weeks gives «lav»; an active warning, a sales history shorter than 104 weeks with stockout weeks counted, or fewer than 100 valid weeks gives «middels»; otherwise the label is «høy» (FR-19, R-16)
**And** E29 a to g match

**Given** the label, the warnings and the notes
**When** `explanation/` writes their texts
**Then** each text follows its Message Catalogue row: the reason with the label word, the deciding condition and the other active warnings (for example «Middels: 2 utsolgte uker og 1 uvanlig uke de siste 12 ukene.»); the warnings for stockout weeks, unusual weeks (included, excluded and several), old data and insufficient data (the list text and the warning, for few weeks and for the window); and the FR-7 note (AD-4, UX-DR40)
**And** a level shift is named only in the reason («nytt nivå de siste 12 ukene»), because its warning text is FR-17b (Should)

**Given** the reasons
**When** a forecast is missing because of the window, or several R-16 conditions for the same label apply
**Then** the reason for the window case is «Lav: ingen prognose, færre uker enn vinduet.» (E29 e), and with several conditions the reason names the first in R-16 order as the deciding condition (an active warning, then a sales history shorter than 104 weeks, then fewer than 100 valid weeks), followed by the other active warnings (FR-19, R-16)
**And** snapshots cover the window case and a product with both an active warning and a short sales history

**Given** the seed data
**When** the core runs for every product
**Then** every warning and every confidence label, «høy» included, is triggered by at least one test product (SM-7)
**And** a product labeled «lav» because it has too few valid weeks exists for the SM-10 check

### Story 2.6: Sort the products by what needs ordering first

As a purchasing manager,
I want the products sorted so that the ones to order soon come first, with their weeks of cover,
So that I start with what is most urgent.

**Priority:** Must. **Requirements:** FR-3 and DR-3 (the rule test products), FR-24 (the order), NFR-2; R-12; SM-1; PRD §10 question 4; AD-2, AD-17; E13, E23, E24; UX-DR33, UX-DR35.

**Acceptance Criteria:**

**Given** a product with a suggested order quantity above 0
**When** its order-soon status is set
**Then** it has order-soon status (R-12)
**And** when the week-1 normal forecast is 0, the weeks of cover are «–» and there is no order-soon status (E23)

**Given** the stock on hand and the week-1 normal forecast
**When** the weeks of cover are calculated
**Then** they are the stock on hand ÷ the week-1 normal forecast, and E13 matches (R-12)

**Given** every product of a company
**When** `build_overview(results, adjustments)` runs
**Then** it gives three groups in this order: the order-soon products by weeks of cover, lowest first, with ties by product number (E24); the products without a forecast, by product number; and the other products, by product number (R-12)
**And** the adjustments input stays empty until FR-29 is built

**Given** the overview
**When** it is built
**Then** it also gives the four week figures (products with order-soon status, the sum of the suggested order quantities, products without a forecast, products with at least one active warning), the review sequence (order-soon, then without a forecast), and the previous and next product of each product across all groups (AD-2, UX-DR33, UX-DR35)

**Given** the core from Stories 2.1 to 2.6
**When** `uv run pytest` runs
**Then** every Must reference example passes as a test that reads the spreadsheet: E1 to E13, E15 to E21, E23, E24, E28 and E29 (SM-1, NFR-2)
**And** for every rule test product in the seed data, the core's base forecast, suggested order quantity, unusual weeks, level-shift weeks, warnings and confidence label equal its expected results in the reference spreadsheet (FR-3, DR-3, PRD §10 question 4)

### Story 2.7: Show what to order and whether to trust it on the product screen

As a purchasing manager,
I want a product screen that shows the suggested order quantity and the confidence label with its warnings without scrolling,
So that I see the decision and how far to trust it at a glance.

**Priority:** Must. **Requirements:** FR-2, FR-8, FR-11, FR-19, FR-25, NFR-6, NFR-8, NFR-11; AD-2, AD-4, AD-7, AD-11; UX-DR6, UX-DR7, UX-DR10, UX-DR20, UX-DR22, UX-DR24, UX-DR44.

**Acceptance Criteria:**

**Given** a logged-in company
**When** `/produkter/<varenummer>/` opens for one of its products
**Then** the page has the product list on the left (for now the list from Story 1.8, whose rows now link to their product screens) and the product on the right, after the skip link «Gå til produktet» (UX-DR10, UX-DR44)
**And** the product header has the product name as the `h1`, the large trust label, and «Varenr. [10012] · Lagerbeholdning [5] · Uker dekning [0,3]»

**Given** the decision panel «Hva bør du bestille?»
**When** the product has a forecast
**Then** it shows the suggested order quantity in 44 px blue, or in ink when it is 0, as the largest number on the screen, with «Foreslått bestillingsmengde for neste uke, uke [46]», and no buttons (FR-11, UX-DR22)
**And** without a forecast it shows «–», «Ingen foreslått bestillingsmengde» and «Prognose foreslår ingen mengde for dette produktet. Du bestemmer bestillingen selv.» (FR-8)

**Given** the trust panel «Kan du stole på prognosen?»
**When** it renders
**Then** it has the same height as the decision panel and shows the large trust label, the reason, and one row per active warning in R-15 order with its Message Catalogue text and its shape icon, data problems on red-tint and demand patterns on amber-tint (FR-19, FR-25, UX-DR24)
**And** it shows nothing that does not apply to the product

**Given** a 1366 × 768 screen (1366 × 640 px of content)
**When** the product screen opens
**Then** the suggested order quantity, the confidence label and the active warnings are visible without scrolling (FR-25)
**And** they stay visible also for the product with the most warning rows in the seed data; the layout follows UX-DR6 and UX-DR7, with no horizontal page scrolling and nothing overlapping or cut off from 320 px wide (NFR-6), checked by hand and recorded in the QA log

**Given** a screen 900 px wide or narrower, such as an iPad held upright or a phone
**When** the product screen opens
**Then** the layout has one column: the product header, the decision panel and the trust panel come first, then the rest of the product, and the product list last, with no scroll frame of its own (NFR-6, UX-DR7)
**And** the skip link «Gå til produktet» stays the first focusable element, and the HTML and keyboard order stay as on a wide screen (UX-DR44)

**Given** test company A
**When** it requests one of test company B's product numbers
**Then** the not-found page appears with none of B's data, and the two-account test covers this route (FR-2, AD-7)

**Given** the page
**When** it loads its data
**Then** it uses the one loader `web/company_data.py`, which reads the company's settings, products and sales weeks through `web/queries.py` in a fixed number of queries whatever the number of products, and computes the whole overview (AD-2)
**And** a test checks the number of queries with 50 products of 104 weeks (NFR-8)

### Story 2.8: List the products in R-12 order

As a purchasing manager,
I want the list of products to show each product's suggested quantity, forecast, cover and trust, grouped by what needs ordering first,
So that I see at a glance where to start.

**Priority:** Must. **Requirements:** FR-2, FR-24, NFR-6, NFR-8; AD-2, AD-11; E13, E23, E24; UX-DR7, UX-DR15 (without the button), UX-DR16, UX-DR17, UX-DR18, UX-DR20.

**Acceptance Criteria:**

**Given** a logged-in company
**When** `/produkter/` or a product screen opens
**Then** the list shows every product in the groups «Bestill snart», «Uten prognose» and «Øvrige produkter», in the order from `build_overview`, each group with its heading and summary («[4] produkter · [31] enheter foreslått», «[1] produkt · du bestemmer selv», «[25] · etter varenummer»), and an empty group is not shown (FR-24, UX-DR16)
**And** it replaces the list from Story 1.8

**Given** a product in «Bestill snart» or «Uten prognose»
**When** its card renders
**Then** it shows the name, «Varenr.», «Foreslått» over the quantity, «Lager», «Ukeprognose uke 1» and «Uker dekning», the trust label and, unless the label is «høy», the reason without the label word and the full stop; the whole card is one link to its product screen (UX-DR17)
**And** without a forecast, the card shows the FR-8 reason in red in place of the week-1 forecast (for example «Ingen prognose: færre enn 3 gyldige uker»), «–» for the quantity and the weeks of cover, and a dashed red border (FR-24)

**Given** a product in «Øvrige produkter»
**When** its row renders
**Then** it shows the name, the line «Varenr. [10001] · Lager [40] · Ukeprognose uke 1: [9,3] · Uker dekning [4,3]», «Foreslått» over the quantity in ink, and the trust label with the reason unless it is «høy» (UX-DR18)

**Given** the product shown on a product screen
**When** the list renders beside it
**Then** its card or row has the selected style and `aria-current="page"`, and selection wins over the dashed red border (UX-DR17, UX-DR44)

**Given** a screen 900 px wide or narrower
**When** the overview or a product screen opens
**Then** the list follows the product area with no scroll frame of its own, and every card and row stays one link that can be tapped anywhere (NFR-6, UX-DR7)
**And** the settings bar wraps onto more lines instead of being cut off (UX-DR7, UX-DR15)

**Given** a company without products
**When** the product overview opens
**Then** the list says «Ingen data er lastet inn. Kjør [lastekommandoen] som står i README.» with the exact load command (FR-24)

**Given** any page after login
**When** it renders
**Then** the settings bar shows the settings in use («Glidende gjennomsnitt, 3 uker», «Scenarioprosent 10 %», «Sikkerhetsmargin 10 %», «Uvanlige uker: tas med») and «Endringen gjelder alle produkter i bedriften.»; the button «Endre innstillinger» comes in Epic 3 (UX-DR15)

**Given** 50 products of 104 weeks
**When** the product overview opens
**Then** it uses a fixed number of queries, and a hand check on an ordinary laptop, recorded in the QA log, shows that it opens within 2 seconds (NFR-8)
**And** the two-account test checks that the list holds only the logged-in company's products (FR-2)

**Given** the texts in the list
**When** they depend on a result or a count
**Then** the card reason without the label word and the full stop, and the group summaries in singular or plural, come ready from `explanation/`, and the templates only place them (AD-4)

### Story 2.9: Show how the forecast and the order quantity were calculated

As an examiner,
I want the product screen to show the weekly sales, the forecast calculation with the weeks used and every week left out, the scenarios and the order calculation line,
So that I can check the forecast and the suggested order quantity by hand against the reference spreadsheet.

**Priority:** Must. **Requirements:** FR-7, FR-10, FR-12, FR-15, FR-16, FR-35, NFR-6; R-9; AD-3, AD-4; E1, E2, E3, E4, E6, E21; UX-DR7, UX-DR28, UX-DR29, UX-DR30, UX-DR42.

**Acceptance Criteria:**

**Given** the worksheet panel «Slik er tallene regnet ut»
**When** it renders
**Then** «Salgshistorikk, siste 12 uker» lists each of the last 12 weeks, or «Salgshistorikk, alle ukene» every week of a history of 12 weeks or fewer, with its units sold and a status tag for each flagged week: «utsolgt», «uvanlig», «nytt nivå», or «brukt» for a week used in the forecast (the last N calculation weeks for the moving average, every calculation week for exponential smoothing) (UX-DR28, UX-DR30)
**And** a sentence below the table explains the tags, as in the mockup

**Given** the moving average
**When** «Prognoseutregning» renders
**Then** it shows the FR-35 line in a calculation line, for example «Glidende gjennomsnitt, 3 uker: (16 + 12 + 15) / 3 = 14,3» (E1), followed by «Uker brukt: uke 43, 44 og 45.» (FR-35, UX-DR29)

**Given** exponential smoothing
**When** «Prognoseutregning» renders
**Then** it shows the last update, for example «Eksponentiell glatting, faktor 0,3: 0,3 × 15 + 0,7 × 13,3 = 13,8» (E2), with «Tallene er avrundet for visning.» inside the box (FR-35, R-9)
**And** a table of every calculation week with its sales and level, in its own scroll frame

**Given** weeks left out of the calculation
**When** «Prognoseutregning» renders
**Then** it lists every stockout week and every excluded unusual week in the whole history with its reason, for example «Holdt utenfor: uke 38 og 39 (utsolgt).», with the year in lists that reach before the recent period (FR-15, FR-16, UX-DR42)
**And** with unusual weeks excluded, each excluded week is listed and «[3] uker brukt i beregningen» is stated (FR-16)

**Given** «Ukeprognoser og scenarioer»
**When** it renders
**Then** a table has the columns «Uke 1 · uke [46]», «Uke 2 · uke [47]» and «Uke 3 · uke [48]» and the rows «Optimistisk», «Normal» in bold and «Pessimistisk», with values that match E3 for the E1 case (FR-10, UX-DR28)
**And** below it stand the scenario text with the actual percentage, «Scenarioene viser hva som skjer hvis salget blir [10] % høyere eller lavere. De er ikke sannsynligheter.», and, without seasonal adjustment, the note «Merknad: Uke 2 og 3 viser samme tall som uke 1 fordi metoden ikke tar hensyn til trend eller sesong.» (FR-10, FR-7)

**Given** «Utregning av bestillingsmengde»
**When** it renders
**Then** the order calculation line shows E4 as «Prognose 14,3 + sikkerhetsmargin 10 % (1,4) − lager 5 = 10,77 → foreslått bestillingsmengde 11», E6 ending with «= −40,00 → foreslått bestillingsmengde 0 (lageret dekker behovet)» and E21 ending with «= 0,07 → foreslått bestillingsmengde 1», with «Tallene er avrundet for visning.» inside the box (FR-12, UX-DR29)
**And** below the box it always shows «Sikkerhetsmarginen er en enkel tommelfingerregel. Leveringstid og varer som allerede er bestilt, er ikke tatt med.» (FR-12)

**Given** these lines and texts
**When** they are produced
**Then** their sentences come from `explanation/` and their numbers from `forecasting/display.py`, and the values match the reference spreadsheet (AD-3, AD-4)
**And** a product without a forecast shows only the sales table, with no «Prognoseutregning», no scenarios and no order calculation line (UX-DR10)

**Given** a screen from 320 px wide
**When** the worksheet renders
**Then** a table wider than the panel scrolls inside its own frame, calculation lines wrap between terms and never inside a number, and the page does not scroll sideways (NFR-6, UX-DR7)

### Story 2.10: Show the sales history and the forecast in a chart, also as text

As a purchasing manager,
I want a chart of the whole sales history and the next three weeks, with every left-out, unusual or level-shift week marked by its own shape, and the same information as text,
So that I see at once what happened to sales and what Prognose expects, whether or not I can see the chart.

**Priority:** Must. **Requirements:** FR-15, FR-16, FR-17, FR-25, NFR-1, NFR-6, NFR-7, NFR-11; AD-4, AD-11; UX-DR5, UX-DR7, UX-DR26, UX-DR27.

**Acceptance Criteria:**

**Given** the product screen
**When** it opens
**Then** the panel «Hva skjer med salget?», right below the decision and trust panels, holds an inline SVG chart rendered on the server, with no chart library, script or CDN (AD-11, NFR-1)
**And** the chart's geometry comes from a pure function in `web/chart.py` that uses only `ProductResult` and display strings, with unit tests for a product with every marker type

**Given** the sales history
**When** the chart renders
**Then** it shows every week, up to 104, as an ink line with dots where the weeks are at least 12 px apart, and its subtitle describes the whole history, not 12 weeks as in the mockup (FR-25, UX-DR26)
**And** the three forecast weeks lie on a turquoise-tint area labeled «De neste tre ukene», joined to the last sales week by a dashed line, with the scenario band, its dashed edges and the captions «Optimistisk», «Normal» and «Pessimistisk» with their values

**Given** stockout, unusual and level-shift weeks
**When** the chart renders
**Then** each stockout week breaks the line with a dashed connector and gets a hollow red square, each unusual week an amber triangle with its sales value, and each level-shift week an ink diamond (FR-15 to FR-17)
**And** the markers differ by shape, not by color alone (NFR-7, UX-DR5)

**Given** the axes and the recent period
**When** the chart renders
**Then** a dashed line marks where the last 12 weeks begin, labeled «Siste 12 uker», with no line when the whole history lies in the last 12 weeks; the axes use week numbers, with the year on the first week of a new year («1/2027»); and the forecast week numbers are turquoise (UX-DR26)

**Given** the legend
**When** it renders
**Then** it explains every marker type, whether or not the product has one: «Solgt», «Utsolgt uke, ikke brukt», «Uvanlig uke, tatt med» (with «holdt utenfor» when the setting excludes them), «Nytt nivå», «Prognose» and «Optimistisk og pessimistisk scenario», with 14 px markers and 24 px for lines and the band (UX-DR26)
**And** the chart's full-width rule does not reach the legend icons or any other SVG

**Given** a product without a forecast
**When** the chart renders
**Then** it shows the weeks that exist and no forecast region (UX-DR10)

**Given** the chart
**When** it renders
**Then** it has a title and a short summary from `explanation/`: the weeks shown, the stockout, unusual and level-shift weeks, the forecast and the scenario range (AD-4, UX-DR27)
**And** a snapshot test covers the summary for a product with every marker type

**Given** the chart panel
**When** it renders
**Then** it says «Tallene i diagrammet står i tabellene under «Slik er tallene regnet ut».», and the disclosure «Tabell med alle ukene i grafen» lists every week in the chart with its units sold and status (NFR-11, UX-DR27)
**And** a screen reader meets the chart as one image with its title and summary

**Given** a narrow screen, such as a phone
**When** the chart renders
**Then** its axis labels and captions are never smaller than 12 and 13 px; where the panel is too narrow for that, the chart keeps the width it needs inside its own horizontally scrolling frame, the legend wraps below it at the panel's width, and the page does not scroll sideways (NFR-6, UX-DR7)
**And** the summary and «Tabell med alle ukene i grafen» give the same values without sideways scrolling (NFR-11, UX-DR27)

### Story 2.11: Go through the week's products and find a product quickly

As a purchasing manager,
I want the overview to sum up the week and lead me through the products that need a decision, and I want to search the list and step through it with the keyboard,
So that I finish the review in the 20 minutes before the meeting, with or without the mouse.

**Priority:** Must. **Requirements:** FR-2, FR-24, NFR-6, NFR-11, UJ-1 steps 1 and 2; AD-2, AD-11; UX-DR7, UX-DR9, UX-DR19, UX-DR32 to UX-DR36, UX-DR43, UX-DR44, UX-DR45.

**Acceptance Criteria:**

**Given** the product overview
**When** it opens
**Then** the right side shows «Denne uken» as the `h1`, the line «Bestillingsforslag for neste uke, uke [46]. Tallene bygger på salget til og med uke [45].», the week path with step 1 current, and the four week figures as plain text (UX-DR9, UX-DR32, UX-DR33)
**And** the week path has two steps; step 3 comes with FR-30 (Epic 6)

**Given** «Slik leser du tillitsmerket»
**When** «Denne uken» renders
**Then** it shows the three labels with their conditions, as in UX-DR9 (the user's decision, 2026-11-18)

**Given** the review sequence
**When** the primary button «Start med [product]» is used
**Then** it opens the first product in «Bestill snart», or in «Uten prognose» when nothing needs ordering soon (UX-DR9)
**And** this story decides and tests what the button does when both groups are empty, and documents the choice where needed: in the story specification, and in EXPERIENCE.md with a row in its change log if the UX changes

**Given** a product in the review sequence
**When** its product screen opens
**Then** the progress bar shows its place, for example «Gå gjennom produktene: produkt [2] av [4] som bør bestilles snart», then «produkt [1] av [1] uten prognose», and it is not shown for «Øvrige produkter» (UX-DR34)
**And** this story decides, and documents in the same way, how many segments the bar shows for a long group

**Given** any product screen
**When** it renders
**Then** the previous and next links («← [Isskrape]», «[Lyspære LED E27 9 W] →») go to the previous and next product in R-12 order across all groups, in a navigation labeled «Forrige og neste produkt» (UX-DR35)

**Given** a company without products, or with nothing to order soon
**When** the overview opens
**Then** «Denne uken» is not shown without products, and with nothing to order soon the «Bestill snart» group is absent and the first week figure is 0 (UX-DR9, UX-DR45)

**Given** the search field «Søk i produktene»
**When** the user types a product number or part of a name and presses Enter
**Then** `/produkter/?sok=` shows only the matching products, in their groups and their order, matching the product number or any part of the name without regard to case (UX-DR19)
**And** the results and the week figures do not change, no other company's product is ever shown, the form goes to `/produkter/?sok=` also from a product screen, and the previous and next links ignore the filter (AD-2, FR-2)

**Given** a search without a match
**When** the list renders
**Then** it shows «Ingen produkter passer søket.» and the link «Vis alle produkter» (UX-DR19)

**Given** `web/static/web/app.js`
**When** scripts are on
**Then** it filters while typing, moves between products with ↑ and ↓, opens one with Enter, and keeps the list's scroll position when a product is selected (AD-11, UX-DR36)
**And** with scripts off, the search form, Tab and Enter still do everything (UX-DR43)

**Given** the list
**When** it renders
**Then** it ends with «↑ ↓ forrige og neste produkt · Enter åpner produktet» in keyboard keys, except on touch screens, where the hint is hidden (UX-DR7, UX-DR36)
**And** Tab follows the order of the page: the header, the settings bar, the list and the product, also in the one-column layout (UX-DR43, NFR-11)

**Given** the texts on «Denne uken» and in the product header
**When** they depend on a count
**Then** the labels of the week figures and the progress text come ready from `explanation/` in singular or plural, and the templates only place them (AD-4)

### Story 2.12: Explain each forecast in plain Norwegian

As a purchasing manager,
I want a short explanation in Norwegian of how each forecast and order quantity came about,
So that I can understand and explain the decision without reading every number.

**Priority:** Must. **Requirements:** FR-26, FR-27, AG-1, AG-2, SM-6; AD-4, AD-5; UX-DR31.

**Acceptance Criteria:**

**Given** a product screen
**When** it renders
**Then** its last panel, «Forklaring», below every calculated number, shows the template explanation in this order: the method and settings; the number of calculation weeks and the week forecasts; the weeks left out and why; every active warning and note; the order calculation; the weeks of cover; the confidence label and its reason; the scenarios (FR-26, FR-27, UX-DR31)
**And** for the demo product «Strøsand 25 kg» the text equals the example in EXPERIENCE.md

**Given** the same calculation result
**When** the explanation is written twice
**Then** the text is the same, and a snapshot test covers each template (FR-26)

**Given** every template explanation
**When** a test takes every number from it
**Then** each number is allowed for that product: a value that `ProductResult` exposes as a display string, or a fixed number named in the active warnings, the notes or the reason (the horizon labels 1, 2 and 3, and the thresholds 3, 8, 12, 100 and 104); any other number fails the test (FR-27, AD-5, SM-6)

**Given** the templates
**When** they are written
**Then** they use named placeholders such as `{base_forecast}`, filled from `ProductResult` through `forecasting/display.py` (AD-5)
**And** they leave out sales figures and the week numbers of calculation weeks, included unusual weeks and level-shift weeks, and name a year only next to a week left out, or a horizon week, that lies in another year than the latest data week (FR-27)

**Given** a product without a forecast
**When** its explanation is written
**Then** it says that there is no forecast and why, with the warning and the confidence label, using only allowed numbers (FR-26, FR-27)
**And** no language model takes part (AG-1, AG-2)

## Epic 3: Change the settings and see every product update at once

Mounia changes the forecasting method, the window, the smoothing factor, the scenario percentage, the safety margin or the handling of unusual weeks from the product screen or the settings page. Every product updates at once, the screen confirms the previous and the new value, and the settings stay after logging out and after a restart.

### Story 3.1: Change the company settings on the settings page

As a purchasing manager,
I want to change the forecasting method and the other settings on one page, with a clear message when a value is not allowed,
So that I can choose how Prognose calculates for all my products.

**Priority:** Must. **Requirements:** FR-2, FR-20, FR-22, NFR-5, NFR-6, NFR-10, NFR-11, SM-5; AD-7, AD-9, AD-10, AD-11; UX-DR7, UX-DR11, UX-DR15 (the button), UX-DR38, UX-DR40; D-4.

**Acceptance Criteria:**

**Given** the settings bar on any page after login
**When** the user selects «Endre innstillinger»
**Then** `/innstillinger/` opens as a page of its own, not a modal, and starts with «Endringen gjelder alle produkter i bedriften.» (UX-DR11, UX-DR15)

**Given** the settings page
**When** it opens
**Then** it has one field per FR-20 setting, each with a visible label and the company's current value: «Prognosemetode» (the radio buttons «Glidende gjennomsnitt» and «Eksponentiell glatting»), «Vindu» (a number field with «uker», 2–12), «Glattingsfaktor» (a number field, 0,1–0,9), «Scenarioprosent» and «Sikkerhetsmargin» (number fields with «%», 0–50 and 0–100) and «Uvanlige uker» (the radio buttons «Tas med» and «Holdes utenfor») (FR-20, UX-DR11)
**And** «Sesongjustering» is added with FR-9 (Epic 5)

**Given** the settings page on an iPad or a phone
**When** it is used by touch from 320 px wide
**Then** every field, radio button and button has a target of at least 44 × 44 px, the number fields use 16 px text, and the page does not scroll sideways (NFR-6, UX-DR7)

**Given** the saved forecasting method
**When** the page renders
**Then** the setting that does not apply is disabled and shown as not in use: the window under exponential smoothing, with «Ikke i bruk med eksponentiell glatting.», and the smoothing factor under the moving average, with «Ikke i bruk med glidende gjennomsnitt.» (FR-20)
**And** a disabled field keeps its saved value

**Given** the settings form with `app.js`
**When** the user chooses the other forecasting method
**Then** the setting that the chosen method uses is enabled at once, before saving, and the setting it does not use is disabled and shown as not in use (AD-11, D-4)
**And** the form accepts the method and that setting in one POST, which a test checks; without the script, a field disabled for the saved method is changed in a second save, and the QA log records a hand check of the script

**Given** a number field
**When** the user enters a decimal comma or a decimal point
**Then** both are accepted, for example 0,3 and 0.3 (NFR-10, AD-9)

**Given** a value outside its range
**When** the form is submitted
**Then** it is refused with the Message Catalogue text, for example «Sikkerhetsmargin må være mellom 0 og 100 %. Den forrige verdien er beholdt.», shown above the field with `role="alert"` and linked to it with `aria-describedby` (FR-20, UX-DR38)
**And** the previous value stays

**Given** an empty or non-numeric value
**When** the form is submitted
**Then** it is refused with «Skriv et tall, for eksempel 10 eller 0,3. Den forrige verdien er beholdt.», and the previous value stays (NFR-10)

**Given** a value with decimals
**When** the form is submitted
**Then** a value whose extra decimals are all zero counts as that number, so 10,0 is 10 and 0,30 is 0,3 (NFR-10, AD-9)
**And** a window or a percentage with a non-zero decimal, or a smoothing factor with a non-zero second decimal, is refused with a Norwegian message that this story writes under the UX copy rules, because the Message Catalogue has none, and the previous value stays (Deferred)

**Given** «Lagre» with valid values
**When** the form is submitted
**Then** the settings are saved for the logged-in company with a POST and a redirect back to the page the user came from, which must be a path inside the app; an address outside the app is ignored, and the product overview opens instead (AD-10, AD-11)
**And** «Avbryt» returns to the same page without changes

**Given** the FR-20 defaults and ranges
**When** the form validates
**Then** it reads them from `forecasting/settings.py`, as the model defaults and `load_seed` do (AD-9)

**Given** saved settings
**When** the user logs out and in again, or the app and the database restart
**Then** the settings are unchanged (FR-22, SM-5)

**Given** test company A
**When** it tries to read or change test company B's settings
**Then** the page and the POST only ever read and change A's settings, and the two-account test covers `/innstillinger/` (FR-2, AD-7)
**And** submitting the form twice, reloading or going back gives the same result without errors (NFR-10)

### Story 3.2: Confirm a settings change with the old and the new value

As a purchasing manager,
I want the screen to confirm each settings change with the affected value before and after,
So that I see what the change did.

**Priority:** Must. **Requirements:** FR-21, FR-25 (changing the settings from the screen), SM-3; AD-2, AD-4, AD-17; E1, E2, E3, E4, E8; UX-DR37.

**Acceptance Criteria:**

**Given** a saved settings change
**When** the user is back on the page they came from
**Then** the confirmation message at the top of the product area says «Innstillingen er endret: [sikkerhetsmargin] er nå [50] %.», followed by one line per affected value, for example «Foreslått bestillingsmengde: 11 → 17», with `role="status"`, and it is shown once (FR-21, UX-DR37)
**And** a value that did not change ends with «(uendret)», for example «Grunnprognose: 14,3 → 14,3 (uendret)»

**Given** the confirmation
**When** it is written
**Then** `describe_settings_change(before, after)` in the core compares the product the user came from before and after the change, and `explanation/` words the lines (AD-2, AD-4)
**And** from a page without a product, only the line naming the new setting is shown

**Given** the FR-21 table
**When** a test changes each setting for the test product it affects
**Then** the affected value changes: the method (E1 → E2, the base forecast), the window (E1 with 4 instead of 3), the smoothing factor (E2 with 0,5 instead of 0,3), the scenario percentage (E3 with 20 %), the safety margin (E4 with 50 %, the suggested order quantity 11 → 17) and unusual weeks (E8, the base forecast 41,0 → 21,3) (FR-21)
**And** the test reads the expected values of these variants from the reference spreadsheet, where Story 1.5 records them as calculated by hand, so that neither the test nor the calculation code holds an expected value (AD-17)

**Given** any settings change
**When** it is saved
**Then** it applies at once to every product of the company, and the results are computed again on the next request and never stored (FR-21, AD-2)
**And** every place where the settings can change says «Endringen gjelder alle produkter i bedriften.» (FR-21)

**Given** a change that removes or gives a forecast, for example a window longer than a product's calculation weeks
**When** the confirmation is written
**Then** «–» stands for the missing value, for example «Grunnprognose: 14,3 → –», and a test covers both directions (FR-21)

**Given** the confirmation message at the top of the product area
**When** a product screen opens after a change on a 1366 × 768 screen
**Then** the suggested order quantity, the confidence label and the active warnings are still visible without scrolling, checked by hand and recorded in the QA log (FR-25)

### Story 3.3: Switch unusual weeks on the product screen

As a purchasing manager,
I want to switch unusual weeks in or out right below the chart,
So that I see in one step how much the unusual weeks matter.

**Priority:** Must. **Requirements:** FR-2, FR-16, FR-21, FR-25, SM-3, NFR-6, NFR-10, NFR-11; AD-7, AD-10, AD-11; E8; UX-DR7, UX-DR25, UX-DR37; D-5.

**Acceptance Criteria:**

**Given** the product screen
**When** it renders
**Then** the unusual-weeks switch stands below the chart legend, after a hairline: a real checkbox with `role="switch"` in a POST form to `/innstillinger/uvanlige-uker/`, with a 40 × 22 px track, the state in bold («Uvanlige uker tas med.»), what switching does («Slå av for å holde dem utenfor.») and «Endringen gjelder alle produkter i bedriften.» (UX-DR25)
**And** the excluded state mirrors this wording

**Given** the switch
**When** it is toggled with the mouse, by touch or with Space
**Then** the company setting changes between «tas med» and «holdes utenfor», the page reloads with the confirmation message, and every product of the company updates (FR-21, UX-DR25)
**And** with scripts off, the small secondary button «Lagre» next to the switch sends the change; `app.js` hides the button and sends the change on toggle (AD-11, D-5)
**And** on touch screens the switch with its text, and the «Lagre» button, each have a target of at least 44 × 44 px, while the track keeps its 40 × 22 px size (NFR-6, UX-DR7)

**Given** the demo product built from E8
**When** unusual weeks are switched off
**Then** the confirmation shows «Grunnprognose: 41,0 → 21,3», the chart still marks the unusual weeks, the warning says «holdt utenfor», and «Prognoseutregning» lists the excluded weeks and the number of weeks used (FR-16, FR-21, UJ-1 step 4, DR-1)
**And** switching back restores the values, and the unusual-weeks warning neither appears nor disappears (FR-16)

**Given** the core flow in SM-3
**When** an automated test logs in through the web application, opens a product, checks the sales history, the forecast calculation and the scenarios, and changes the forecasting method, the safety margin and the unusual-weeks setting
**Then** it sees each affected value change (SM-3)
**And** when this test and SM-1 pass, the Must scope has passed its gate, and Should work may start (DR-6, SM-C2)

**Given** test company A
**When** it uses the switch
**Then** only A's setting changes, and the two-account test covers `/innstillinger/uvanlige-uker/` (FR-2, AD-7)
**And** submitting twice, reloading or going back gives the same result without errors (NFR-10)

## Epic 4: Ready for the examiner

The examiner installs Prognose from the README on macOS or Windows within 15 minutes once the prerequisites are installed, follows «Prøv selv», compares the results with the reference spreadsheet and traces every FR to its stories and tests. The final commit passes every check.

### Story 4.1: Set up and try Prognose from the README

As an examiner,
I want a README that takes me from a fresh clone to a logged-in test company and then through «Prøv selv»,
So that I can install and check Prognose on my own computer within 15 minutes once the prerequisites are installed.

**Priority:** Must. **Requirements:** DR-1, DR-2, DR-4, DR-7, DR-9, DR-10, SM-2, NFR-1, NFR-2, NFR-3, NFR-6; D-1, D-3; the examiner guidelines, criterion 1 («Arbeidsflyt»), criterion 2 («Funksjonalitet og omfang») and criterion 6 («README og kjørbarhet»); the Product Brief and the teacher's feedback on it; the teacher's clarification on Canvas of 2026-11-19 (D-1); the `issues.md` points on the README sequence and the link to the QA log. It runs right after Epic 3, before any Should work.

**Acceptance Criteria:**

**Given** the README
**When** the examiner opens it
**Then** right under the title it says how to start Prognose locally, with the commands from the clone to a logged-in test company or a link to them, gives a link to the test companies' login details, and notes that version 1 is not published, with the reason (DR-1, DR-10, D-1)
**And** it says what Prognose does and for whom, with screenshots of at least the login page, the product overview and the product screen (DR-1)
**And** a screen recording of UJ-1 steps 1 to 4, at most 2 minutes long, is optional

**Given** the scope of Prognose
**When** the examiner compares the app with the proposal and the chosen task (the examiner guidelines, criterion 2, «Funksjonalitet og omfang»)
**Then** the README explains that Prognose covers only module 4.1 «Prognoser og Demand Management» of the proposal «KI-støttet MRP II», and that bills of materials, production planning, the other MRP II modules and supplier integrations are out of scope, with a link to the Product Brief (`brief.md`, §1 and §8) (DR-1)
**And** it gives the reason with a link to the teacher's feedback on the brief (`tilbakemelding-product-brief.md`, 2026-10-06), which calls the narrowing wise («Avgrensningen er klok») and says that it makes a difficult proposal feasible for one person
**And** it uses the feedback's own words and calls it the teacher's assessment, not an approval; it claims an approval from the teacher only where it can link to a document that states one

**Given** the prerequisites section
**When** it is read
**Then** it names the programs to install, Git, uv and Docker Desktop, with the minimum version and the tested version of uv and Docker Desktop, and says that uv installs Python 3.13 and Docker Compose runs PostgreSQL 18.7, so neither needs an installation of its own; and it names the supported platforms: macOS on Apple silicon or Intel, and Windows 10 22H2 or Windows 11 23H2 on x64; Windows on ARM is not supported (DR-1)
**And** for Windows it names WSL 2 and hardware virtualization, which Docker Desktop needs, with the fix when Docker Desktop does not start

**Given** the setup section
**When** it is followed
**Then** it says how to install each program, with a link to its official installation guide, and then gives the exact commands from the clone to a logged-in test company, the same in macOS Terminal and Windows PowerShell, how to start and stop the local database, how the session secret is created, and the fixes for a database that is not started and for a port that is in use (DR-1, NFR-3)

**Given** the section «Nøkler og hemmeligheter»
**When** the examiner reads it before the setup
**Then** it says that Prognose needs no API key, paid service or third-party account, and that every variable in `.env.example` is optional (NFR-1, SM-2)
**And** it says that `load_seed` creates the session secret in `.secret_key`, which Git ignores and nobody edits, that the local database has no password and listens only on `127.0.0.1`, and that the optional local language model needs no key (NFR-3, FR-28)

**Given** the expected setup time
**When** the examiner plans the installation
**Then** the README says, before the setup section, how long installing the prerequisites takes, with Docker Desktop's download size and, on Windows, WSL 2 and a possible restart, as measured in Story 1.3, or that this time was not measured (SM-2, D-3)
**And** it says that the first start downloads the PostgreSQL image once and needs a network, and that the time from the clone to a logged-in test company is at most 15 minutes once the prerequisites are installed, with the measured time (SM-2, NFR-1)

**Given** the test companies
**When** the examiner wants to log in
**Then** the README gives both customer numbers and passwords, how to generate and load the data, and how an explicit reset restores the seed state and also resets the settings and adjustments (DR-1, DR-4)

**Given** «Prøv selv»
**When** the examiner follows it
**Then** it has 5 to 10 steps that follow UJ-1, with the E8 product for UJ-1 step 4, so that switching unusual weeks changes the base forecast from 41,0 to 21,3 (DR-1); its first step checks the settings bar against the defaults and sets them back on Innstillinger if they differ, because an earlier session may have changed them (DR-4)
**And** a table lists the test products with the rule, warning or confidence label that each one shows and its reference example

**Given** the sections on tests and folders
**When** they are read
**Then** they give the test commands, `uv run pytest` with the result to expect and the Ruff checks `uv run ruff check` and `uv run ruff format --check` that CI also runs, and explain every top-level folder, including the BMAD and Claude Code folders (DR-1, DR-2, NFR-2)
**And** they link to the PRD, the architecture spine, this document, the decision logs, the AI steering log, the QA log and the status table, and the root holds no loose files other than the README, a license and configuration files

**Given** the section on tested screens and browsers
**When** it is read
**Then** it lists the screen sizes, devices and browsers that were actually tested, taken from the QA log: the desktop browsers, at least one per operating system; the real iPhone 13 with Safari over the local network; and the iPad and Android sizes and 320 px in the browser's responsive view (NFR-6, DR-1)
**And** each entry says whether it was a real device or the responsive view, and nothing is listed that was not tested
**And** it describes the phone test over the local network as an optional step for a private network, with `PROGNOSE_LAN_HOST` and the start command, and says that the app is stopped after the test (AD-13)

**Given** the project's list of defects and open points
**When** the examiner looks for issues, as the examiner guidelines say (criterion 1 and step 6)
**Then** the README links clearly to `.logs/<bruker>/issues.md` as the project's issue list and explains how it is used: each defect or open point gets a dated line with a link to the session log it came from; a pull request that solves a point names it; a solved point is marked `[x]` with the date and the fix; and lines are never deleted (DR-7)
**And** the README says that defects in AI-generated code or text are also recorded in the QA log, and that GitHub Issues is not used because the examiner guidelines accept issues or an equivalent (DR-9)

**Given** the limitations
**When** they are read
**Then** the README states the trend lag (FR-7), the assumptions behind the suggested order quantity (R-8) and the project-defined rules, and the limitations of R-14 once FR-9 is built (DR-1)
**And** the section on the optional language model comes with FR-28, and the list of Should items not built with Story 4.4

**Given** a fresh clone with the prerequisites installed
**When** a group member follows only the README on macOS, and on Windows where D-3 allows it
**Then** a test company is logged in within 15 minutes, and the README states the measured setup time (SM-2)
**And** the QA log records each run with the date, the operating system, the uv and Docker Desktop versions and the time taken (DR-9)

### Story 4.2: Check the confidence label with real readers and review the finished design

As a purchasing manager,
I want the confidence label tried on people outside the group and the screens reviewed against the approved design,
So that the label is understood and the screens work as designed while there is still time to fix them.

**Priority:** Must. **Requirements:** SM-10, FR-19, FR-25, NFR-4, NFR-6, NFR-7, NFR-11, DR-9; UX-DR7, UX-DR45; the `issues.md` points on the Impeccable finish review and the `docs/DESIGN.md` link. It runs right after Epic 3, before any Should work.

**Acceptance Criteria:**

**Given** a test product labeled «lav», such as «Snøskuffe aluminium»
**When** two people outside the group see its product screen and explain in their own words, without reading the reason aloud, why it has that label
**Then** the check passes when both name the deciding condition (R-16, SM-10)
**And** the QA log records the date and the result, without the people's names (NFR-4, DR-9)

**Given** a failed SM-10 check
**When** the group revises the reason texts
**Then** the Message Catalogue gets the new texts with a row in the UX change log, `explanation/` follows them, and the check is repeated (SM-10)

**Given** the built screens
**When** the Impeccable finish review runs against the approved design in `docs/DESIGN.md`
**Then** every material finding is fixed in this story or recorded with its reason in the QA log
**And** because the mockup shows only the desktop layout, the review also checks 390 × 844 and 820 × 1180 against the narrow and touch rules in the spines (UX-DR7)
**And** no Impeccable command writes `DESIGN.md` through the link without the user's approval and a row in the UX change log

**Given** the manual checklist
**When** it runs on the Must build
**Then** it covers NFR-6 at the UX-DR7 test sizes (no horizontal page scrolling and nothing cut off from 320 px, the one-column order, the touch targets and the field text, the chart labels, and the 1366 × 768 fold), NFR-7 (markers that differ by shape), NFR-11 (keyboard only, visible focus, labels, contrast, `lang="nb"` and the chart's text alternative) and every state in UX-DR45 (DR-9)
**And** the QA log records the date, the operating system, the browser, the screen size, whether the test ran on a real device or in the responsive view, and the result, and each defect is fixed or recorded

### Story 4.3: Make the process traceable for the examiner

As an examiner,
I want the decisions, the use of AI and the status of every requirement documented and linked,
So that I can trace how Prognose was planned and built.

**Priority:** Must. **Requirements:** DR-5, DR-7, DR-8, AG-6, SM-8, NFR-4; PRD §10 question 3; addendum §7; D-2; the `issues.md` points on the Product Brief and the textbook sources. It runs right after Epic 3, before any Should work; later stories keep these documents current, and Story 4.4 checks their final state.

**Acceptance Criteria:**

**Given** the AI steering log `docs/ki-styringslogg.md`
**When** it is reviewed
**Then** it holds at least five cases, at least one for each epic that was implemented, each with what the AI proposed, what was wrong, what the group decided, and the commit or pull request (DR-5, SM-8, D-2)

**Given** the status table `docs/statustabell.md`
**When** it is reviewed
**Then** every FR, and DR-10, has its priority, its status (built, partly built, not built or changed), its stories and tests, and the reason for any deviation, and an epic that was not built is marked as not built (DR-8, D-2)
**And** the README links it

**Given** the trace from requirement to code
**When** the group checks the stories, the tests and the commits
**Then** every story names its FR-n, every test names its FR-n or E-n, or its NFR-n, DR-n or AD-n when it verifies no FR (D-10), every commit names its story, and every story was merged through a pull request with its BMAD Code Review comment: the findings, the decisions and the fixes with their commits (DR-5, DR-7, SM-8, D-8)

**Given** the Product Brief
**When** this story is done
**Then** it holds the changes listed in addendum §7, so that the repository history shows how the plan developed (DR-5)

**Given** the inventory rules
**When** the sources are checked
**Then** textbook sources for the order-up-to policy and the percentage safety margin are added if they are found, and otherwise the process documentation states the gap (PRD §10 question 3)

**Given** the decision logs, the session logs and the saved AI sessions
**When** they are reviewed
**Then** they show how BMAD and Claude Code were used, they are linked from the README, and they hold no personal data or local paths (AG-6, DR-5, NFR-4)
**And** every implemented story has its exported sessions in `.logs/<bruker>/sessions/`, linked from its pull request and its session log, as the routine for AI sessions requires (DR-5)
**And** every change made after approval to the PRD, the architecture spine, the UX spines and this document is in their change logs (DR-5)

### Story 4.4: Check the final commit before submission

As an examiner,
I want the submitted commit checked from end to end,
So that what I receive works as documented.

**Priority:** Must. **Requirements:** DR-1, DR-2, DR-7, DR-8, DR-9, NFR-4, NFR-6, NFR-7, NFR-8, NFR-11, SM-2; D-2, D-3; UX-DR7. It comes last in the sprint plan, on the final commit, after every story that is actually implemented.

**Acceptance Criteria:**

**Given** the final commit
**When** the manual test checklist runs
**Then** it covers NFR-6, NFR-7, NFR-8, NFR-11 and SM-2 with the offline start, and the QA log records each result with the date, the operating system, the browser and the result (DR-9)
**And** NFR-6 runs at the UX-DR7 test sizes: on the real iPhone 13 in Safari over the local network (AD-13), and in the browser's responsive view for the iPad and Android sizes and 320 px; the QA log records the two kinds of test apart, with the device or the size

**Given** a fresh clone of the final commit
**When** a group member follows only the README on macOS, and on Windows where D-3 allows it
**Then** a test company is logged in within 15 minutes, Prognose also starts with the network switched off after installation, and the setup time in the README matches (SM-2, D-3)

**Given** the whole Git history
**When** the group scans it for secrets, personal data and local paths
**Then** the QA log records the result (NFR-4)

**Given** Docker Desktop's terms
**When** they are checked again
**Then** Docker Desktop is still free for personal use and education, and the QA log records the check (Deferred in the spine)

**Given** the status table and the README
**When** they are final
**Then** every FR has its status at submission, every Should item that was not built is listed with its reason in both, and every epic that was not built is marked as not built (DR-1, DR-8, D-2)
**And** the AI steering log has at least one case for each epic that was implemented (DR-5, D-2)

**Given** the final commit
**When** the checks run
**Then** `uv run pytest`, `uv run ruff check` and `uv run ruff format --check` pass locally and in CI (DR-2, DR-7)

## Epic 5: Seasonal products and clearer warnings

Mounia can switch on seasonal adjustment so that the week forecasts follow the season. A product with a seasonal pattern that the forecast does not use, or with a level shift, gets its own warning text.

### Story 5.1: Adjust the forecast for the season

As a purchasing manager,
I want to switch on seasonal adjustment for my company and see week forecasts that follow the season,
So that a seasonal product is not ordered as if every week were the same.

**Priority:** Should (PRD §8.2, item 1). **Requirements:** FR-9, FR-20 (the setting), FR-21 (the E14 row), FR-26 and FR-27 (the note in the explanation), FR-35 (the seasonal values); R-9, R-14, R-15 (the note); AD-2, AD-3, AD-9, AD-15, AD-17; E14, E25, E26, E27; UX-DR11, UX-DR15, UX-DR28, UX-DR42. It starts only after the Must scope has passed SM-1 and SM-3 and Stories 4.1 to 4.3 are done. R-14 steps 1 and 2 live in one place in the core and are shared with FR-36 (Story 5.2). If the story proves too large during implementation, it is split into the calculation and the screen (the user's decision, 2026-11-18).

**Acceptance Criteria:**

**Given** the company settings
**When** this story adds «Sesongjustering»
**Then** it is a new field on `CompanySettings`, off by default, with its default defined in `forecasting/settings.py` (FR-9, FR-20, AD-9)
**And** its migration only adds a field, so that `migrate` keeps the data already in the database (AD-15)

**Given** seasonal adjustment on and a product where R-14 can be used
**When** the core calculates
**Then** each week number's index is the mean of its calculation weeks' sales divided by the mean of all week-number means, kept at full precision; each calculation week's sales are divided by its index, the base forecast is calculated on these adjusted values with the chosen method, and each horizon week's forecast is the base forecast × the index of its week number (R-14 steps 1 to 3)
**And** E14 matches

**Given** these week forecasts
**When** the scenarios, the suggested order quantity and the weeks of cover are calculated
**Then** they use the seasonally adjusted week forecasts, so E27 gives a suggested order quantity of 8, not 18 (FR-9, R-7, R-8, R-12)

**Given** a week number without a calculation week, or a week-number mean of 0
**When** the core calculates
**Then** the product gets its week forecasts without seasonal adjustment and the note «Sesongjustering kunne ikke brukes for dette produktet, så ukeprognosene er regnet uten.», shown in «Ukeprognoser og scenarioer» where the FR-7 note stands (FR-9, R-14 step 4, R-15)
**And** E25 and E26 match

**Given** the cycle length
**When** the tests run
**Then** it is a parameter of the calculation, 52 in the app, so that E14 and E25 to E27 run with a 4-week cycle (FR-9)
**And** a week 53 uses the index of week 52 `[ASSUMPTION]` (R-14)

**Given** seasonal adjustment on
**When** a product screen opens
**Then** the week forecasts differ, the FR-7 note is gone, and «Prognoseutregning» shows the seasonal indices with four decimals and the adjusted values with one decimal for the weeks used and for weeks 1 to 3, with the week forecasts and «Tallene er avrundet for visning.» below the seasonal values (FR-35, R-9, UX-DR28, UX-DR42)

**Given** Innstillinger and the settings bar
**When** they render
**Then** «Sesongjustering» is a checkbox on Innstillinger, and the settings bar shows its state (UX-DR11, UX-DR15)
**And** switching it on for the seasonal test product confirms the week forecasts going from flat to seasonal (the E14 row of FR-21), with the expected values read from the reference spreadsheet (FR-21, AD-17)

**Given** seasonal adjustment off
**When** the tests run
**Then** the seasonal test product's week forecasts stay flat, and the FR-7 note is shown (FR-9)

**Given** the seasonal test product
**When** seasonal adjustment is on
**Then** its seasonal indices and week forecasts equal the expected values that this story adds to the reference spreadsheet, calculated by hand (PRD §10 question 4, AD-17)

**Given** the template explanation
**When** seasonal adjustment could not be used for a product
**Then** the explanation includes the note and uses only allowed numbers, so it never shows a seasonal index, while «Prognoseutregning» does; a snapshot covers the case (FR-26, FR-27, FR-35)
**And** the README states the limitations of R-14 in PRD §5.5 (FR-9, DR-1)

### Story 5.2: Warn about an unused seasonal pattern and a level shift

As a purchasing manager,
I want a warning when a product has a clear seasonal pattern that the forecast ignores, and a plain warning when demand seems to have moved to a new level,
So that I know when to trust the forecast less.

**Priority:** Should (PRD §8.2, item 2). **Requirements:** FR-36, FR-17b, FR-17, FR-19, FR-25, FR-26, FR-27; R-15 (item 6), R-16, R-17; SM-1 (E30), SM-7; AD-4, AD-17; E30; UX-DR24, UX-DR40. It does not depend on Story 5.1: if 5.1 is built, it reuses R-14 steps 1 and 2; if 5.1 is cut, it builds those two steps itself, without the setting, the adjusted forecast or any screen change of FR-9 (the user's decision, 2026-11-18).

**Acceptance Criteria:**

**Given** that Story 5.1 is cut
**When** this story is built
**Then** the core gets R-14 steps 1 and 2 only: the mean of each week number's calculation weeks and the indices, with the cycle length as a parameter and the check that every week number has a calculation week and that no mean is 0 (R-14, R-17)
**And** no «Sesongjustering» setting, adjusted forecast or seasonal values on the screen are built, so seasonal adjustment counts as not used for every product

**Given** a product where R-14 steps 1 and 2 can be calculated
**When** any of its seasonal indices is 1.3 or more, or 0.7 or less `[ASSUMPTION]`
**Then** the product has a seasonal pattern (R-17)

**Given** a seasonal pattern while seasonal adjustment is off, or not used for the product
**When** the trust panel renders
**Then** it shows the active warning «Produktet har tydelig sesongvariasjon som prognosen ikke tar hensyn til.» in R-15 order, with the ring «!» on amber-tint (FR-36, R-15, UX-DR24)
**And** the warning counts for the confidence label, so the label is at most «middels» (R-16)

**Given** E30
**When** the test runs it with seasonal adjustment off and then on
**Then** the warning appears when it is off and not when it is on, as in the reference spreadsheet (FR-36, AD-17)
**And** the part with seasonal adjustment on runs once FR-9 is built

**Given** a product with at least one level-shift week in the recent period
**When** the trust panel renders
**Then** it shows «Etterspørselen ser ut til å ha endret nivå.» with the diamond icon on amber-tint, and no other product shows it (FR-17b, UX-DR24)
**And** the warning does not change the confidence label, whose reason still names «nytt nivå de siste 12 ukene» (FR-17, FR-17b)

**Given** both warnings
**When** their texts are written
**Then** they come from `explanation/`, with the Message Catalogue as the source, and the template explanation includes them with only allowed numbers; snapshots cover both (AD-4, FR-26, FR-27)

**Given** the seed data
**When** the core runs for every product
**Then** the seasonal test product triggers the FR-36 warning with seasonal adjustment off, and the level-shift test product triggers the FR-17b warning, so SM-7 also covers these two warnings (SM-7)
**And** R-17 behaves as expected on the seasonal test product, as PRD §10 question 4 asks

## Epic 6: Plan the order for the Monday meeting

Mounia sees the order quantity per scenario and the overstock note, adjusts a suggested quantity when she knows better, and takes one combined order overview to the meeting.

### Story 6.1: Show the order quantity per scenario and the overstock note

As a purchasing manager,
I want the order quantity for the optimistic and the pessimistic scenario, and a note when the stock already covers next week,
So that I see how much the scenarios would change my order, and why some products need none.

**Priority:** Should (PRD §8.2, item 3). **Requirements:** FR-13, FR-14, FR-26, FR-27; R-8, R-12, R-15 (the note); AD-2, AD-4, AD-17; E22, E23; UX-DR18, UX-DR22, UX-DR28, UX-DR40; D-6. It follows the Should items before it in PRD §8.2, whether they were built or cut.

**Acceptance Criteria:**

**Given** a product with a forecast
**When** the order quantities per scenario are calculated
**Then** each one uses R-8, with the safety margin and the scenario's week-1 value in place of the week-1 normal forecast (FR-13, R-8)
**And** E22 gives 13 for the optimistic and 10 for the pessimistic scenario, read from the reference spreadsheet (AD-17)

**Given** «Ukeprognoser og scenarioer»
**When** it renders
**Then** the scenario table has a «Bestillingsmengde» column, with the normal quantity in blue, followed by «Bestillingsmengden per scenario er regnet ut fra uke 1, med sikkerhetsmargin.» (FR-13, UX-DR28)

**Given** a suggested order quantity of 0 and a stock on hand above 0
**When** the product overview and the product screen render
**Then** the product's row in the list, and the decision panel below the suggested order quantity, show «Lagerbeholdningen dekker forventet behov neste uke.» (FR-14, UX-DR18, UX-DR22, D-6)
**And** when both the week-1 normal forecast and the stock on hand are 0, no overstock note is shown (E23)

**Given** the note and the new texts
**When** they are written
**Then** they come from `explanation/`, with the Message Catalogue as the source (AD-4)
**And** the template explanation includes the overstock note but leaves out the order quantities per scenario, which are not allowed numbers in FR-27; snapshots cover both cases (FR-26, FR-27)

### Story 6.2: Adjust a suggested order quantity

As a purchasing manager,
I want to replace a suggested order quantity with my own, and go back to the suggestion when I want,
So that I can use what I know and Prognose does not.

**Priority:** Should (PRD §8.2, item 4). **Requirements:** FR-29, FR-2, NFR-10, NFR-11; AD-2, AD-7, AD-10, AD-11; UX-DR17, UX-DR23, UX-DR38, UX-DR45. It follows the Should items before it in PRD §8.2, whether they were built or cut.

**Acceptance Criteria:**

**Given** the decision panel of a product with a forecast
**When** it renders
**Then** it has the primary button «Behold [11] og gå videre», which keeps the suggestion and opens the next product in the review sequence, or the next product in R-12 order for a product outside it; and the secondary button «Juster mengden», which opens a whole-number field labeled «Justert bestillingsmengde», with «Lagre» and «Tilbake til forslaget» (UX-DR23, NFR-11)
**And** for a product without a forecast, «Sett mengden selv» opens the same field

**Given** a whole number of 0 or more
**When** the user saves it
**Then** a POST to `/produkter/<varenummer>/mengde/` stores it and redirects, the suggestion stays visible next to the adjusted quantity, and the decision panel and the product's card or row show «Justert av deg» (FR-29, AD-10, UX-DR17)
**And** a suggested quantity of 70 changed to 80 is marked «Justert av deg», as in FR-29

**Given** a negative number, a number with a non-zero decimal, an empty field or text
**When** the user saves it
**Then** it is refused with «Skriv et helt tall fra 0 og oppover.» at the field, with `role="alert"`, and the previous quantity stays (FR-29, UX-DR38)
**And** a number whose decimals are all zero, such as 80,0, counts as that whole number (NFR-10)

**Given** an adjusted quantity
**When** the user chooses «Tilbake til forslaget»
**Then** the adjustment is removed, and the suggestion and «Foreslått» return (FR-29)

**Given** the storage of adjusted quantities
**When** a quantity is saved
**Then** it lives in the server-side session, keyed by product number and latest data week, is reached only through `web/adjustments.py`, and enters the core as the adjustments input of `build_overview` (AD-2, AD-10)
**And** it lasts for the session only, because FR-31 is Could, and it applies only to the latest data week it was made for

**Given** adjusted quantities
**When** the list and «Denne uken» render
**Then** the order of the products, the group summaries and the week figures stay based on the suggested order quantities (R-12, UX-DR33)
**And** an adjusted quantity never changes a forecast, a scenario, a warning, the confidence label or the suggested order quantity; it enters `build_overview` only for the marking and the combined order overview, and a test checks that the R-12 order and every result stay the same after an adjustment (AD-2, R-12)

**Given** the last product in the review sequence, or the last product in R-12 order
**When** its decision panel renders
**Then** the primary button becomes «Tilbake til produktoversikten», and «Gå til samlet bestillingsoversikt» once FR-30 is built (UX-DR23, UX-DR45)

**Given** test company A
**When** it tries to set or reset a quantity for one of test company B's products
**Then** it gets the not-found page and nothing changes, and the two-account test covers the route (FR-2, AD-7)
**And** submitting twice, reloading or going back gives the same result without errors (NFR-10)

### Story 6.3: Take one combined order overview to the meeting

As a purchasing manager,
I want one list of every product with the quantity I will order, marked as suggested or adjusted,
So that I can take the week's orders to the purchasing meeting.

**Priority:** Should (PRD §8.2, item 5). **Requirements:** FR-30, FR-2, FR-29 (the adjusted quantities); R-12; AD-2, AD-7, AD-11; UX-DR12, UX-DR14, UX-DR23, UX-DR32, UX-DR39. It follows the Should items before it in PRD §8.2, whether they were built or cut; without Story 6.2, every product shows its suggestion.

**Acceptance Criteria:**

**Given** the app header
**When** a page after login renders
**Then** it has the link «Samlet bestillingsoversikt» to `/bestillingsoversikt/`, marked as the current page there (UX-DR14)

**Given** `/bestillingsoversikt/`
**When** it opens
**Then** it shows the page title «Samlet bestillingsoversikt», the line «Bestillingene for neste uke, uke [46]. Prognose bestiller ingenting: ta listen med til innkjøpsmøtet.», the week path with steps 1 and 2 done and step 3 current, and «Tilbake til produktoversikten» (UX-DR12, UX-DR32)

**Given** the combined order table
**When** it renders
**Then** every product of the company appears in R-12 order with «Varenr.», «Produkt», «Bestillingsmengde» and «Merking»: a suggested quantity marked «Foreslått», and a product without a forecast and without an adjusted quantity with «–» and «Uten prognose» in red; each product name links to its product screen (FR-30, UX-DR39)
**And** when FR-29 is built, an adjusted quantity is shown in blue with the suggestion in brackets («13 (foreslått 11)») and the tag «Justert av deg», also for a product without a forecast whose quantity the user has set

**Given** the total row
**When** the table renders
**Then** «Totalt» in bold sums the quantities in the table, with «–» counted as nothing, and `build_overview` computes the rows and the total, not the template (AD-2)

**Given** «Denne uken» and the review sequence
**When** they render
**Then** step 3 of the week path opens the combined order overview (UX-DR32)
**And** when FR-29 is built, the primary button on the last product reviewed becomes «Gå til samlet bestillingsoversikt»; without FR-29 the decision panel has no buttons, and the header link and step 3 lead there (UX-DR23)

**Given** test company A
**When** it opens the combined order overview
**Then** the list holds only A's products, and the two-account test covers `/bestillingsoversikt/` (FR-2, AD-7)
**And** the page has no action that places or sends an order (PRD §7)

## Epic 7: Optional local language model

A group member can switch on a local language model that rephrases the explanation, under the FR-28 checks. Prognose works fully without it.

### Story 7.1: Rephrase the explanation with an optional local language model

As a purchasing manager,
I want the explanation to read more naturally when a local language model is switched on, with no risk to the numbers,
So that the text is easier to read while every number still comes from Prognose.

**Priority:** Should (PRD §8.2, item 6, the last). **Requirements:** FR-28, FR-27, AG-1, AG-3, AG-4, AG-5, SM-6, NFR-1, NFR-8, DR-1; AD-5, AD-13, AD-17; PRD §10 question 5; UX-DR31; the `issues.md` point on the model and its license. It can be implemented on its own, after the Should items before it, whether they were built or cut. The runtime and the model are decided at the start of the story (Deferred in the spine), and the timeout's fit with NFR-8 is decided in D-7; if that exception turns out not to fit the PRD or the teacher's requirements, the story is postponed rather than the architecture made more complex (the user's decision, 2026-11-18).

**Acceptance Criteria:**

**Given** the start of the story
**When** the group chooses the runtime and the model
**Then** the story specification and the README record the choice, the model's license obligations, and its download size and expected download time (PRD §10 question 5, FR-28, DR-1)

**Given** NFR-8
**When** the model is off, which is the default and the basic setup
**Then** every page meets NFR-8's 2 seconds, and the NFR-8 check in the QA log runs with the model off (NFR-8, D-7)
**And** with the model switched on locally, a product screen may wait up to the 10-second timeout before it shows the rephrased text or the template text; the README states this exception, and no caching or background loading is added (AD-2, AD-10, D-7)

**Given** the default configuration
**When** Prognose starts
**Then** the feature is off; it is switched on only in the local `.env` with `PROGNOSE_LLM_URL` and `PROGNOSE_LLM_MODEL`, which `.env.example` now lists as optional (FR-28, AD-13)
**And** it is not a company setting, needs no API key, paid service or internet connection, and sends no data to any external service (FR-28, AG-5)

**Given** the template explanation
**When** it is sent to the model
**Then** every number is replaced by a named placeholder, such as `{base_forecast}`, and the application itself inserts every number into the returned text (FR-28, AD-5, AG-1)

**Given** a returned text
**When** the pure checks in `explanation/` run
**Then** the text is rejected if its placeholders differ from the template's in name, count or order, if the Norwegian §3 label nearest before a placeholder differs from the template's, or if it contains a number outside a placeholder (FR-28)
**And** a test sends a prepared answer with each fault and checks that the template explanation is shown (SM-6)

**Given** that the model server is not running, the model is missing, no answer arrives within 10 seconds `[ASSUMPTION]`, the response contains an error (also inside a 200 response), or the text is rejected
**When** a product screen opens
**Then** the template explanation is shown, without an error message, and tests with a fake model cover each case (FR-28, AG-3)

**Given** an accepted rephrased text
**When** the explanation panel renders
**Then** «KI-omformulert forklaring» stands above the text, which stays in its own panel below the calculated numbers (FR-27, AG-4, UX-DR31)

**Given** `web/rephrase.py`
**When** the code is reviewed
**Then** it is the only network call in the application, uses the standard library and the 10-second timeout, and is off unless the local `.env` names a model URL (AD-5, AD-13)

**Given** the README
**When** this story is done
**Then** it describes the model as a separate, optional step: which model, its download size and expected time, its license obligations, how to switch it on, and that Prognose works fully without it (FR-28, DR-1)
**And** the model is never part of the basic setup, and `uv run pytest` and CI run without a model, a network or a key (SM-2, AD-17, NFR-1)

## Epic 8: Extras if time allows

Small additions to the weekly routine: settings per product, saved and approved adjustments, CSV export, a note when the stock will not last through weeks 2 and 3, and forecast accuracy.

Each story states its FR and what the architecture and the UX already fix. Its full testable consequences are written, approved by the user and added to the story, with a row in this document's change log, before the story starts (PRD §4).

### Story 8.1: Give one product its own settings

As a purchasing manager,
I want a product to have its own settings that override the company settings,
So that one unusual product does not force a setting on all the others.

**Priority:** Could (PRD §8.3). **Requirements:** FR-23, FR-20, FR-21; AD-9, which needs an amendment.

**Acceptance Criteria:**

**Given** a product with its own settings
**When** it is calculated
**Then** its own settings override the company settings for that product only, and every other product keeps the company settings (FR-23)

**Given** the architecture and the UX
**When** this story is planned
**Then** AD-9, which defines one `CompanySettings` row per company, is amended first, with a row in the spine's change log (AD-9)
**And** EXPERIENCE.md gets the screens for per-product settings, including what replaces «Endringen gjelder alle produkter i bedriften.» for such a product, with a row in its change log (FR-21)

**Given** the planning of this story
**When** it is about to start
**Then** its testable consequences are written, approved by the user and added to this story, with a row in this document's change log (PRD §4)

### Story 8.2: Keep adjusted quantities between sessions and mark products as approved

As a purchasing manager,
I want my adjusted quantities to stay between sessions, and to mark a product as approved,
So that I can spread the weekly review over more than one session.

**Priority:** Could (PRD §8.3). **Requirements:** FR-31, FR-29, FR-2, DR-4; AD-7, AD-10, AD-15. It needs Story 6.2 (FR-29); without it, this story is not built.

**Acceptance Criteria:**

**Given** an adjusted quantity
**When** the user logs out and in again, or the app restarts
**Then** the adjusted quantity is still there (FR-31)

**Given** a product
**When** the user marks it as approved
**Then** the mark is saved and shown on the product, and it can be removed again (FR-31)

**Given** the storage
**When** this story is built
**Then** it replaces only the storage behind `web/adjustments.py`, so the views and the input to the core stay the same, and the new table comes with a migration that only adds (AD-10, AD-15)
**And** the two-account test covers the saved adjustments and approvals, and an explicit reset deletes them with the company's other data (FR-2, DR-4, AD-15)

**Given** the planning of this story
**When** it is about to start
**Then** its testable consequences are written, approved by the user and added to this story, with a row in this document's change log (PRD §4)

### Story 8.3: Export the combined order overview as CSV

As a purchasing manager,
I want to download the combined order overview as a CSV file,
So that I can bring the week's orders into a spreadsheet.

**Priority:** Could (PRD §8.3). **Requirements:** FR-32, FR-30, FR-2, NFR-5; AD-2, AD-7, AD-10, AD-11. It needs Story 6.3 (FR-30); without it, this story is not built.

**Acceptance Criteria:**

**Given** the combined order overview
**When** the user exports it
**Then** a CSV file holds the same rows in the same order, with the same quantities and markings as the page (FR-32)
**And** the story decides the separator and the encoding so that Norwegian letters survive when the file is opened in a spreadsheet, and records the choice

**Given** the export
**When** it is planned
**Then** its address is added to the URL map in AD-11 as a GET request, with a row in the spine's change log (AD-10, AD-11)
**And** the file holds only the logged-in company's products, the two-account test covers the address, and nothing is sent anywhere (FR-2, AD-7, PRD §7)

**Given** the planning of this story
**When** it is about to start
**Then** its testable consequences are written, approved by the user and added to this story, with a row in this document's change log (PRD §4)

### Story 8.4: Note when the stock will not last through weeks 2 and 3

As a purchasing manager,
I want a note when the stock and my order will not cover weeks 2 and 3,
So that I remember to order more soon.

**Priority:** Could (PRD §8.3). **Requirements:** FR-33, FR-26, FR-27; R-15 (the note); AD-4, AD-17. The teacher asked for its testable consequences before it is planned (the teacher's feedback, 4.4).

**Acceptance Criteria:**

**Given** a product with a forecast
**When** the stock on hand plus the suggested order quantity is less than the sum of the week forecasts for weeks 1 to 3
**Then** the product screen shows the note «Lageret og bestillingen dekker ikke uke 2 og 3.» (FR-33)
**And** it is a note, not a warning, so it does not change the confidence label (R-15)

**Given** the reference spreadsheet
**When** the tests run
**Then** they read hand-calculated cases just below, at and above the limit from the spreadsheet (AD-17)

**Given** the template explanation
**When** the note applies
**Then** the explanation includes it with only allowed numbers, so it does not state the sum of the week forecasts (FR-26, FR-27)
**And** the note's place on the product screen is added to EXPERIENCE.md, with a row in its change log, when the story is planned

**Given** the planning of this story
**When** it is about to start
**Then** its testable consequences are written, approved by the user and added to this story, with a row in this document's change log (PRD §4)

### Story 8.5: Show the forecast accuracy

As a purchasing manager,
I want to see how far past one-week forecasts were from the actual sales,
So that I can judge how well the method fits a product.

**Priority:** Could (PRD §8.3). **Requirements:** FR-34, FR-27; AD-1, AD-2, AD-3, AD-17.

**Acceptance Criteria:**

**Given** a product's sales history
**When** the accuracy is calculated
**Then** the product screen shows the mean absolute error (MAE) of past one-week forecasts, and MAPE is not used, because weeks with zero sales make it undefined (FR-34)

**Given** the calculation
**When** it is built
**Then** it lives in the pure core, uses the same rules for which weeks count, and is checked against hand-calculated cases in the reference spreadsheet (AD-1, AD-2, AD-17)
**And** which past forecasts it covers (how many weeks back, with which settings, and how stockout weeks are handled) is decided when the story is planned

**Given** the template explanation
**When** the accuracy is shown
**Then** the explanation leaves the MAE out, because FR-27 does not allow it, unless FR-27 is changed first (FR-27)

**Given** the planning of this story
**When** it is about to start
**Then** its testable consequences are written, approved by the user and added to this story, with a row in this document's change log (PRD §4)

## Change Log

This document was approved by the user and set to `final` on 2026-11-18. Every later change is recorded here with the date, the reason and the commit, as PRD §12 and DR-5 require. The rows below record the changes made before the approval.

| Date | Change | Reason | Commit |
|---|---|---|---|
| 2026-11-18 | Created with `bmad-create-epics-and-stories`: the requirements inventory, 8 epics with 39 stories, and the decisions D-1 to D-7. | The architecture spine of 2026-11-17; the archived epics of 2026-11-08 were built on the old architecture. | `9dee8b1` |
| 2026-11-18 | Fixes from the BMAD review (A1–A14, E1–E15): the demo values and the split between the test companies (UX-DR46, Story 1.6); story rules for DR-7 and DR-9; missing criteria for 405, the 503 path, the published reset, short histories, the 1366 × 768 fold, search, the decision buttons, the field label, zero decimals, negative seed values, the reasons and the confirmation; the Also-covers lists; what happens if time runs short in the Must scope. No story or feature was added, and no priority changed. | The review found contradictions and missing acceptance criteria, and the user approved fixing all 29 findings. NFR-8 is unchanged after a check against FR-28 and addendum §3 (D-7). | `9dee8b1` |
| 2026-11-18 | The user's decisions on the review: A2 approved (4 products with warnings in Testbedrift A) with the other simple solutions; NFR-8 stays unchanged (A4); `issues.md` stays the issue tracker for DR-7 (A5), with a note in the story rules. UX-DR23 and EXPERIENCE.md now also give the last product in R-12 order the last-product button. | A5 was checked against the teacher's feedback and the examiner-guideline summary, which do not require GitHub Issues. | `9dee8b1` |
| 2026-11-18 | Routine for AI sessions and AI corrections in the story rules: each story's relevant Claude Code sessions are exported to `.logs/<bruker>/sessions/`, checked for privacy and committed with the story; cases go into the AI steering log and defects into the QA log as they happen; the planning phase is documented from the work log, the memlogs and the session logs, without reconstructed prompts. Story 1.1 and Story 4.3 got matching criteria, and the Documents convention and Epic 1's Also-covers list were aligned. No story or feature added. | The examiner guidelines for part 1 (criterion 1) ask for saved prompts and AI sessions, which the repository did not have; the user approved the routine. | `9dee8b1` |
| 2026-11-18 | The A5 note in the story rules now cites the original examiner guidelines, which accept «issues eller tilsvarende»; Story 4.1 requires the README to link to `.logs/<bruker>/issues.md` and explain how it is used. No story or feature added. | The user decided to keep `issues.md` as the project's list of defects and open points; the earlier note rested only on the summary in `review-sensorveiledning.md`. | `9dee8b1` |
| 2026-11-18 | Routine for code review in the story rules: each finished story is reviewed with BMAD Code Review, and the findings, the user's decisions and the fixes with their commits are documented in the pull request. The Definition of Done says that no second reviewer is needed (D-8), and Story 4.3 checks the review comments. No story or feature added. | The user works alone; DR-7, SM-8 and the examiner guidelines (criterion 3) ask for review traces in pull requests, without saying who reviews. | `9dee8b1` |
| 2026-11-18 | Story 1.9 is scheduled right after Story 1.8, before any Epic 2 story, and is postponed only while it waits on something outside the group's control; the organization is asked about the Vercel app when Epic 1 starts (D-1, the planning constraints, the Epic 1 notes, not story work). After Story 1.9, a failed deploy of `main` is fixed before the next merge. Story 4.1 requires the README to give the published address at the top, the programs to install with their versions, the installation steps, the test commands and the expected setup time with Docker; Story 1.3 records the installation time, and the Epic 4 text and Story 4.4 follow. No story or feature added, and the architecture is unchanged. | The user's decision of 2026-11-18, after the check against the examiner guidelines (criterion 6, «README og kjørbarhet»): the examiner follows the README on a clean machine, and the published address is the quickest way in. | `9dee8b1` |
| 2026-11-18 | Story 4.1 requires the README to explain why Prognose covers only module 4.1 «Prognoser og Demand Management» of the proposal «KI-støttet MRP II», with links to the Product Brief and to the teacher's feedback on it of 2026-10-06, in the feedback's own words and without calling it an approval. No story or feature added. | Point 7 of the check against the examiner guidelines (criterion 2 measures the app against the proposal and the chosen task); the user's decision of 2026-11-18. The feedback assesses the narrowing, and the approval recorded on 2026-10-14 in `docs/arbeidslogg.md` is the user's own approval of the brief. | `9dee8b1` |
| 2026-11-18 | Responsive design for PC, iPad and phone, following the updated NFR-6 in the PRD and the UX spines: NFR-6, DR-1 and DR-9 in the inventory; UX-DR7, UX-DR19, UX-DR36, UX-DR43 and UX-DR44; a rule for every story on checks in the responsive view; criteria in Stories 1.4, 1.9, 2.7, 2.8, 2.9, 2.10, 2.11, 3.1, 3.3, 4.1, 4.2 and 4.4. The README lists the screen sizes, devices and browsers that were actually tested, with the real iPhone 13 kept apart from the responsive view (point 8 of the check against the examiner guidelines). No story or feature added, and the architecture is unchanged. | The user's decision of 2026-11-18: the website must also work on a phone and an iPad; the user has an iPhone 13 for tests on a real device, and the iPad and Android sizes are tested in the browser's responsive view. | `9dee8b1` |
| 2026-11-18 | Fixes from the final check before commit: NFR-2 in Story 2.6, whose criterion runs every Must reference example as a test; NFR-6 and UX-DR7 in «Also covers» for Epics 1, 3 and 4, and UX-DR7 in Stories 4.2 and 4.4; the UX-DR7 test sizes say which sizes run in the desktop browsers, which in the responsive view and which on the real iPhone 13. No story or feature added. | The user approved the proposals from the final check: Epic 2 named NFR-2 in «Also covers» without a story that names it, and the PC size was described as tested only in the responsive view. | `9dee8b1` |
| 2026-11-19 | Publishing removed from version 1 (D-1): Story 1.9 is removed, so Epic 1 has 8 stories and the plan 38. Updated: D-1, kept with its history; D-7; the requirements inventory (FR-4, NFR-1, NFR-3, NFR-6, NFR-8, NFR-9, DR-1, DR-9, DR-10, SM-9); the architecture summary (AD-5, AD-13, AD-14, AD-16, the delivery order, the stack and the deferred items); the planning constraints; UX-DR7 and UX-DR31; the FR coverage map; the rules for every story; the work outside stories; the Epic 1, 4 and 7 texts; and Stories 1.1 (the setting for the phone test, and the keys in the README), 1.8 (the first test on the real iPhone over the local network), 4.1 (how to start Prognose at the top, and the section «Nøkler og hemmeligheter»), 4.4 and 7.1. No feature added. | The teacher's clarification on Canvas on 2026-11-19, as reported by the user: publishing is not mandatory; the application may run locally, but the README must explain how to start it and which API keys are needed. The user approved removing publishing and Story 1.9, and keeping the real iPhone test over the local network. | `ea06f01` (PR #5) |
| 2026-11-19 | The deadline moves to 8 December 2026 at 23:59 (DR-6 and the planning constraints), and the planning constraints name the sprint plan that holds the milestone dates. | The new submission deadline of 8 December 2026 at 23:59 and the sprint planning of 2026-11-19. | `67694f7` (PR #6) |
| 2026-11-19 | Fixes from the implementation-readiness check: NFR-1 and NFR-2 on separate lines; the AD-13 summary without «in both modes»; the Configuration convention lists `PROGNOSE_LAN_HOST` as the spine does, without the production database URL; the Commands convention and Story 1.1 use `uv sync --locked`, as the spine now does; Stories 5.1 and 8.2 give AD-15 instead of the removed AD-16 as the reason why their migrations only add. | The implementation-readiness check of 2026-11-19 found text left from publishing that disagreed with the spine, and two different install commands. The user approved the fixes. No story, priority or requirement changes. | `67694f7` (PR #6) |
| 2026-11-21 | D-9: Story 1.1 may be merged before CI exists, when `uv run pytest`, `uv run ruff check` and `uv run ruff format --check` pass locally on its final commit. The rule for every story, step 5 of the routine for code review and the «Checks before a pull request» summary refer to D-9. | The user's decision of 2026-11-21: the rules asked for CI before every merge, while CI comes in Story 1.2, after Story 1.1, so Story 1.1 could not meet them. The contradiction was found while checking whether Story 1.1 can be merged, and the QA log records it. No story, priority or requirement changes. | `fa237e7` |
| 2026-11-21 | D-10: a test that verifies no FR names the NFR-n, DR-n or AD-n it verifies instead of an FR-n or E-n. The rule for every story, the AD-17 summary and Story 4.3's check refer to D-10. | The user's decision in the BMAD Code Review of Story 1.1 on 2026-11-21 (finding AA-2): DR-5 asks every test to name an FR-n or E-n, but most tests of Story 1.1 verify no FR, and Story 4.3's check would flag them. No story, priority or requirement changes. | `bcd8223` |
| 2026-11-23 | UX-DR4: the focus outline in the app header is white. No story or feature added. | The user's decision of 2026-11-23 in Story 1.8, which puts the first links in the navy header (the UX change log of the same date). | Story 1.8 (hash follows) |
| 2026-11-23 | AD-11 (summary): `app.js` may also reload a page that the browser restores from its back/forward cache, so that Back after «Logg ut» does not show a company's page. No story or feature added. | The manual test in Safari on 2026-11-23 (Story 1.8) and the user's decision of the same day (the spine change log of the same date). | Story 1.8 (hash follows) |
