---
title: 'Story 1.1: Project skeleton running locally and on Vercel'
type: 'feature'
created: '2026-11-10'
status: 'ready-for-dev'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-08/ARCHITECTURE-SPINE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Prognose has no code yet, and the publishing path (Vercel with Neon PostgreSQL) is unproven, so every later story would build on an untested base.

**Approach:** Create the Django 5.2 skeleton from the architecture's structural seed, with settings that run locally on SQLite and on Vercel with Neon: a Norwegian start page, Norwegian 404 and 500 pages, the custom user model in the first migration, a health check, and a first `load_seed` that only creates the local secret. The owner then connects Vercel and Neon, and the first deploy from `main` proves the path.

## Boundaries & Constraints

**Always:** follow AD-1, AD-5, AD-12, AD-13, AD-15 and AD-16 of the architecture spine; exact pins in `requirements.txt`; Norwegian UI text and `lang="nb"`; DEBUG off unless `.env` turns it on locally; settings never connect to the database at import; ORM only; on Vercel the database is always Neon PostgreSQL through `DATABASE_URL`, never SQLite (user decision at approval, 2026-11-10).

**Never:** no login UI, seed data, product models or design tokens (Stories 1.2 to 1.4); no `pyproject.toml`, `asgi.py` or Django admin; no CDN; no hard-coded or committed secret; no raw SQL; no preview deployments; no commit or push without the user's approval.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Local run | no `VERCEL`, no `DATABASE_URL` | SQLite at `db.sqlite3`; `/` returns 200 with `lang="nb"` and `/static/css/app.css` | N/A |
| Secret missing | `.secret_key` absent | `load_seed` creates it with mode 0600; until then each process uses a random in-memory key | N/A |
| Secret present | `.secret_key` exists | settings read it; `load_seed` leaves it unchanged | N/A |
| PostgreSQL URL | `postgresql://u:p%40ss@h:5432/db` | engine postgresql, NAME `db`, USER `u`, PASSWORD `p@ss`, HOST `h`, PORT 5432, `sslmode=require`, `CONN_MAX_AGE=0`, `DISABLE_SERVER_SIDE_CURSORS=True` | N/A |
| Published | `VERCEL=1`, `SECRET_KEY`, `DATABASE_URL`, `VERCEL_PROJECT_PRODUCTION_URL=x.vercel.app`, `VERCEL_URL=y.vercel.app` | DEBUG off; both hosts allowed; `https://` trusted origins; secure cookies; proxy SSL header | N/A |
| Published, incomplete | `VERCEL=1` without `SECRET_KEY` or `DATABASE_URL` | startup stops | `ImproperlyConfigured` naming the missing variable |
| Unknown address | `GET /finnes-ikke/` | 404 with the Norwegian «Ikke funnet» page and a link to `/` | never a debug page |
| Health | `GET /helse/` | 200 `ok` after an ORM read of `Company` | a database error gives the Norwegian 500 page |

</frozen-after-approval>

## Code Map

Greenfield: no application code exists. Existing files to touch: `.gitignore` (append) and `README.md` (keep the intro, add sections). Leave `_bmad/`, `.claude/`, `.impeccable/`, `docs/`, `.logs/` and `PRODUCT.md` untouched.

## Tasks & Acceptance

