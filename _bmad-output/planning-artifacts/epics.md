---
stepsCompleted: ["step-01-validate-prerequisites", "step-02-design-epics", "step-03-create-stories", "step-04-final-validation"]
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md
  - _bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/addendum.md
  - _bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-08/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-06/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-06/EXPERIENCE.md
---

# Prognose - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Prognose, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

IDs follow the PRD (§4). Priority in brackets. The calculation rules R-1 to R-17 and the reference examples E1 to E30 (PRD §5) are the answer key for every calculation story.

- FR-1: A user logs in to their company with customer number and password. [Must]
- FR-2: A logged-in company sees and changes only its own products, sales history, stock on hand, settings and order quantities. [Must]
- FR-3: Synthetic dataset for two test companies (10 to 50 products each) with known patterns, rule test products built from the reference examples, a deterministic generator script and documented logins. [Must]
- FR-4: Products, sales history, stock on hand and settings persist between sessions: a SQLite file locally, PostgreSQL when published. [Must]
- FR-5: Moving average over the last N calculation weeks (window 2 to 12, default 3). [Must]
- FR-6: Exponential smoothing over the calculation weeks in time order (smoothing factor 0.1 to 0.9, default 0.3; formula and start value per R-4). [Must]
- FR-7: Week forecasts for weeks 1 to 3 after the latest data week, with the fixed note when they are equal. [Must]
- FR-8: No forecast for a product without enough data, with the reason. [Must]
- FR-9: Seasonal adjustment per R-14 when «Sesongjustering» is on. [Should]
- FR-10: Normal, optimistic and pessimistic scenario for each horizon week from the week forecast and the scenario percentage (R-7). [Must]
- FR-11: Suggested order quantity for next week from the week-1 normal forecast, the safety margin and the stock on hand (R-8). [Must]
- FR-12: Order calculation line on the product screen: forecast, margin as percentage and amount, stock on hand, unrounded result and suggested quantity. [Must]
- FR-13: Order quantity for the optimistic and the pessimistic scenario (R-8). [Should]
- FR-14: Overstock note «Lagerbeholdningen dekker forventet behov neste uke.» when the suggested quantity is 0 and the stock on hand is above 0. [Should]
- FR-15: Stockout weeks are never used in any calculation. [Must]
- FR-16: Unusual weeks are found with R-10, marked, and included or excluded according to the company setting. [Must]
- FR-17: Three or more unusual weeks in a row are a level shift (R-11). [Must for the calculation and the confidence label; Should for the warning text]
- FR-18: Old-data warning when the latest valid week is more than 8 weeks before the latest data week, counted by position. [Must]
- FR-19: Every product gets a confidence label with a plain-language Norwegian reason (R-16). [Must]
- FR-20: One set of company-wide settings with the defaults and ranges in PRD §11. [Must]
- FR-21: A settings change takes effect at once for every product and can be made from the product screen. [Must]
- FR-22: Settings are saved per company between sessions. [Must]
- FR-23: Per-product settings that override the company settings. [Could]
- FR-24: Product overview after login: product number, name, stock on hand, week-1 normal forecast, suggested quantity, weeks of cover, confidence label and order-soon status, ordered by R-12. [Must]
- FR-25: Product screen with a chart and the decision details. [Must]
- FR-26: Template explanation in Norwegian, built only from the calculation result. [Must]
- FR-27: The explanation sits in its own «Forklaring» area below the calculated numbers. [Must]
- FR-28: Optional local language model rephrases the template explanation; off by default, with fallback to the template. [Should]
- FR-29: The user can replace the suggested order quantity with an adjusted order quantity. [Should]
- FR-30: Combined order overview. [Should]
- FR-31: Adjustments saved between sessions, and products can be marked as approved. [Could]
- FR-32: Export of the combined order overview as CSV. [Could]
- FR-33: Note when stock on hand plus the suggested quantity will not last through weeks 2 and 3. [Could]
- FR-34: Forecast accuracy (MAE of past one-week forecasts) on the product screen. [Could]
- FR-35: The product screen shows how the base forecast and the week forecasts were calculated, so they can be checked by hand. [Must]
- FR-36: Seasonal-pattern warning (R-17) when the forecast does not use a seasonal pattern the product shows. [Should]

### NonFunctional Requirements

From PRD §6 and §9. All are part of the Must scope (§8.1).

- NFR-1: Every Must feature runs on one computer without paid services, API keys or third-party accounts; the local app works offline after installation (no CDN); the README covers macOS and Windows; the published version uses only free plans.
- NFR-2: All rules live in one calculation module with no dependency on the UI or the database; unit tests cover every rule and every applicable reference example; one documented test command.
- NFR-3: Established password hashing; the company is checked on the server on every request; the session secret is created by the load command into a gitignored file (a Vercel environment variable when published); no secrets in the repository.
- NFR-4: Synthetic data only; no personal data or local paths in the repository or saved AI sessions; history scan before submission.
- NFR-5: Norwegian (bokmål) everywhere; decimal comma; whole-number percentages with «%».
- NFR-6: Desktop browser; no horizontal page scrolling from 1024 px; FR-25 content visible at 1366 × 768; no mobile layout required.
- NFR-7: Chart markings differ by more than color, with a legend.
- NFR-8: With 50 products of 104 weeks, the overview and product screen open, and settings changes update, within 2 seconds locally; the first published request after idle may be slower.
- NFR-9: One web application and one database: SQLite locally, PostgreSQL when published.
- NFR-10: Decimal comma or point accepted; invalid input refused with a Norwegian message and the previous value kept; no stack traces or debug pages; Norwegian «not found» page; resubmits, reloads and back are safe.
- NFR-11: WCAG 2.2 AA contrast, full keyboard use with visible focus, visible labels, `lang="nb"`, and a chart text alternative (summary and table).
- AG-1 to AG-6: no numbers from AI; the Must explanation is template-based; the optional local model is off by default, only rephrases and falls back; AI text is labeled and kept apart; no data to external AI services; AI use in development is documented.
- DR-1: README with screenshots, prerequisites, macOS and Windows setup, test logins, load command, «Prøv selv», test-product table, tests, optional model, folders, limitations, and the published address with the publishing steps.
- DR-2: Documented repository layout, `.gitignore`, `.env.example`, one formatter and one linter, exact pins in one file.
- DR-3: Reference spreadsheet with E1 to E30 and the rule test products; the tests use the same inputs and expected results.
- DR-4: Deterministic seed generator and one idempotent load command that resets the data.
- DR-5: Decision and AI-session records, an AI steering log (at least five cases, at least one per epic), traceability from FR to story, test and commit, and the Product Brief updated after approval (PRD §10, question 6).
- DR-6: Deadline 1 December 2026; Should and Could items start only after the Must scope passes SM-1 and SM-3.
- DR-7: One branch and one reviewed pull request per story; issues for defects; small commits; Definition of Done (tests and linter pass, no dead code, docs and status table updated, PR reviewed).
- DR-8: Status table of every FR at submission.
- DR-9: QA log of defects in AI output; manual checklist for NFR-6, NFR-7, NFR-8, NFR-11, SM-2 and SM-9 on the final commit.
- DR-10: Published on Vercel from `main` with PostgreSQL on free plans; shared demo; debug off; secrets as Vercel variables; no local model there.
- SM-1 to SM-9 (targets): reference examples pass (Must set E1–E13, E15–E21, E23, E24, E28, E29); setup from the README in at most 15 minutes and offline start; automated core-flow web test; two-account isolation test; persistence; explanation integrity; every warning and label triggered by a test product; traceable process; published version works.
- Open questions to close during the build (PRD §10): the order of the Should items (sprint planning); the 15-minute setup test on clean macOS and Windows, also offline; textbook sources for the inventory rules, or the gap stated in the process documentation; the project-defined rules checked against the test products; the local model and its license if FR-28 is built; the Product Brief update.

