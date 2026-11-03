---
title: 'Research extract for the PRD: reports C (technology stack) and D (explanations without paid API)'
created: '2026-11-02'
inputs:
  - '_bmad-output/planning-artifacts/research/technical-technology-stack-selection-2026-11-01/research.md'
  - '_bmad-output/planning-artifacts/research/technical-explanation-without-paid-api-2026-11-01/research.md'
---

# Research extract: reports C and D

Report C selects the technology stack. Report D selects how explanations are produced without a paid API. Both are complete and dated 2026-11-01. Citations keep each report's own source numbers with a C or D prefix ([C27] means report C, source 27). "C frame" and "D frame" mean the requirements frame each report agreed on 2026-11-01. C-R1 or D-R1 means that report's recommendation 1. Confidence words are the reports' own. Sections 1, 2 and 6 feed the PRD, and section 3 feeds the technical addendum.

## 1. PRD-level constraints and non-functional requirements implied

| ID | Constraint or NFR | Source | Basis and confidence |
|---|---|---|---|
| N1 | The app, explanations included, runs locally with no paid service, paid API or private key, so a reviewer can run it on their own machine. | C frame; D frame; [D6][D7] | Hard gate in both reports. All stack candidates run locally at no cost (C). |
| N2 | The explanation feature works offline. For charts to work offline too, the chart library ships with the app instead of loading from a CDN. | D frame; C-R4 [C22] | Gate (D). C-R4 says to "consider" vendoring (medium). |
| N3 | Data is kept in a local embedded database. A single-user local demo is well inside SQLite's limits. | C frame; [C12] | Gate (C); source high |
| N4 | Users log in with passwords stored only as hashes, and login state is kept in a session. | C frame; [C16][C19]; [C6] | Gate (C); sources high. Django's PBKDF2 iteration count is not stated [C16]. |
| N5 | Per-company data isolation: the server checks every request for a record against the logged-in company (deny by default), and every query is filtered by that company. Random identifiers never replace the check. A two-account test proves company A cannot read company B's data. | C frame; C-R2; [C35][C36][C37][C4] | Hard gate. Medium: the OWASP sources are high, but no framework documents a per-company pattern and OWASP shows no ready company-A-versus-B test. |
| N6 | Forecast calculations are deterministic and sit in a module that can be tested without the web app. | C frame; D frame; C hedge | Gate (C, D) |
| N7 | Every number shown, including numbers inside explanations, comes only from the deterministic calculations. No AI component creates or changes a figure. | D frame; [D2][D19][D23] | Gate (D). The risk evidence is medium and comes from older models [D2]. |
| N8 | AI-written text is labelled as AI-written and shown visually apart from calculated results. | D-R4; [D4] | Medium. EU Article 50 duties (from 2026-08-02) probably do not apply to a school project, but labelling supports the brief's success criterion. |
| N9 | The optional language-model layer is off by default. If the model is missing, not running, slow or fails validation, the app shows the template explanation and stays fully usable. | D-R2; D hedge; [D14][D15] | Low-medium (D-R2). What happens when the server is not running is undocumented (inference). |
| N10 | Forecasts are shown as line charts. | C frame; [C22] | Gate (C); source high |
| N11 | A reviewer can create the environment, install, set up the database, seed demo data and start the app by following README steps that the group has written and tested. | C-R3; [C15] | Medium |
| N12 | Template explanations are deterministic and checked by committed snapshot tests. | D-R1; [D5] | Source high; D-R1 medium |
| N13 | No feature depends on a hosted free AI tier. Any hosted option is a separate optional setting. | D-R3; [D22] | Medium (official terms) |
| N14 | The stack is mainstream and well documented. | C frame | Gate (C) |

## 2. Explanation feature

- **Verdict.** D's matrix weights are no invented numbers 30, no key 25, text quality 20, setup 15 and testability 10. Template scored 88 (the pick) and Hybrid 82 (runner-up). Local model alone scored 58, and hosted free tier plus template scored 56 (cut as a primary approach). The gap between Template and Hybrid is within scoring uncertainty, so the report treats them as the Must and Should of one design.
- **Template explanation (Must, D-R1).** A plain-language explanation in fixed sentences that state the forecasting method, the inputs, the calculation line, any warnings and the confidence label. Templates have "built-in faithfulness to input", a regulated style and quick response. Their costs are a new template for every kind of message and stiff wording [D1]. The output can be tested deterministically with committed snapshot tests [D5].
- **Optional model layer (Should, D-R2).** It runs locally only, is off by default and sits behind a setting.
  - It may rephrase the template's text around named placeholders for the numbers.
  - It may not supply, compute or change any number or placeholder, and it may not replace the template path (the template always runs). It may not require a key or a hosted service. It may not act as the number checker either: the study authors found GPT-4 unreliable as an automatic number checker [D2].
