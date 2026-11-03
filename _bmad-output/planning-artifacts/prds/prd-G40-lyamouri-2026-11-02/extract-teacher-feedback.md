# Extract: teacher feedback on the product brief

Source: `_bmad-output/planning-artifacts/briefs/brief-G40-lyamouri-2026-09-18/tilbakemelding-product-brief.md`, by the IBE160 subject teacher (faglærer), "prepared with AI support", dated 2026-10-06, reviewing the brief at commit `e75456f`. Section 7 is judged only against the revised `_bmad-output/planning-artifacts/briefs/brief-G40-lyamouri-2026-09-18/brief.md` (updated 2026-10-14). Translated from Norwegian; nothing is added beyond the teacher's text.

## 1. Overall verdict and difficulty rating

- **Verdict:** "Good starting point with adjustments" (Godt utgangspunkt med justeringer); the group can proceed and work in the points. Feasibility conclusion: "Feasible with adjusted scope" (Gjennomførbart med justert omfang).
- **What is good:** (1) wise scoping (avgrensning): only module 4.1 "Prognoser og Demand Management" from the AI-supported MRP II proposal, with BOM, production planning and supplier integration explicitly out, which makes a hard proposal feasible for one person; (2) concrete, testable success criteria (a company sees only its own data, data persists between sessions, changing forecasting method, safety margin and outlier handling "visibly changes the output"): "almost finished test cases".
- **Difficulty: Medium (Middels).** Comparable to proposal 4, AI-supported MRP II (hard), limited to module 4.1; with only one module the project becomes medium, as the difficulty guidance says. Close in scope to proposal 2, AI CV and application assistant (medium), but with more calculation logic and less text generation.
- **Factor levels:** domain logic **High** (methods, season and trend, scenarios, safety margin and outlier handling must give professionally correct numbers (faglig riktige tall), "the core of the assignment"); data model Medium; users, roles and login Medium; AI functionality Medium but unresolved (medium if AI only explains or suggests, "very hard to quality-assure" if AI makes the numbers); security and privacy Medium; integrations, real-time/concurrency and file handling Low.
- **Brief-part review (S1):** OK for Executive Summary, The Problem and Scope; Adjust (Juster) for The Solution, What Makes This Different (missing), Who This Serves, Success Criteria and Vision (missing).
- **What Medium means:** "a well-balanced choice"; finish and stabilise the core flow (kjerneflyt) before adding more (section 5, item 10).

## 2. Most important required changes (De viktigste endringene)

1. Decide what "AI-generated demand forecasts" means. If a language model makes the numbers, neither the group nor the examiner (sensor) can check whether they are correct. Calculate the forecasts with known methods in ordinary code (e.g. moving average (glidende gjennomsnitt) and exponential smoothing (eksponentiell glatting)), and optionally use AI to explain the result or suggest parameters.
2. Define how the three scenarios (optimistic, normal, pessimistic) and the safety margin (sikkerhetsmargin) are calculated, and what counts as an outlier (avvik). Without such rules the success criteria cannot be tested against an answer key (fasit).
3. Fill in the missing parts "What Makes This Different" and "Vision", and describe the primary user more concretely (type of company, how many products, how often the planner uses the tool).

