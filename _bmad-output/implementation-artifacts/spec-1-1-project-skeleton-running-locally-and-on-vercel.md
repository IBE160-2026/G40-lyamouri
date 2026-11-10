---
title: 'Story 1.1: Project skeleton running locally and on Vercel'
type: 'feature'
created: '2026-11-10'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'c87e1cb3faf19e6ce3d837cc59ed0f863fd8f19c'
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
- [x] `requirements.txt` -- pin `Django==5.2.19`, `psycopg[binary]==3.3.8`, `ruff==0.17.4` and their resolved dependencies -- DR-2
- [x] `.python-version`, `ruff.toml`, `vercel.json`, `.env.example`, `.gitignore` -- `3.13`; Ruff for Python 3.13 excluding `_bmad*`, `.claude`, `.impeccable` and migrations; `"regions": ["fra1"]` and `"git": {"deploymentEnabled": {"**": false, "main": true}}`; optional `DEBUG`, `PROGNOSE_LLM_URL`, `PROGNOSE_LLM_MODEL`; ignore `db.sqlite3`, `staticfiles/`, `.secret_key` -- AD-13, AD-16
- [x] `manage.py`, `prognose/__init__.py`, `prognose/wsgi.py`, `prognose/urls.py` -- entry points; `WSGI_APPLICATION` for Vercel
- [x] `prognose/env.py` -- pure helpers `read_dotenv`, `database_config`, `published_settings`, `load_secret_key` -- keeps settings testable
- [x] `prognose/settings.py` -- apps `auth`, `contenttypes`, `sessions`, `staticfiles`, `accounts`, `planning`; `LoginRequiredMiddleware`; `AUTH_USER_MODEL`, `LOGIN_URL='/'`; templates and static dirs, `STATIC_ROOT=staticfiles/`; local `ALLOWED_HOSTS` `127.0.0.1` and `localhost`; `nb`, `Europe/Oslo`; `.env` read only locally -- AD-5, AD-13
- [x] `accounts/` -- `Company(AbstractBaseUser)` with unique `customer_number` (`USERNAME_FIELD`), `name`, a manager with `create_user`; `migrations/0001_initial.py` -- AD-5
- [x] `planning/` -- views `start` and `health`, both `login_not_required`; `management/commands/load_seed.py` that creates `.secret_key` (`secrets.token_urlsafe(50)`) when missing -- AD-12
- [x] `forecasting/__init__.py`, `explanation/__init__.py`, `data/.gitkeep`, `reference/.gitkeep` -- structural seed
- [x] `templates/base.html`, `templates/planning/start.html`, `templates/404.html`, `templates/500.html`, `static/css/app.css` -- Norwegian pages: «Prognose» start page, «Ikke funnet» with «Til startsiden», «Noe gikk galt»
- [x] `prognose/tests.py`, `accounts/tests.py`, `planning/tests.py` -- the I/O matrix, PBKDF2 hashing, the first migration, `load_seed` idempotence, and that `forecasting/` and `explanation/` import no Django (AD-1)
- [x] `README.md` -- «Kom i gang lokalt» (macOS Terminal and Windows PowerShell) and «Publisering» (owner steps below)

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

Implementation pass, 2026-11-10:

- **Files:** `requirements.txt`, `.python-version`, `ruff.toml`, `vercel.json`, `.env.example`, `.gitignore` (appended), `README.md` (intro kept); `manage.py`; `prognose/` (`__init__`, `env`, `settings`, `urls`, `wsgi`, `tests`); `accounts/` (`__init__`, `models`, `tests`, `migrations/0001_initial`); `planning/` (`__init__`, `views`, `tests`, `management/commands/load_seed`); `forecasting/__init__.py`, `explanation/__init__.py`, `data/.gitkeep`, `reference/.gitkeep`; `templates/` (`base`, `planning/start`, `404`, `500`); `static/css/app.css`.
- **Pins:** asgiref 3.13.0, sqlparse 0.6.1, psycopg-binary 3.3.8 and tzdata 2026.6 (Windows only, through its marker). typing-extensions is not needed on Python 3.13. Wheels exist for macOS, Windows and Linux x86_64 (Vercel).
- **Decisions:**
  - `prognose/env.py` also has `env_flag()`, which parses DEBUG. DEBUG is read only from `.env`, so a `DEBUG` variable in the process environment cannot turn it on (AD-13 wording).
  - `database_config()` refuses a non-PostgreSQL URL and ignores URL query parameters, so `sslmode` is always `require`. No error message repeats a secret or the URL.
  - The `SECRET_KEY_FILE` setting holds the secret file's path, so the tests point `load_seed` at a temporary folder.
  - `LOGGING` sends the `django` logger to the console in both run modes. Without it, Django drops request errors when DEBUG is off, and Vercel's logs would show no traceback behind the 500 page.
  - `Company` has Norwegian verbose names («kundenummer», «navn», «bedrift»); Django's login form uses the first as its label. `REQUIRED_FIELDS` is a tuple to satisfy Ruff (RUF012).
  - Ruff 0.17 ships a broad curated default rule set, so `ruff.toml` keeps the defaults and adds only the Django rules (DJ). Ruff 0.17's formatter also checks Python code blocks in Markdown files (`.logs/`, `docs/`, README); none exist today.
  - Tests check the run modes twice: through the helpers, and by starting Django through `prognose.wsgi` in a subprocess (local, published, and published without each required variable). AD-1 is checked by parsing every file in `forecasting/` and `explanation/` for imports of `django`, `accounts`, `planning` or `prognose`.
