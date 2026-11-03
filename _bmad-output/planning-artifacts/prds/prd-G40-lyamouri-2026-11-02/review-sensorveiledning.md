---
title: 'Review: PRD against the examiner guidelines, part 1'
created: '2026-11-03'
reviewed: 'prd.md (updated 2026-11-03) and addendum.md (updated 2026-11-02)'
---

# Review: PRD against the examiner guidelines (part 1, «Prosjektkode og funksjonalitet»)

- **Basis.** `prd.md` and `addendum.md` in this folder, checked against a summary of the IBE160 examiner guidelines for part 1. The brief, research reports, other review files and code were not read; two repository facts (1.6, 7.2) come from the git status and log available when the review started. Part 1 grades the delivered app and repository, so this review judges how well the PRD sets the project up for A–B, not whether the PRD meets the criteria itself.
- **Severity.** High = likely to cost a grade band on that criterion if left open; Medium = could cost; Low = polish.
- **Fix in.** PRD = add or sharpen in the PRD; Later = UX, architecture, epics and stories, or implementation; WoW = the group's way of working, which the PRD may only reference.

## The criteria (from the examiner guidelines)

Part 1 of the portfolio («Prosjektkode og funksjonalitet») counts 70% of the final grade. It is assessed on seven criteria with guiding weights. Criteria 1, 6 and 7 (process and verifiability) make up 45%, and criteria 2 to 5 (the product) make up 55%. The short descriptions are quoted from the guidelines in Norwegian, with an English translation.

| # | Criterion | Short description in the guidelines | English | Weight |
|---|---|---|---|---|
| 1 | Prosess og KI-styring (process and AI governance) | Sporbar vei fra plan til kode: commits, prompts, iterasjoner og beslutninger | A traceable path from plan to code: commits, prompts, iterations and decisions | 30% |
| 2 | Funksjonalitet og omfang (functionality and scope) | Hva appen gjør, sett mot proposal og valgt oppgave | What the app does, measured against the proposal and the chosen task | 20% |
| 3 | Kvalitetssikring og testing (quality assurance and testing) | Tester, kodegjennomgang og retting av KI-generert kode | Tests, code review and fixing of AI-generated code | 15% |
| 4 | Design og brukeropplevelse (design and user experience) | Visuelt uttrykk, konsistens, brukervennlighet og tilgjengelighet | Visual expression, consistency, usability and accessibility | 10% |
| 5 | Kodekvalitet og arkitektur (code quality and architecture) | Lesbar, strukturert og sammenhengende kode | Readable, structured and coherent code | 10% |
| 6 | README og kjørbarhet (README and runnability) | Tydelig beskrivelse av hvordan appen installeres og kjøres | A clear description of how the app is installed and run | 10% |
| 7 | Ryddighet i repoet (repository tidiness) | Struktur, riktige filer, ingen hemmeligheter eller byggeartefakter | Structure, the right files, no secrets or build artifacts | 5% |

The examiner spends a guiding 15 to 20 minutes getting the app to run from the README alone. Gaps a normal user cannot solve from the README count against the README. If the app cannot run, functionality is judged from code, tests, screenshots and video in the repository, which clearly lowers criterion 6 and limits criterion 2.

*Checked on 2026-11-03 against the guidelines the user provided: the criterion names, weights, the 45/55 split, the short descriptions and the "what the examiner looks for" points used in the sections below match the guidelines. The guidelines themselves are not stored in the repository.*

## Verdict

A strong, testable product specification: the Must scope, 17 rules and a 30-example answer key set up criteria 2, 3 and 5 well. The weak side is the evidence the examiner looks for under criteria 1, 6 and 7 (45% together): DR-5 and SM-8 ask for traceability but do not say what must exist in the repository (saved AI sessions, steering examples, reviewed pull requests, an FR status table, a change log). Basic accessibility and robustness against wrong input are missing. About ten short PRD edits close most gaps.

