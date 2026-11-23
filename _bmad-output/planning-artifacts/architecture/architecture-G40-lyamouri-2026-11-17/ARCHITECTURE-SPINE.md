---
name: 'Prognose'
type: architecture-spine
purpose: build-substrate
altitude: feature
paradigm: 'server-rendered Django monolith with a functional core and an imperative shell'
scope: 'Prognose v1: one web application for weekly forecasts, order quantities and purchase planning, with PostgreSQL locally in Docker Compose; not published in v1'
status: final
created: '2026-11-17'
updated: '2026-11-21'
binds: [FR-1, FR-2, FR-3, FR-4, FR-5, FR-6, FR-7, FR-8, FR-9, FR-10, FR-11, FR-12, FR-13, FR-14, FR-15, FR-16, FR-17, FR-17b, FR-18, FR-19, FR-20, FR-21, FR-22, FR-23, FR-24, FR-25, FR-26, FR-27, FR-28, FR-29, FR-30, FR-31, FR-32, FR-33, FR-34, FR-35, FR-36, NFR-1, NFR-2, NFR-3, NFR-4, NFR-5, NFR-6, NFR-7, NFR-8, NFR-9, NFR-10, NFR-11, AG-1, AG-2, AG-3, AG-4, AG-5, AG-6, DR-1, DR-2, DR-3, DR-4, DR-5, DR-6, DR-7, DR-8, DR-9, DR-10]
sources:
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md'
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/addendum.md'
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/tilbakemelding-prd.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/DESIGN.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/EXPERIENCE.md'
  - '_bmad-output/planning-artifacts/architecture/technology.md'
companions:
  - 'teknologinotat.md'
---

# Architecture Spine — Prognose

## Design Paradigm

A **server-rendered Django monolith with a functional core and an imperative shell**. The core is pure Python: inputs in, results out. The shell is one Django app that authenticates, reads and writes PostgreSQL, calls the core and renders HTML.

| Layer | Package (in `src/`) | Holds |
|---|---|---|
| Core | `forecasting/` | rules R-1 to R-17, `ProductResult`, the overview, the FR-20 settings constants, R-9 rounding and the Norwegian number format |
| Core | `explanation/` | every result-dependent Norwegian sentence, the template explanation, the FR-27 and FR-28 checks |
| Shell | `web/` | the company user, models, company-scoped queries, adjustments, views, forms, chart geometry, templates, static files, management commands, the local-model adapter |
| Project | `prognose/` | settings, URLs and the WSGI entry point |

```mermaid
flowchart LR
  T[web templates, CSS and the enhancement script] --> W[web: Django shell]
  W --> E[explanation: pure]
  W --> F[forecasting: pure]
  E --> F
  W --> DB[(PostgreSQL)]
  W -.->|optional, local only| L[local language model]
```

Arrows point from the depender to the dependency. Nothing points back into the shell.

## Invariants & Rules

### AD-1 — Functional core, imperative shell [ADOPTED]

- **Binds:** all; NFR-2, AG-1
- **Prevents:** calculation rules leaking into views, models, templates or JavaScript, where they cannot be unit-tested against the reference examples
- **Rule:** `forecasting/` and `explanation/` import only the Python standard library, and `explanation/` may import `forecasting/`, never the reverse. They never import Django, a database driver or an HTTP library, and never read the clock, files or environment variables. Every other package may import them.

### AD-2 — One compute path per company

- **Binds:** FR-5 to FR-19, FR-17b, FR-21, FR-24, FR-25, FR-29, FR-30, FR-33 to FR-36; R-1 to R-17; NFR-8
- **Prevents:** two screens showing different numbers, groups or orders for the same data, and stale stored results after a settings change
- **Rule:**
  - The core computes from inputs only: `forecast_product(weeks, stock_on_hand, settings)` returns a frozen `ProductResult`; `build_overview(results, adjustments)` applies R-12 and gives the groups, the week figures, the previous and next product and the combined order overview; `describe_settings_change(before, after)` gives the FR-21 confirmation lines.
  - The shell has one loader, `web/company_data.py`, that reads a company's settings, products, sales weeks and adjustments through `web/queries.py` (AD-7), in a fixed number of queries independent of the number of products, and calls the core. Every page uses it, and the product screen computes the whole overview for its list and its previous and next links.
  - The FR-21 confirmation compares the product the user came from, before and after the change. From a page without a product, it shows only the line naming the new setting.
  - Search hides products from the computed overview. It never changes their order, their results or the week figures.
  - The database stores inputs only. Results are computed on every request and never stored.
  - Nothing outside the core calculates, rounds, sorts or groups domain values.