### Additional Requirements

From the architecture spine (AD-1 to AD-16). No starter template: Epic 1 Story 1 creates the Django project skeleton and publishes it on Vercel with Neon.

- AR-1 (AD-1 to AD-3): pure `forecasting/` and `explanation/` packages with no Django imports; `forecasting.compute_product(...)` returns a frozen `ProductResult`, and `sort_overview` applies R-12; results are computed on every request and never stored.
- AR-2 (AD-4): R-9 rounding only in `forecasting/rounding.py`; Norwegian number formatting only in `forecasting/display.py`.
- AR-3 (AD-5): custom user model `accounts.Company` with `customer_number` as login field, created before the first migration; PBKDF2; `LoginRequiredMiddleware`, with only the landing/login view exempt.
- AR-4 (AD-6): all company data through `planning/queries.py`, filtered by the logged-in company; `Http404` outside the company; the two-account test covers every view and list.
- AR-5 (AD-7): weeks identified by position; products addressed as `/produkter/<varenummer>/`, unique per company.
- AR-6 (AD-8): form POST with redirect for login, logout, settings and adjustments; GET filters; one `CompanySettings` row per company; defaults and ranges defined once in `forecasting/settings.py`.
- AR-7 (AD-9): adjustments in the database-backed Django session, only through `planning/adjustments.py`.
- AR-8 (AD-10): `explanation.explain(result)`, with snapshot tests of the template text (addendum §3); the optional model only through `explanation/rephrase.py` with a 10 s timeout and the number-and-label check. Runtime notes and model candidates are in addendum §3; the choice is open (PRD §10, question 5).
- AR-9 (AD-11): Django templates; one stylesheet with the DESIGN.md tokens; self-hosted Albert Sans; vendored Chart.js 4.6.1; `static/js/charts.js` is the only JavaScript and draws from `json_script` data.
- AR-10 (AD-12): `data/generate_seed.py` writes versioned seed files to `data/seed/`; `python manage.py load_seed` resets idempotently and creates the gitignored session-secret file.
- AR-11 (AD-13): local run with `runserver --insecure` and SQLite; on Vercel (`VERCEL` set) DEBUG off, hosts from Vercel's system variables, secure cookies, required `SECRET_KEY` and `DATABASE_URL`; Norwegian 404 and 500 pages; `nb` and `Europe/Oslo`.
- AR-12 (AD-14): `python manage.py test` runs everything; calculation tests read `reference/examples.json`; core-flow and isolation tests use the Django test client; Ruff lints and formats.
- AR-13 (AD-15): `DATABASE_URL` selects PostgreSQL through psycopg (`sslmode=require`, `CONN_MAX_AGE = 0`, `DISABLE_SERVER_SIDE_CURSORS`); ORM and migrations only; tests on SQLite; no file writes at request time.
- AR-14 (AD-16): Vercel Hobby owned by one group member; only `main` deploys (`vercel.json`: region `fra1`, `git.deploymentEnabled`); migrations and seed loading only from the owner's PC with the unpooled URL.
- AR-15 (Stack): Python 3.13, Django 5.2.19, psycopg[binary] 3.3.8, Chart.js 4.6.1, Ruff 0.17.4; `requirements.txt`, `.python-version`, `vercel.json` and `ruff.toml`; no `pyproject.toml`; Neon PostgreSQL in Frankfurt.
- AR-16 (Conventions): checks (`test`, `ruff check`, `ruff format --check`) run locally before every pull request; no CI service; the first story proves publishing; Must first.
- AR-17 (Deferred): in the first story, confirm that the course organization allows the Vercel GitHub app and that Hobby does not block deployments (fallbacks per the spine); before submission, re-check the stack versions, the free-plan terms and, if FR-28 is built, the Ollama version and model sizes (addendum §5).

### UX Design Requirements

From DESIGN.md and EXPERIENCE.md. The spines win over the mockups (`mockups/key-landing.html`, `mockups/key-produktoversikt.html`).

- UX-DR1: Implement the DESIGN.md tokens as CSS custom properties in one stylesheet: 22 colors, 19 typography tokens, `rounded` (xs, sm, md, full) and the spacing scale.
- UX-DR2: Self-host Albert Sans (OFL) with a fallback stack (state «Fonts unavailable»).
- UX-DR3: Landing page with login: wordmark, map frame, login panel with text fields and primary button, «Prøv selv»; the one login error «Feil kundenummer eller passord.» announced with `role="alert"`; a skip link to the login.
- UX-DR4: App rail navigation with the active nav item, and a skip link to the content.
- UX-DR5: Produktoversikt: product table with group rows and row hover, status sentence, GET filters, confidence labels (high, medium, low as shape plus word), Bestill snart with visually hidden text, the adjusted tag, and the empty states «No data loaded» (with the `load_seed` command) and «Filter without hits».
- UX-DR6: Produktside per the 1366 × 768 wireframe: course chart (Chart.js) with Tegnforklaring and a data-table toggle, calculation line, order figure, scenario strip, calculation steps, Varsel and Merknad, settings as a segmented control with the settings confirmation (`role="status"`), and the Forklaring area.
- UX-DR7: Calculation display rules: the order calculation line format (with «(lageret dekker behovet)» for negative raw values), the moving-average and smoothing calculation formats, the excluded weeks with reasons, «Uke 1 · uke 46» horizon labels with the equal-forecast note, the no-forecast layout with «Du bestemmer bestillingen selv.», R-9 decimals and «–» for weeks of cover when the week-1 forecast is 0.
- UX-DR8: Samlet bestillingsoversikt (Should) per its wireframe: order table, adjusted tag, and the invalid-adjusted-quantity state.
- UX-DR9: Ikke funnet page in Norwegian with a link to the product overview.
- UX-DR10: The 18 state patterns: logged out, login error, no data loaded, filter without hits, product without forecast, stock covers next week, unusual weeks excluded, level shift, old data, setting not in use, invalid setting, setting changed, seasonal adjustment not possible, adjusted quantity, invalid adjusted quantity, not found, resubmit or back, fonts unavailable.
- UX-DR11: Voice and tone: binding Norwegian labels and fixed strings, «uke 46» in running text, show the working, «Ingen tall kommer fra KI.»
- UX-DR12: Interaction primitives: everything reachable by Tab in reading order; Post/Redirect/Get for settings and adjustments; pages work without client-side code except the charts; touch targets of at least 44 px; no drag and drop, settings dialogs, auto-refresh, timed confirmations or order placement.
- UX-DR13: Accessibility floor: WCAG 2.2 AA; `lang="nb"`; visible labels; a 3 px `magenta-ink` focus ring; each chart has a text summary (caption or `aria-label` on the canvas) and a data table; status never by color alone; `prefers-reduced-motion` skips the course animation; table semantics kept on small screens.
- UX-DR14: Responsive rules from the two tables: Landing (901 px and above, 1100, 900, 760, 700 and 640 px and below) and App (1181 px and above, 961–1180, 960, 700, 640 and 560 px and below); the product table scrolls inside its frame between 961 and 1023 px.
- UX-DR15: Flow 1 (UJ-1, Mounia's Monday planning) and Flow 2 (the examiner's «Prøv selv») are the end-to-end acceptance paths.
- UX-DR16: Run the Impeccable finish review and design documentation on the real build.