- **Surprises:**
  - Vercel sets the Framework Preset at import and uses it for all later deployments. Before the merge, `main` has no `manage.py`, so Vercel would choose «Other». README step 1 tells the owner to choose «Django».
  - Vercel runs `manage.py` and `collectstatic` during the build, so the settings load at build time with `VERCEL=1`. `SECRET_KEY` and the Neon variables must exist before the first Django deploy; owner steps 2 and 3 come before the merge.
  - The 400 (unknown host) and 403 (CSRF) pages are still Django's English defaults. This story does not require Norwegian versions.

Verification pass, 2026-11-10:

- The README flow ran on a copy holding only the files git would commit, with a new `.venv`: `pip install`, `migrate`, `load_seed` (mode 0600, unchanged on the second run), `check`, `makemigrations --check`, 28 tests, Ruff, and the curl checks all passed. `collectstatic` with `VERCEL=1` needed no database. The pins resolve to wheels for Linux x86_64 (cp313), Windows and macOS, and tzdata 2026.6 exists.
- Matrix audit: two tests were tightened. The subprocess probe now records which secret file the settings read (`.secret_key` locally, none on Vercel), so the «Secret present» row checks the real settings, not only the helper. The health test now checks that its one query reads `accounts_company`. Both new checks failed against a mutated copy and pass against the real code.

Review pass 1 patches, 2026-11-10 (see the Review Triage Log):

- Tests: the probe now controls `.env` through `PROBE_DOTENV` (local DEBUG on from `.env`, off from the process environment, never read on Vercel), starts the local settings with `DATABASE_URL`, and checks that a `django.request` error reaches stderr with DEBUG off. Each new check failed against its mutation (DEBUG from the process environment, `DATABASES` only on Vercel, no `LOGGING` block). 30 tests pass.
- README: step 5 reads `DATABASE_URL_UNPOOLED` from the clipboard (`"$(pbpaste)"`, `Get-Clipboard` in `try`/`finally`), so the URL stays out of shell history (AD-16). This intentionally differs from the inline example in Design Notes, and later stories that run `load_seed` against Neon should reuse it. Step 1 now says the first deploy at import is expected to fail and that the CLI fallback runs from a fresh clone. Step 6 names the production domain.
- `.gitignore` uses `db.sqlite3*`, and `base.html` has `<link rel="icon" href="data:,">`.

## Spec Change Log

## Review Triage Log

Review pass 1, 2026-11-10. Layers: blind hunter (BH), edge case hunter (EC), verification gap (VG). Routes: patch, defer, reject.