### AD-3 — One rounding and one Norwegian number format

- **Binds:** R-8, R-9, FR-12, FR-27, FR-35, NFR-5
- **Prevents:** 70 on one screen and 71 on another, «14.3» next to «14,3», and display rounding that disagrees with the reference spreadsheet
- **Rule:**
  - The core keeps full float precision and returns numbers, never formatted strings.
  - Every rounding goes through `forecasting/rounding.py`: first to 6 decimals, then up to whole units (R-8) or half away from zero for display (R-9), with the `decimal` module and never with `round()`.
  - Norwegian display text comes only from `forecasting/display.py`: a decimal comma, the minus sign U+2212, no thousands grouping, and a no-break space before «%». Week labels come from the same module, with the year at New Year and in lists that reach before the recent period. One template-filter module, the explanation and the chart all call it.

### AD-4 — Result wording in one place

- **Binds:** FR-7 to FR-19, FR-17b, FR-21, FR-24 to FR-27, FR-35, FR-36; the EXPERIENCE.md Message Catalogue
- **Prevents:** the list, the trust panel, the chart text and the explanation phrasing the same warning differently
- **Rule:** every Norwegian sentence that depends on a result comes from `explanation/`, with the EXPERIENCE.md Message Catalogue as its copy source: warnings, notes, confidence reasons, the forecast and order calculation lines, the FR-21 confirmation, the chart summary and the template explanation. Templates place these strings and never compose them. Fixed interface text lives in the templates.

### AD-5 — Explanation guardrails

- **Binds:** FR-26, FR-27, FR-28, AG-1 to AG-5, SM-6
- **Prevents:** a number in the explanation that the screen does not show, a language model supplying or moving a number, and network calls from anywhere else
- **Rule:**
  - Every explanation template is written with named placeholders in curly braces, such as `base_forecast`. The template path fills them from `ProductResult` through `forecasting/display.py`.
  - `ProductResult` exposes the FR-27 allowed numbers as display strings. A test takes every number from every template explanation and checks it against them.
  - The FR-28 checks are pure functions in `explanation/`: placeholder names, count and order; the §3 label before each placeholder; no number outside a placeholder.
  - The only network call in the application is `web/rephrase.py`. It uses the standard library and a 10-second timeout, and it is off unless the local `.env` names a model URL. It returns the template text on any failure.

### AD-6 — The company is the authenticated principal [ADOPTED]

- **Binds:** FR-1, NFR-3
- **Prevents:** two ways of linking data to a company, and pages reachable without login
- **Rule:** the custom user model `web.Company` has `customer_number` as its login field and is created in the first migration. Passwords use Django's default PBKDF2 hasher. `LoginRequiredMiddleware` denies by default; only the login page at the app root and the error pages, which show no company data, are exempt. Logging out is a POST.

### AD-7 — Company isolation in one data-access module

- **Binds:** FR-2, SM-4
- **Prevents:** one view forgetting the company filter and showing another company's data
- **Rule:** every read or write of company data goes through functions in `web/queries.py` that take the logged-in company as their first argument and filter by it. Views, forms and the chart never use model managers for company data; only `load_seed` and the migrations touch the tables directly. A lookup outside the company raises `Http404` and renders the same page as an unknown address. The two-account test covers every route in the URL map (AD-11) and every list.

### AD-8 — Weeks by ISO week and position

- **Binds:** PRD §3 (Week, Latest data week), R-10 to R-17, FR-7, FR-18
- **Prevents:** calendar arithmetic that disagrees with the reference examples, and products whose histories end at different weeks
- **Rule:**
  - A week is an ISO 8601 week, identified by its ISO year and week number. A sales week is identified by its product and its position, from 1 to N. The position orders every calculation and measures every distance.
  - Each product's history is a run of consecutive weeks without gaps that ends at the company's latest data week. `load_seed` refuses seed files that break this. The latest data week is derived from the sales weeks and is never stored separately.
  - Calendar arithmetic is used only to label weeks 1 to 3 of the forecast horizon. No domain code reads today's date.