### FR Coverage Map

- FR-1: Epic 1 - Login with customer number and password
- FR-2: Epic 1 - Company data isolation
- FR-3: Epic 1 - Synthetic dataset and generator
- FR-4: Epic 1 - Data stored between sessions (SQLite locally, PostgreSQL published)
- FR-5: Epic 2 - Moving average
- FR-6: Epic 2 - Exponential smoothing
- FR-7: Epic 2 - Three-week horizon
- FR-8: Epic 2 - Insufficient data
- FR-9: Epic 5 - Seasonal adjustment
- FR-10: Epic 2 - Three scenarios
- FR-11: Epic 2 - Suggested order quantity
- FR-12: Epic 2 - Order calculation line
- FR-13: Epic 5 - Order quantity per scenario
- FR-14: Epic 5 - Overstock note
- FR-15: Epic 2 - Stockout weeks left out
- FR-16: Epic 2 - Unusual weeks
- FR-17: Epic 2 (calculation and confidence label) and Epic 5 (warning text) - Level shift
- FR-18: Epic 2 - Old-data warning
- FR-19: Epic 2 - Confidence label
- FR-20: Epic 3 - Company-wide settings
- FR-21: Epic 3 - Changes apply to all products at once
- FR-22: Epic 3 - Settings saved between sessions
- FR-23: Epic 5 - Settings per product (Could)
- FR-24: Epic 2 - Product overview
- FR-25: Epic 2 - Product screen
- FR-26: Epic 3 - Template explanation in Norwegian
- FR-27: Epic 3 - Explanation kept apart from the numbers
- FR-28: Epic 7 - Optional local language model
- FR-29: Epic 6 - Adjust an order quantity
- FR-30: Epic 6 - Combined order overview
- FR-31: Epic 6 - Save adjustments and mark as approved (Could)
- FR-32: Epic 6 - CSV export (Could)
- FR-33: Epic 6 - Stock not lasting through weeks 2 and 3 (Could)
- FR-34: Epic 5 - Forecast accuracy (Could)
- FR-35: Epic 2 - Forecast calculation
- FR-36: Epic 5 - Seasonal-pattern warning

## Epic List

Epics 1 to 4 are the Must scope. Epics 5 to 7 start only after the Must scope passes SM-1 and SM-3 (DR-6), and their order is set in sprint planning (PRD §10, question 1). Could items come last within their epic. Every story meets the Definition of Done in DR-7 and names the FR-n it implements, and its tests name the FR-n or E-n they verify (DR-5).

### Epic 1: Secure login and own data, published from day one
A user of a test company can log in, locally and on the published Vercel address, and see only their own products with the synthetic data loaded. The first story creates the Django skeleton and publishes it on Vercel with Neon.
**FRs covered:** FR-1, FR-2, FR-3, FR-4 (Must)

### Epic 2: Weekly forecast, warnings and order suggestion
The purchasing manager sees the product overview and opens a product screen with the forecast, scenarios, order calculation line, warnings, confidence label and forecast calculation, all checked against the reference examples.
**FRs covered:** FR-5, FR-6, FR-7, FR-8, FR-10, FR-11, FR-12, FR-15, FR-16, FR-17 (calculation and confidence label), FR-18, FR-19, FR-24, FR-25, FR-35 (Must)

### Epic 3: Tune the settings and read the explanation
The purchasing manager changes a company setting and sees every product update, and reads a Norwegian template explanation kept apart from the numbers. This completes the core flow (SM-3).
**FRs covered:** FR-20, FR-21, FR-22, FR-26, FR-27 (Must)

### Epic 4: The examiner can install, try and verify Prognose
The examiner follows the README («Prøv selv») locally or on the published address and checks the results against the reference spreadsheet. The group delivers the status table, the QA checklist and the Impeccable finish review. The last story runs on the final commit.
**Requirements covered:** DR-1, DR-8, DR-9, SM-2, SM-9; no further FRs (Must)

### Epic 5: Seasonal products and clearer decision notes
Forecasts can use seasonal adjustment, and the product screen adds the seasonal-pattern warning, the level-shift warning text, the order quantity per scenario and the overstock note.
**FRs covered:** FR-9, FR-13, FR-14, FR-17 (warning text), FR-36 (Should); FR-23, FR-34 (Could)

### Epic 6: Plan the week's purchases
The purchasing manager adjusts order quantities and reviews the combined order overview.
**FRs covered:** FR-29, FR-30 (Should); FR-31, FR-32, FR-33 (Could)

### Epic 7: Optional local AI rephrasing
When switched on locally, a language model rephrases the template explanation, with the number check and the fallback to the template.
**FRs covered:** FR-28 (Should)

## Epic 1: Secure login and own data, published from day one

A user of a test company can log in, locally and on the published Vercel address, and see only their own products with the synthetic data loaded. Also covers DR-2, DR-4, DR-10, AR-3 to AR-5, AR-10 to AR-17, UX-DR1 to UX-DR4 and UX-DR9.

### Story 1.1: Project skeleton running locally and on Vercel

As a group member,
I want the Django project skeleton to run locally and to deploy from `main` to Vercel with a Neon database,
So that publishing is proven in the first week and every later story deploys the same way.

**Acceptance Criteria:**

**Given** a fresh clone and Python 3.13
**When** the developer creates a virtual environment and runs `pip install -r requirements.txt`, `python manage.py migrate`, `python manage.py load_seed` and `python manage.py runserver --insecure`
**Then** a Norwegian start page (`lang="nb"`) loads on 127.0.0.1:8000 with SQLite and one stylesheet served from `/static/`
**And** this first version of `load_seed` only creates the gitignored session-secret file when it is missing, so no secret is hard-coded or committed; Story 1.2 adds the data (NFR-3, AD-12)
**And** `python manage.py test`, `ruff check` and `ruff format --check` pass

**Given** the repository
**When** it is inspected
**Then** it follows the structural seed in the architecture spine, with exact pins in `requirements.txt` (Django 5.2.19, psycopg[binary] 3.3.8, Ruff 0.17.4), `.python-version`, `ruff.toml`, `.env.example` and `vercel.json` (`"regions": ["fra1"]`, deployments from `main` only)
**And** `.gitignore` keeps out `db.sqlite3`, `staticfiles/`, the session-secret file and `.env`