| Criterion (weight) | PRD readiness | Gaps H / M / L |
|---|---|---|
| 1 Process and AI governance (30%) | Partial: tracing rules exist, the evidence is not specified | 3 / 3 / 1 |
| 2 Functionality and scope (20%) | Good: testable Must scope with non-trivial rules | 2 / 2 / 1 |
| 3 Quality assurance and testing (15%) | Good: answer key and named automated tests | 1 / 1 / 1 |
| 4 Design and user experience (10%) | Partial: journey and texts strong, accessibility missing | 1 / 3 / 0 |
| 5 Code quality and architecture (10%) | Good, mostly a later step | 0 / 1 / 1 |
| 6 README and runnability (10%) | Good: DR-1 and SM-2, but no final re-test | 1 / 4 / 0 |
| 7 Repository tidiness (5%) | Partial: no secrets, but no .gitignore rule | 0 / 2 / 1 |
| **Total** | | **8 / 16 / 5** |

## 1. Process and AI governance (30%)

**Provides.** §0 links the brief, the teacher's feedback, the brainstorm, research A–D, the review and reconcile reports and the decision log. §12 explains each change from the brief; §11 and the source tags in §5 (sourced, partly supported, project-defined) give the rationale. DR-5, AG-6 and SM-8 require recorded decisions, a description of AI use and FR → story → test tracing, with every commit naming its story. §10 Q7 updates the brief after approval, and the addendum records the technology rationale and rejected alternatives (§2, §4). Checks of AI output are already visible in planning: the answer key was recomputed independently during review (§5.7), assumptions are tagged, and the addendum corrects a report's weight arithmetic (§2).

- **1.1 AI evidence not specified** · High · PRD (DR-5) + WoW. DR-5 only says that AI use "is described"; the examiner looks for saved prompts and sessions and several examples, linked to changes, of the group correcting AI. *Add to DR-5:* "Prompts and AI sessions for each story are saved in a documented folder (DR-2), redacted per NFR-4. An AI steering log records at least five cases, at least one per epic, where the group clarified, rejected or corrected AI output: what the AI proposed, what was wrong, what the group decided, and the commit or PR. The planning-phase review and reconcile rounds give its first entries."
- **1.2 No development workflow** · High · PRD (new DR-7) + WoW. Nothing asks for branches, pull requests, issues or small commits spread over time; DR-5 only asks that commits name their story. *Add:* "DR-7 Workflow. Each story is built on its own branch and merged through a pull request that names the story and FR-n and says what was tested; review comments stay in the PR. Defects and open points are tracked as issues. Commits are small and pushed as the work happens, so the history spans the whole build period."
- **1.3 PRD not kept current after approval** · High · PRD. No rule covers deviations during implementation. With Should items at risk (§8.2 note), the delivered app may differ from the PRD, which is a named warning sign. *Add:* "§13 Change log. Every change to a requirement, priority or rule after approval is recorded here with date, reason and commit or PR, and the status moves from draft to approved to final. The architecture, UX and epics documents follow the same rule."
- **1.4 No traceability artefact** · Medium · PRD. SM-8 asks for FR → story → test tracing but names no file and no status at submission. *Add:* "DR-8 Traceability table. One table lists every FR with its priority, status at submission (built, partly built, not built, changed), stories, tests and the reason for any deviation. The README links it."
- **1.5 No fixed checkpoints** · Medium · PRD (DR-6) + sprint planning. About four weeks remain, and DR-6 leaves every date to sprint planning. *Add to DR-6:* "Fixed checkpoints: the Must scope passes SM-1 and SM-3 by [date]; feature freeze by [date, about one week before 1 December 2026]; final clean-clone test (SM-2) and submission tag by [date]."
- **1.6 PRD history not yet in git** · Medium · WoW. The PRD folder was untracked when this review started. Commit the PRD, the addendum and the review files now, and each later revision as its own commit, so the history shows iteration rather than documents added at the end.
- **1.7 Addendum references drift** · Low · PRD (addendum). Addendum §1 and §3 point to PRD §10 question 7 for the model choice, which is question 6, and addendum §5 says E3 to E14 rest on hand calculation, while the answer key now runs to E30. *Fix:* correct both.

