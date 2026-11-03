---
title: 'Addendum: Prognose PRD'
created: '2026-11-02'
updated: '2026-11-03'
---

# Addendum: Prognose PRD

## 1. Purpose

This addendum goes with the PRD in this folder (`prd.md`). The PRD states capabilities. This document keeps the technical detail, research figures and rejected alternatives that the architecture, UX and epics steps need, with their rationale. The PRD refers to it for the technology rationale (§0, NFR-9) and the local model candidates (§10, question 5).

- **No new requirements.** Every requirement, priority and calculation rule is in the PRD. If this addendum and the PRD disagree, the PRD wins.
- **Nothing is decided here** unless the PRD says so. The technology stack, the local model runtime and the model itself are still open. For these, this addendum gives the research recommendation for the architecture step.
- **Citation keys.** [An], [Bn], [Cn] and [Dn] are source n in research report A, B, C or D (§6). C-R1, D-R2 and so on are a report's numbered recommendations. "Inference" marks a report's own reasoning without a source. "Addendum note" marks this document's own arithmetic or reading of the PRD.

## 2. Technology stack (research recommendation for the architecture step, not decided)

The PRD sets constraints, not a stack:
- one web application with one local file database (NFR-9, FR-4);
- no paid services, keys, accounts or internet connection when running (NFR-1);
- salted password hashes and a server-side company check on every request (NFR-3, FR-1, FR-2);
- one calculation module with no dependency on the user interface or the database (NFR-2);
- a README for macOS and Windows (DR-1).

Report C scored four candidates, and all four passed its gates. The 1 to 5 scores are the report's own judgements. Weighted total = sum of score × weight, divided by 5.

| Criterion (weight) | Django | Flask | FastAPI | Next.js |
|---|---|---|---|---|
| Setup simplicity (25) | 4 | 5 | 3 | 2 |
| Testability (20) | 5 | 4 | 4 | 3 |
| Fit for AI coding assistants (20) | 3 | 3 | 3 | 3 |
| Login plus database (15) | 5 | 3 | 2 | 2 |
| Charting (10) | 5 | 5 | 5 | 3 |
| Learning curve (10) | 3 | 4 | 3 | 2 |
| **Weighted total** | **83** | **80** | **65** | **50** |

**Recommended (C-R1, basis medium-low): Django + SQLite** with Django templates and Chart.js. The forecasting logic goes in a plain-Python package that does not import Django. Without extra packages, Django provides:
- login (`LoginView`, `@login_required`, `authenticate()`/`login()`) and sessions [C19];
- password hashing through `create_user`: PBKDF2-SHA256 by default, Argon2 optional; the documentation does not state the iteration count [C16];
- a test client with `login()`/`force_login()`, per-test rollback in `TestCase`, an in-memory test database, and `SimpleTestCase` for pure logic [C18][C20];
- seeding through management commands [C21].

Versions as of 2026-11-01: Django 6.1.2 is the latest stable release. 5.2 LTS is supported to April 2028, and 6.2 LTS is due in April 2027 [C13]. Django 6.1 supports Python 3.12 to 3.15 [C14] and needs SQLite 3.37 or newer [C17]. SQLite is the default database and ships with Python [C14], and a single-user local demo is well inside its limits [C12].

**Runner-up: Flask + SQLite (80)** with Jinja templates and Chart.js.
- **Versions and login:** Flask 3.1.3 (2026-02-19) needs Python 3.9 or newer [C1][C2]. Login uses Werkzeug `generate_password_hash` (scrypt by default) [C6] and a signed session cookie [C4].
- **Data access and tests:** data access uses plain `sqlite3` with `?` placeholders. The queries and a `login_required` decorator of about 6 lines are written by hand [C3][C4]. Tests use pytest, `test_client()` and `session_transaction()`, with no built-in per-test rollback [C5].
- **When Flask wins:** if setup simplicity is weighted about 35 and login plus database about 10, Flask scores 83 and Django 81. (Addendum note: these totals only add up if testability also drops to 15, so that the weights still sum to 100.)
- **Strongest case against Django:** its project and app structure, settings and migrations are more concepts than a small app needs. Its official tutorial does not mention a virtual environment and leaves `migrate` until part 2 [C15].