**Given** AD-5
**When** the first migration is created
**Then** it already contains the custom user model `accounts.Company` with `customer_number` as the login field

**Given** a Vercel project owned by one group member and a Neon database in Frankfurt created from the Vercel dashboard
**When** a commit lands on `main`
**Then** Vercel deploys it, and the start page loads over HTTPS on the production address with DEBUG off, hosts from the Vercel system variables and the stylesheet from the CDN
**And** the owner has run `python manage.py migrate` against Neon from their PC with the unpooled URL, and the page reads from PostgreSQL without errors
**And** a push to any other branch creates no deployment

**Given** the published version
**When** `SECRET_KEY` or `DATABASE_URL` is missing
**Then** it stops with a clear error message instead of starting with defaults

**Given** an unknown address, locally or published
**When** it is requested
**Then** a Norwegian «ikke funnet» page with a link to the start page is shown, never a debug page (NFR-10, UX-DR9)
**And** the result of the account checks in AR-17 is recorded in the story's pull request

### Story 1.2: Synthetic data for two test companies

As an examiner,
I want two test companies with synthetic products and sales history that one command loads,
So that I can try Prognose on known cases without real data.

**Acceptance Criteria:**

**Given** `data/generate_seed.py`
**When** it runs twice
**Then** both runs write identical seed files to `data/seed/`, including the password hashes (fixed salts), and no plaintext password appears in them (FR-1, FR-3)

**Given** the seed files
**When** they are inspected
**Then** each of the two companies has 10 to 50 products, each with a product number, a name, a weekly sales history by position with year and week number, a stockout flag per week and a stock on hand
**And** most products have 104 weeks, every pattern listed in FR-3 is present, and the rule test products use the series of E1 to E4, E7 to E10 and E15 to E19
**And** this story creates only the product and sales-week models, with `varenummer` unique per company and weeks identified by position (AD-7)

**Given** an empty or loaded database
**When** `python manage.py load_seed` runs, once or several times
**Then** the database holds exactly the seed state, without duplicates or errors (DR-4)
**And** it still creates the gitignored session-secret file when it is missing (NFR-3)

**Given** loaded data
**When** the application is stopped and started again
**Then** all data is unchanged (FR-4, SM-5)

**Given** the published database
**When** the owner runs `load_seed` from their PC with the unpooled URL
**Then** the published version holds the same data
**And** the README documents the generator, the load command and the two test logins

### Story 1.3: Log in on the landing page

As a purchasing manager,
I want to log in with my customer number and password on the landing page,
So that I reach my company's data and nobody else's.

**Acceptance Criteria:**

**Given** the landing page
**When** it loads
**Then** it follows DESIGN.md, EXPERIENCE.md and `mockups/key-landing.html`: wordmark, map frame, login panel with visible labels, primary button and «Prøv selv», using the DESIGN.md tokens as CSS custom properties and self-hosted Albert Sans with a fallback (UX-DR1 to UX-DR3)

**Given** a test company's correct customer number and password
**When** the form is posted
**Then** the user is redirected to the product overview address, which this story creates as an empty placeholder page (FR-1)
**And** passwords are checked with Django's default PBKDF2 hasher, and no plaintext password appears in the database or the logs (NFR-3)

**Given** a wrong customer number or password
**When** the form is posted
**Then** the page shows only «Feil kundenummer eller passord.», announced with `role="alert"`, without revealing which of the two was wrong

**Given** a user who is not logged in
**When** any page other than the landing page is requested
**Then** the user is sent to the landing page (`LoginRequiredMiddleware`)
**And** logging out with a POST ends the session and returns to the landing page

**Given** a keyboard user
**When** they move through the landing page
**Then** a skip link leads to the login, every control is reachable by Tab in reading order with the 3 px focus ring, contrast meets WCAG 2.2 AA, and the layout follows the landing rows of the responsive table (UX-DR12 to UX-DR14)
**And** login works the same on the published address

### Story 1.4: See only my own company's products

As a purchasing manager,
I want the product overview to list only my company's products,
So that I can trust that I plan with my own data.

**Acceptance Criteria:**

**Given** a user logged in as test company A
**When** the product overview opens
**Then** it lists only A's products with product number, name and stock on hand, inside the app shell with the app rail and a skip link to the content (UX-DR4); Epic 2 adds the forecast columns
**And** a minimal product page at `/produkter/<varenummer>/` shows the product's number, name and stock on hand

**Given** the same product number in both companies
**When** company A opens it
**Then** A sees only its own product

**Given** a product number that belongs only to company B, or does not exist
**When** A requests its address
**Then** the response is the same Norwegian «ikke funnet» page (404), now with a link to the product overview, and shows none of B's data (FR-2, NFR-10)

**Given** any view that reads company data
**When** its code is reviewed
**Then** it reads only through `planning/queries.py` functions that take the logged-in company first (AD-6)
**And** an automated two-account test (Django test client) tries every view and list built so far as company A against company B's data and passes only if every attempt is refused (SM-4); later stories extend it

## Epic 2: Weekly forecast, warnings and order suggestion

The purchasing manager sees the product overview and opens a product screen with the forecast, scenarios, order calculation line, warnings, confidence label and forecast calculation, all checked against the reference examples. Uses the default settings from `forecasting/settings.py`; Epic 3 makes them changeable. Also covers DR-3, NFR-2, NFR-5 to NFR-8, NFR-11, SM-1, SM-7, AR-1, AR-2, AR-5, AR-9, AR-12, UX-DR5 to UX-DR7, UX-DR10, UX-DR13 and UX-DR14.

### Story 2.1: Weeks the forecast can trust

As a purchasing manager,
I want stockout weeks, unusual weeks and level shifts to be recognized by fixed rules,
So that a forecast is not distorted by weeks that do not show real demand.

**Acceptance Criteria:**

**Given** `reference/examples.json` with the inputs and expected results of E1 to E30 from PRD §5.7, and the reference spreadsheet in `reference/` with the same values (DR-3)
**When** the calculation tests run
**Then** they read their expected values only from that file (AD-14)

**Given** a sales history with stockout weeks
**When** the weeks are classified (R-1)
**Then** stockout weeks are not valid weeks and count in no threshold or calculation: E7 gives 4 valid weeks, and E16 gives 6 valid weeks with 3 stockout weeks left out (FR-15)

**Given** the valid weeks of a product
**When** the single forward pass of R-10 and R-11 runs
**Then** E8 marks weeks 4 and 5 as unusual, E9 marks weeks 4 to 6 as a level shift, E10 marks no unusual week, E15 marks weeks 4 to 6 as a level shift and week 7 as unusual, E18 a keeps 42 as normal while E18 b marks 43 as unusual, and E19 follows the baseline rule for the first weeks (FR-16, FR-17)

**Given** the unusual-week setting from `forecasting/settings.py` (default: included)
**When** the calculation weeks are built (R-2)
**Then** excluded unusual weeks stay valid weeks but leave the calculation weeks, and level-shift weeks always stay in
**And** the classification is part of the frozen `ProductResult` from `forecasting.compute_product`, and `forecasting/` imports no Django code (AD-1, AD-2)