## 2. Functionality and scope (20%)

**Provides.** UJ-1 with a Must or Should priority per step; FR-1 to FR-36 with testable consequences; the MoSCoW split in §8, guarded by SM-C2; non-trivial rules R-1 to R-17; saved data and settings (FR-4, FR-22); two isolated companies (FR-2); wrong-input handling for login, setting ranges and adjusted quantities (FR-1, FR-20, FR-29); changes from the brief in §12 (if the approved proposal is a separate document from the brief, link it in §0 and cover it in §12 too). Read-only data (§7) keeps the input surface small, which helps stability.

- **2.1 Proposal features sit at Should** · High · PRD. Seasonal adjustment (suggested by the brief and the teacher, §8.2) and an AI-written explanation (a brief success criterion, mapped to SM-6) may not be delivered, and §10 Q1 and Q2 are still open. If they are dropped, scope falls below the proposal. *Add to §8.2:* "Should items from the approved brief come first: FR-36, which needs only R-14 steps 1 and 2 and lets the app at least detect season, then FR-9, then FR-28 unless the teacher's answer to Q1 makes it Must, then FR-29 and FR-30. Any item not built is listed, with its reason, in the traceability table (DR-8) and the README." Drop "built together with FR-9" from FR-36, and record the teacher's answer to Q1 in §10 with its date.
- **2.2 No robustness requirement** · High · PRD (new NFR-10) + Later. Range checks exist, but nothing covers empty or non-numeric input, a decimal point versus the decimal comma that NFR-5 makes the norm (a user will type «0,5»), unknown URLs, repeated submits, the back button or framework debug pages. *Add:* "NFR-10 Robustness. Numeric fields accept a decimal comma or a decimal point; empty or non-numeric input is refused with a Norwegian message, and the previous value stays. No URL or input shows a stack trace or debug page; an unknown page shows a Norwegian not-found page with a link to the product overview. Submitting the same change twice, reloading or going back gives the same result without errors."
- **2.3 The examiner may miss the interesting cases** · Medium · PRD (DR-1). The examiner tests the flows the README describes, and nothing maps the test products to the rules they show. *Add to DR-1:* "A 'Try it' section of 5 to 10 steps following UJ-1, and a table of the test products naming the warning, rule or confidence label each one shows and its E-n in the reference spreadsheet."
- **2.4 Re-running the seed is undefined** · Medium · PRD (DR-4). A retry after a failed setup step is common. *Add to DR-4:* "Running the load command again resets the database to the seed state without duplicates or errors; the README says that this also resets settings and adjustments."
- **2.5 Complexity case not stated** · Low · PRD (§8). The examiner weighs roles and integrations, and v1 has neither by design. *Add:* "The complexity of v1 lies in 17 deterministic rules checked by 30 reference examples, two isolated companies with saved settings and a guarded explanation layer, not in roles or integrations."

## 3. Quality assurance and testing (15%)

**Provides (strong).** NFR-2 (isolated calculation module, all tests with one command); SM-1 (100% of the Must reference examples); §5.7 and DR-3 (the same answer key in the tests and the spreadsheet); SM-3 (a core-flow test through the web application); FR-2 and SM-4 (company A against B, including lists); the FR-21 table (one test per setting); FR-26 snapshot tests; FR-28 and SM-6 (number check); SM-7 (every warning and label triggered by test data); DR-5 (each test names its FR-n or E-n); FR-1 and NFR-3 (salted hashes, no secrets).

