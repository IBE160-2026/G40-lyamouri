# Epic 1 Context: Secure login and own data, published from day one

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

A user of one of two synthetic test companies can log in, on their own PC and on the published Vercel address, and see only their own company's products, loaded from deterministic seed data. The epic also proves the whole delivery path in the first week: a Django skeleton that runs locally on SQLite and deploys from `main` to Vercel with a Neon PostgreSQL database. Later epics build forecasts, settings and explanations on top of it.

## Stories

- Story 1.1: Project skeleton running locally and on Vercel
- Story 1.2: Synthetic data for two test companies
- Story 1.3: Log in on the landing page
- Story 1.4: See only my own company's products

## Requirements & Constraints

- Login with customer number and password; one general Norwegian error, «Feil kundenummer eller passord.»; every page except the landing/login page requires login; logout ends the session.
- Passwords use Django's default PBKDF2 hasher; no plaintext password in the database, seed files or logs.
- Company isolation is enforced on the server for every request: another company's product gives the same Norwegian "not found" page as an unknown one, lists show only the logged-in company's data, and an automated two-account test covers every view and list.
- Seed data: two companies with 10 to 50 products each (number, name, weekly history with stockout flags, stock on hand), most with 104 weeks, covering the patterns the rules need. The generator gives identical output on every run, including password hashes, and its output is versioned; one load command resets the database to the seed state without duplicates.
- Data survives restarts: SQLite locally, PostgreSQL when published.
- Norwegian (bokmål) UI with `lang="nb"`; no debug pages or stack traces; unknown addresses show a Norwegian "not found" page.
- The local app works offline after installation: no CDN, self-hosted fonts and assets.
- Free services only; secrets are never committed; `.env.example` lists optional configuration.
- Accessibility floor: WCAG 2.2 AA contrast, keyboard-only use with a visible focus, visible labels.
- Every story: tests and Ruff pass, one branch and one reviewed pull request, FR references in the story, tests and commits.

## Technical Decisions

- Python 3.13, Django 5.2.19 LTS, psycopg[binary] 3.3.8 and Ruff 0.17.4, with exact pins in one `requirements.txt`, plus `.python-version` and `ruff.toml`; no `pyproject.toml`.
- Layout: `prognose/` (project), `accounts/`, `planning/`, `forecasting/` and `explanation/` (pure Python, never importing Django), `static/`, `templates/`, `data/` (generator and `seed/`), `reference/`, `docs/`.
- Custom user model `accounts.Company` with `customer_number` as the login field, present in the very first migration; `LoginRequiredMiddleware`, with only the landing/login view exempt.
- All company data goes through `planning/queries.py` functions that take the logged-in company first; outside the company they raise `Http404`; views never use model managers for company data.
- Products are addressed as `/produkter/<varenummer>/`, unique per company; sales weeks are identified by position, with year and week number for display only.
- Every mutation is a form POST followed by a redirect, with CSRF on.
- `python manage.py load_seed` resets idempotently from `data/seed/` and creates the gitignored session-secret file when it is missing.
- Without `DATABASE_URL` the app uses `db.sqlite3` (gitignored). With it, PostgreSQL: the URL is parsed with `urllib.parse`, with `sslmode=require`, `CONN_MAX_AGE = 0` and `DISABLE_SERVER_SIDE_CURSORS = True`. ORM and migrations only, tests on SQLite, and no file writes at request time.
- Local run: `python manage.py runserver --insecure` on 127.0.0.1. DEBUG is off by default, and only `.env` turns it on locally. `LANGUAGE_CODE = 'nb'`, `TIME_ZONE = 'Europe/Oslo'`, Norwegian 404 and 500 templates.
- Published: Vercel Hobby runs `prognose/wsgi.py` as one function in `fra1`; `STATIC_ROOT` is `staticfiles/` (gitignored), and Vercel runs `collectstatic` and serves `/static/` from its CDN. When `VERCEL` is set, settings force DEBUG off, build `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` from `VERCEL_PROJECT_PRODUCTION_URL` and `VERCEL_URL`, set `SECURE_PROXY_SSL_HEADER` and secure cookies, and stop with a clear error if `SECRET_KEY` or `DATABASE_URL` is missing.
- `vercel.json`: `"regions": ["fra1"]` and `"git": {"deploymentEnabled": {"**": false, "main": true}}`; no preview deployments.
- Neon free plan, created from the Vercel dashboard in AWS Frankfurt. The app uses the pooled `DATABASE_URL`; the owner runs `migrate` and `load_seed` from their PC with `DATABASE_URL_UNPOOLED` for one command and never stores it in a file.
- One group member owns the Vercel project. Account limits to check: the course GitHub organization must allow the Vercel app (fallback: Vercel CLI deploy by the owner), and Hobby can block deployments with commit authors other than the owner in private repositories (the repository is public; fallback: the owner merges with a merge commit).
- Console logging only; never log passwords, secrets or request bodies.
- Before every pull request: `python manage.py test`, `ruff check` and `ruff format --check`; no CI service.

## UX & Interaction Patterns

- DESIGN.md (tokens, components) and EXPERIENCE.md (behavior) win over the mockups; the approved landing mockup is `ux-designs/ux-G40-lyamouri-2026-11-06/mockups/key-landing.html`.
- DESIGN.md tokens become CSS custom properties in one stylesheet; Albert Sans is self-hosted (OFL) with a fallback stack.
- The landing page is the login page: wordmark, map frame, login panel with visible labels, primary button and «Prøv selv»; the login error is announced with `role="alert"`; a skip link leads to the login.
- The app shell has the app rail with the active nav item and a skip link to the content.
- A 3 px `magenta-ink` focus ring, Tab order in reading order, touch targets of at least 44 px, and the landing breakpoints from 901 px down to 640 px.

## Cross-Story Dependencies

- Story 1.1 provides the project, settings, Vercel and Neon, `accounts.Company` and the first `load_seed`, which only creates the secret.
- Story 1.2 builds on 1.1; 1.3 on 1.1 and the test logins from 1.2; 1.4 on 1.2 and 1.3 and fills the overview page that 1.3 creates as a placeholder.
- The two-account isolation test from 1.4 is extended by later epics (settings in Epic 3, order quantities in Epic 6), and Epic 2 builds the product screen on the minimal product page from 1.4.