### Story 2.2: Base forecast for the next three weeks

As a purchasing manager,
I want a base forecast with the moving average or exponential smoothing for weeks 1 to 3,
So that I know the expected demand that my order builds on.

**Acceptance Criteria:**

**Given** the moving average with window N (default 3, range 2 to 12)
**When** the base forecast is calculated (R-3)
**Then** it is the mean of the last N calculation weeks, looking further back past skipped weeks, and E1 (14.333), E7 (22.0), E8, E15 to E20 and E28 match (FR-5)

**Given** exponential smoothing with factor 0.3
**When** the base forecast is calculated (R-4)
**Then** E2 gives 13.790 and E17 gives 21.404, with stockout weeks skipped rather than treated as zero (FR-6)

**Given** a base forecast
**When** the horizon is built (R-5)
**Then** the week forecasts for weeks 1, 2 and 3 equal the base forecast, and only week 1 feeds the order quantity (FR-7)

**Given** too little data
**When** the forecast is calculated (R-6)
**Then** a product with fewer than 3 valid weeks gets no forecast and a warning about insufficient data (E11 a)
**And** with the moving average, a product with fewer calculation weeks than the window gets no forecast and a warning that names the window and the number of calculation weeks (E11 b, FR-8)

**Given** any calculated value
**When** it is rounded or formatted
**Then** `forecasting/` keeps full precision, R-9 rounding lives only in `forecasting/rounding.py`, and Norwegian display formatting only in `forecasting/display.py`, so E20 (10.25) is shown as «10,3» (AR-2, NFR-5)

### Story 2.3: Scenarios and suggested order quantity

As a purchasing manager,
I want the three scenarios and a suggested order quantity for next week,
So that I get a concrete order proposal that I can check.

**Acceptance Criteria:**

**Given** a week forecast and the scenario percentage (default 10 %)
**When** the scenarios are calculated (R-7)
**Then** E3 gives optimistic 15.767, normal 14.333 and pessimistic 12.900, and the pessimistic scenario is never below 0 (FR-10)

**Given** the week-1 normal forecast, the safety margin (default 10 %) and the stock on hand (R-13)
**When** the suggested order quantity is calculated (R-8, R-9)
**Then** E4 gives 11, E5 gives 70 (not 71), E6 gives 0 and E21 gives 1; the value is rounded to 6 decimals and then up once, is never negative, and a product without a forecast has none (FR-11)

**Given** the parts of the order calculation
**When** the line is formatted in `forecasting/display.py`
**Then** E4 reads «Prognose 14,3 + sikkerhetsmargin 10 % (1,4) − lager 5 = 10,77 → foreslått bestillingsmengde 11», E6 ends with «… = −40,00 → foreslått bestillingsmengde 0 (lageret dekker behovet)», and E21 ends with «… = 0,07 → foreslått bestillingsmengde 1» (FR-12)

**Given** the results of a company's products
**When** order-soon status, weeks of cover and order are set (R-12)
**Then** E13, E23 (weeks of cover «–» when the week-1 forecast is 0) and E24 match, and `forecasting.sort_overview` places products without a forecast right after the order-soon products

### Story 2.4: Warnings and confidence label

As a purchasing manager,
I want warnings and a confidence label with a reason for every product,
So that I know when a forecast should not be trusted.

**Acceptance Criteria:**

**Given** a product whose latest valid week lies far behind the latest data week
**When** the warnings are set (R-15)
**Then** E12 gives the old-data warning after 9 weeks, stating the number of weeks, and none after 8 weeks (FR-18)

**Given** stockout weeks, unusual weeks or a level shift in the recent period of 12 weeks
**When** the active warnings are set (R-15)
**Then** each counts as an active warning, unusual weeks count whether they are included or excluded, and a level shift counts for the label even though its dedicated warning text comes in Epic 5 (FR-15 to FR-17)

**Given** the active warnings and the history length
**When** the confidence label is set (R-16)
**Then** E29 a to g match, and the Norwegian reason names the deciding condition and lists the active warnings, for example «Middels: 1 uvanlig uke de siste 12 ukene.» (FR-19)

**Given** the seed data from Story 1.2
**When** `compute_product` runs for every test product
**Then** every Must warning and each of the labels «lav», «middels» and «høy» is triggered by at least one product (SM-7)
**And** every Must reference example in SM-1 now passes as an automated test

### Story 2.5: Product overview with forecasts and order status

As a purchasing manager,
I want the product overview to show the forecast, order proposal, weeks of cover and confidence for every product,
So that I see at once which products need an order this week.

**Acceptance Criteria:**

**Given** a logged-in company with products
**When** the product overview opens
**Then** it shows product number, name, stock on hand, week-1 normal forecast, suggested order quantity, weeks of cover, the confidence label (shape and word) and order-soon status (symbol and visually hidden text), per EXPERIENCE.md and `mockups/key-produktoversikt.html` (FR-24, UX-DR5)
**And** the products are ordered by `sort_overview` (E13, E24), and a product without a forecast shows the reason instead of a number

**Given** the filters and the status sentence in EXPERIENCE.md
**When** a filter is chosen
**Then** it works as a GET link, and a filter without hits shows its empty state
**And** a company without products sees «no data loaded» naming `python manage.py load_seed`

**Given** 50 products of 104 weeks
**When** the overview opens locally
**Then** it opens within 2 seconds (NFR-8), and every number is formatted by `forecasting/display.py`

**Given** widths from 560 px to 1440 px
**When** the overview is shown
**Then** it follows the app rows of the responsive table, the table scrolls inside its frame between 961 and 1023 px, and table semantics stay on small screens (UX-DR13, UX-DR14)
**And** the two-account test covers the overview's columns and filters

### Story 2.6: Product screen with chart and decision details

As a purchasing manager,
I want a product screen with a chart and every number behind the decision,
So that I can check the order proposal before I decide.

**Acceptance Criteria:**

**Given** a product with a forecast
**When** its product screen opens
**Then** the chart shows the sales history and the week forecasts with the three scenarios, and stockout, unusual and level-shift weeks each have a marker that differs by more than color, explained in the Tegnforklaring (FR-25, NFR-7)
**And** the chart has a text summary (caption or `aria-label`) and a data table that can be shown (NFR-11, UX-DR13)

**Given** the chart code
**When** the page loads, also offline
**Then** vendored Chart.js 4.6.1 and `static/js/charts.js` draw from `json_script` data, and every number shown comes as a display string from the server (AR-9)

**Given** the decision details
**When** the screen is read
**Then** it shows the stock on hand, the safety margin, the scenario strip with «Scenarioene viser hva som skjer hvis salget blir 10 % høyere eller lavere. De er ikke sannsynligheter.» (with the actual percentage), the order calculation line with «Tallene er avrundet for visning.» and the fixed safety-margin text, the order figure, all active warnings and notes, and the confidence label with its reason (FR-10, FR-12, FR-19)
**And** the horizon is labeled «Uke 1 · uke 46» to «Uke 3 · uke 48» with the FR-7 note when the three forecasts are equal (FR-7, UX-DR7)