- **3.1 No review or defect evidence** · High · PRD (new DR-9) + WoW. A–B asks for concrete examples of errors found and fixed, and the PRD never asks for them. *Add:* "DR-9 QA log. Each defect found in AI-generated code or text, by a test, the reference spreadsheet, a review or a manual test, is recorded with how it was found, the fix and the commit or PR."
- **3.2 No manual test plan** · Medium · PRD (DR-9). Automated tests do not cover NFR-6 (browsers), NFR-7 (markers and legend), NFR-8 (timing), SM-2 (clean machine, offline start) or keyboard use. *Add to DR-9:* "A manual test checklist for NFR-6, NFR-7, NFR-8, NFR-11 and SM-2 is run on the final commit and recorded with date, operating system, browser and result."
- **3.3 Test-run details** · Low · PRD (NFR-2) + Later. If the core-flow test needs a separate browser driver, running the tests as the README describes can fail. *Add to NFR-2:* "The test command needs nothing beyond the README's install steps, and the README shows its expected result." Running tests and the linter on every pull request (CI) would add visible QA traces.

## 4. Design and user experience (10%)

**Provides.** UJ-1 (persona, context, steps, edge cases) as a UX description; binding Norwegian labels with no synonyms (§3); exact Norwegian texts for errors, notes and fixed explanations (FR-1, FR-7, FR-10, FR-12, FR-14, FR-21, FR-27); a clear structure in FR-24 (sorted by R-12) and FR-25; a reason instead of a number when there is no forecast (FR-8, FR-24); markers that differ by more than colour, with a legend (NFR-7); the decimal comma (NFR-5).

- **4.1 Basic accessibility missing** · High · PRD (new NFR-11) + Later (UX). Only NFR-7 is specified, and a canvas chart such as Chart.js (addendum §2) has no text alternative by default. *Add:* "NFR-11 Basic accessibility. Text contrast meets WCAG 2.2 AA; every function works with the keyboard alone, with visible focus; every form field has a visible label; pages declare Norwegian as their language; the chart has a text alternative: a short summary and the plotted values in a table."
- **4.2 Screen sizes undefined** · Medium · PRD (NFR-6). Desktop only is a sound choice for an office user, but the examiner may resize the window. *Add to NFR-6:* "No horizontal page scrolling from 1024 px wide upwards; narrower windows stay readable, without overlapping or cut-off content. Desktop first, because the user plans at an office PC (UJ-1)."
- **4.3 Feedback and empty states incomplete** · Medium · PRD (FR-21, FR-24) + Later (UX). *Add to FR-21:* "After a change, the screen confirms it in Norwegian and shows the previous and the new value of the affected number." This makes the teacher's core flow visible. *Add to FR-24:* "With no products, the overview says that no data is loaded and names the load command." NFR-10 covers the not-found page.
- **4.4 Design work and screen hierarchy** · Medium · PRD reference + Later (UX). The product screen holds about a dozen elements without a priority order, and the PRD names no UX deliverables. *Add to FR-25:* "The suggested order quantity, the confidence label and the active warnings are visible without scrolling on a 1366 × 768 screen." *Add to §0:* "The UX step delivers DESIGN.md and EXPERIENCE.md, with wireframes of the login page, product overview, product screen and combined order overview."

## 5. Code quality and architecture (10%)

**Provides.** A calculation module with no dependency on the user interface or the database (NFR-2); one web application and one local database, with no more parts than needed (NFR-9); a folder layout fixed in the architecture step and listed in the README (DR-2); `.env.example` (NFR-3); a framework-free forecasting package, one data-access layer that filters by company, and seed code outside the web app (addendum §2); glossary terms as a naming source (§3). The change-log rule in 1.3 keeps the architecture document matching the code.

- **5.1 No style or dependency rule** · Medium · PRD (DR-2) + Later (tool choice). *Add:* "One formatter and one linter, chosen in the architecture step, run with a documented command and pass on the submitted commit. Dependencies are pinned to exact versions in one file."
- **5.2 Nothing against AI leftovers** · Low · WoW (Definition of Done) + PRD. *Add to §3:* "Code uses the English glossary terms for domain names." *Add to DR-7:* "Definition of Done: tests and linter pass; no commented-out, unused or duplicated code; traceability table and documents updated; pull request reviewed."