### AD-9 — Settings defined once

- **Binds:** FR-20 to FR-22, NFR-5, NFR-10
- **Prevents:** defaults, ranges and validation drifting between the model, the form, the seed and the core, and a factor on screen that differs from the one used
- **Rule:**
  - Each company has one `CompanySettings` row. The FR-20 defaults and ranges are defined once, in `forecasting/settings.py`; the model defaults, the form validation and `load_seed` read them.
  - The window and both percentages are whole numbers. The smoothing factor has one decimal, from 0,1 to 0,9.
  - Number fields accept a decimal comma or a decimal point. Other input is refused with a Norwegian message, and the previous value stays.

### AD-10 — Server-side state and Post/Redirect/Get

- **Binds:** FR-20 to FR-22, FR-29 to FR-31, NFR-10, NFR-11, DR-4
- **Prevents:** client-side state that diverges from the server, double submissions, and two storages for adjusted quantities
- **Rule:**
  - Every change is an HTML form POST with CSRF protection, followed by a redirect: login, logout, settings, the unusual-weeks switch and adjusted quantities. Navigation and search are GET requests. There are no fetch or XHR calls and no client-side state.
  - Adjusted order quantities live in the server-side session, which uses Django's database backend. They are keyed by product number and latest data week and reached only through `web/adjustments.py`, and they enter the core as an input. FR-31 replaces only the storage behind that module.
  - Only the explicit reset in AD-15 deletes sessions.

### AD-11 — Rendering, URLs and the chart