- **Numeric validation rule.** The application inserts every number itself. The validator rejects any model output whose numbers or placeholders differ from the input, and it **checks each label and value together**, not just whether the value appears. The reason: in model-written financial summaries about 5% of numbers were wrong, and the most common error was a real number in the wrong context (context mismatch 1.59-3.28% against fabrication 0-0.81%, 2023-era models). A check that "every number appears in the input" misses that error [D2]. Schema-valid structured output can still be semantically wrong [D23]. The published pattern verifies each numeric claim in the renderer, not in the model, under a stated policy (exact equality, rounding or tolerance) [D19]. Restricting a model to provided data reduces hallucinations but does not eliminate them [D3].
- **Fallback.** Use one interface, `explain(result) -> text`, plus a numeric validator. Ship the template implementation first and add the model implementation behind a setting. Fall back to the template whenever the model is missing, slow or fails validation (D hedge). Check that the model is available before calling it, using the local model list [D15]. A missing model returns 404, and errors in the middle of a stream arrive inside a 200 response [D14]. Ollama does not document what happens when its server is stopped (inference: the client gets a connection failure).
- **Open question for the teacher.** Does the course expect an AI feature that visibly uses a language model? The task asks for "AI explanations" and the brief says AI explains the forecasts, but a pure template is not AI. The answer decides whether the model layer is a Should or a Must. If it is a Must, it must be demonstrable without a key. In D's matrix, Hybrid overtakes Template if the text-quality weight rises from 20 to about 40 while the no-invented-numbers weight falls.

## 3. Addendum-level technical detail

**Stack verdict.** The 1-5 scores in C's matrix are the report's own judgement. Each total is the sum of score times weight, divided by 5.

| Criterion (weight) | Django | Flask | FastAPI | Next.js |
|---|---|---|---|---|
| Setup simplicity (25) | 4 | 5 | 3 | 2 |
| Testability (20) | 5 | 4 | 4 | 3 |
| Fit for AI coding assistants (20) | 3 | 3 | 3 | 3 |
| Login plus database (15) | 5 | 3 | 2 | 2 |
| Charting (10) | 5 | 5 | 5 | 3 |
| Learning curve (10) | 3 | 4 | 3 | 2 |
| **Weighted total** | **83** | **80** | **65** | **50** |

- **Pick (C-R1).** Django + SQLite with Django templates and Chart.js, and the forecasting logic in a plain-Python package that does not import Django. Without extra packages, Django provides:
  - login (`LoginView`, `@login_required`, `authenticate()`/`login()`) and sessions;
  - password hashing (`create_user`, PBKDF2-SHA256 by default, Argon2 optional);
  - testing: a test client with `login()`/`force_login()`, per-test rollback in `TestCase`, an in-memory test database and `SimpleTestCase` for pure logic;
  - seeding through management commands [C16][C18][C19][C20][C21].

  Versions: 6.1.2 is the latest stable release. 5.2 LTS is supported to April 2028, and 6.2 LTS is due in April 2027 [C13]. Django 6.1 supports Python 3.12-3.15 [C14] and needs SQLite 3.37 or newer [C17]. SQLite is the default database and ships with Python [C14].
- **Runner-up: Flask + SQLite (80).**
  - Flask 3.1.3 (2026-02-19) needs Python 3.9 or newer [C1][C2].
  - Login uses Werkzeug `generate_password_hash` (scrypt by default) and a signed session cookie [C4][C6].
  - Data access uses plain `sqlite3` with `?` placeholders. The queries and a `login_required` decorator of about 6 lines are written by hand [C3][C4].
  - Testing uses pytest, `test_client()` and `session_transaction()`, with no built-in per-test rollback [C5].

  **Flask wins** if setup simplicity is weighted about 35 and login plus database about 10 (Flask 83, Django 81). The strongest case against Django: its project and app structure, settings and migrations are more concepts than a small app needs, and the official tutorial omits the virtual-environment and migrate steps [C15].