| ID | Location | Finding | Verdict | Route | Evidence |
|----|----------|---------|---------|-------|----------|
| VG-1 | `prognose/tests.py` `test_local_run` | DEBUG from `.env` never runs through the real settings; the expectation reads the developer's own `.env` | medium | patch | Pre-verified: on a fresh clone, settings that read `.env.example` or set `DEBUG = False` pass all 28 tests; with a `.env` holding `DEBUG=1`, reading DEBUG from the process environment passes too. |
| VG-2 | `prognose/settings.py` `DATABASES` | A local run with `DATABASE_URL` (README step 5) is never started through the real settings | medium | patch | Pre-verified: building `DATABASES` from `DATABASE_URL` only on Vercel passes all 28 tests, and step 5 then migrates the local SQLite file and reports success while Neon gets no tables. |
| VG-3 | `prognose/settings.py` `LOGGING` | No test checks that request errors reach the console with DEBUG off | medium | patch | Pre-verified: deleting `LOGGING` passes all 28 tests, because `assertLogs` replaces the handlers; without it the published 500 leaves stderr empty, the only diagnostic channel on Vercel. |
| VG-O1 | `load_seed.py`, `prognose/env.py` | An empty `.secret_key` is never repaired and gives a new key per process | low | reject | Reproduced by the layer, but only `touch` or a write failing right after `os.open` makes an empty file; the effect is local and is cured by deleting the file; the fix adds a repair branch. Same root cause as BH-8 and EC-12. |
| BH-1 | `README.md` step 5 | The unpooled Neon URL typed into the command is saved in shell history | medium | patch | macOS `/etc/zshrc` sets `HISTFILE=~/.zsh_history` and `SAVEHIST=1000`, so the password lands in a file, against AD-16; the owner meets it on every run; reading the value from the clipboard is a direct README fix. Same root cause as EC-20. |
| BH-2 | `README.md` step 1 | The CLI fallback run from the working copy uploads git-ignored files | low | patch | Vercel's docs: the CLI uploads everything except `.vercelignore` entries and a default list that has `.venv`, `__pycache__` and `.env.local` but not `.env`, `.secret_key`, `db.sqlite3`, `staticfiles/` or local tool config. The files stay behind login (`/_src`), but every deploy would use this path if AR-17 fails. Direct README fix. Same root cause as EC-21. |
| BH-3a | `vercel.json` | The Framework Preset is left to a manual dashboard choice | low | reject | README step 1 already says to pick Django, and a wrong preset fails visibly and is fixed in Settings; Vercel's docs list no slug for Django in text, so adding `"framework"` is an unverified new parameter. |
| BH-3b | `README.md` step 1 | Importing deploys today's `main`, which fails, and the README does not say this is expected | low | patch | Import starts a production deploy of the default branch, and `main` has no `manage.py` before the merge, so the owner will see a failed first deploy; one sentence fixes it. |
| BH-4 | `prognose/env.py` `published_settings`, `settings.py` `ON_VERCEL` | Missing Vercel system variables give no clear error | low | reject | Vercel exposes `VERCEL`, `VERCEL_URL` and `VERCEL_PROJECT_PRODUCTION_URL` by default, so the owner would have to switch that off; the result is a loud 400 with the DisallowedHost reason in the logs, not silent insecurity; the fix adds guards. Same root cause as EC-4 and EC-11. |
| BH-5 | `README.md` step 6 | `<adresse>` is unspecified, and the branch alias gets Django's English 400 | low | patch | Only `VERCEL_PROJECT_PRODUCTION_URL` and `VERCEL_URL` are allowed (frozen matrix), so the `…-git-main-…` alias gets the built-in 400; naming the production domain is a direct fix. Sub-points are not defects: a failed build shows its log in the dashboard, and no custom domain is planned. Same root cause as EC-5. |
| BH-6 | `README.md` «Tester og kodekontroll» | No check catches a missing or unapplied migration | low | defer | The README lists exactly the architecture's pre-PR checks (DR-7); `manage.py test` builds its database from migrations and catches most cases; adding `makemigrations --check` changes an approved convention, so the gap predates this story. |
| BH-7 | `prognose/tests.py` `PureCoreTests` | The test enforces only the Django half of AD-1 | low | reject | The pure core holds only docstrings, so nothing can break AD-1 yet; adding network modules first needs a decision on AD-10's `explanation/rephrase.py`, which is more than a direct correction. Same root cause as EC-22. |
| BH-8 | `load_seed.py` | An empty `.secret_key` is never repaired | low | reject | Same as VG-O1. |
| BH-9 | `templates/` | No Norwegian 400, 403 or CSRF page, and the gap is untracked | low | reject | In this story only a non-allowed host reaches the 400 (no forms, no `PermissionDenied`); the spec and AD-13 name 404 and 500; new templates are more than a direct correction. Recorded as an open item for Story 1.3, whose login form makes the CSRF page reachable. Same root cause as EC-17. |
| BH-10 | `prognose/tests.py` `SETTINGS_PROBE` | The probe never controls `.env` | medium | patch | Same root cause as VG-1. |
| BH-11 | `prognose/env.py` `published_settings` | `check --deploy` warnings W004 and W008 are unhandled | low | reject | Vercel redirects HTTP to HTTPS at the edge, so `SECURE_SSL_REDIRECT` changes nothing there, and HSTS is defense in depth; no everyday harm is shown; the fix adds settings and a test. |
| BH-12 | `sprint-status.yaml` | The story is `in-progress` while in review | false | reject | Step 3 sets `in-progress` by design, and the workflow's present step syncs the story to `review`. |
| BH-13 | `templates/base.html` | No icon link, so every visit requests `/favicon.ico` | low | patch | Each request renders the 404 page, logs a `django.request` warning and costs a function call on Vercel; `<link rel="icon" href="data:,">` is a one-line fix. |
| EC-1 | `prognose/env.py` `database_config` | Unencoded `/`, `?` or `#` in the password gives a raw `ValueError` that repeats part of it | low | reject | Real for a hand-written URL (`urlsplit` reads the fragment as the port), but the Neon integration sets an encoded URL; the fix adds a guard. |
| EC-2 | `prognose/env.py` `database_config` | A URL without host or database name passes startup | low | reject | Unreachable through the Neon integration; a wrong URL fails loudly at the first query with the Norwegian 500 and a logged error; the fix adds a guard. |
| EC-3 | `prognose/env.py` `database_config` | No `connect_timeout` | low | reject | A hang needs an unreachable endpoint, a suspended Neon compute wakes during the connection attempt, and the function timeout ends the request; a new option is more than a direct correction. |
| EC-4 | `prognose/env.py` `published_settings` | No host variables give an empty `ALLOWED_HOSTS` | low | reject | Same as BH-4. |
| EC-5 | `prognose/env.py` `published_settings` | The branch alias and other domains get a 400 | low | patch | Same root cause as BH-5. |
| EC-6 | `prognose/env.py` `published_settings` | A whitespace-only `SECRET_KEY` passes | low | reject | The owner makes the key with the README's `secrets.token_urlsafe(50)` command; a blank value needs a deliberate mistake; the fix extends a guard. |
| EC-7 | `prognose/env.py` `load_secret_key` | An unreadable `.secret_key` crashes every command | false | reject | Nothing in the flow makes the file unreadable (`load_seed` writes it as the user, mode 0600); a loud, named `PermissionError` is correct behavior. |
| EC-8 | `prognose/env.py` `read_dotenv` | A UTF-16 `.env` gives `UnicodeDecodeError` | low | reject | The README makes `.env` with `Copy-Item` from the UTF-8 `.env.example`; the failure is loud and names `.env`, which is optional; the fix adds a guard. |
| EC-9 | `prognose/env.py` `read_dotenv` | Inline comments and `export` are not parsed | low | reject | `.env.example` uses whole-line comments and plain `KEY=VALUE`; the failure keeps DEBUG off, the safe default; the fix adds parsing branches. |
| EC-10 | `prognose/settings.py` `ON_VERCEL` | `VERCEL=0` selects published mode | false | reject | Only Vercel sets `VERCEL` (to 1), and AD-13 detects the published version by it; a hand-set value fails loudly with the named missing variable. |
| EC-11 | `prognose/settings.py` `ON_VERCEL` | System variables not exposed give local mode on Vercel | low | reject | Same as BH-4. |
| EC-12 | `load_seed.py` | An empty `.secret_key` | low | reject | Same as VG-O1. |
| EC-13 | `load_seed.py` | A race or dangling symlink gives `FileExistsError` | false | reject | No flow runs `load_seed` in parallel or leaves a dangling `.secret_key` link; `O_EXCL` then fails loudly, which is correct. |
| EC-14 | `accounts/models.py` `create_user` | A padded customer number is stored unstripped | low | reject | No caller exists yet, and Story 1.2's seed is generated digit strings; the fix adds normalization. |
| EC-15 | `accounts/models.py` `create_user` | A missing name saves an empty name | low | reject | No caller exists yet, and Story 1.2's seed always has names; the fix adds a guard. |
| EC-16 | `accounts/models.py` `CompanyManager` | `createsuperuser` raises `AttributeError` | low | reject | The spec rules out Django admin and the README never runs `createsuperuser`; the failure is loud; the fix adds a manager method. |
| EC-17 | `templates/` | 400, 403 and CSRF pages fall back to English | low | reject | Same as BH-9. |
| EC-18 | `.gitignore` | `db.sqlite3-journal` is not ignored | low | patch | Only `db.sqlite3` is listed (line 70); a hard-killed write leaves the journal beside it, and `git add .` would stage it; `db.sqlite3*` is a direct fix. |
| EC-19 | `README.md` step 5 (Windows) | Ctrl+C during `migrate` skips `Remove-Item`, so later commands in that window use Neon | medium | patch | PowerShell stops the rest of the line on Ctrl+C; a later `runserver`, `test` or `load_seed` there would use the production database; `try`/`finally` runs on Ctrl+C and is a direct fix. |
| EC-20 | `README.md` step 5 | The URL is saved in shell history | medium | patch | Same root cause as BH-1. |
| EC-21 | `README.md` step 1 | The CLI does not read `.gitignore` | low | patch | Same root cause as BH-2. |
| EC-22 | `prognose/tests.py` `PureCoreTests` | ORM and network imports are not caught | low | reject | Same as BH-7. |