**Further notes for the architecture step.**
- **Reversibility hedge:** keep the forecasting package framework-free, with plain-Python unit tests and no web imports. NFR-2 already requires this of the calculation module. Keep the seed data and its generator script outside the web app too. If Django proves heavy, only the web layer, templates and seed commands move to Flask. Report D applies the same idea to explanations (§3).
- **Libraries and options to avoid (C-R5):** avoid Flask-Login. Its last release is 0.6.3 (2023-10-30, Beta), its changelog names Flask 3 but not 3.1, and version 0.7.0 is unreleased [C7][C8]. If Flask is chosen, its own session and Werkzeug hashing replace Flask-Login [C4][C6]. FastAPI tutorials built on passlib are out of date [C10]. For FastAPI as the default and for Next.js, see §4.
- **Charting (C-R4):** Chart.js needs one script tag and no build step. A line chart is the getting-started example with a different chart type [C22]. Django's `json_script` filter passes the data from Python to the page safely [C23]. C-R4 allows a pinned CDN link or a vendored file and suggests considering the vendored file for offline use. Addendum note: NFR-1 requires Must features to work without an internet connection, and only the vendored file meets that. The research did not check how Chart.js draws the markings that differ by more than colour, or the legend, that NFR-7 asks for.
- **Company isolation (C-R2, basis medium):** OWASP is the main source. It is usually enforced like this:
  - OWASP ranks Broken Access Control first in its Top 10:2025. It prescribes deny by default and server-side enforcement, and says access control should enforce record ownership [C35]. Its cheat sheets require an access check on every request for the specific object, and say that random identifiers do not replace that check [C36][C37]. OWASP recommends unit and integration tests for authorisation logic but gives no ready-made company-A-versus-B test [C35][C36].
  - C-R2 turns this into a project-defined rule. Every query filters by the logged-in company, and one data-access layer enforces this. A two-account test proves that company A cannot read company B's data (FR-2 and SM-4 require this test). The Next.js authentication guide uses the same kind of layer, which reads the session on every query [C27].
  - Neither Django nor Flask documents a per-company pattern. Flask's tutorial checks ownership one record at a time (`get_post` returns 404 if the record is missing and 403 if another author owns it), but its index page lists every user's posts [C38]. Django's docs show filtering a query by a value taken from the request; the report marks this finding as partly disputed.
  - Addendum note: if every query filters by company, a request for another company's record returns the "not found" that FR-2 asks for, not the 403 that Flask's tutorial returns.
- **README (C-R3):** the group writes and tests the setup sequence itself (for Django: virtual environment, install, migrate, seed, runserver), because the official tutorial does not give it [C15]. This sequence is the report's own inference. DR-1 and SM-2 already ask for a README that the group tests from a fresh clone on macOS and Windows.

## 3. Explanation layer, technical notes

The PRD fixes the shape:
- a template explanation (Must, FR-26 and FR-27);
- an optional local model that only rephrases (Should, FR-28), off by default;
- no numbers from AI (AG-1) and no external AI services (AG-5).

The optional language model (FR-28) stays Should; its priority does not depend on the teacher, and its place among the Should items is decided in sprint planning (user decision, 2026-11-03).

Report D weighted five criteria: no invented numbers and easy to test 30, runs without a key 25, text quality 20, setup effort 15 and testability 10. The template scored 88 (the pick) and the hybrid of template plus optional model 82 (the runner-up). A local model alone scored 58, and a hosted free tier plus template 56. The 6-point gap is inside the scoring uncertainty, so the report treats template and hybrid as the Must and Should of one design. The hybrid wins if text quality or a visible AI feature counts for more, for example with a text-quality weight of about 40 and a lower no-invented-numbers weight. That matches the case where FR-28 becomes Must.