- **Reversibility hedge.** Keep the forecasting package framework-free, with plain-Python unit tests and no web imports. Keep the seed data and its generator script outside the web app. If Django proves heavy, only the web layer, templates and seed commands move to Flask. Report D applies the same idea to explanations: `explain(result) -> text` with a template implementation and an optional model implementation.
- **Isolation in code (C-R2).** A project-defined rule that every query filters by the logged-in company, enforced in one data-access layer. Neither framework documents a per-company pattern. In Flask's tutorial, `get_post` (404 if missing, 403 for the wrong author) checks one record at a time, while its index page lists every user's posts [C38]. Django's docs show queryset filtering by a captured value; this finding is partly disputed.
- **Libraries to avoid, and why.**
  - Flask-Login: its last release is 0.6.3 (2023-10-30, Beta), its changelog names Flask 3 but not 3.1, and 0.7.0 is unreleased [C7][C8].
  - FastAPI as the default: it is still 0.x and Beta [C9]. It uses token (JWT) login instead of cookie sessions, with pwdlib/Argon2, and older passlib tutorials are outdated [C10]. It also needs extra pieces: SQLModel, pwdlib, PyJWT and httpx [C9][C10][C11].
  - Next.js: it needs the most separate pieces (an auth library or hand-rolled sessions, an ORM or driver, a test runner and a chart library), requires Node 20.9 or newer, and v16 brought breaking changes [C24][C25][C27]. It has frequent security releases (one is announced for 2026-11-03) and the highest ongoing maintenance cost [C25][C33]. Around it, Recharts 3.10.1 has no confirmed support for React 19 or Next.js [C34], `better-sqlite3` is a native module with unstated build needs [C31], `node:sqlite` is still a release candidate [C32], and Auth.js is now maintained by the Better Auth team [C28][C29].
- **Charting (C-R4).** Load Chart.js from a pinned CDN link or, for offline use, a vendored file. It needs one script tag and no build step, and a line chart is the getting-started example with a different type [C22]. Pass data from Python with Django's `json_script` filter [C23].
- **Local model option (Ollama).**
  - Setup: no account or key. Install from the download page or with a one-line script on macOS and Windows [D6][D7].
  - API: it listens on `localhost:11434`, and the generate endpoint accepts a JSON schema in `format` [D8][D9][D10]. `GET /api/tags` lists the installed models [D15].
  - Releases: several a week (v0.40.13 on 2026-10-28), so a README can only say "current version" [D11].
  - Gaps: there is no hardware table, and offline use is not stated explicitly [D8].
  - Ollama's own tips: also put the schema in the prompt, set temperature 0, and validate the parsed result with Pydantic or Zod [D10].

| Model (Ollama library) | Size | Licence | Notes |
|---|---|---|---|
| llama3.2 1B / 3B | 1.3 GB / 2.0 GB [D12] | 3B: custom community licence; distributing requires "Built with Llama" attribution on related UI or documentation; gated on Hugging Face [D16] | The library page calls 3B strong at instruction following and summarisation; there is no independent measure [D12] |
| gemma4 e2b | 4.6-7.5 GB [D13] | Apache 2.0 according to Google's blog of 2026-04-02 [D18], not confirmed on the Ollama model page; the older Gemma Terms of Use are a custom licence [D17] | None |
| Ollama quickstart example | about 7.2 GB; needs about 8 GB of memory [D6] | Not stated | Ollama has no hardware table [D8] |

- **Hosted APIs (not recommended, D-R3).**
  - Gemini free tier: submitted content is used to improve Google's products, and humans may review it [D20][D22]. Rate limits are shown only in AI Studio [D21]. In the EEA, Switzerland and the UK, paid-service data terms apply and clients made available there may use only Paid Services. The free tier is therefore likely unavailable to Norwegian users (inference; Norway is not named) [D22]. Users must be 18 or older [D22].
  - Others: Groq shows only Developer-plan limits, so its free limits are unconfirmed [D24]. OpenRouter free models allow 20 requests per minute and 50 per day without purchased credits [D25]. Hugging Face gives free users no monthly credits [D26]. Anthropic lists no free tier [D27].
  - If one is used anyway, make it a separate optional setting with a `.env.example`.

## 4. All recommendations from both reports