The next steps (Neste steg) repeat these and add: write the decisions (v1 methods; how scenarios, safety margin and outliers are calculated; the AI's role in the app) into the brief or the PRD with rationale; make a small synthetic dataset with known trend and season and calculate the expected forecasts by hand or in a spreadsheet, for use as success criteria and later as tests; replace "not yet specified" with the submission deadline; update the brief in the repo so its history shows how the plan developed.

## 3. Grading criteria for part 1 of the portfolio (mappen)

Criteria and weights follow the examiner guidelines (sensorveiledningen) for part 1 and total 100 %. Status is the teacher's rating of the brief (Adjust = Juster).

| # | Criterion | Weight | What the brief/PRD should enable | Status | Teacher's comment |
|---|---|---|---|---|---|
| 1 | Process and AI governance (Prosess og KI-styring) | 30 % | A brief precise enough that PRD and stories can be built directly on it, so requirements can be traced from brief to code | Adjust | Good structure, but the open questions are the core of the app; document the decisions on forecasting method and AI role with rationale, which is "good process material" |
| 2 | Functionality and scope (Funksjonalitet og omfang) | 20 % | Realistic scope for the group and semester: a clear core flow that can become finished and stable, and enough content to show real functionality | OK | Realistic and clearly limited to one module, with enough content to show real functionality |
| 3 | Quality assurance and testing (Kvalitetssikring og testing) | 15 % | Success criteria and functions concrete enough to become test cases | Adjust | Testable once the rules for methods, scenarios and outliers are defined; make a test dataset with a known answer key (fasit) |
| 4 | Design and user experience (Design og brukeropplevelse) | 10 % | Clear users and usage situations the design can be built around, ideally with the key screens or flows sketched | Adjust | Screens can be derived (login, product overview, forecast with controls), but a graphical display of history and scenarios should be described in the UX step |
| 5 | Code quality and architecture (Kodekvalitet og arkitektur) | 10 % | Technology choices that are justified and no more complex than the app needs | Adjust | The stack is open; choose a simple stack with one database, and keep the forecasting logic in its own module that can be tested in isolation |
| 6 | README and runnability (README og kjørbarhet) | 10 % | A solution others can run locally without paid accounts and without access to the group's own services and keys | OK | Synthetic data and local running make it easy for the examiner, as long as the test user and any AI fallback are in the README |
| 7 | Repository tidiness (Ryddighet i repoet) | 5 % | A plan for where secrets, test data and documentation will live | Adjust | Not described; plan where the synthetic dataset and the script that generates it will live, and use `.env.example` for any keys |

## 4. Feasibility risks and the teacher's mitigations

| Area | Rating | Risk as stated | Teacher's mitigation |
|---|---|---|---|
| BMAD flow | Risk | The core flow is clear, but forecasting method, scenario rules and outlier rules, "the most important requirements", are left open | Resolve them in the PRD, "not left to AI during implementation" |
| Control over the AI's work (Kontroll på KI-ens arbeid) | Risk | Forecasting is logistics subject matter (fagstoff); the group must be able to tell whether the code does the right thing | Be able to check the numbers, e.g. calculate a small example by hand or in a spreadsheet and compare with the app |
| Dependencies and costs | Risk | Depends on change 1 (the app's AI role is "unresolved" in the difficulty table); the question asks for a plan for cost, test mode or mock data if paid APIs such as language models are used | No cost if forecasts are calculated in code, but then the AI part of the app must be described differently; scope suggestion 1: AI as a plain-language explanation of the forecast and the recommendation |
| Time and scope | OK | The deadline is open in the brief | Limit to two–three forecasting methods; insert the submission date (innleveringsdato) and plan backwards |
| Claude Code fit, testability, runnable for examiner | OK | No major risk; conditions apply | Common web app with database and login, methods in well-documented libraries; testable "provided the methods are calculated in code", with a synthetic dataset of known trend and season as answer key; test company in README and a fallback without key if a language model is used |

## 5. Expectations the PRD must carry forward

Tags: OV = Samlet vurdering (overall); DIF = Vurdert vanskelighetsgrad (difficulty table and "what it means"); FEAS = Gjennomførbarhet med BMAD og Claude Code (row named); SCOPE n = Forslag til justering av omfang; WHY = Hvorfor product brief er viktig for mappen; S1 = 1. Gjennomgang av briefens deler (part named); S2-Cn = 2. Utgangspunkt for del 1, criterion n; S3-n = 3. Neste steg, step n.

1. Forecast numbers are calculated with known methods in ordinary code; a language model must not produce them. [OV change 1; DIF AI functionality; FEAS Testability; SCOPE 1]
2. v1 names two–three forecasting methods (teacher's examples: moving average, exponential smoothing, a simple seasonal adjustment). [FEAS Time and scope; SCOPE 1; S3-1]
3. Calculation rules for the three scenarios (optimistic, normal, pessimistic) and the safety margin, plus what counts as an outlier (avvik) and how it is handled. [OV change 2; S3-1]
4. Method, scenario and outlier rules are resolved in the PRD, not left to AI during implementation, so architecture and a manageable number of stories follow without big gaps. [FEAS BMAD flow]
5. The app's AI role is decided and limited, e.g. a plain-language explanation of the forecast and the recommendation (optionally parameter suggestions). [OV change 1; FEAS Dependencies and costs; SCOPE 1; S3-1]
6. The decisions on forecasting method and AI role are documented with rationale (begrunnelse). [S2-C1; S3-1]
7. A correctness success criterion against a hand calculation, e.g. "for the test dataset, moving average over three periods gives the same number as a hand calculation"; the numbers must be professionally correct. [S1 Success Criteria; DIF Domain logic]
8. A small synthetic test dataset with known trend and season and expected forecasts calculated by hand or in a spreadsheet (answer key), used as success criteria, later as tests, and to compare against the app's output. [FEAS Testability; FEAS Control over the AI's work; S2-C3; S3-2]
9. Keep the functional criteria (own data only, data persists between sessions, visible change when method, margin or outlier handling changes), concrete enough to become test cases. [OV what is good 2; S2-C3]
10. Core-flow priority: log in → select product → see history and forecast in three scenarios → adjust method, margin and outliers → see that the forecast changes; finished and stable before adding more. [DIF what Medium means]
11. The three decision points (method, margin, outliers) as adjustable controls. [S1 The Solution]
12. Visual display: describe what the planner sees on screen, e.g. a chart with history and the three scenarios (graphical display described in the UX step); derivable screens: login, product overview, forecast with controls; key screens or flows ideally sketched. [S1 The Solution; S2-C4]
13. A concrete primary user: type of company, number of products, how often the planner uses the tool, and which decision they make after seeing the forecast. [OV change 3; S1 Who This Serves; S3-3]
14. An honest differentiation from a spreadsheet or a standard ERP system, e.g. the decisions on method, margin and outliers become visible and documented. [OV change 3; S1 What Makes This Different]
15. A short vision showing how the forecast could later feed S&OP or MPS, without taking that into v1. [OV change 3; S1 Vision]
16. The submission deadline is stated and work is planned backwards from it. [FEAS Time and scope; S3-3]
17. One simple, justified stack with one database, no more complex than the app needs (web app with database and login). [S2-C5; FEAS Suitable for Claude Code]
18. Forecasting logic in its own module that can be tested in isolation. [S2-C5]
19. The app runs locally per the README without the group's keys, paid accounts or own infrastructure. [FEAS Runnable for examiner; S2-C6]
20. The README gives a test company with a known customer number and password. [FEAS Runnable for examiner; S2-C6]
21. If a language model is used: a fallback without a key (reserve uten nøkkel), documented in the README. [FEAS Runnable for examiner; S2-C6]
22. A plan for cost, test mode or mock data if any paid API is used. [FEAS Dependencies and costs]
23. A plan for where secrets, test data and documentation live, including where the synthetic dataset and the script that generates it live. [S2-C7]
24. `.env.example` for any keys. [S2-C7]
25. Synthetic data loaded as seed data; CSV import is possible but not necessary. [DIF File handling]
26. Login with customer number and password, isolation between companies, one role, password hashing. [DIF Users, roles and login; DIF Security and privacy]
27. Data model as the teacher sees it: company/account, product, period, historical sales, forecast with parameters, plus campaigns and customer orders (which SCOPE 2 suggests deferring). [DIF Data model]
28. Requirements traceable from brief to PRD, stories and code. [S2-C1; WHY]
29. Scope boundaries: season/trend and historical sales in v1; campaign/market data and incoming customer orders deferred; BOM, production planning and supplier integration out. [SCOPE 2; OV what is good 1]

## 6. Scope advice (v1 vs later)

- **In v1:** module 4.1 only, with one clear core flow; two–three forecasting methods (e.g. moving average, exponential smoothing, a simple seasonal adjustment); season/trend and historical sales; AI limited to a plain-language explanation of the forecast and recommendation, which gives "numbers that can be checked and a limited AI function". [SCOPE 1–2; FEAS Time and scope]
- **Consider postponing:** campaign/market data and incoming customer orders, because "each new signal requires its own rules and test data". [SCOPE 2]
- **Keep out (praised):** BOM, production planning and supplier integration; S&OP/MPS only as a later vision, "without it being taken into v1". [OV; S1 Vision]
- **Optional:** CSV import ("possible, but not necessary"); AI suggesting parameters is also framed as optional ("eventuelt"). [DIF File handling; OV change 1]
- **Order of work:** finish and stabilise the core flow before adding more, and leave time for the whole BMAD flow (brief → PRD → architecture → epics and stories) plus testing, fixing and README at the end. [DIF; FEAS intro]

## 7. Addressed in the revised brief vs still open

| Teacher point | Status in the revised brief | Brief section |
|---|---|---|
| Forecasts calculated by known methods, not by AI | Addressed: "AI must not generate the numerical forecasts"; deterministic, hand-checkable | §1, §4 |
| Two–three methods in v1 | Addressed: two (moving average, exponential smoothing) | §3, §8 |
| Rules for scenarios, safety margin and outliers | Partly: drafted, but labelled "Proposed rules, to be validated during BMAD planning" | §4, §11 |
| AI role in the app and a fallback without key | Partly: AI explains forecasts; an alternative without a paid API is in scope; how both work is still an open question | §1, §3, §8, §11 |
| Decisions documented with rationale | Partly: decisions stated with a short reason (deterministic, hand-checkable); no rationale for the choice of methods | §4 |
| What Makes This Different | Addressed: transparency, visible method, adjustable assumptions; no explicit spreadsheet comparison (enterprise systems only implied) | §5 |
| Vision | Addressed in general terms; S&OP/MPS not named | §9 |
| Concrete primary user | Mostly: small business, 10–50 products, weekly review; the decision taken after seeing the forecast is not stated (§4 only mentions a "suggested planning quantity") | §6 |
| Correctness success criterion | Addressed generically ("match independently checked examples"), without a concrete hand-calculated case | §7 |
| Test dataset with known answers | Partly: "synthetic datasets with known results" planned; no hand-calculated expected values yet | §8, §10 |
| Season/trend in v1; campaigns and customer orders later | Addressed for scope; season/trend appear only as patterns in the test data, with no seasonal method listed | §8 |
| What the planner sees (chart of history and scenarios) | Partly: "charts of sales history and forecasts"; screen description left for the UX step | §3 |
| Simple stack, one database, isolated forecasting module | Partly: principle stated (local database, calculations testable on their own); stack choice deferred to architecture | §10, §11 |
| Runnable per README with test account, no paid keys | Addressed in principle | §10 |
| Core-flow priority | Not stated explicitly; covered piecemeal by the success criteria | §7 |
| Login, data isolation, password hashing | Login and isolation addressed; password hashing not mentioned | §1, §3, §7 |
| Location of synthetic dataset and generator script; `.env.example` | Open: not mentioned | none |
| Submission deadline | Open: listed as "Confirm the final submission deadline" | §11 |
| Brief updated in the repo to show how the plan developed | Addressed as far as the file shows (`updated: 2026-10-14`) | frontmatter |

## 8. Traceability and what the examiner (sensor) looks for

- The brief is the starting point for PRD, architecture, stories and finally the code. Part 1 of the portfolio is assessed, among other things, on whether the examiner can follow a traceable path from plan to finished app (sporbar vei fra plan til ferdig app). [WHY]
- Part 1 is also assessed on whether the app does what was described, whether it is tested, whether it is well designed, and whether it can be run following the README. [WHY]
- An unclear, too large or too small brief makes all of this harder later; it is "much easier to fix now than late in the semester". [WHY]
- Criterion 1 (30 %) asks for a brief precise enough that PRD and stories build directly on it, so requirements can be traced from brief to code; documenting the decisions on forecasting method and AI role with rationale is "good process material". [S2-C1]
- Updating the brief in the repo after changes, so the history shows how the plan developed, "is part of the process the examiner looks for". [closing note of the feedback]
- The examiner must be able to verify the numbers (the reason for no LLM-made forecasts) and to run the app locally without the group's keys, paid accounts or own infrastructure. [OV change 1; FEAS Runnable for examiner]
