---
name: 'Prognose'
type: architecture-spine
purpose: build-substrate
altitude: feature
paradigm: 'server-rendered Django monolith with a functional core (functional core, imperative shell)'
scope: 'Prognose v1: one web app for weekly forecasts, order quantities and purchase planning; runs locally and is published on Vercel'
status: final
created: '2026-11-08'
updated: '2026-11-08'
binds: [FR-1, FR-2, FR-3, FR-4, FR-5, FR-6, FR-7, FR-8, FR-9, FR-10, FR-11, FR-12, FR-13, FR-14, FR-15, FR-16, FR-17, FR-18, FR-19, FR-20, FR-21, FR-22, FR-23, FR-24, FR-25, FR-26, FR-27, FR-28, FR-29, FR-30, FR-31, FR-32, FR-33, FR-34, FR-35, FR-36, NFR-1, NFR-2, NFR-3, NFR-4, NFR-5, NFR-6, NFR-7, NFR-8, NFR-9, NFR-10, NFR-11, DR-10, SM-9]
sources:
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md'
  - '_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/addendum.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-06/DESIGN.md'
  - '_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-06/EXPERIENCE.md'
companions: []
---

# Architecture Spine — Prognose

## Design Paradigm

A **server-rendered Django monolith with a functional core**. The core (`forecasting/`, `explanation/`) is pure Python: data in, results out, with no Django, database or network access. The shell (the Django apps `accounts/` and `planning/`, plus templates and static files) loads inputs, calls the core, renders HTML and handles every write.

```mermaid
flowchart LR
  T[templates + static/js/charts.js] --> P[planning app]
  P --> A[accounts app]
  P --> F[forecasting - pure]
  P --> E[explanation - pure]
  E --> F
  P --> D[(SQLite)]
  A --> D
```

Arrows point from the depender to the dependency. Nothing points back into the shell. The pure core and `planning/queries.py` are the seams for later growth, such as another UI or an API, without touching the rules.

## Invariants & Rules

### AD-1 — Functional core, imperative shell [ADOPTED]
- **Binds:** all; NFR-2
- **Prevents:** calculation rules leaking into views, models or templates, where they can't be unit-tested against the reference examples
- **Rule:** `forecasting/` and `explanation/` never import Django, the ORM or a network library. Django apps may import them; the reverse never happens.

### AD-2 — One compute entry point
- **Binds:** FR-5 to FR-19, FR-24, FR-33 to FR-36; R-1 to R-17
- **Prevents:** two screens showing different numbers for the same product
- **Rule:** `forecasting.compute_product(history, stock_on_hand, settings)` returns a frozen `ProductResult`, and `forecasting.sort_overview(results)` applies R-12. Views, templates, `charts.js`, the explanation and tests read values only from `ProductResult`. Nothing else recalculates or re-sorts.

### AD-3 — Results are computed, never stored
- **Binds:** FR-21, FR-22, NFR-8
- **Prevents:** stale cached results after a settings change, and two owners of one computed value
- **Rule:** the database holds inputs only: sales weeks, stock on hand, settings and adjustments. Every request computes the results it shows.

### AD-4 — One rounding and one display format
- **Binds:** R-9, FR-12, FR-35, NFR-5
- **Prevents:** a figure shown as 70 on one screen and 71 on another, or as «14.3» next to «14,3»
- **Rule:**
  - `forecasting/` keeps full precision. All R-9 rounding happens in `forecasting/rounding.py`: 6 decimals before rounding up, then display rounding half away from zero.
  - Norwegian display (decimal comma, U+2212 minus, a no-break space before %) comes from one pure module, `forecasting/display.py`. The template filters, the explanation and the chart data all call it.
  - `compute_product` returns numbers, never formatted strings.

### AD-5 — The company is the authenticated principal [ADOPTED]
- **Binds:** FR-1, NFR-3
- **Prevents:** two ways of linking data to a company, and pages reachable without login
- **Rule:** the custom user model `accounts.Company` has `customer_number` as its login field and is created before the first migration. Passwords use Django's default PBKDF2 hasher. `LoginRequiredMiddleware` denies by default, and only the landing/login view is exempt.

### AD-6 — Company isolation in one data-access module
- **Binds:** FR-2, SM-4
- **Prevents:** one view forgetting the company filter and leaking another company's data
- **Rule:** every read or write of company data goes through `planning/queries.py` functions that take the logged-in company first and filter by it. Views never use model managers for company data. A lookup outside the company raises `Http404`. The two-account test covers every view and list.