- **Binds:** FR-24, FR-25, FR-35, NFR-1, NFR-6, NFR-7, NFR-11; DESIGN.md; EXPERIENCE.md
- **Prevents:** a CDN or front-end library dependency, chart code that computes values, and drift from the approved design
- **Rule:**
  - Pages are Django templates. One stylesheet defines the DESIGN.md tokens as CSS custom properties, and components use only those variables. Fonts are the system stacks in DESIGN.md. There is no front-end framework, UI library, web font or CDN.
  - The forecast chart is inline SVG rendered on the server, as in the approved mockup. A pure function in `web/chart.py` computes its geometry from `ProductResult` and display strings only, and its summary text comes from AD-4.
  - One optional script, `web/static/web/app.js`, only enhances: arrow keys, scroll positions, submitting the switch, filtering while typing, reloading a page that the browser restores from its back/forward cache (so that Back after «Logg ut» does not show a company's page), and enabling on Innstillinger the setting that the chosen forecasting method uses, so that the method and that setting change in one save. Every function works without it: a button next to the switch sends the change, and a field disabled for the saved method is changed in a second save. The settings form accepts the method and the setting it uses in one POST, which the tests check.
  - URL map, with Norwegian slugs:

    | Path | Page or action |
    |---|---|
    | `/` | Innlogging (GET and POST) |
    | `/logg-ut/` | log out (POST) |
    | `/produkter/` | Produktoversikt, with `?sok=` for search |
    | `/produkter/<varenummer>/` | Produktside |
    | `/produkter/<varenummer>/mengde/` | set or reset an adjusted quantity (POST, FR-29) |
    | `/innstillinger/` | Innstillinger (GET and POST); returns to the page it came from, which must be a path inside the app |
    | `/innstillinger/uvanlige-uker/` | the unusual-weeks switch (POST) |
    | `/bestillingsoversikt/` | Samlet bestillingsoversikt (FR-30) |

  - DESIGN.md and EXPERIENCE.md win over the mockup.

### AD-12 — Norwegian error pages

- **Binds:** NFR-10, FR-2; the EXPERIENCE.md Message Catalogue
- **Prevents:** a stack trace, a debug page or an English default page reaching a user
- **Rule:** DEBUG is off unless the local `.env` turns it on. The responses 400, 403 (including a failed CSRF check), 404, 405 and 500 render Norwegian pages with the Message Catalogue texts in the not-found panel. A database connection error renders the Database unavailable page with status 503 wherever it is raised, also in middleware, so the handler sits in the outermost middleware, and that page reads nothing from the database. Errors are logged to the console without request bodies, passwords, secrets or database URLs.

### AD-13 — Local run mode and configuration

- **Binds:** NFR-1, NFR-3, NFR-6, NFR-9, NFR-10, SM-2
- **Prevents:** secrets in the repository, a setup that needs file editing or an API key, and an app that is reachable from the network by default
- **Rule:**
  - Prognose has one run mode, the local one; version 1 is not published (AD-16). Settings read only environment variables, after loading an optional local `.env`. Nothing in `.env` is needed for the basic setup, and no API key or account is needed.
  - `DATABASE_URL` defaults to the Docker Compose database, `postgresql://prognose@127.0.0.1:15432/prognose`. The session secret comes from the git-ignored file `.secret_key`, which `load_seed` creates when it is missing and never overwrites. The app runs with `uv run python src/manage.py runserver --insecure` on 127.0.0.1.
  - **Phone test over the local network** (NFR-6): only for the manual test on a real phone, the group sets the optional local variable `PROGNOSE_LAN_HOST` to the computer's address on a private network and starts the app with `runserver --insecure 0.0.0.0:8000`. The settings add that address to `ALLOWED_HOSTS`; without the variable only `127.0.0.1` and `localhost` are allowed. DEBUG stays off, the database port stays on `127.0.0.1`, and after the test the app is stopped and the variable removed.
  - `LANGUAGE_CODE` is `nb` and `TIME_ZONE` is `Europe/Oslo`.

### AD-14 — PostgreSQL locally and in CI [ADOPTED]

- **Binds:** FR-4, NFR-1, NFR-9, DR-2, SM-5
- **Prevents:** behavior that differs between the app's database and the tests' database, and raw SQL that bypasses the migrations
- **Rule:**
  - PostgreSQL 18 everywhere: the image `postgres:18.7` in `compose.yaml` locally and in CI. Data access goes through the Django ORM and migrations with psycopg 3, without raw SQL.
  - `compose.yaml` holds only the database: user and database `prognose`, trust authentication, the port `127.0.0.1:15432`, a named volume at `/var/lib/postgresql`, `restart: unless-stopped` and a `pg_isready` health check. It is started with `docker compose up -d --wait`.
  - The tests run against the local PostgreSQL. The app writes no files at request time.

### AD-15 — Seed data and the explicit reset

- **Binds:** FR-1, FR-3, FR-4, DR-3, DR-4, NFR-3, NFR-4
- **Prevents:** plain-text passwords in the repository, seed data that disagrees with the answer key, and user data deleted by a routine command
- **Rule:**
  - `data/generate_seed.py` writes the versioned JSON files in `data/seed/` and gives identical output on every run. The files hold inputs and password hashes made with Django's hasher and a fixed salt per company. The rule test products take their series from the reference spreadsheet (AD-17). The two test companies have disjoint product numbers.
  - `load_seed` without options loads into an empty database only. When any company exists, it stops with a Norwegian message and changes nothing.
  - `load_seed --reset` is the only command that deletes data. It asks for typed confirmation. Then, in one transaction, it deletes the companies with their data and all sessions and loads the seed, so settings and adjustments return to the seed state (DR-4). Nothing runs it automatically.

### AD-16 — Publishing on Vercel (removed from v1)

- **Binds:** DR-10, which is not in version 1
- **Prevents:** work on a published version that version 1 does not need
- **Rule:**
  - Version 1 is not published. On Canvas on 2026-11-19 the teacher clarified that publishing is not mandatory, so publishing on Vercel with Neon and Story 1.9 in `epics.md` were removed (PRD DR-10). The clarification is summarized, not quoted, in the PRD folder (`avklaring-publisering-2026-11-19.md`).
  - Until then this decision set a Vercel Hobby project in `fra1` that deployed only `main`, a build script that migrated only additive changes and loaded the seed data only into an empty database, and deploys that never ran `load_seed --reset`, `flush` or a data migration. The change log keeps the history.

### AD-17 — One test command and one answer key

- **Binds:** NFR-2, DR-3, DR-7, SM-1, SM-3, SM-4, SM-6, SM-7
- **Prevents:** tests and the reference spreadsheet drifting apart, and checks that only some machines run
- **Rule:**
  - `uv run pytest` runs every test against the local PostgreSQL. It covers the core rules, a snapshot of each explanation template, the FR-27 number test, web tests through Django's test client, including the SM-3 core flow and the SM-4 two-account test, an import test for AD-1, and `makemigrations --check`.
  - The reference spreadsheet in `reference/` is the single answer key. The tests and the seed generator read its inputs and expected values with openpyxl, and no expected value is copied into test code.
  - When a test and the spreadsheet disagree, the case is calculated again by hand. Whichever was wrong is corrected, and the finding is recorded in the QA log (DR-9).
  - Every test names the FR-n or E-n it verifies (DR-5); a test that verifies no FR names its NFR-n, DR-n or AD-n (D-10 in `epics.md`).
  - `uv run ruff check` and `uv run ruff format --check` lint and format Python files only.
  - GitHub Actions runs the tests and Ruff on every pull request on Linux, with the database started from the same `compose.yaml`. A pull request is merged only when they pass.
  - Story 1.1 comes before CI, so it is merged when the same checks pass locally on its final commit (D-9 in `epics.md`). The first CI run, in Story 1.2, runs every test, also those from Story 1.1.

## Consistency Conventions

| Concern | Convention |
| --- | --- |
| Naming | Code is in English with the PRD §3 terms (`base_forecast`, `week_forecasts`, `calculation_weeks`, `safety_margin`, `stock_on_hand`, `weeks_of_cover`, `order_soon`, `confidence_label`). UI text is Norwegian, with the glossary labels and fixed strings verbatim. URL slugs are Norwegian (AD-11). |
| Data and formats | The product number (`varenummer`) is a string of 5 digits, unique within a company. Units sold, stock on hand and quantities are integers; forecasts are floats. Percentages are stored as whole numbers (10 means 10 %); the smoothing factor is stored with one decimal. Enum values: `moving_average`, `exponential_smoothing`, `included`, `excluded`. |
| Errors | Norwegian messages name the problem and the fix. Validation keeps the previous value. Unknown addresses and other companies' objects give the same not-found page (AD-7, AD-12). |
| Logging | Console only. Never log passwords, the session secret, database URLs or request bodies (NFR-4). |
| Configuration | Environment variables only (AD-13). `.env.example` lists every optional local variable that the code uses and marks each as optional or secret: `PROGNOSE_DEBUG`, `DATABASE_URL` and `PROGNOSE_LAN_HOST` (the phone test, AD-13), and `PROGNOSE_LLM_URL` and `PROGNOSE_LLM_MODEL` once FR-28 is built. None of them is needed for the basic setup, and no API key is needed. |
| Dependencies | `pyproject.toml` declares the direct dependencies with exact pins; `uv.lock` pins every package exactly and is the one lock file (DR-2); installs use `uv sync --locked`. A new package needs an update to the Stack table. |
| Commands | The README commands are the same on macOS and Windows and run through `uv run`, so no virtual environment is activated: `docker compose up -d --wait`, `uv sync --locked`, `uv run python src/manage.py migrate`, `uv run python src/manage.py load_seed`, `uv run python src/manage.py runserver --insecure`, and `uv run pytest`. |
| Platforms | macOS on Apple silicon or Intel, and Windows 10 22H2 or Windows 11 23H2 on x64, each with Docker Desktop; on Windows, Docker Desktop needs WSL 2 and hardware virtualization switched on. Windows on ARM is not supported in v1, because psycopg has no wheel for it. |
| Optional features | Should and Could items exist in code only once they are built. There are no runtime feature flags except the FR-28 switch. A story that builds an item updates every place EXPERIENCE.md ties to it, for example the header link, step 3 of the week path and the last-product button for FR-30. |
| Checks before a pull request | Each story is built on its own branch and merged through a reviewed pull request (DR-7). Before that, `uv run pytest`, `uv run ruff check` and `uv run ruff format --check` pass locally and in CI (AD-17). Story 1.1 comes before CI and passes them locally (D-9 in `epics.md`). |
| Documents | `docs/` holds `PRODUCT.md`, the `DESIGN.md` link, `arbeidslogg.md`, `qa-logg.md` (DR-9), `ki-styringslogg.md` (DR-5) and `statustabell.md` (DR-8). Session logs and saved AI sessions are in `.logs/`, and story specifications in `_bmad-output/implementation-artifacts/`. |
| Delivery order | The first stories prove the local path: the project skeleton with `compose.yaml` (Story 1.1 in `epics.md`) and CI (Story 1.2). The setup test on Windows x64 and offline is a story of its own (Story 1.3), and no other story waits for it, so it blocks no other development. Version 1 is not published (AD-16). Then the Must items. Should and Could items start only after the Must scope passes SM-1 and SM-3 (DR-6). |

## Stack

| Name | Version |
| --- | --- |
| Python | 3.13 (from `.python-version`; uv installs it) |
| Django | 5.2.19 (LTS, supported to April 2028) |
| psycopg[binary] | 3.3.9 |
| PostgreSQL | 18.7 (image `postgres:18.7`) |
| Docker Desktop (local prerequisite) | 4.99.0 tested, with Docker Compose v5.7.0 |
| uv | 0.13.9 at authoring (0.12.13 tested) |
| pytest | 9.2.0 |
| pytest-django | 4.14.0 |
| Ruff | 0.17.5 |
| openpyxl (development only) | 3.1.5 |

## Structural Seed

```text
G40-lyamouri/
  README.md, pyproject.toml, uv.lock, .python-version, compose.yaml, .env.example, .gitignore
  .github/workflows/   # CI: tests and Ruff on Linux with compose.yaml; the setup on Windows without Docker
  src/
    manage.py
    prognose/          # Django project: settings, urls, wsgi
    forecasting/       # pure: rules R-1 to R-17, ProductResult, overview, settings constants, rounding, display
    explanation/       # pure: result wording, template explanation, FR-27 and FR-28 checks
    web/               # Django app: Company, models, queries, company_data, adjustments, views, forms,
                       #   chart, rephrase, middleware, templates, static, management commands
  tests/               # pytest
  data/                # generate_seed.py and seed/ (versioned JSON)
  reference/           # the reference spreadsheet, the answer key (DR-3)
  docs/                # PRODUCT.md, DESIGN.md link, arbeidslogg, qa-logg, ki-styringslogg, statustabell
  _bmad/ _bmad-output/ .claude/ .impeccable/ .logs/   # BMAD, planning artifacts, Claude Code, Impeccable, session logs
```

```mermaid
flowchart LR
  subgraph Local["Local: macOS or Windows x64"]
    B1[Browser] -->|http 127.0.0.1:8000| R[Django runserver through uv]
    R -->|127.0.0.1:15432| P1[(PostgreSQL 18.7 in Docker Compose)]
    R -.->|optional, off by default| LM[Local language model]
    PH[Phone, manual test only] -.->|http on the local network| R
  end
  PR[Pull request] --> CI[GitHub Actions on Linux]
  CI -->|compose.yaml| P2[(PostgreSQL 18.7)]
```

```mermaid
erDiagram
  COMPANY ||--|| COMPANY_SETTINGS : has
  COMPANY ||--o{ PRODUCT : owns
  PRODUCT ||--o{ SALES_WEEK : has
```

## Capability → Architecture Map

| Capability / Area | Lives in | Governed by |
| --- | --- | --- |
| Login and isolation (FR-1, FR-2) | `web` (Company, `queries.py`) | AD-6, AD-7 |
| Seed data and storage (FR-3, FR-4) | `data/`, `web` models, `load_seed`, `compose.yaml` | AD-8, AD-14, AD-15 |
| Forecasts, scenarios and order quantities (FR-5 to FR-14) | `forecasting/` | AD-2, AD-3, AD-8, AD-9 |
| Warnings and confidence (FR-15 to FR-19, FR-17b, FR-36) | `forecasting/`, wording in `explanation/` | AD-2, AD-4 |
| Settings (FR-20 to FR-23) | `forecasting/settings.py`, `web` (CompanySettings, forms, views) | AD-9, AD-10 |
| Overview, product screen and forecast calculation (FR-24, FR-25, FR-35) | `web` views and templates, `web/chart.py` | AD-2, AD-4, AD-11 |
| Explanation (FR-26 to FR-28) | `explanation/`, `web/rephrase.py` | AD-4, AD-5 |
| Purchase planning (FR-29 to FR-32) | `web/adjustments.py`, the overview in `forecasting/`, views | AD-2, AD-10 |
| Stock note and accuracy (FR-33, FR-34) | `forecasting/` | AD-2 |
| Robustness and error pages (NFR-10) | `web` middleware and templates | AD-10, AD-12 |
| Run mode and configuration (NFR-1, NFR-3, NFR-6, NFR-9, SM-2) | `src/prognose/settings.py`, `compose.yaml`, `pyproject.toml`, `.env.example` | AD-13, AD-14 |
| Tests and quality (NFR-2, DR-3, DR-7, SM-1, SM-3, SM-4, SM-6, SM-7) | `tests/`, `reference/`, `.github/workflows/` | AD-17 |
| Delivery and process documents (DR-1, DR-2, DR-5, DR-6, DR-8, DR-9) | README, `docs/`, `.logs/` | Consistency Conventions |

## Deferred

- **Local language model (FR-28, PRD §10 question 5):** the runtime and the model are chosen when FR-28 is scheduled, as the last Should item, and AD-5 fixes the seam. How the 10-second timeout fits NFR-8 was decided on 2026-11-18: every page meets NFR-8's 2 seconds with the model off, which is the default and the basic setup (SM-2). With the model switched on locally, a product screen may wait up to the 10-second timeout of FR-28 before it shows the rephrased text or the template text, and the README states this exception. FR-28 sets the 10-second timeout, and addendum §3 makes the timeout and its fit with NFR-8 architecture choices, so NFR-8's text is unchanged; the teacher's feedback sets no response-time requirement. No caching or background loading is added; if the exception does not fit when FR-28 is scheduled, the story is postponed instead.
- **Schemas of the seed JSON and of the spreadsheet's answer-key sheet:** set in the data story. AD-15 and AD-17 fix who writes and who reads them.
- **Could items:** FR-31 replaces only the storage behind `web/adjustments.py` (AD-10); FR-23 needs an amendment to AD-9; FR-32 to FR-34 are decided when scheduled.
- **Caching:** only if the NFR-8 check fails, and it needs an amendment to AD-2.
- **Not in v1:** a Content Security Policy, browser end-to-end tests (Playwright) and rate limiting, because the test logins are public in the README.
- **Operations:** no monitoring, backup or alerting service in v1. The app holds synthetic data only, an explicit reset restores it (DR-4), and the console shows the logs.
- **Validation messages the Message Catalogue lacks,** for a percentage with decimals or a factor with two decimals: settled in the settings story under the UX copy rules.
- **Setup tests from Story 1.3** (recorded in `docs/qa-logg.md`): the offline start passed on macOS on 2026-11-22, also with Docker Desktop quit first. The README setup with Docker Desktop and the offline start are not tested on Windows x64, because nothing may be installed on the Windows x64 PC at work and the group has no other one; the README and the status table say so (D-3). `.github/workflows/windows-setup.yml` runs the setup without Docker, with the runner's own PostgreSQL, on GitHub's Windows Server 2025 x64 runner for every pull request that changes the code or the dependencies. Both run again on the final commit (DR-9, SM-2).
- **Publishing (removed from v1):** Vercel with Neon was planned as Story 1.9 until 2026-11-19, when the teacher's clarification on Canvas made it optional and the user removed it (AD-16, PRD DR-10). Story 1.2 still checks that GitHub Actions is allowed in the organization.
- **Docker Desktop's terms:** re-checked before submission: Docker Desktop is free for personal use and education.

## Change Log

The spine was set to `final` on 2026-11-17. Every later change is recorded here with the date, the reason and the commit, as PRD §12 and DR-5 require.

| Date | Change | Reason | Commit |
|---|---|---|---|
| 2026-11-18 | AD-11: `app.js` may also enable, on Innstillinger, the setting that the chosen forecasting method uses, so that the method and that setting change in one save, and the settings form accepts both in one POST. Without the script, a button next to the unusual-weeks switch sends the change, and a method change and its setting take two saves. | The user's decisions when approving Epic 3 in `epics.md` (D-4 and D-5): change the method and its setting before saving, and make the switch work without JavaScript. | `9dee8b1` |
| 2026-11-18 | Consistency Conventions, «Delivery order», and two Deferred items: the first stories prove the local path and CI; publishing on Vercel with Neon is Story 1.9 and the setup test on Windows x64 and offline is Story 1.3 in `epics.md`, and no other story waits for either. The checks before publishing are split between Story 1.2 (GitHub Actions) and Story 1.9 (Vercel and Neon). Two limitations are stated: a later first deploy finds Vercel or Neon problems later, and Windows stays untested if no Windows x64 computer can be used. | The user's decisions when approving Epics 1 and 4 in `epics.md` (D-1 and D-3): publishing can be cut under PRD §8.1 without holding back the Must scope, and the Windows test must not block other development. | `9dee8b1` |
| 2026-11-18 | Deferred, «Local language model»: how the 10-second timeout fits NFR-8 is decided. Every page meets NFR-8 with the model off; with the model switched on locally, a product screen may wait up to the timeout, and the README states this. No caching or background loading is added. | The user's decision when approving Epic 7 in `epics.md` (D-7), after a check that the exception fits the PRD (NFR-8 and FR-28 are assumptions, and addendum §3 leaves the fit to the architecture) and the teacher's feedback, which sets no response-time requirement. | `9dee8b1` |
| 2026-11-18 | Fixes from the BMAD review: AD-12 also covers 405, and the 503 page appears wherever a database error is raised, from the outermost middleware, without reading the database; the Configuration row lists the language-model variables only once FR-28 is built (Story 1.1); the Platforms row names WSL 2 and hardware virtualization for Docker Desktop on Windows; the Deferred item on the local language model cites FR-28 and addendum §3 for the timeout, and NFR-8's text is unchanged. | The review of `epics.md`, this spine and EXPERIENCE.md (findings A3, A4, A13, E7 and E8); the user approved fixing all findings. | `9dee8b1` |
| 2026-11-19 | Publishing removed from v1. Updated: the scope; AD-5; AD-13 (one local run mode, and the phone test over the local network with the optional `PROGNOSE_LAN_HOST`); AD-14 (PostgreSQL locally and in CI, without Neon and the pooled URL); AD-16 (kept as history, marked removed); the Configuration and Delivery order rows; the Stack table; the Structural Seed; the deployment diagram; the capability map; and the Deferred items on the language model, operations, publishing and Docker Desktop's terms. | The teacher's clarification on Canvas on 2026-11-19, as reported by the user: publishing is not mandatory, but the README must explain how to start the app and which API keys are needed. The user approved removing publishing on Vercel with Neon and keeping the real iPhone test over the local network. | `ea06f01` (PR #5) |
| 2026-11-19 | Consistency Conventions, «Commands»: the README installs with `uv sync --locked`, as the Dependencies row requires and CI runs (Story 1.2). | The implementation-readiness check of 2026-11-19 found that the Commands row said `uv sync`, while the Dependencies row says that installs use `uv sync --locked`. The user approved one install command for the README and CI. | `67694f7` (PR #6) |
| 2026-11-21 | AD-17 and the «Checks before a pull request» row: Story 1.1, which comes before CI, is merged when the tests and Ruff pass locally on its final commit (D-9 in `epics.md`). | The user's decision of 2026-11-21: CI comes in Story 1.2, after Story 1.1, so Story 1.1 could not meet the rule that a pull request is merged only when CI passes. | `fa237e7` |
| 2026-11-21 | AD-17: a test that verifies no FR names its NFR-n, DR-n or AD-n (D-10 in `epics.md`). | The user's decision in the BMAD Code Review of Story 1.1 on 2026-11-21: most tests of Story 1.1 verify no FR, because the story builds none. | `bcd8223` |
| 2026-11-22 | Structural Seed: `.github/workflows/` also holds the setup on Windows without Docker. Deferred: «Tests not run yet» becomes «Setup tests from Story 1.3», with the results instead of the plan for the Windows x64 PC at work. | Story 1.3: nothing may be installed on the work PC, and the user chose to record the limitation and add the partial test on GitHub's Windows runner (D-3). BMAD Code Review of Story 1.3 found that the spine still described the old plan, and the user approved the fix. | PR #12 |
| 2026-11-23 | AD-11: `app.js` may also reload a page that the browser restores from its back/forward cache, on the logged-in pages, so that Back after «Logg ut» does not show a company's page. Without the script, Back may show the old page, and any reload or click goes to the login page. | The manual test in Safari on 2026-11-23 (Story 1.8): `Cache-Control: no-store` does not stop Safari's back/forward cache, which WebKit leaves to `pageshow`. The user chose the script on 2026-11-23. | Story 1.8 (hash follows) |
