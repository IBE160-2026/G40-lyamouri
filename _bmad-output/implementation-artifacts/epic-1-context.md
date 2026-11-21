# Epic 1 Context: Log in and see only your own company's data

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Build Prognose's foundation so that an examiner can go from a fresh clone, without paid services, keys or file editing, to logging in as either of two synthetic test companies and seeing only that company's products, kept in a local database that survives restarts. Later epics reuse its CI, app shell, error pages, answer-key spreadsheet, seed data and isolation test. Version 1 runs only locally and is not published.

## Stories

- Story 1.1: Start Prognose locally from a fresh clone
- Story 1.2: Check every pull request automatically
- Story 1.3: Confirm the setup on Windows and without a network
- Story 1.4: Norwegian app shell and error pages
- Story 1.5: Reference spreadsheet as the answer key
- Story 1.6: Generate the synthetic seed data
- Story 1.7: Load the seed data into an empty database, with an explicit reset
- Story 1.8: Log in and see only your own company's products

## Requirements & Constraints

- **Login (FR-1):** one Norwegian message for any failed login, never naming the wrong field. No plain-text password anywhere, the seed data and logs included. Logging out ends the session.
- **Isolation (FR-2):** enforced on the server: lists hold only the company's products, and a direct request for another company's product gives "not found". The two-account test covers every route and list, and each new one extends it.
- **Data (FR-3, FR-4, DR-4):** synthetic and deterministic, so every rule, warning and confidence label has a known answer. Products, sales and stock are read-only in the app, data and settings survive restarts, and only a confirmed explicit reset deletes data.
- **Local and robust (NFR-1, NFR-3, NFR-4, NFR-10):** runs offline on macOS and Windows with no paid service, key, account or CDN; no secrets, personal data or local paths in the repository; reload, Back and double submit are safe.
- **Every story (DR-5, DR-7, DR-9):**
  - Own branch. Done when the tests and Ruff pass locally and in CI, no commented-out, unused or duplicated code remains, and the status table and affected documents are updated. Only Story 1.1, built before CI, merges on local checks (D-9).
  - The pull request names the story, its FR-n and what was tested, and records each BMAD Code Review finding with its decision and fix commit (D-8).
  - Each test names its FR-n or E-n; one that verifies no FR, as tests of the setup, run-mode settings, secret file or repository do, names its NFR-n, DR-n or AD-n instead (D-10).
  - Open points go to `.logs/<bruker>/issues.md`, AI defects to `docs/qa-logg.md`, rejected or corrected AI output to `docs/ki-styringslogg.md` (at least one case per epic), and privacy-checked AI sessions to `.logs/<bruker>/sessions/`.
  - Changed pages are checked in the responsive view at 320 px, 390 × 844 and 820 × 1180.

## Technical Decisions

- **Pure core (AD-1 to AD-3):** `forecasting/` and `explanation/` import only the standard library (`explanation/` may import `forecasting/`, not the reverse) and read no clock, files or environment, as an import test enforces. Only the core calculates, rounds, sorts or groups domain values; `forecasting/display.py` formats every shown number and week label.
- **Login and state (AD-6, AD-10):** the company is the user, with Django's default PBKDF2 hasher; login-required middleware denies by default, exempting only the login and error pages. Every change, logout included, is a CSRF-protected POST and a redirect, and sessions live in the database.
- **Company data (AD-7, AD-8, AD-14):** besides `load_seed` and the migrations, company data goes only through `web/queries.py` functions that take the logged-in company first and filter by it, and a lookup outside it raises `Http404`. Histories are gapless ISO-week runs ending at the latest data week, which is derived from the data and never stored; no domain code reads today's date. ORM only, no raw SQL.
- **Errors (AD-12):** DEBUG stays off unless the local `.env` turns it on; every error status gets a Norwegian page, and a database error raised anywhere gets the 503 page from the outermost middleware, which reads nothing from the database. Logs never hold request bodies, passwords, secrets or database URLs.
- **Seed and reset (AD-15):** the generator's versioned JSON is identical on every run and takes the rule-test series from the spreadsheet; `load_seed` loads only into an empty database, and `--reset` asks for typed confirmation.
- **Tests and CI (AD-17):** `uv run pytest` runs everything against the local PostgreSQL, including the import test and `makemigrations --check`; CI runs it and Ruff on Linux for each pull request, with the same `compose.yaml`. The spreadsheet in `reference/` is the only answer key: no expected value is copied into code, and a disagreement is recalculated by hand and logged in the QA log.

## UX & Interaction Patterns

- Pages share one stylesheet of design-token CSS variables, system fonts and a flat look: no shadows or animation, a 3 px blue focus outline, and never color alone. Every page has `lang="nb"`, the responsive viewport, one `h1` and the navy app header (only the wordmark when logged out).
- All text is Norwegian bokmål, messages come verbatim from the Message Catalogue, and login follows its wireframe. Nothing scrolls sideways from 320 px, touch targets are at least 44 × 44 px, and everything works without scripts and by keyboard (WCAG 2.2 AA). Error pages reuse the not-found panel and show no data or technical details.

## Cross-Story Dependencies

- **Order:** 1.1, 1.2, 1.4, 1.6, 1.7, then 1.8. Story 1.5 may run alongside 1.1 to 1.4 but must precede 1.6, whose generator reads it. Story 1.3 blocks nothing.
- **CI (D-9):** the first CI run comes with Story 1.2's pull request and runs every test on Linux, Story 1.1's included.
- **Data chain:** Story 1.6 reads the spreadsheet in Story 1.5's documented schema, and Story 1.7 loads the seed in Story 1.6's, extending Story 1.1's `load_seed`, which so far only creates the secret file and must never overwrite it.
- **Story 1.8** needs Story 1.4's 503 page and creates the header's week label in `forecasting/display.py`, with a test, for Story 2.3 to extend (a tracked open point).
- **Later epics:** Epic 2 checks the seeded rule-test products against the spreadsheet and replaces Story 1.8's simple product list.