**Given** a product without a forecast
**When** its screen opens
**Then** it shows no forecast and no order quantity, a warning that names the reason (and the window when that applies), and «Du bestemmer bestillingen selv.» (FR-8)

**Given** a 1366 × 768 screen
**When** the product screen opens
**Then** the suggested order quantity, the confidence label and the active warnings are visible without scrolling (FR-25, NFR-6)
**And** Epic 3 adds the settings and the Forklaring area to this screen

### Story 2.7: See how the forecast was calculated

As a purchasing manager,
I want to see how the base forecast was calculated, week by week,
So that I can check it by hand.

**Acceptance Criteria:**

**Given** the moving average
**When** the forecast calculation is shown
**Then** it reads «Glidende gjennomsnitt, 3 uker: (16 + 12 + 15) / 3 = 14,3» for E1 and lists the week numbers of the calculation weeks used (FR-35)

**Given** exponential smoothing
**When** the forecast calculation is shown
**Then** it shows the last update, «Eksponentiell glatting, faktor 0,3: 0,3 × 15 + 0,7 × 13,3 = 13,8» for E2, and a table of all calculation weeks with their sales and level

**Given** weeks left out of the calculation
**When** the forecast calculation is shown
**Then** it lists each stockout week and each excluded unusual week by week number with its reason, and, when unusual weeks are excluded, the number of calculation weeks used (FR-15, FR-16)
**And** every number is rounded for display by R-9 and matches the reference examples

## Epic 3: Tune the settings and read the explanation

The purchasing manager changes a company setting and sees every product update, and reads a Norwegian template explanation kept apart from the numbers. This completes the core flow (SM-3). Also covers NFR-10, SM-3, SM-5, SM-6, AG-1, AG-2, AG-4, AR-6, AR-8, UX-DR6, UX-DR10 to UX-DR12 and UX-DR15 (Flow 1).

### Story 3.1: Change and save the company settings

As a purchasing manager,
I want to change my company's forecast settings from the product screen and have them saved,
So that the forecasts follow how my company plans.

**Acceptance Criteria:**

**Given** a logged-in company
**When** the product screen opens
**Then** its settings area shows the forecasting method as a segmented control, the window, the smoothing factor, the scenario percentage, the safety margin and the unusual-week choice, with the defaults and ranges from `forecasting/settings.py` (FR-20, UX-DR6)
**And** the setting that does not apply to the chosen method is shown as not in use, and seasonal adjustment is not shown until FR-9 is built

**Given** a new value inside its range, written with a decimal comma or a decimal point
**When** the form is posted
**Then** the value is saved in the company's one `CompanySettings` row, created by this story, and the page redirects to itself (Post/Redirect/Get, AR-6)
**And** every product of the company is calculated with the new value on its next view (FR-21)

**Given** an empty, non-numeric or out-of-range value
**When** the form is posted
**Then** it is refused with a Norwegian message that names the allowed range, and the previous value stays (FR-20, NFR-10)

**Given** saved settings
**When** the user logs out and in again, or the application restarts
**Then** the settings are unchanged (FR-22, SM-5)
**And** `load_seed` resets every company's settings to the defaults (DR-4)

**Given** company A logged in
**When** A tries to read or change company B's settings, directly or through a form
**Then** every attempt is refused, and the two-account test covers it (FR-2, SM-4)

### Story 3.2: See the effect of a change on every product

As a purchasing manager,
I want a confirmation that shows what my change did,
So that I understand the effect before I plan the order.

**Acceptance Criteria:**

**Given** the settings area
**When** it is shown
**Then** it always shows «Endringen gjelder alle produkter i bedriften.» (FR-21)

**Given** a saved change
**When** the product screen reloads
**Then** a Norwegian confirmation with `role="status"` shows the previous and the new affected value, for example «Grunnprognose: 14,3 → 13,8» (UX-DR6, UX-DR10)
**And** reloading the page, going back or posting the same change again gives the same result without errors (NFR-10)

**Given** the test products named in FR-21
**When** an automated test changes each setting
**Then** the affected value changes as the FR-21 table states: E1 → E2 (14.333 → 13.790), E1 with window 4, E2 with factor 0.5, E3 with 20 %, E4 with a 50 % safety margin, and E8 with unusual weeks excluded (41.0 → 21.333)

**Given** the web application
**When** the core-flow test runs through the Django test client
**Then** it logs in, selects a product, sees the sales history, forecast calculation and scenarios, changes the forecasting method, safety margin or unusual-week setting, and sees the affected value change (SM-3, UJ-1 steps 1 to 4)

### Story 3.3: Read a plain-language explanation

As a purchasing manager,
I want a short Norwegian explanation of the forecast and the order proposal,
So that I understand the numbers without reading every rule.

**Acceptance Criteria:**

**Given** a product's `ProductResult`
**When** `explanation.explain(result)` builds the text
**Then** it covers the forecasting method and settings used, the number of calculation weeks, the weeks left out and why, every active warning and note, the confidence label with its reason, and the order calculation line (FR-26)
**And** it uses only values from the result, so the same result always gives the same text, and `explanation/` imports no Django code (AG-1, AG-2, AD-1)

**Given** each template
**When** the tests run
**Then** snapshot tests compare the generated text with committed expected output (addendum §3)
**And** a number check confirms that every number in the text is also shown among the calculated numbers on the product screen (FR-27, SM-6)

**Given** the product screen
**When** it is shown
**Then** the explanation sits in its own area under the heading «Forklaring», below the calculated numbers, in the voice of EXPERIENCE.md (UX-DR6, UX-DR11)
**And** a product without a forecast gets an explanation that names the reason and says that the user decides the order; the label for AI-rephrased text comes with FR-28 in Epic 7

## Epic 4: The examiner can install, try and verify Prognose

The examiner follows the README («Prøv selv») locally or on the published address and checks the results against the reference spreadsheet, and the group delivers the status table, the logs and the final checks. Stories 4.1 to 4.3 start when the Must scope is built; Story 4.4 runs on the final commit. Also covers DR-1, DR-2, DR-5, DR-6, DR-8, DR-9, NFR-1, NFR-4, NFR-6, NFR-7, NFR-11, SM-2, SM-8, SM-9, AR-17, UX-DR15 (Flow 2) and UX-DR16.

### Story 4.1: README that lets the examiner set up and try Prognose

As an examiner,
I want a README that takes me from a fresh clone to a logged-in product overview and through «Prøv selv»,
So that I can run and check Prognose without help.

**Acceptance Criteria:**

**Given** the README
**When** it is read
**Then** it covers DR-1: purpose and audience with screenshots of the login page, product overview and product screen; prerequisites with minimum versions; exact setup commands for macOS Terminal and Windows PowerShell, including activating the virtual environment and how the session secret is created; fixes for likely setup errors; the two test logins; the generator, the load command and that reloading resets settings and adjustments; and the published address
**And** it has a «Prøv selv» section of 5 to 10 steps that follows UJ-1, and a table of the test products naming the rule, warning or confidence label each shows and its E-n (UX-DR15, Flow 2)