### AD-7 — Weeks by position, products by varenummer per company
- **Binds:** PRD §3 (Week), R-10 to R-15, FR-18
- **Prevents:** calendar arithmetic that disagrees with the reference examples, and URL clashes between companies
- **Rule:** a sales week is identified by (product, `position` 1..N), and `position` orders every calculation. Year and week number are used only for display and the seasonal index. `varenummer` is unique within a company only. Products are addressed as `/produkter/<varenummer>/` and resolved through `queries.py`.

### AD-8 — Server-side mutations with Post/Redirect/Get
- **Binds:** FR-20 to FR-22, FR-29, NFR-10, NFR-11
- **Prevents:** client-side state that diverges from the server, double submissions, and inconsistent validation
- **Rule:**
  - Login, logout, settings changes and adjustments are HTML form POSTs (CSRF on), followed by a redirect.
  - Filters are GET parameters.
  - There are no fetch calls and no client-side state.
  - Each company has one `CompanySettings` row, validated server-side with Norwegian messages; a decimal comma or point is accepted.
  - The defaults and allowed ranges (FR-20) are defined once, in `forecasting/settings.py`. The form validates against those constants.

### AD-9 — Adjusted quantities behind one service
- **Binds:** FR-29 to FR-31
- **Prevents:** two storage mechanisms for adjustments
- **Rule:** adjusted order quantities live in the Django session (Django's default database backend, in both run modes), keyed by varenummer and latest data week, and are reached only through `planning/adjustments.py`. FR-31 (Could) replaces the storage behind the same functions.

### AD-10 — Explanation boundary
- **Binds:** FR-26 to FR-28, AG-1 to AG-5, NFR-1
- **Prevents:** a number in the explanation that the calculation did not produce, and network calls from anywhere else
- **Rule:** `explanation.explain(result)` builds the template text from `ProductResult` only. The optional local model is reached only through `explanation/rephrase.py`, with a 10 s timeout and the number-and-label check, and any failure falls back to the template. No other module calls a model or the network.

### AD-11 — UI rendering
- **Binds:** NFR-1, NFR-6, NFR-7, NFR-11; the UX spines
- **Prevents:** a CDN dependency, chart logic duplicating calculations, and drift from the approved design
- **Rule:**
  - Pages are Django templates with one stylesheet that defines the DESIGN.md tokens as CSS custom properties.
  - Albert Sans is self-hosted and Chart.js is vendored.
  - The only JavaScript is `static/js/charts.js`. It draws from `json_script` data and computes nothing. Every number it prints arrives as a display string from the server.
  - DESIGN.md and EXPERIENCE.md win over the mockups.

### AD-12 — Seed data and secrets
- **Binds:** FR-1, FR-3, FR-4, NFR-3, DR-4
- **Prevents:** plaintext passwords in the repository, and a manual setup step for the secret
- **Rule:**
  - `data/generate_seed.py` deterministically writes the versioned seed files in `data/seed/`. They hold inputs and password hashes only.
  - `python manage.py load_seed` resets the database idempotently.
  - `load_seed` also creates the gitignored session-secret file when it is missing.
  - Published: `SECRET_KEY` is a Vercel environment variable, set once by the project owner, and there is no secret file. The published database gets its seed through the same `load_seed`, run as AD-16 describes.

### AD-13 — Run modes: local and published
- **Binds:** NFR-1, NFR-9, NFR-10, SM-2, DR-10, SM-9
- **Prevents:** debug pages or stack traces reaching the examiner, and a published version that differs from the local one in unlisted ways
- **Rule:**
  - **Local** (development, tests and the examiner's PC): one process, `python manage.py runserver --insecure` on 127.0.0.1, with SQLite. It works offline (NFR-1). `runserver` is used only here.
  - **Published:** Vercel's Python runtime runs `prognose/wsgi.py` as one function in region `fra1`, with Python 3.13 from `.python-version` and packages from `requirements.txt`. Vercel runs `collectstatic` into `STATIC_ROOT` (`staticfiles/`, gitignored) and serves `/static/` from its CDN.
  - `settings.py` detects the published version by the `VERCEL` variable, and only then:
    - forces DEBUG off;
    - builds `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` (https) from `VERCEL_PROJECT_PRODUCTION_URL` and `VERCEL_URL`;
    - sets `SECURE_PROXY_SSL_HEADER` and secure session and CSRF cookies;
    - requires `SECRET_KEY` and `DATABASE_URL`, and stops with a clear error if either is missing.
  - **Both:** DEBUG is off by default, with Norwegian 404 and 500 pages; only `.env` can turn DEBUG on, and only locally. `LANGUAGE_CODE = 'nb'` and `TIME_ZONE = 'Europe/Oslo'`. The local language model stays off on Vercel.

### AD-14 — One test command and one answer key
- **Binds:** NFR-2, DR-3, SM-1, SM-3, SM-4
- **Prevents:** tests and the reference spreadsheet drifting apart
- **Rule:**
  - `python manage.py test` runs every test.
  - Forecasting tests read expected values only from `reference/examples.json`, which the spreadsheet mirrors.
  - The core-flow and isolation tests use the Django test client.
  - Ruff lints and formats.

### AD-15 — Database chosen by environment
- **Binds:** FR-4, NFR-9, DR-10, AD-13
- **Prevents:** SQLite- or PostgreSQL-specific code that breaks the other database, and connection settings that fail behind Neon's connection pooler
- **Rule:**
  - Without `DATABASE_URL` the app uses the local SQLite file `db.sqlite3` (gitignored). With `DATABASE_URL` it uses PostgreSQL through psycopg. The URL is parsed with `urllib.parse`, and every PostgreSQL connection sets `sslmode=require`, `CONN_MAX_AGE = 0` and `DISABLE_SERVER_SIDE_CURSORS = True`.
  - The published database is Neon PostgreSQL on the free plan, created from the Vercel dashboard (Storage → Neon) in AWS Frankfurt (`eu-central-1`), next to `fra1`. The app uses the pooled `DATABASE_URL` that the integration sets. `DATABASE_URL_UNPOOLED` is used only for `migrate` and `load_seed` (AD-16).
  - Data access uses the Django ORM and migrations only, with no raw SQL, and the same migrations run on both databases. Tests run on SQLite.
  - The app writes no files at request time.

### AD-16 — Deploys from main; database changes by the owner
- **Binds:** DR-10, DR-7, SM-9, NFR-3
- **Prevents:** preview deployments without a database, unmerged code reaching the published data, and production database URLs stored in files
- **Rule:**
  - One group member owns the Vercel Hobby account and project and connects it to the public GitHub repository. Only `main` deploys, always to production. `vercel.json` holds `"regions": ["fra1"]` and `"git": {"deploymentEnabled": {"**": false, "main": true}}`. Pull requests are reviewed by running the branch locally (DR-7).
  - Migrations and seed loading never run in the build, at startup or in a request. At first setup, and right after a merge that adds a migration, the owner runs `python manage.py migrate` from their PC, plus `python manage.py load_seed` when the demo should be reset. `DATABASE_URL` is set to the `DATABASE_URL_UNPOOLED` value for that one command and is never written to `.env` or any other file.
  - On Vercel, the group sets only `SECRET_KEY`. The Neon integration adds the database variables, and Vercel provides the system variables.

## Consistency Conventions

| Concern | Convention |
| --- | --- |
| Naming | Code is in English with the PRD glossary terms (`base_forecast`, `week_forecasts`, `safety_margin`, `stock_on_hand`, `weeks_of_cover`, `order_soon`, `confidence_label`). UI text is Norwegian, using the glossary labels and fixed strings verbatim. URL slugs are Norwegian (`/produkter/`, `/bestilling/`, `/logg-ut/`). |
| Data & formats | `varenummer` is a string of digits. Quantities are integers. Forecasts are floats. Percentages are stored as whole numbers (10 means 10 %). Enum values: `moving_average` and `exponential_smoothing`; `included` and `excluded`. |
| Errors | User-facing messages are Norwegian and name the problem and the fix. Validation keeps the previous value (FR-20). Unknown addresses and other companies' objects give the same «ikke funnet» page. |
| Logging | Console logging only. Never log passwords, the session secret or full request bodies (NFR-4). |
| Config | Settings come from the environment, with an optional `.env` read by a small standard-library parser. `.env.example` lists `DEBUG`, `PROGNOSE_LLM_URL` and `PROGNOSE_LLM_MODEL`. Nothing in `.env` is needed for the basic setup, and `.env` never holds a value for the published version. On Vercel, settings read only `SECRET_KEY`, the Neon integration's `DATABASE_URL` and Vercel's system variables (AD-13). |
| Dependencies | Exact pins in one `requirements.txt`, which Vercel also installs from. There is no `pyproject.toml`; Ruff reads `ruff.toml`. No other Python packages without a new AD. |
| Checks | `python manage.py test`, `ruff check` and `ruff format --check` run locally before every pull request (DR-7). No CI service is required in v1. |
| Delivery order | The first story publishes the project skeleton on Vercel with Neon, so the publishing path is proven in the first week; after that every merge to `main` deploys. Must items first; Should and Could items start only after SM-1 and SM-3 pass (DR-6). |

## Stack

| Name | Version |
| --- | --- |
| Python | 3.13 (locally, and on Vercel through `.python-version`) |
| Django | 5.2.19 (LTS, supported to April 2028) |
| SQLite (local) | bundled with Python (≥ 3.31) |
| Chart.js (vendored) | 4.6.1 |
| Albert Sans (self-hosted, OFL) | Google Fonts release at build time |
| Ruff | 0.17.4 (settings in `ruff.toml`) |
| psycopg[binary] | 3.3.8 |
| PostgreSQL (published) | Neon free plan via the Vercel Marketplace, AWS Frankfurt, Neon's default version (Django 5.2 needs 14 or later) |
| Vercel (published) | Hobby plan (free), Python runtime, region `fra1` |

## Structural Seed

```text
G40-lyamouri/
  manage.py, requirements.txt, .python-version, vercel.json, ruff.toml, .env.example, README.md, PRODUCT.md
  prognose/      # Django project: settings, urls, wsgi
  accounts/      # Company (custom user), login and logout
  planning/      # models, queries.py, adjustments.py, forms, views, templates, templatetags
  forecasting/   # pure: rules R-1 to R-17, rounding.py, compute_product, sort_overview
  explanation/   # pure: explain(), number check, optional rephrase.py
  static/        # css (tokens + app), fonts, vendor/chart.js, js/charts.js
  templates/     # base, landing, 404, 500
  data/          # generate_seed.py and seed/ (versioned)
  reference/     # examples.json and the reference spreadsheet
  docs/          # process documents, QA log, status table, AI steering log
```

```mermaid
flowchart LR
  B[Browser on the same PC] -->|HTTP 127.0.0.1:8000| W[Django runserver]
  W --> S[(db.sqlite3, gitignored)]
  W -.optional, off by default.-> L[Local language model endpoint]
  G[GitHub: main branch] -->|deploy| V[Vercel Function in fra1: Django WSGI]
  U[Browser on the internet] -->|HTTPS| V
  U -->|/static/| C[Vercel CDN]
  V -->|pooled DATABASE_URL| P[(Neon PostgreSQL, Frankfurt)]
  O[PC of the project owner] -.migrate and load_seed, unpooled URL.-> P
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
| Login and isolation (FR-1, FR-2) | `accounts/`, `planning/queries.py` | AD-5, AD-6 |
| Seed data and storage (FR-3, FR-4) | `data/`, `planning` models, `load_seed` | AD-12 |
| Forecasts, scenarios, orders (FR-5 to FR-13) | `forecasting/` | AD-2, AD-3, AD-4, AD-7 |
| Warnings and confidence (FR-14 to FR-19, FR-36) | `forecasting/` | AD-2 |
| Settings (FR-20 to FR-23) | `planning` (CompanySettings, forms, views) | AD-8 |
| Overview, product screen, forecast calculation (FR-24, FR-25, FR-35) | `planning` views and templates, `static/js/charts.js` | AD-2, AD-11 |
| Explanation (FR-26 to FR-28) | `explanation/` | AD-10 |
| Purchase planning (FR-29 to FR-32) | `planning/adjustments.py`, views | AD-8, AD-9 |
| Accuracy and stock through weeks 2 and 3 (FR-33, FR-34) | `forecasting/` | AD-2 |
| Quality and delivery (NFR-1 to NFR-11, DR-1 to DR-9) | conventions, `docs/` | AD-11 to AD-14 |
| Publishing (DR-10, SM-9) | `prognose/settings.py`, `vercel.json`, `.python-version`, Vercel project, Neon | AD-12, AD-13, AD-15, AD-16 |

## Deferred

- **Local model runtime and model (FR-28, PRD question 5):** chosen when FR-28 is scheduled. AD-10 already fixes the seam.
- **Exact schemas of the seed files and `reference/examples.json`:** set in the data story. AD-12 and AD-14 fix where they live and who reads them.
- **Could items (per-product settings FR-23, saved adjustments FR-31, CSV export FR-32):** decided when scheduled. FR-31 swaps the storage behind AD-9.
- **Caching:** only if the NFR-8 check fails, and it needs an amendment to AD-3.
- **How Impeccable reads the single DESIGN.md during the build:** decided in the first UI story. There is never a second copy.
- **Account limits, checked in the first story:**
  - The IBE160-2026 organization must allow the Vercel GitHub app. If it does not, the owner deploys `main` with the Vercel CLI (65.12.1) instead.
  - Vercel Hobby blocks deployments when a commit author other than the owner appears in a private repository, and community reports say Claude co-author lines can trigger this. The repository is public, which Vercel staff describe as exempt.
  - If deployments are still blocked, the owner merges pull requests with a merge commit, so the deployed commit is the owner's.
- **Free-plan terms:** re-checked before submission. Vercel Hobby is for non-commercial use, and Neon stops access at its limits instead of charging.
