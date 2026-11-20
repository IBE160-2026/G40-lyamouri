# Epic 1 Context: Log in and see only your own company's data

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Build Prognose's foundation by hand, since there is no starter template. From a fresh clone, an examiner starts a local PostgreSQL with one command, loads two synthetic test companies, logs in as either one and sees only that company's products, and the data survives restarts. Later epics build on the skeleton, CI, app shell, answer key, seed data and isolation test made here. Version 1 runs only locally and is not published (D-1).

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

- **Login (FR-1):** a failed login gets one message that does not say which field was wrong, and no password exists in plain text anywhere.
- **Isolation (FR-2, SM-4):** the server checks the company on every request, and lists hold only that company's products. A two-account test covers every route and list, and every later route or list extends it.
- **Data (FR-3, FR-4, DR-4, NFR-4):** deterministic synthetic data gives every rule, warning and confidence label a known answer. It survives restarts, and only a confirmed reset deletes it.
- **Local and free (NFR-1, NFR-3, NFR-9):** one app and one local database, with no paid service, API key, account or CDN. It works offline, and the repository holds no secrets.
- **Robust and responsive (NFR-10, NFR-6):** no page ever shows a stack trace or a debug page, and from 320 px wide nothing scrolls sideways.
- **Every story (DR-5, DR-7, DR-9, D-8):**
  - It uses its own branch. It is done when tests and Ruff pass locally and in CI, no commented-out, unused or duplicated code remains, and the status table and affected documents are updated.
  - Its pull request names the story, its FR-n and what was tested, and records each BMAD Code Review finding with its decision and fix commit. Each test names its FR-n or E-n.
  - Open points go to `.logs/<bruker>/issues.md`, AI defects to `docs/qa-logg.md`, and rejected or corrected AI output to `docs/ki-styringslogg.md`. Session exports go to `.logs/<bruker>/sessions/`, privacy-masked and committed with the pull request.
  - Page changes are checked in the responsive view at 320 px, 390 × 844 and 820 × 1180.

## Technical Decisions

- **Pure core (AD-1, AD-2, AD-3):**
  - `forecasting/` and `explanation/` import only the standard library, and `explanation/` may import `forecasting/` but not the reverse. Neither reads the clock, files or environment, and an import test enforces this.
  - Nothing outside the core calculates, rounds, sorts or groups domain values.
  - `forecasting/display.py` formats every number and week label shown.
- **Login and state (AD-6, AD-10):** `web.Company` is the user model from the first migration, with `customer_number` as its login field and Django's default PBKDF2 hasher. `LoginRequiredMiddleware` exempts only the login page at `/` and the error pages. Every change, login and logout included, is a CSRF-protected POST and a redirect, and sessions live in the database.
- **Company data (AD-7, AD-8):** apart from `load_seed` and the migrations, all company data goes through functions in `web/queries.py` that take the logged-in company first and filter by it. A lookup outside the company raises `Http404`. Weeks are ISO weeks ordered by position, and the latest data week is derived, never stored.
- **Errors (AD-12):** DEBUG is off unless the local `.env` sets `PROGNOSE_DEBUG`. Every error status gets a Norwegian page. A database error raised anywhere gets a 503 page from the outermost middleware, and that page reads nothing from the database. Logs hold no request bodies, passwords, secrets or database URLs.
- **Run mode (AD-13, AD-14):** settings come only from environment variables, whose defaults need no setup. The app and the database listen only on 127.0.0.1, except the app during the phone test (`PROGNOSE_LAN_HOST`). `load_seed` creates the git-ignored session secret `.secret_key` and never overwrites it.
- **Seed (AD-15):** the generator writes identical, versioned JSON with password hashes made with a fixed salt per company. `load_seed` loads only into an empty database, and only `--reset` deletes data, after a typed confirmation.
- **Tests (AD-17):** `uv run pytest` runs everything against the local PostgreSQL, including the import test and `makemigrations --check`. The spreadsheet in `reference/` is the single answer key, so no expected value is written into code.

## UX & Interaction Patterns

- One stylesheet turns the DESIGN.md tokens into CSS custom properties, and components use only those. Nothing loads from outside the app.
- Every page declares `lang="nb"` and the responsive viewport, has one `h1` and shows the navy app header (only the wordmark when logged out).
- Messages come verbatim from the Message Catalogue, and labels from the glossary. Error pages use the not-found panel and show no data or technical details.

## Cross-Story Dependencies

- **Order:** 1.1, 1.2, 1.4, 1.6, 1.7, then 1.8. Story 1.5 can run alongside 1.1 to 1.4 but must be done before 1.6, whose generator reads it. Story 1.3 blocks nothing.
- **Story 1.1** makes a `load_seed` that only creates the secret file (Story 1.7 adds the loading). It also starts the status table, the AI steering log and the QA log.
- **Story 1.8** needs the 503 page from Story 1.4. For its header it creates the first week label in `forecasting/display.py`, with a test, and Story 2.3 extends it. This is recorded as an open point.
- **Epic 2** replaces Story 1.8's product list, and tests its calculations and the seeded rule test products against the spreadsheet. Only its core can compute the demo figures that Story 1.6 aims at.