**Given** the README
**When** it is read
**Then** it also explains how to run the tests with the expected result, the browsers tested, every top-level folder (including `PRODUCT.md` and the BMAD and Claude Code folders) with links to the planning and process documents, and the known limitations: the trend lag (FR-7), R-14, the R-8 assumptions and the project-defined rules (DR-1, DR-2)
**And** its language-model section says how to switch the model on if FR-28 is built, or that it was not built

**Given** a clean macOS machine and a clean Windows machine
**When** a person follows only the README from a fresh clone
**Then** they log in as a test company and see the product overview within 15 minutes, and the app also starts and works with the network switched off (SM-2, NFR-1)
**And** the measured time is stated in the README, and the test is recorded in the QA log (DR-9)

### Story 4.2: Design finish review on the real build

As a user of Prognose,
I want the built screens to match the approved design and the accessibility floor,
So that the app is as clear and usable as the approved mockups promised.

**Acceptance Criteria:**

**Given** the built landing page, product overview and product screen
**When** the Impeccable finish review runs against the direction contract and the approved mockups (UX-DR16)
**Then** its material fixes are applied, or listed with a reason in the status table, without adding features
**And** DESIGN.md is updated from the shipped build where they differ, so that one DESIGN.md stays the only copy

**Given** the built screens
**When** they are checked with the keyboard, at 1024 px, 1366 × 768 and 1440 px, and for contrast
**Then** there is no horizontal page scrolling from 1024 px, chart markings differ by more than color, contrast meets WCAG 2.2 AA, and focus and labels are visible (NFR-6, NFR-7, NFR-11)
**And** the results are recorded in the QA log (DR-9)

### Story 4.3: Status table and process documentation

As a teacher or examiner,
I want to trace every requirement to its stories, tests and commits, and to see how AI was steered,
So that I can assess the process as well as the product.

**Acceptance Criteria:**

**Given** the status table linked from the README
**When** it is read
**Then** every FR has its priority, its status at submission (built, partly built, not built or changed), its stories and tests, and the reason for any deviation (DR-8)

**Given** the AI steering log
**When** it is read
**Then** it has at least five cases and at least one per epic built, each with what the AI proposed, what was wrong, what the group decided and the commit or pull request, starting with the planning-phase cases (DR-5, SM-8)

**Given** the QA log
**When** it is read
**Then** every defect in AI-generated code or text that a test, the reference spreadsheet, a review or a manual test found is recorded with how it was found, the fix and the commit or pull request (DR-9)

**Given** the planning documents
**When** the build ends
**Then** the Product Brief is updated with the changes in addendum §7, and the process documentation names textbook sources for the inventory rules or states that none were found (PRD §10, questions 3 and 6)
**And** the saved AI sessions for each story sit in the documented folder, cleaned of personal data and local paths (DR-5, NFR-4)

### Story 4.4: Final check on the final commit

As an examiner,
I want the submitted version to be verified on the final commit, both locally and published,
So that what I install and open is what the group tested.

**Acceptance Criteria:**

**Given** the final commit
**When** the checks run
**Then** `python manage.py test`, `ruff check` and `ruff format --check` pass (SM-1, SM-3)
**And** the manual checklist for NFR-6, NFR-7, NFR-8, NFR-11, SM-2 (including the offline start) and SM-9 is run and recorded with date, operating system, browser and result (DR-9)

**Given** the published address
**When** a person logs in as each test company
**Then** they see the product overview and can run the core flow of SM-3 by hand (SM-9, DR-10)

**Given** the whole repository history
**When** it is scanned before submission
**Then** no secrets, personal data or local paths remain, and the result is recorded in the QA log (NFR-4)

**Given** the stack versions, the free-plan terms and, if FR-28 is built, the Ollama version and model sizes
**When** they are re-checked before 1 December 2026
**Then** the README and the architecture spine state the checked values (AR-17, DR-6)
**And** the README, the status table and the change log in PRD §12 are final, and every Should item not built is listed with its reason (DR-1, DR-8)

## Epic 5: Seasonal products and clearer decision notes

Forecasts can use seasonal adjustment, and the product screen adds the seasonal-pattern warning, the level-shift warning text, the order quantity per scenario and the overstock note. Starts only after the Must scope passes SM-1 and SM-3 (DR-6); Stories 5.4 and 5.5 are Could. Also covers SM-1 (E14, E22, E25 to E27, E30) and SM-7.

### Story 5.1: Seasonal adjustment for seasonal products

As a purchasing manager,
I want to switch on seasonal adjustment for my company,
So that products with a seasonal pattern get week forecasts that follow the season.

**Acceptance Criteria:**

**Given** the settings area
**When** the company switches «Sesongjustering» on (default off)
**Then** the setting is saved and validated like the other settings, and the FR-21 confirmation shows the change (FR-9, FR-20)

**Given** seasonal adjustment on and a cycle length of 52 in the app
**When** a product is calculated (R-14)
**Then** the week forecasts are seasonally adjusted, and the scenarios, suggested order quantity and weeks of cover use them; E14 and E27 match with the cycle length set to 4 in the tests

**Given** a product where seasonal adjustment is not possible (a week number without calculation weeks, or a week-number mean of 0)
**When** it is calculated
**Then** it gets week forecasts without seasonal adjustment and a note (E25, E26)

**Given** seasonal adjustment off
**When** the seasonal test product is calculated
**Then** its week forecasts stay flat with the FR-7 note, and the FR-21 test row for E14 (flat → seasonal) passes when the setting is switched on
**And** the forecast calculation shows the seasonal indices, the adjusted values and the week forecasts for weeks 1 to 3 (FR-35, E14), and the README states the limitations in PRD §5.5

### Story 5.2: Warnings for seasonal patterns and level shifts

As a purchasing manager,
I want a warning when a product has a seasonal pattern the forecast ignores, or when demand has moved to a new level,
So that I know when to judge the order myself.

**Acceptance Criteria:**

**Given** a product where R-14 steps 1 and 2 can be calculated
**When** a seasonal index is 1.3 or more, or 0.7 or less, and seasonal adjustment is off or not used for the product (R-17)
**Then** the product screen shows «Produktet har tydelig sesongvariasjon som prognosen ikke tar hensyn til.», and E30 matches (FR-36)

**Given** a level shift in the recent period
**When** the product screen is shown
**Then** it shows «Etterspørselen ser ut til å ha endret nivå.» (FR-17, warning text)

**Given** either warning
**When** the confidence label is set (R-16)
**Then** it counts as an active warning and is named in the label's reason and in the explanation
**And** the seed data has a test product that triggers each warning, so SM-7 still holds

### Story 5.3: Order quantity per scenario and overstock note

As a purchasing manager,
I want the order quantity for the optimistic and the pessimistic scenario, and a note when my stock already covers next week,
So that I can weigh the order against the risk.

**Acceptance Criteria:**

**Given** a product with a forecast
**When** the product screen is shown
**Then** it shows the order quantity for the optimistic and the pessimistic scenario, each calculated with R-8 including the safety margin and the scenario's week-1 value, and E22 matches (FR-13)

**Given** a suggested order quantity of 0 and a stock on hand above 0
**When** the product screen or the product overview is shown
**Then** it shows the note «Lagerbeholdningen dekker forventet behov neste uke.» (FR-14)
**And** when both the week-1 normal forecast and the stock on hand are 0, no note is shown (E23)

