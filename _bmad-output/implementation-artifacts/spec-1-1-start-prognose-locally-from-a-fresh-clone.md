---
title: 'Story 1.1 part A: Start Prognose locally from a fresh clone'
type: 'feature'
created: '2026-11-20'
status: 'done'
baseline_commit: 'ae7b72c1aa5f2b39eab961c2b19f7922b7c52523'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-17/ARCHITECTURE-SPINE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The repository holds only plans, so nobody can start Prognose. The examiner must start it from a fresh clone with one database command and the documented `uv run` commands, with no paid service, key or file editing (NFR-1, NFR-3).

**Approach:** Build the Structural Seed by hand: Django in `src/` with `web.Company` in the first migration, PostgreSQL from `compose.yaml`, settings from environment variables with local defaults, a `load_seed` that only creates `.secret_key`, a page at `/`, pytest and Ruff, and the README setup. Part B of Story 1.1 (status table, AI steering log, planning-phase QA records) follows on this branch (`deferred-work.md`).

## Boundaries & Constraints

**Always:**
- Story 1.1's exact pins in `pyproject.toml` (tools in the `dev` group), `.python-version` 3.13, `uv.lock` the only lock file.
- `compose.yaml` exactly as AD-14.
- Settings (AD-13) read the process environment over an optional repo-root `.env`, without changing `os.environ`; blank values count as unset. DEBUG is on only when `.env` sets `PROGNOSE_DEBUG` (1/true/yes/on) and `PROGNOSE_LAN_HOST` is unset (AD-12).
- `BASE_DIR` is the repository root. `SECRET_KEY_FILE` is a setting; a missing or blank file gives a random key per process, so `migrate` and CI run before `load_seed`.
- Configuration errors raise `ImproperlyConfigured` in Norwegian and never echo the URL or a secret.
- Code in English; page text, command output, README, `.env.example` and QA log in Norwegian. Each test's docstring names the IDs it verifies (DR-5).

**Never:** new packages, raw SQL, the admin or superusers; work of Stories 1.2–1.8 (CI, AD-1 import test, base template, stylesheet, error pages, logging, login, seed loading); rewriting an existing `.secret_key`; secrets, e-mail addresses or local paths in tracked files; the archive's Vercel, Neon, SQLite, `/helse/` or pip/venv parts.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Defaults | no variables, no `.env` | hosts `127.0.0.1`, `localhost`; DEBUG off; database `prognose` at `127.0.0.1:15432`, user `prognose`, no password | N/A |
| Phone test | `PROGNOSE_LAN_HOST=192.168.1.20` | address added; DEBUG off even with `PROGNOSE_DEBUG=1` | N/A |
| Unsafe host | `*`, `0.0.0.0`, a public IP or a host name | refused | `ImproperlyConfigured` |
| `.env` | UTF-8 (BOM allowed), comments, quoted values; a key also in the environment | file values used; the environment wins | not UTF-8 → `ImproperlyConfigured` |
| Custom URL | `postgres://u:p%40ss@h:5433/x` | NAME `x`, USER `u`, PASSWORD `p@ss`, HOST `h`, PORT `5433` | other scheme, bad port, no host or name → `ImproperlyConfigured` |
| No secret | no `.secret_key` | `load_seed` creates it exclusively, mode 600 on POSIX, from `secrets.token_urlsafe(50)` | N/A |
| Secret exists | non-blank file | unchanged byte for byte; says so | N/A |
| Blank secret | empty file | unchanged | `CommandError`: delete it and run again |

</frozen-after-approval>

## Code Map

- `.gitignore` -- drop lines 1–14 (Next.js), `db.sqlite3*` and `staticfiles/`; the rest hides local BMAD, Claude and Impeccable files. Database data lives in the Docker volume, outside the repository.
- `README.md` -- keep the intro and the member list.
- `docs/qa-logg.md` -- follow the style of the 2026-11-17 entry.
- `_bmad/scripts/`, `.claude/skills/` -- tracked Python that Ruff must skip; Ruff 0.17.5 `format` also reads Python blocks in Markdown unless `include = ["*.py"]`.
- Tag `archive/story-1-1-project-skeleton` (read with `git show`) -- adapt `planning/management/commands/load_seed.py` 17–26, `prognose/env.py` 31–55, 67–78 and 115–125, `accounts/models.py`, `manage.py` (a uv hint instead of venv/pip), and the tests in `prognose/tests.py` 39–116 and 155–168, `accounts/tests.py` 12–51 and `planning/tests.py` 90–123.