**Template approach (D-R1).**
- **Content:** fixed sentences state the method, the inputs, the calculation line, the warnings and the confidence label. Templates have "built-in faithfulness to input", a regulated style and quick response. The costs are a new template for each kind of message, and stiff wording [D1].
- **Snapshot tests:** these compare the generated text with committed expected output, so any change in wording fails a test until someone updates the snapshot on purpose [D5]. [D5] is the Jest documentation; with a Python stack, the same idea is one committed expected-text file per template. The research did not look at a Python snapshot library.
- **Suggested code seam (report D's hedge):** one function `explain(result) -> text` plus a numeric validator. The template implementation ships first. The model implementation sits behind a setting and falls back to the template.
- **Labelling (D-R4):** the EU Article 50 transparency duties apply from 2 August 2026 to AI text published on matters of public interest, with an exception for human editorial review [D4]. They probably do not apply to a school project, but the report still calls labelling good practice.

**Optional local model (FR-28).**
- **Runtime:** report D examined only Ollama, and the runtime is not decided. Ollama needs no account or key and installs from a download page or with a one-line script on macOS and Windows [D6][D7].
- **Endpoints:** Ollama listens on `localhost:11434`. Its generate endpoint accepts a JSON schema in the `format` field [D8][D9][D10].
- **Versions and offline use:** Ollama ships several releases a week (v0.40.13 on 2026-10-28), so a README can only say "current version" [D11]. Its documentation has no hardware table. It says Ollama runs locally but does not explicitly say it works offline [D8], so the docs do not confirm FR-28's "no internet connection". The FAQ also covers privacy and a cloud toggle [D8]. Addendum note: under AG-5, only models running on the machine qualify.
- **Model's role (D-R2):** the application inserts every number. The model rephrases the text around named placeholders. It may not supply, compute or change a number or placeholder. It may not replace the template path, need a key, or act as the number checker.
- **Detecting a missing model:** `GET /api/tags` lists the installed models, so the app can check before calling the model [D15].
- **Error behaviour:** a missing model returns 404. An error in the middle of a stream arrives inside a 200 response, so a 200 status alone does not prove success [D14]. The docs do not say what happens when the server is stopped (inference: the client gets a connection failure). FR-28 and AG-3 send all of these cases, a timeout and a rejected text to the template explanation, without an error. No source measured how fast a small model answers on a laptop, so the timeout, and how it fits NFR-8's 2-second target, are architecture choices.
- **Structured output does not guarantee correct values:** Ollama advises putting the schema in the prompt as well, setting temperature 0, and validating the parsed result with Pydantic or Zod [D10]. A valid structure only fixes the shape. Google states that schema-valid output "can still be semantically wrong", and that the application has to validate the values [D23]. The OpenAI and Ollama pages that were read say nothing either way [D28][D10].
- **Why each label and value are checked together (FR-28):** in summaries of financial reports written by language models, about 5% of the numbers were wrong. The most common error was a real number in the wrong context: context mismatch 1.59 to 3.28%, against fabrication 0 to 0.81%, for models from 2023 [D2]. A check that every number appears somewhere in the input misses that error. The same authors found GPT-4 unreliable as an automatic number checker [D2]. Restricting a model to provided data reduces hallucinations but does not eliminate them [D3].
- **Proof-carrying numbers:** a preprint proposes that the model writes each number as a token tied to a structured claim. The renderer, not the model, then verifies each claim under a stated policy: exact equality, rounding or tolerance [D19]. D-R2 rests on this pattern. Addendum note: FR-28 rejects text where a number "differs from the template explanation", which amounts to an exact-equality policy.

**Model candidates (open, PRD §10 question 5).** Sizes are from the Ollama library pages as of 2026-11-01.

| Model (Ollama library) | Size | Licence and obligations | Notes |
|---|---|---|---|
| llama3.2 1B / 3B | 1.3 GB / 2.0 GB [D12] | Llama 3.2 community licence (read for 3B): distributing requires "Built with Llama" attribution on related UI or documentation; access on Hugging Face requires approval [D16] | The library page calls 3B strong at instruction following and summarisation; no independent measure [D12] |
| gemma4 e2b | 4.6 to 7.5 GB [D13] | Apache 2.0 according to Google's blog of 2026-04-02 [D18], not confirmed on the Ollama model page; older Gemma models use the custom Gemma Terms of Use [D17] | None |
| Ollama quickstart example | about 7.2 GB; needs about 8 GB of memory [D6] | Not stated | Ollama publishes no hardware table [D8] |

D-R5 recommends naming the chosen model and its licence in the README. The options are a 2 GB model such as Llama 3.2 3B with the "Built with Llama" attribution, or Gemma 4 under Apache 2.0 once that licence is confirmed on the model page.

**Why hosted free tiers are not used.** The PRD rules out hosted AI services (AG-5, §7), and NFR-1 and FR-28 exclude API keys and paid services. Report D gives these reasons (D-R3):
- **Terms in the EEA:** in the EEA, Switzerland and the UK, Gemini's data terms for paid services apply, and apps offered there may use only paid services. The free tier is therefore probably unavailable to Norwegian users (inference: Norway is not named) [D22]. Google uses free-tier content to improve its products, and humans may review it [D20][D22].
- **Age limit:** Gemini API users must be 18 or older [D22].
- **Unstable or unconfirmed limits:** Gemini shows its rate limits only inside AI Studio [D21]. Blog posts say its free quotas were cut in December 2025, but they disagree and none was opened (low confidence). Groq shows only Developer-plan limits [D24]. OpenRouter's free models allow 20 requests per minute and 50 per day without bought credits [D25]. Hugging Face gives free users no monthly credits [D26], and Anthropic lists no free tier [D27]. Free tiers have changed before and can change again.
- **No optional hosted setting:** D-R3 suggests a separate optional setting with `.env.example` for a group that wants a hosted tier anyway. That does not apply to version 1, because under AG-5 no data goes to external AI services.

## 4. Rejected alternatives and why

- **Tukey fences or the Hampel filter instead of the 2 × median rule (R-10).** Tukey fences lie 1.5 or 3 × IQR beyond the quartiles [A21], but FPP3 (the forecasting textbook) applies them to what is left after a robust STL decomposition, not to raw sales, and prefers 3 × IQR [A13]; used as intended, they need a decomposition that cannot be checked by hand. The Hampel filter (rolling median ± 3 × 1.4826 × MAD) [A14][A15] fails like the brief's rule when the MAD is 0 (inference), so it also needs a zero guard. The PRD keeps the brief's rule as a project-defined rule with the zero-baseline guard that A-R3 asks for, tested by E8 to E10. FR-16 includes unusual weeks by default, which fits FPP3's warning that replacing outliers without knowing why they occurred is "a dangerous practice" [A13].
- **Ratio-to-moving-average indices or STL instead of the simple seasonal index (R-14).** Ratio-to-moving-average indices divide each week by a centred 2×52 moving average, which loses 26 weeks at each end [A7][A8]; with 104 weeks that leaves one ratio per week number, so a single stockout or promotion week feeds straight into its index (inference). FPP3 says classical decomposition "is not recommended" and is not robust to unusual values [A7]. STL and Fourier terms handle the 52.18-week year but cannot be checked by hand [A9][A10], and Holt-Winters needs m − 1 initial seasonal parameters, which is 51 for weekly data [A11]. The PRD's index uses up to two values per week number and ignores trend (§5.5). Report A names seasonal naive (same week last year) as the benchmark any seasonal method should beat [A2]; the PRD does not require that comparison.
- **Prediction intervals instead of fixed-percentage scenarios (R-7).** An interval is forecast ± c × σ(h), with c = 1.96 (95%) or 1.28 (80%) if errors are normal, and it widens with the horizon; for exponential smoothing, σ(h)² = σ² × [1 + α² × (h − 1)] [B8][B9]. It needs a history of forecast errors and an assumption about their distribution, and in one 2010 lab study, 50% or 95% intervals did not lead to better production decisions than a single forecast [B12]. The PRD keeps what-if scenarios that are not probabilities and do not widen with the horizon; B-R3 advises basing any later statistical range on forecast error [B8].
- **Statistical safety stock z × σ × √(T + L) instead of the percentage margin (R-8).** It needs a service-level target (z), a standard deviation σ and a lead time [B1][B2][B5][B7]; v1 models no lead time (§7), and whether σ should come from demand or from forecast error is unresolved (B-Q3). R-8 is a simplified version of the standard order-up-to policy [B2][B3][B5] (inference): review period T = 1 week, lead time L = 0, a percentage instead of z × σ × √(T + L), and stock on hand instead of inventory position, which match only when nothing is on order. The closest finding is that days-of-cover rules are easy to communicate but "rarely optimal", though acceptable when data is unreliable [B1]; B-R2 keeps the margin as a rule of thumb and names z × σ as a possible later improvement.
- **MAPE instead of MAE (FR-34).** MAPE (mean absolute percentage error) is undefined when any actual value is 0, extreme near zero, and penalises over-forecasts less than under-forecasts [B10]; zero-sales weeks occur in the reference examples (E10). FPP3 recommends MASE and advises against sMAPE [B10]. The PRD keeps MAE (mean absolute error) as a Could (B-R5).
- **SES start value by optimisation instead of the first observation (R-4).** For simple exponential smoothing (SES), FPP3 estimates the starting level by optimisation, which cannot be done by hand [A1]. NIST lists starting values that can be checked by hand: the first observation, or the average of the first four or five [A3]. The PRD takes the first calculation week (A-R1).
- **Imputing stockout weeks instead of leaving them out (R-1, FR-15).** When stock runs out, recorded sales understate true demand [A18][A22]. FPP3's options for missing values are to use only the data after the last gap, or to interpolate [A13]. A 2025 preprint argues that stockouts are not missing at random, so ordinary imputation is not enough [A22], and the only survey found on reconstructing true demand concerns airline revenue management and was read as an abstract only [A19]. The PRD leaves stockout weeks out and looks further back, which A-R4 calls a design decision with partial support.
- **Croston's method for products with many zero weeks.** It is the standard method for products that often sell nothing in a week, but its equations were not retrieved, and report A leaves it out of v1 [A23]. The PRD uses only moving average and exponential smoothing, with the zero-baseline guard in R-10.
- **Order-soon status from weeks of cover against a user-set threshold (B-R4).** R-12 gives a product order-soon status when its suggested order quantity is above 0, and uses weeks of cover only for sorting, so no extra setting is needed. Addendum note: for a positive forecast, this equals a weeks-of-cover threshold of 1 + safety margin (1.1 weeks at the default 10%). [B4] gives example thresholds of 2 to 8 weeks, with the advice that lead time should be shorter than the cover; v1 models no lead time (§7).
- **Hosted AI APIs.** AG-5 and §7 exclude them. They need an account and a key, the Gemini free tier is probably unavailable in the EEA and requires users aged 18 or older, and free limits are unstable or unconfirmed [D20][D21][D22][D24]-[D27]. Details are in §3.
- **FastAPI (65).** It is still at version 0.x and marked Beta (0.162.0) [C9]. It logs users in with tokens (JWT), using pwdlib and Argon2, instead of cookie sessions [C10], and it needs extra packages: SQLModel, pwdlib, PyJWT and httpx [C9][C10][C11]. It scored 3 on setup and 2 on login plus database, against Django's 4 and 5.
- **Next.js (50).** It needs the most separate parts for this app (an auth library or hand-written sessions, an ORM or database driver, a test runner and a chart library) and Node 20.9 or newer [C24][C27]. Version 16 removed synchronous access to cookies and request parameters and renamed middleware to proxy [C25], and its frequent security releases (one announced for 2026-11-03) give it the highest maintenance cost [C33]. Around it, Recharts 3.10.1 has no confirmed support for React 19 or Next.js [C34], `better-sqlite3` is a native module with unstated build requirements [C31], `node:sqlite` is still a release candidate [C32], Auth.js is now maintained by the Better Auth team [C28][C29], and Vitest does not support async Server Components [C26].

**Deliberately set to Could, not rejected.** Two items were placed at Could on purpose during planning: settings per product (FR-23), and saving adjusted order quantities between sessions with an approved mark per product (FR-31). Until they are built, one company-wide set of settings applies to every product and the screen says so (FR-20 to FR-22). Adjustments last for the current session only (UJ-1 priority note). Like every Should and Could item, they start only after the Must scope passes SM-1 and SM-3 (DR-6, SM-C2).

## 5. Evidence quality

| Report | Topic | Verification | Main source base |
|---|---|---|---|
| A | Forecasting methods, seasonality, outliers | 4 of 8 load-bearing claims independently verified | Mostly one textbook (FPP3) and a few web pages; several full texts could not be fetched |
| B | Safety stock and order quantity | 3 claims verified, 4 unverified | Vendor pages and a short university tutorial |
| C | Technology stack | 2 claims verified, 5 unverified | Each candidate's own official documentation, read through a fetch tool that summarises pages |
| D | Explanations without a paid API | 0 claims verified, 6 unverified; no recommendation independently verified | Preprints, vendor documentation and official terms |

- **Inventory rules rest on vendor sources.** Every inventory-policy source in report B is a vendor page or a short university tutorial. One family of vendors supplies the order policy, the safety-stock formula and the weeks-of-cover measure. No textbook or professional-body source (such as ASCM) was readable, and [B6] (2023) is already out of date. No source supports a percentage safety margin or fixed-percentage scenarios. PRD §10 question 4 records this gap (B-R6).
- **Several forecasting rules are project-defined.** The outlier, level-shift and seasonal-index rules, and every threshold, have no source (A-R3, A-R5, A-R6). Leaving stockout weeks out has partial support (A-R4). The variance formula for exponential smoothing and the MAPE zero-demand problem rest on FPP3 alone (A-Q5, B-Q4).
- **Reference examples:** the PRD's E1 and E2 match report A's worked examples. E3 to E30 have no research example and rest on the group's own hand calculation, recomputed independently during review (PRD §5.7, DR-3).
- **AI-assistant fit is not evidenced.** No benchmark or statement was found that measures coding assistants on Django, Flask or FastAPI. The only related item is Vercel's own statement about `AGENTS.md` for Next.js [C24]. Every candidate scored 3, so this 20-point criterion did not separate them. C-R6 asks for this to be recorded as a known limitation in the process documentation (DR-5).
- **Matrix scores are judgements.** The 1 to 5 scores and the weights in reports C and D are the reports' own. Both margins (Django 83 against Flask 80, template 88 against hybrid 82) are inside the stated scoring uncertainty. No source measured learning time, and the licence terms of the stack candidates were not checked.
- **Explanation evidence is thin or dated.** The number-error figures come from 2023 models and show the type of error, not today's rate [D2]. The strengths of templates come from a qualitative preprint survey without error rates [D1]. The guardrail pattern rests on one preprint [D19]. No source measured small local models on this task; the claim about the 3B model's quality is the vendor's own [D12].
- **Inferences, not findings:** that Gemini's EEA terms cover Norway [D22]; that a stopped Ollama server shows up as a connection failure; the Django README sequence [C15]; R-8 as a simplified order-up-to policy; the one-ratio-per-week problem; and the Hampel filter failing when the MAD is 0.
- **Still open or not covered:** Django's PBKDF2 iteration count [C16]; an official Django pattern for tying records to a company; which small model gives acceptable explanations, and how fast. The research also did not cover Chart.js support for the NFR-7 markings, the 2-second targets in NFR-8, or whether the SQLite that ships with Python on macOS and Windows meets Django 6.1's 3.37 minimum.
- **Dates to re-check sources:**
  - By 2026-12-01, which is also the submission deadline (DR-6): stack version claims [C1][C9][C13][C24][C33][C34], and the Ollama version and model sizes [D11]-[D13].
  - By 2027-02-01: hosted-tier terms and limits [D20]-[D22] and [D24]-[D27].
  - By 2027-04-21: report B's claims about vendor practice.
  - By 2027-05-01: signals about library maintenance [C7][C8][C29] and report A's software documentation. After this date, re-check reports C and D as a whole before acting on them.
  - By 2027-11-01: the stockout preprint [A22].
  - Already older than the reports' age limit: [B6] and the number-error study [D2].

## 6. Rule Rationale

The PRD (§5) states the rules; this section keeps the reasons and the alternatives that were considered, so that the PRD stays short without losing the professional content.

- **R-1 Valid weeks (partly supported).** The research found that stockout weeks are usually treated as missing data, but no source recommends this exact simple rule, and one preprint argues that stockouts are not missing at random [A22].
- **R-4 Start value of exponential smoothing.** The first observation is one of the start values listed in the NIST/SEMATECH handbook, and it can be checked by hand; the textbook FPP3 estimates the start value by optimisation, which cannot. No source gives a standard smoothing factor; the default 0.3 comes from the Product Brief.
- **R-10 and R-11, why the baseline leaves out unusual weeks.** If it did not, a lasting rise would raise the median after two weeks, the third high week would not be flagged, and R-11 could never trigger.
- **R-10 and R-11, why a single forward pass.** The calculation review found that, without a defined processing order, the same data could give a base forecast of 51.0 or 70.333 (PRD E15). Reclassifying a run as a level shift at the moment its third unusual week appears gives one answer and compares later weeks with the new level.
- **R-10 status.** The "2 × the median of the last 3 weeks" threshold comes from the Product Brief, and the research found no source for it. Tukey fences (1.5 or 3 × the interquartile range) and the Hampel filter are the established alternatives (§4). The rule is kept because it is simple to explain and to check by hand, and it is tested with PRD E8 to E10, E15, E16, E18 and E19.
- **R-12 Order-soon status.** A user-set weeks-of-cover threshold, which research report B suggested, was considered and not chosen, to keep the settings simple; order-soon status follows directly from a suggested order quantity above 0.
- **R-16 Confidence label.** Warnings about stockout weeks, unusual weeks and level shifts count only in the recent period of 12 weeks, so that one old event does not keep a product at «middels» for two years. «Høy» requires 104 weeks of sales history and at least 100 valid weeks (user decision, 2026-11-03), so that a few old stockout weeks do not make «høy» unreachable.
- **Seasonal adjustment as Should.** The Product Brief and the teacher suggested season in version 1, and the user first wanted seasonal variation to affect the calculation. It was moved to Should to protect the core flow before the deadline, because R-14 is the most demanding rule.

## 7. Changes from the Product Brief

Moved from the PRD on 2026-11-03.

The Product Brief (approved 2026-10-14) proposed the rules "to be validated during BMAD planning". Planning changed or added the following, with the rationale recorded in the decision logs:

- **Period and horizon:** the period is defined as a week (orders are placed weekly), and the forecast horizon is the three weeks after the latest data week.
- **Order quantity:** the brief's "suggested planning quantity" is now the suggested order quantity for next week: week-1 normal forecast plus safety margin minus stock on hand, never below 0, rounded up. Stock on hand was added to the data.
- **Data quality:** stockout weeks, valid weeks and calculation weeks were added; stockout weeks are left out of the calculation.
- **Outlier rule:** the brief's "2 × the median of the three preceding periods" is kept but made precise (baseline without unusual weeks, single forward pass, zero-baseline guard, first weeks not checked), and the level shift was added.
- **Trust:** the old-data warning, warnings and notes, the recent period, the confidence label, order-soon status and weeks of cover were added.
- **Settings:** settings are company-wide and saved; the safety margin got a default of 10% (0% to 100%), the scenario percentage a range of 0% to 50%, and unusual weeks are included by default.
- **Exponential smoothing:** the start value and the rounding rule were fixed.
- **Season:** the seasonal adjustment was specified as a simple index and made Should, with stated limitations, plus a seasonal-pattern warning.
- **AI role:** a template explanation in Norwegian is Must; an optional local language model is Should; hosted AI is excluded.
- **Purchase planning:** adjusting order quantities and the combined order overview were added as Should; saving adjustments, approval and CSV export as Could.
- **Data:** the data is read-only in the app; only settings and adjusted order quantities change.
- **User interface:** Norwegian, with the visible forecast calculation and order calculation line.
- **Deadline:** 1 December 2026.

## 8. Sources

The four research reports. Each has a source list giving the publisher, date and confidence for every [n].
- A, forecasting methods, seasonality and outliers: `_bmad-output/planning-artifacts/research/academic-lit-forecasting-methods-seasonality-outliers-2026-11-01/research.md`
- B, safety stock and order quantity: `_bmad-output/planning-artifacts/research/domain-safety-stock-and-order-quantity-2026-11-01/research.md`
- C, technology stack: `_bmad-output/planning-artifacts/research/technical-technology-stack-selection-2026-11-01/research.md`
- D, explanations without a paid API: `_bmad-output/planning-artifacts/research/technical-explanation-without-paid-api-2026-11-01/research.md`

Details from reports A and B come from `extract-research-ab.md` in this folder. Figures from reports C and D were checked against the reports themselves.