## 6. README and runnability (10%)

**Provides.** DR-1 (macOS and Windows, tested from a fresh clone; the session secret; test logins; generating and loading data; running tests; browsers; the optional model and its licence; known limitations); folders listed (DR-2); one load command (DR-4); `.env.example` for optional settings (NFR-3, FR-28); SM-2 (README only, at most 15 minutes, offline after installation, a clean machine per operating system); no keys and local assets (NFR-1); §1 promises that the examiner can check forecasts against worked examples.

- **6.1 README checklist incomplete** · Medium · PRD (DR-1). DR-1 lacks several items the examiner checks. *Add to DR-1:* "Purpose and target user, with a screenshot; prerequisites with minimum versions; copyable commands for macOS Terminal and Windows PowerShell, including activating the virtual environment (Linux: as macOS, untested); links to the PRD, architecture, epics, decision log, AI steering log, QA log and traceability table; the expected test output; fixes for the three most likely setup errors." Versions matter: the recommended Django 6.1 needs Python 3.12 or newer (addendum §2), which a clean machine may lack.
- **6.2 No re-test on the final commit** · High · PRD (SM-2). The SM-2 test happens once, before the README is final, and its start state is undefined, so README drift is not caught. *Change SM-2:* "The clock starts on a machine with only the README's prerequisites installed; target: at most 10 minutes from clone to logged in. The clean-clone test is repeated on the final commit on macOS and Windows and recorded in the QA log (DR-9) with date, versions, time and deviations."
- **6.3 Manual secret step** · Medium · PRD (NFR-3) + Later. A hand-made session secret is a likely failure point, especially on Windows. *Add to NFR-3:* "Setup needs no manual file editing: the setup or load command creates the session secret in an ignored local file when it is missing."
- **6.4 The model could break the time budget** · Medium · PRD (FR-28, §10 Q1). If FR-28 becomes Must, a model download of 1.3 to 7.5 GB (addendum §3) does not fit in 15 to 20 minutes. *Add to FR-28:* "Whatever its priority, the model is never part of the basic setup (SM-2): the README gives it as a separate optional step with download size and time, and the app runs fully without it (AG-3)."
- **6.5 No fallback evidence** · Medium · PRD (DR-1). If the app cannot run, the examiner judges functionality from code, tests, screenshots and video. *Add:* "The repository holds screenshots of the login page, product overview and product screen, and a screen recording of UJ-1 steps 1 to 4 of at most 2 minutes, updated at feature freeze."

## 7. Repository tidiness (5%)

**Provides.** Documented places for the data, generator, spreadsheet, documentation and planning artifacts, `.env.example` and no committed secrets (DR-2); a session secret that is never committed (NFR-3); no personal data or local paths in the repository (NFR-4); generator output versioned on purpose (FR-3).

- **7.1 No .gitignore rule** · Medium · PRD (DR-2). FR-4 makes the database a local file, but nothing says it stays out of git. *Add to DR-2:* "A .gitignore keeps out the virtual environment, caches, test and coverage output, the local database file, .env, the session-secret file, and operating-system and editor files. The generated seed data is versioned; the database is not."
- **7.2 Tool folders unexplained** · Low · PRD (DR-2) + WoW. The repository also versions the BMAD framework and skills (commit history), which can look like clutter. *Add to DR-2:* "The README explains every top-level folder, including the BMAD and Claude Code folders; the root holds no loose files other than the README, a licence and configuration files."
- **7.3 No final secret and privacy check** · Medium · PRD (NFR-3, NFR-4). Saved AI sessions (1.1) often contain local paths and names, which NFR-4 forbids. *Add to NFR-4:* "AI sessions are redacted before they are committed. Before submission the group scans the full history for secrets, personal data and local paths and records the result in the QA log."