| # | Recommendation | Feeds | Basis |
|---|---|---|---|
| 1 (C-R1) | Choose Django + SQLite for the web layer and keep the forecasting logic framework-free. | Architecture decision; PRD technical constraints | Medium-low: narrow margin, single-publisher official docs |
| 2 (C-R2) | Define the isolation rule in the architecture: every query filters by the logged-in company, enforced in one data-access layer, with a two-account test that proves company A cannot read company B. | Architecture; test plan | Medium [C35][C36][C4]; no framework pattern for companies |
| 3 (C-R3) | Write and test the README setup sequence yourselves (virtual environment, install, migrate, seed, runserver), because the Django tutorial does not give it [C15]. | README | Medium |
| 4 (C-R4) | Use Chart.js from a pinned CDN link or a vendored file (consider vendoring for offline use), and pass data with `json_script` [C22][C23]. | UX; architecture | Medium |
| 5 (C-R5) | Avoid Flask-Login and FastAPI as defaults. If Flask is chosen later, use Flask's own session plus Werkzeug hashing [C4][C6]. | Architecture | Medium-high for Flask-Login [C7][C8] |
| 6 (C-R6) | Record "AI-assistant fit not evidenced" as a known limitation, and say that no framework got an advantage on it. | Process documentation | High that no source exists |
| 7 (D-R1) | Make the template explanation the Must feature: method, inputs, calculation line, warnings and confidence label in fixed sentences. | PRD functional requirements; README | Medium [D1][D5] |
| 8 (D-R2) | Make model rephrasing a Should feature, local only and off by default. The app inserts all numbers, the model rephrases around named placeholders, and the app rejects output whose numbers or placeholders differ from the input (label and value checked together). | PRD; architecture | Low-medium: a single preprint [D19] and Ollama's own tips [D10] |
| 9 (D-R3) | Do not depend on a hosted free tier. If the group wants one, make it a separate optional setting with a `.env.example`, and expect it to be unavailable in the EEA under Gemini's terms [D22]. | Architecture; README | Medium (official terms) |
| 10 (D-R4) | Label AI-written text in the UI and keep it visually apart from calculated results [D4]. | UX | Medium |
| 11 (D-R5) | If a model is used, document the choice and its licence in the README: a 2 GB model such as Llama 3.2 3B with "Built with Llama" attribution [D16], or Gemma 4 under Apache 2.0 once that is confirmed. | README; process documentation | Medium for Llama, low for Gemma |

## 5. Open questions

1. (C) What is the PBKDF2 iteration count in Django 6.1, and is it adequate? The password page does not state it [C16].
2. (C) Is there an official or well-regarded Django pattern for tying records to a company?
3. (C, Next.js path only) Does Recharts 3.x support React 19 and Next.js 16? [C34]
4. (C) What do developers report after 6 to 12 months with Django on a small app? No retrospective source was found.
5. (C, Next.js path) Which build prerequisites does `better-sqlite3` need on Windows and macOS? [C31]
6. (D) Which small model gives acceptable short explanations on an ordinary laptop, and how fast is it? No source measured this.
7. (D) Is Ollama usable fully offline, and how should the app detect that the server is not running? Neither is documented [D8][D14].
8. (D, blocks the PRD) Does the course expect an AI feature that visibly uses a language model? Ask the teacher. The answer makes the model layer a Should or a Must.
9. (D) Is the Gemma 4 Apache 2.0 licence confirmed on the official model card? [D17][D18]
10. (D) Do the Anthropic, Gemini or Ollama structured-output docs state that valid structure does not guarantee valid values? The report found that only Google's does [D23].

## 6. Evidence-quality caveats the PRD should state

- **AI-assistant fit is not evidenced.** No benchmark or statement measuring coding assistants on Flask, FastAPI or Django was found. The only related item is a Vercel vendor statement about `AGENTS.md` for Next.js [C24]. That 20% criterion therefore did not separate the candidates: all scored 3 (C-R6).
- **Scores and weights are judgements.** All 1-5 scores are the reports' own, and the weights are meant to be adjusted. Both margins sit inside the stated scoring uncertainty: Django 83 against Flask 80, and Template 88 against Hybrid 82. No source measured learning time.
- **Most evidence comes from one publisher per candidate.** Report C rests mainly on each candidate's own official documentation, read through a fetch tool that summarises pages. It marks 2 claims verified and 5 unverified. Report D marks 0 verified and 6 unverified, and no independent source verified any of its recommendations. Licence terms for the stack candidates were not checked (C).
- **The number-error figures are dated.** They come from 2023-era models, older than the reports' three-month bar for AI claims, so they show the type of error, not today's rate [D2]. The evidence for template strengths is a qualitative preprint survey with no measured error rates [D1]. The numeric-guardrail pattern rests on a single preprint [D19].
- **Local model quality is unmeasured.** No source measured small local models on this task. The 3B quality claim comes from the vendor's library page [D12].
- **Isolation has no ready-made pattern.** Neither framework documents end-to-end per-company isolation, and OWASP shows no ready company-A-versus-B test (partial confirmation) [C35][C36]. The Django finding is partly disputed.
- **Some statements are the reports' own inferences:** that Gemini's EEA terms cover Norway (Norway is not named) [D22], the README setup sequence [C15], and that a stopped Ollama server would show up as a client connection failure.
- **Staleness.** Re-check by 2026-12-01: version claims [C1][C9][C13][C24][C33][C34] and Ollama version and model sizes [D11]-[D13]. Re-check by 2027-02-01: hosted-tier terms and limits [D20]-[D22] and [D24]-[D27]. Re-check by 2027-05-01: ecosystem signals [C7][C8][C29]. Both reports should be re-checked before anyone acts on them after 2027-05-01.
- **Low confidence:** blog posts say Gemini free quotas were cut in December 2025, but the sources disagree and none was opened.