## Tasks & Acceptance

**Execution:**
- [x] `pyproject.toml`, `uv.lock`, `.python-version` -- pins, `package = false`; pytest `DJANGO_SETTINGS_MODULE`, `pythonpath = ["src"]`, `testpaths = ["tests"]`, `django_find_project = false`; Ruff `include = ["*.py"]`, `extend-exclude = ["_bmad", ".claude", "**/migrations"]`, lint adds B, DJ, I, UP
- [x] `compose.yaml` -- the service `db`
- [x] `src/manage.py`, `src/prognose/{__init__,env,settings,urls,wsgi}.py` -- pure helpers in `env.py` for the matrix; `staticfiles` installed so `--insecure` works
- [x] `src/forecasting/__init__.py`, `src/explanation/__init__.py`, `data/.gitkeep`, `reference/.gitkeep` -- the Structural Seed
- [x] `src/web/{__init__,apps,models,views}.py`, `src/web/migrations/0001_initial.py`, `src/web/templates/web/start.html` -- `Company(AbstractBaseUser)` with a unique `customer_number` as login field, `name` and a manager with `create_user`; GET `/` with `lang="nb"`, the viewport tag, a `data:,` icon and the wordmark «Prognose»
- [x] `src/web/management/commands/load_seed.py` -- the secret rows of the matrix; loads no data
- [x] `tests/test_settings.py`, `tests/test_company.py`, `tests/test_load_seed.py`, `tests/test_start_page.py` -- the matrix; settings reloaded with `.env` stubbed, `PROGNOSE_*` and `DATABASE_URL` removed, and a non-default URL; `makemigrations --check --dry-run`; PBKDF2 hashes; the page
- [x] `.env.example` -- the three variables commented out, each marked optional, `DATABASE_URL` as secret if it holds a password
- [x] `README.md` -- «Kom i gang»: prerequisites, the five commands (the same in Terminal and PowerShell), Windows on ARM not supported; «Nøkler og hemmeligheter»; «Tester»
- [x] `docs/qa-logg.md` -- the first setup on macOS: date, macOS, Docker Desktop version, the client, each command's result and the total time

**Acceptance Criteria:**
- Given a copy of only the files to be committed, on macOS with uv and Docker Desktop, when the five README commands run, then `http://127.0.0.1:8000/` answers 200 with `lang="nb"` and «Prognose», the server listens only on 127.0.0.1, and no step activates a virtual environment, needs `.env` or a key, or asks for an edit.
- Given `compose.yaml`, when `docker compose up -d --wait` runs, then the database is healthy, listens only on `127.0.0.1:15432` and has no password.
- Given an empty database, when `migrate` runs, then `web.0001_initial` creates `Company`, and `makemigrations --check` finds nothing.
- Given the repository, when `uv run pytest`, `uv run ruff check` and `uv run ruff format --check` run, then they pass, and Ruff reads only the Python in `src/` and `tests/`.
- Given `.gitignore`, `.env.example` and the README, when they are read, then they meet Story 1.1's criteria; DR-1's other README parts (stop commands, fixes, «not published») are Story 4.1.

## Implementation Notes

- Decisions within the spec: the environment can turn DEBUG off but never on; a `#` after whitespace ends an unquoted `.env` value, lines without `=` are skipped and `export` is not supported; `PROGNOSE_LAN_HOST` accepts only RFC 1918 IPv4 addresses; a `DATABASE_URL` without a port uses 5432, port 0 is refused and query parameters are ignored; a `.secret_key` that is not UTF-8 raises `ImproperlyConfigured`.
- The health check runs `pg_isready` over TCP, because the image's first-start server listens only on its socket and would report healthy too early.
- `/` shows «Prognose» as its `h1` with the approved line from the Innlogging wireframe; the navy header with the wordmark is Story 1.4, and the login page at `/` is Story 1.8. A POST to `/` gets Django's blank 405 until Story 1.4 adds the error pages.
- `REQUIRED_FIELDS` is a tuple, because Ruff flagged the list (RUF012) during implementation, before any commit.
- Verification: 69 tests passed with none skipped, Ruff passed on the 19 Python files in `src/` and `tests/`, and the clean-copy run passed twice (7.8 s and 7.2 s in total, image and packages cached), with the app on `127.0.0.1:8000` only, the database on `127.0.0.1:15432` only and no password on the `prognose` role.
- Review pass 1 changed three of the decisions above: `export ` is now stripped from `.env` keys, an unquoted value that is only a comment counts as empty, and an unreadable `.env` or `.secret_key` raises `ImproperlyConfigured`. It also narrowed `requires-python` to `==3.13.*`, added `required-version = ">=0.12.13"`, and made `manage.py` and pytest always use `prognose.settings`.
- Verification after the patches: 75 tests passed with none skipped, Ruff passed on the 20 Python files in `src/` and `tests/`, `uv.lock` matched, `load_seed` twice left `.secret_key` unchanged, and a third clean-copy run on the patched files passed (7.2 s in total), with the same checks.