## Warning signs the PRD can prevent

- **Most code in a few commits before the deadline:** partly prevented. DR-5 ties commits to stories and SM-C2 limits scope; 1.2 and 1.5 are needed.
- **Planning documents describe another app or look generated afterwards:** at risk. §12 and the MoSCoW split help, but there is no change log after approval (1.3), no status per FR (1.4), and the PRD is not yet committed (1.6).
- **README is a template or its commands fail:** mostly prevented by DR-1 and SM-2; the final-commit re-test (6.2) closes the rest.

## Conflicts with the guidelines

- **Setup time:** the 15 minutes in SM-2 fit inside the examiner's 15 to 20, but leave no margin for reading, installing prerequisites or one retry, and the start state is open. Aim for 10 minutes with the prerequisites installed (6.2).
- **Platform and screen size:** desktop only (NFR-6) is defensible for an office user, but the examiner may try other sizes; state the reason and a minimum width (4.2). NFR-1 and DR-1 name only macOS and Windows; one Linux line costs little (6.1).
- **Optional model versus runnability:** a Must FR-28 with a multi-gigabyte download conflicts with the time budget unless it stays outside the basic setup (6.4).
- **NFR-4 versus saved AI sessions:** criterion 1 wants saved sessions, while NFR-4 bans personal data and local paths. Redaction resolves it (7.3).
- **One role, no integrations:** not a conflict, but the PRD should say where the complexity lies (2.5).

## Belongs to later steps or the way of working (reference only)

- **UX:** visual style, components, wireframes, wording of empty and error states, an accessibility check against NFR-11.
- **Architecture:** the final stack with rationale; the folder layout (DR-2); the data-access layer for FR-2; switching off debug pages without breaking local static files such as the chart library (NFR-1, NFR-10); CSRF protection on forms that change data; the linter and formatter; how the secret is created; whether the SQLite bundled with Python meets the framework's minimum (addendum §5).
- **Epics and stories:** acceptance criteria from the FR consequences; stories for the README, the clean-clone test, the screenshots and the traceability table.
- **Way of working:** the branch, pull-request and issue routine, commit rhythm, saving and redacting sessions, steering-log entries, code review, session logs.

## Top PRD fixes, in order

1. Sharpen DR-5: saved, redacted prompts and sessions, and an AI steering log with at least five examples linked to commits or pull requests (1.1).
2. Add DR-7 (branch and reviewed pull request per story, issues, steady commits, Definition of Done) and DR-9 (QA log of defects in AI output, manual test checklist) (1.2, 3.1, 3.2, 5.2).
3. Add a §13 change log and a DR-8 FR status table, and fix the Should order now, with items from the brief first (1.3, 1.4, 2.1).
4. Add NFR-10 robustness (decimal comma or point, no debug pages, repeat-safe actions) and NFR-11 basic accessibility (2.2, 4.1).
5. Sharpen SM-2 and DR-1: a defined start state, a 10-minute target, a re-test on the final commit, and a README with a walkthrough of the test products, screenshots and links to the process documents (6.1, 6.2, 2.3, 6.5).

## Outcome (2026-11-03)

The user approved the PRD-level fixes as one package, with these decisions, and they are now in the PRD (see `.memlog.md`):
- The setup target stays at 15 minutes (the 10-minute suggestion was not taken); the clean-machine test is repeated on the final commit (SM-2, DR-9).
- Screenshots in the README are Must; a screen recording is optional (DR-1).
- The order of the Should items is decided in sprint planning (1.5 and 2.1 stay open there), and the optional language model does not depend on the teacher's answer (FR-28).
- Added or sharpened: NFR-6, NFR-10, NFR-11, DR-1, DR-2, DR-4, DR-5, DR-7, DR-8, DR-9, NFR-3, NFR-4, FR-21, FR-24, FR-25, FR-28, §8.1 (complexity) and §12 (change log).
- The addendum references in 1.7 were corrected.