### Story 5.4: Settings per product (Could)

As a purchasing manager,
I want to give a product its own settings,
So that a special product can be calculated differently from the rest.

**Acceptance Criteria:**

**Given** a product with its own value for a setting
**When** it is calculated
**Then** that value overrides the company setting, and the product screen marks it as the product's own (FR-23)
**And** a reset returns the product to the company settings

**Given** a per-product value
**When** it is saved
**Then** it is validated with the ranges of FR-20, a refused value keeps the previous one, and company A cannot read or change company B's product settings (FR-2)
**And** the detailed consequences are completed when the story is planned (PRD §4)

### Story 5.5: Forecast accuracy (Could)

As a purchasing manager,
I want to see how accurate past one-week forecasts were,
So that I know how far to trust the method for this product.

**Acceptance Criteria:**

**Given** a product with enough history
**When** the product screen is shown
**Then** it shows the mean absolute error (MAE) of past one-week forecasts with the chosen method and settings, calculated in `forecasting/` (FR-34)
**And** MAPE is not shown, because weeks with zero sales make it undefined

**Given** the MAE calculation
**When** the tests run
**Then** a hand-calculated example, added to `reference/examples.json` and the reference spreadsheet when the story is planned, passes (DR-3)

## Epic 6: Plan the week's purchases

The purchasing manager adjusts order quantities and reviews the combined order overview. Starts only after the Must scope passes SM-1 and SM-3 (DR-6); Stories 6.3 to 6.5 are Could. Also covers AR-7, UX-DR5 (adjusted tag), UX-DR8, UX-DR10 and UJ-1 steps 5 and 6.

### Story 6.1: Adjust an order quantity

As a purchasing manager,
I want to replace a suggested order quantity with my own,
So that the plan reflects what I know beyond the numbers.

**Acceptance Criteria:**

**Given** the product screen
**When** the user enters an adjusted order quantity and posts it
**Then** it is stored through `planning/adjustments.py` in the database-backed session, keyed by varenummer and latest data week, and the page redirects to itself (AR-7, FR-29)
**And** the suggested order quantity stays visible next to the adjusted one, and the product is marked «Justert av deg» on the product screen and in the overview, for example when 70 is changed to 80

**Given** a value that is not a whole number of 0 or more
**When** it is posted
**Then** it is refused with a Norwegian message, and the previous value stays (NFR-10)

**Given** an adjusted product
**When** the user resets it
**Then** the suggested order quantity applies again

**Given** company A logged in
**When** A tries to change company B's order quantities
**Then** every attempt is refused, and the two-account test covers it (FR-2, SM-4)
**And** `load_seed` clears the stored sessions, so reloading the data also resets the adjustments (DR-4)

### Story 6.2: Combined order overview

As a purchasing manager,
I want one overview of every product with the quantity I plan to order,
So that I can place the week's orders in one go outside Prognose.

**Acceptance Criteria:**

**Given** a logged-in company
**When** the combined order overview opens from the app rail
**Then** every product of the company appears with its suggested or adjusted order quantity, marked «Foreslått» or «Justert av deg», per the Samlet bestillingsoversikt wireframe in EXPERIENCE.md (FR-30, UX-DR8)
**And** it lists only the company's own products, and the two-account test covers it (FR-2)

### Story 6.3: Save adjustments and mark products as approved (Could)

As a purchasing manager,
I want my adjustments and approvals to be kept between sessions,
So that I can finish the plan later.

**Acceptance Criteria:**

**Given** an adjusted order quantity
**When** the user logs out and in again
**Then** the adjustment is still there, because the storage behind `planning/adjustments.py` is replaced without changing its functions (AD-9, FR-31)
**And** the user can mark a product as approved, and the mark is kept and shown in the combined order overview

**Given** saved adjustments and approvals
**When** `load_seed` runs, or another company logs in
**Then** reloading resets them (DR-4), and company A cannot read or change B's (FR-2)

### Story 6.4: Export the combined order overview (Could)

As a purchasing manager,
I want to download the combined order overview as a CSV file,
So that I can use it in my ordering routine.

**Acceptance Criteria:**

**Given** the combined order overview
**When** the user chooses the export
**Then** a CSV file downloads with the same products and quantities, each marked as suggested or adjusted (FR-32)
**And** it contains only the company's own products (FR-2)

### Story 6.5: Note when the stock will not last through weeks 2 and 3 (Could)

As a purchasing manager,
I want a note when my stock plus the suggested order will not cover weeks 1 to 3,
So that I can plan the next order in time.

**Acceptance Criteria:**

**Given** a product with a forecast
**When** the stock on hand plus the suggested order quantity is less than the sum of the week forecasts for weeks 1, 2 and 3
**Then** the product screen shows a Norwegian note in the Merknad pattern, with the wording set when the story is planned (FR-33)
**And** no note is shown when the sum is covered

## Epic 7: Optional local AI rephrasing

When switched on locally, a language model rephrases the template explanation, with the number check and the fallback to the template. Starts only after the Must scope passes SM-1 and SM-3 (DR-6). Also covers AG-1, AG-3 to AG-5, AR-8 and SM-6.

### Story 7.1: Rephrase the explanation with a local language model

As a purchasing manager,
I want the explanation rephrased in more natural Norwegian when a local model is available,
So that it is easier to read, without any risk to the numbers.

**Acceptance Criteria:**

**Given** the default configuration
**When** Prognose runs, locally or on Vercel
**Then** the model is off and the app runs fully without it; it is switched on only through `PROGNOSE_LLM_URL` and `PROGNOSE_LLM_MODEL` in the local `.env`, listed in `.env.example`, never in the company settings (FR-28, AG-3)

**Given** the model is on
**When** a product screen is shown
**Then** `explanation/rephrase.py`, the only module that calls the model, sends the template text with the numbers as placeholders, and the app inserts every number itself (AR-8, AG-1)
**And** the rephrased text is shown under the label «KI-omformulert forklaring» (FR-27, AG-4)

**Given** a rephrased text in which a number, or the label attached to a number, differs from the template explanation
**When** it is checked
**Then** it is rejected, and the template explanation is shown (SM-6)

**Given** the model server is not running, the model is missing, no answer arrives within 10 seconds, or the response contains an error
**When** a product screen is shown
**Then** the template explanation is shown without an error for the user, and a test with a fake model server covers each case

**Given** the README
**When** it is read
**Then** it names the chosen runtime and model, the license obligations, the download size and expected time, and describes the model as a separate optional step outside the basic setup (DR-1, SM-2, PRD §10 question 5)
**And** no data is sent to a hosted AI service (AG-5)

## Change Log

Changes after approval on 2026-11-08, recorded as DR-5 and PRD §12 require.

| Date | Change | Reason | Commit or pull request |
|---|---|---|---|
| 2026-11-08 | Story 1.1: the first version of `load_seed` only creates the session-secret file, and Story 1.2 adds the data. | The readiness check in sprint planning found that Story 1.1 recorded no source for the local secret (NFR-3, AD-12). | `425d818` |