## Spec Change Log

## Review Triage Log

Review pass 1 (2026-11-20): Blind Hunter (BH), Edge Case Hunter (EC) and Verification Gap (VG). Patches P1–P16 went back to the implementation agent.

| ID | Finding | Verdict | Evidence | Route |
|---|---|---|---|---|
| BH-1 | No test guards the `.gitignore` lines for `.secret_key` and `.env` | low | `git check-ignore` confirms both rules today; a regression needs someone to delete a line, and the fix adds a git-dependent test | rejected: unlikely, more than a direct correction; the privacy scan before each commit and in Story 4.4 covers it |
| BH-2 | README states Windows x64 and Intel Mac support that nobody has tested | low | The platforms come from AD-13, but the QA log shows only macOS on Apple M1 | patch P4 |
| BH-3 | README does not say which commands to repeat | false | A second `load_seed` prints «finnes allerede og er ikke endret» and exits 0 (`test_leaves_an_existing_secret_unchanged`), so rerunning all five works; the stop on existing data arrives with Story 1.7, and start/stop is DR-1 work in Story 4.1 | rejected |
| BH-4 | README «Tester» does not say which database the tests use | low | pytest-django creates and drops `test_prognose` on the same server, which needs the right to create databases; the README is silent | patch P5 |
| BH-5 | README and the pyproject comment say Ruff checks only `src/` and `tests/` | low | The config is `include = ["*.py"]` minus `_bmad`, `.claude` and migrations, so Story 1.6's `data/generate_seed.py` will be checked too | patch P6 |
| BH-6 | QA log entry is incomplete | low | One of two clean-copy runs is recorded, the steps add up to 7.5 s against 7.8 s, and nothing says to repeat the setup from a real clone | patch P7 |
| BH-7 | DATABASE_URL format is undocumented | low | Reproduced: `postgresql://u:pa#ss@h:5433/x` gives «ugyldig vert eller port»; nothing mentions percent-encoding or that `?` parameters are unused | patch P8 (with EC-6) |
| BH-8 | The phone-test command binds `0.0.0.0` | low | `ALLOWED_HOSTS` checks only the Host header, but the command is AD-13's own, so binding to the LAN address needs an architecture amendment | defer (with EC-13) |
| BH-9 | Tool versions are not enforced | low | `requires-python = ">=3.13"` lets `uv.lock` carry wheels for later Pythons against the Stack's 3.13, and nothing backs the README's uv minimum | patch P9 |
| BH-10 | A comment after a blank `.env` value becomes the value | medium | Reproduced: `PROGNOSE_LAN_HOST=   # fylles ut` gives `'# fylles ut'`, and the settings refuse to load | patch P1 (with EC-1) |
| BH-11 | `export` lines and typos in `.env` are silently ignored | low | Reproduced: `export PROGNOSE_DEBUG=1` is stored as `export PROGNOSE_DEBUG`; stripping the prefix is one line, while warnings for unknown keys would add branches and are not taken | patch P2 (with EC-2) |
| BH-12 | Other file errors give raw English tracebacks | medium | Reproduced: a `.env` or `.secret_key` that is a directory raises `IsADirectoryError`, against the rule that configuration errors raise `ImproperlyConfigured` in Norwegian; a venv made as `.env` hits it | patch P3 (with EC-4) |
| BH-13 | A missing `.secret_key` falls back to a random key without a warning | low | Real but harmless until Story 1.8 adds login; the README order runs `load_seed` before `runserver`, and a system-check warning adds a branch | rejected; noted for Story 1.8 |
| BH-14 | `create_user` accepts a missing name | low | `create_user("100002", "pw")` saves an empty name, but only Story 1.7's `load_seed` will call it, with names from the seed; the fix adds a guard | rejected (with EC-10) |
| BH-15 | The BOM test cannot detect a regression | low | Confirmed: the BOM sits on a comment line that is skipped either way (`"﻿".isspace()` is False), and it is an invisible literal | patch P10 |
| BH-16 | The 405 test cites decisions that contradict it | low | AD-11 makes `/` the login page with POST, and AD-12 wants a Norwegian 405 page | patch P11 |
| BH-17 | The external-resource check is narrow | low | The regex sees only double-quoted lowercase `src` and `href`; a full HTML scan adds code, so the name and docstring are narrowed instead | patch P12 |
| EC-1 | Blank value followed by an inline comment | medium | Same defect as BH-10 | patch P1 |
| EC-2 | `export` prefix in `.env` | low | Same defect as BH-11 | patch P2 |
| EC-3 | An unclosed quote stays in the value | low | Reproduced (`'1` keeps its quote, so DEBUG stays off), but it needs a typo, and the fix adds a branch | rejected |
| EC-4 | Unreadable `.env` or `.secret_key` raises a raw `OSError` | medium | Same defect as BH-12 | patch P3 |
| EC-5 | A DATABASE_URL without a user is accepted | false | libpq then uses the login name, which is valid PostgreSQL behaviour for peer or trust setups, and PostgreSQL's own error names the missing role | rejected |
| EC-6 | Query parameters such as `sslmode` are dropped | low | Reproduced; v1 runs only against the local Compose database (AD-13), so refusing them in code adds a branch outside the run mode; documenting it joins P8 | patch P8 (with BH-7) |
| EC-7 | A reader can see `.secret_key` between its creation and the write | low | Needs two `load_seed` runs at the same instant; the temp-file-and-link fix adds complexity | rejected |
| EC-8 | `createsuperuser` crashes with `AttributeError` | low | Real, but the frozen Boundaries exclude superusers, and no README step uses the command | rejected: out of scope by intent |
| EC-9 | A padded or blank customer number is accepted | low | Only seed data creates companies, and the login form comes in Story 1.8; stripping adds a guard | rejected |
| EC-10 | `create_user` accepts a blank name | low | Same as BH-14 | rejected |
| EC-11 | An exported `DJANGO_SETTINGS_MODULE` wins | low | Reproduced: `DJANGO_SETTINGS_MODULE=annet.settings uv run pytest` fails with `ImportError`, and `manage.py`'s `setdefault` keeps the foreign value; forcing AD-13's one settings module is one line each | patch P13 |
| EC-12 | Port 15432 may already be in use | low | The failure is loud, and Docker's message names the port; a configurable port contradicts AD-14, and the README's fix for a port in use is DR-1 work in Story 4.1 | rejected |
| EC-13 | The phone test binds `0.0.0.0` | low | Same as BH-8 | defer |
| EC-14 | `build/` and `dist/` are no longer ignored | false | `package = false` and there is no `[build-system]`, so no README command writes them | rejected |
| EC-15 | `env.py` is called pure but uses Django and files | false | `env.py` is in the project package, which AD-1 allows to use Django and files, and no core package imports it; the fix would only edit this spec's wording | rejected |
| VG-1 | The refused-URL test cannot see a password leaked through the chained `ValueError` | medium | Pre-verified by mutation: without `from None` all 8 cases still pass, while `postgresql://u:hemmelig/x` would print the password | patch P14 |
| VG-2 | Decoding of the user and the database name is unpinned | low | Pre-verified by mutation: removing `unquote` on USER and NAME passes every test, although a test docstring claims it | patch P15 |
| VG-3 | `runserver --insecure` is never exercised | medium | Pre-verified by mutation: dropping `staticfiles` or breaking `WSGI_APPLICATION` keeps pytest green while README step 5 fails | patch P16 |

## Design Notes

The first setup runs from a scratchpad copy of the files to be committed, with its own Compose project and volume, removed afterwards. The QA entry says that Claude Code ran it and that `postgres:18.7` was cached; the timed SM-2 runs by a person are Stories 4.1 and 4.4.

Leave every change uncommitted and do not run the `sesjonslogg` skill: the user approves each commit and push, and the parent session writes the session log afterwards.

## Verification

**Commands:** (if `docker` is not on PATH, Docker Desktop's CLI is in `$HOME/.docker/bin`)
- `docker compose up -d --wait` -- the database is healthy
- `uv sync --locked` -- `uv.lock` unchanged
- `uv run python src/manage.py migrate`, then `load_seed` twice -- the second run leaves `.secret_key` unchanged
- `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` -- pass
- the clean-copy run, checked with `curl` and `lsof`

**Manual checks:**
- Before the pull request, the user checks `/` in Safari's responsive design mode at 320 px, 390 × 844 and 820 × 1180.