**Execution:**
- [ ] `requirements.txt` -- pin `Django==5.2.19`, `psycopg[binary]==3.3.8`, `ruff==0.17.4` and their resolved dependencies -- DR-2
- [ ] `.python-version`, `ruff.toml`, `vercel.json`, `.env.example`, `.gitignore` -- `3.13`; Ruff for Python 3.13 excluding `_bmad*`, `.claude`, `.impeccable` and migrations; `"regions": ["fra1"]` and `"git": {"deploymentEnabled": {"**": false, "main": true}}`; optional `DEBUG`, `PROGNOSE_LLM_URL`, `PROGNOSE_LLM_MODEL`; ignore `db.sqlite3`, `staticfiles/`, `.secret_key` -- AD-13, AD-16
- [ ] `manage.py`, `prognose/__init__.py`, `prognose/wsgi.py`, `prognose/urls.py` -- entry points; `WSGI_APPLICATION` for Vercel
- [ ] `prognose/env.py` -- pure helpers `read_dotenv`, `database_config`, `published_settings`, `load_secret_key` -- keeps settings testable
- [ ] `prognose/settings.py` -- apps `auth`, `contenttypes`, `sessions`, `staticfiles`, `accounts`, `planning`; `LoginRequiredMiddleware`; `AUTH_USER_MODEL`, `LOGIN_URL='/'`; templates and static dirs, `STATIC_ROOT=staticfiles/`; local `ALLOWED_HOSTS` `127.0.0.1` and `localhost`; `nb`, `Europe/Oslo`; `.env` read only locally -- AD-5, AD-13
- [ ] `accounts/` -- `Company(AbstractBaseUser)` with unique `customer_number` (`USERNAME_FIELD`), `name`, a manager with `create_user`; `migrations/0001_initial.py` -- AD-5
- [ ] `planning/` -- views `start` and `health`, both `login_not_required`; `management/commands/load_seed.py` that creates `.secret_key` (`secrets.token_urlsafe(50)`) when missing -- AD-12
- [ ] `forecasting/__init__.py`, `explanation/__init__.py`, `data/.gitkeep`, `reference/.gitkeep` -- structural seed
- [ ] `templates/base.html`, `templates/planning/start.html`, `templates/404.html`, `templates/500.html`, `static/css/app.css` -- Norwegian pages: «Prognose» start page, «Ikke funnet» with «Til startsiden», «Noe gikk galt»
- [ ] `prognose/tests.py`, `accounts/tests.py`, `planning/tests.py` -- the I/O matrix, PBKDF2 hashing, the first migration, `load_seed` idempotence, and that `forecasting/` and `explanation/` import no Django (AD-1)
- [ ] `README.md` -- «Kom i gang lokalt» (macOS Terminal and Windows PowerShell) and «Publisering» (owner steps below)

**Acceptance Criteria:**
- Given a fresh clone and Python 3.13, when the README commands run (virtual environment, `pip install -r requirements.txt`, `migrate`, `load_seed`, `runserver --insecure`), then the start page loads on 127.0.0.1:8000, and `python manage.py test`, `ruff check .` and `ruff format --check .` pass.
- Given the owner's Vercel project and Neon database, when the pull request is merged to `main` and the owner has run `migrate` against Neon, then `https://<address>/` and `/static/css/app.css` load, `/helse/` returns `ok`, and a push to another branch creates no deployment.
- Given the first deploy, then the AR-17 results (GitHub app allowed, no Hobby author block) are recorded in the pull request.

## Design Notes

Without a secret file, a random in-memory key keeps `migrate`, `load_seed` and the tests working on a fresh clone, with nothing hard-coded; `load_seed` then makes the key stable. The health check exists because the start page reads no data, and AC 2 needs proof that the published app reads PostgreSQL.

Owner steps (human, after review): import the repository in Vercel (suggested project name `prognose-g40`; if the organization blocks the Vercel app, deploy with `npx vercel@65.12.1 deploy --prod`); add Neon (free plan, AWS Frankfurt) from Storage; set `SECRET_KEY` for Production; merge the pull request; run `DATABASE_URL='<DATABASE_URL_UNPOOLED>' python manage.py migrate` once from the PC; check the address.

## Verification

**Commands:**
- `python manage.py check` -- no issues
- `python manage.py makemigrations --check --dry-run` -- no changes
- `python manage.py test` -- all pass
- `ruff check . && ruff format --check .` -- clean
- `curl` against `runserver --insecure`: `/` 200 with `lang="nb"`, `/static/css/app.css` 200, `/finnes-ikke/` 404 with «Ikke funnet», `/helse/` `ok`

**Manual checks (if no CLI):**
- The owner steps above, and the published address in a browser.

## Implementation Notes

## Spec Change Log

## Review Triage Log
