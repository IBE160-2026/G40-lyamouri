---
title: 'technical research: Technology stack selection'
type: 'technical'
topic: 'Technology stack selection'
decision: 'Select a simple, well-documented web stack with a local database for a weekly demand-forecast app that a reviewer can run locally without paid services'
source: 'native run'
status: complete
preset: 'standard'
validation: 'normal'
shape: 'select'
claims_verified: 2
claims_unverified: 5
created: '2026-11-01'
updated: '2026-11-01'
---

# technical research: Technology stack selection

**Decision this research serves:** Select a simple, well-documented web stack with a local database for a weekly demand-forecast app that a reviewer can run locally without paid services.

## Executive summary

**Pick: Django with SQLite, with the forecasting logic in a plain-Python package that does not import Django.** Runner-up: Flask with SQLite. The gap is narrow (83 against 80 out of 100) and inside our scoring uncertainty, so the choice is close; Django wins on built-in login, password hashing, sessions, test tooling and seeding, and Flask wins on fewest concepts and simplest setup. Next.js scored clearly lowest (50) because it needs the most separate pieces for this app.

**Three findings that drive this.**
1. Django covers login, password hashing, sessions, a test client with rollback per test, in-memory test database and seeding commands with no extra package [16][19][20][21]. Flask's tutorial covers login with hashing and sessions with one extra install (pytest), but the login decorator and every owner-filtering query are written by hand [4][5].
2. Next.js 16 needs several separate pieces for this app (an auth library or hand-rolled sessions, an ORM or driver, a test runner, a chart library), asks for Node 20.9 or newer, has a native SQLite driver option, and is on a formal security-release cadence with a release announced for 2026-11-03 [24][27][31][33].
3. Flask-Login is not a safe default for Flask: its last release is 0.6.3 from 2023-10-30, and its changelog mentions Flask 3 but not 3.1 [7][8]. FastAPI is still version 0.x and classified Beta on PyPI [9].

**Biggest caveat.** No source measured how well AI coding assistants handle any of these frameworks, so that 20% criterion does not discriminate (all candidates scored 3). Per-company data isolation is a hard gate, and neither framework's documentation shows an end-to-end pattern for it; both need an owner filter on every query [36][37]. Most evidence is official documentation of a single publisher per candidate.

## Requirements frame (agreed 2026-11-01)

**Hard gates:** runs locally with no paid service or key; local embedded database; password hashing with sessions and per-company data isolation; forecasting logic in a module that can be tested alone; line charts; mainstream and well documented.
**Weighted criteria (sum 100):** setup simplicity (25), testability (20), fit for AI coding assistants (20), login plus database (15), charting (10), learning curve (10).

## Candidate screen

| Candidate | Gate result |
|---|---|
| Flask + SQLite (Jinja, Chart.js) | Passes all gates. |
| FastAPI + SQLite | Passes, but 0.x Beta [9], token login rather than cookie sessions [10], and more pieces (SQLModel, pwdlib, PyJWT, httpx) [9][10][11]. Kept as a variant of the Python candidate. |
| Django + SQLite (templates, Chart.js) | Passes all gates. |
| Next.js + SQLite | Passes, with the most moving parts and the most upgrade churn [25][33]. |

Nothing was cut at the gates. The Python and Django candidates share the strongest evidence.

## Evidence per criterion

**Setup and versions.**
- Flask 3.1.3 (2026-02-19), Python 3.9 or newer, a slow release cadence [1][2]. Official path: create a virtual environment and `pip install Flask`; Werkzeug, Jinja, ItsDangerous (signs the session cookie) and Click come with it [2].
- Django 6.1.2 is the latest stable; 5.2 LTS is supported to April 2028 and 6.2 LTS is due April 2027 [13]. Django 6.1 supports Python 3.12 to 3.15 [14] and requires SQLite 3.37 or newer [17]. SQLite is the default database and ships with Python; `runserver` is enough [14]. SQLite's own guidance puts a single-user local demo well inside its limits [12]. The official tutorial does not mention a virtual environment and defers `migrate` to part 2, so a README sequence (venv, install, migrate, runserver) is our inference [15].
- Next.js: current minor 16.4 (2026-10-06); a scheduled security release is announced for 2026-11-03, so patch versions change within days [33]. Needs Node 20.9 or newer; `npx create-next-app@latest my-app --yes` then `npm run dev` [24]. Version 16 removed synchronous access to cookies and params and renamed middleware to proxy [25].

**Login and database.**
- Flask's tutorial hashes with Werkzeug `generate_password_hash` (scrypt by default [6]), stores `user_id` in a signed session cookie, defines its own `login_required` decorator in about 6 lines, and uses plain `sqlite3` with `?` placeholders; every query is written by hand [3][4].
- Django: `create_user` hashes passwords (PBKDF2-SHA256 by default, Argon2 optional; the page states no iteration count); `LoginView`, `@login_required` and sessions are built in; `authenticate()` and `login()` store the user in the session [16][19].
- FastAPI docs now recommend `pwdlib` (Argon2) and a token (JWT) login, not a cookie session; older passlib tutorials are outdated [10].
- Next.js: the official guide recommends an auth library for security and simplicity; its own example uses bcrypt, jose and Zod, a data access layer that reads the session on every query, and stresses that Server Actions need their own checks [27]. Auth.js is now maintained by the Better Auth team, which is recommended for new projects [28][29]. Better Auth hashes with scrypt by default [30]. `better-sqlite3` is a native module installed with a prebuilt binary on major platforms, with build requirements not stated [31]. Node's built-in `node:sqlite` is still Stability 1.2 (release candidate) [32].
- Flask-Login: last release 2023-10-30, Beta; the repository's last commit is 2025-08-27 and an unreleased 0.7.0 is on main [7][8].

**Data isolation (a hard gate).**
- OWASP ranks Broken Access Control first in its 2025 Top 10, prescribes deny by default and server-side enforcement, and says access control should enforce record ownership [35]. Its cheat sheets require an access check on every request for the specific object, and say that random identifiers do not replace the check [36][37]. OWASP also recommends unit and integration tests for authorization logic [35][36]; the pages do not show a ready "company A requests company B's record" test (partial confirmation).
- Flask's tutorial shows the pattern: `get_post` returns 404 if the record is missing and 403 if the author differs from the logged-in user, but the index view lists all users' posts, so ownership is checked per record, not enforced as a general partition [38].
- Django's documentation shows queryset filtering by a captured value and mentions `request.user` only in a sentence; there is no official pattern for tying records to a company (partly disputed). Both frameworks therefore need a project-defined rule: every query filters by the logged-in company.

**Testing.**
- Flask: pytest, `app.test_client()`, `session_transaction()` to log in without the login route, a CLI test runner for seed commands; docs advise extracting complex behaviour into separate functions; no built-in per-test database rollback [5].
- Django: `manage.py test`, in-memory test database, `TestCase` rolls back each test, `SimpleTestCase` blocks database access for pure logic, test `Client` with `login()` and `force_login()` [18][20]. The testing page does not mention pytest or pytest-django.
- Next.js: Vitest with a manual setup; async Server Components are not supported and need end-to-end tests; a pure TypeScript module needs none of the React setup (inference) [26].

**Charting.** Chart.js loads with one CDN script tag and no build step; the getting-started example is a bar chart and a line chart is the same code with a different type [22]. Django's `json_script` filter passes Python data to JavaScript safely [23]. Recharts' latest stable is 3.10.1; React 19 and Next.js compatibility are not confirmed by an official source [34].

**Learning curve.** Flask has the fewest concepts. Django adds project and app structure, settings, an ORM and migrations. Next.js adds TypeScript, React, the App Router and server actions. No source measured learning time; these are our judgements.

**Fit for AI coding assistants.** No benchmark or statement measuring assistants on Flask, FastAPI or Django was found; Vercel's own docs describe an `AGENTS.md` file and version-matched docs shipped with Next.js (vendor statement) [24]. All candidates therefore score 3.

## Cost and lock-in

All four candidates run locally and cost nothing to run. Licence terms were not checked. Exit cost is low if the forecasting package has no framework imports: only the web layer, templates and seed commands would move. Next.js carries the highest ongoing maintenance cost because of frequent security releases and breaking changes between majors [25][33].

## Verdict (weighted matrix)

Scores are 1 (poor) to 5 (strong), our judgement from the evidence above; weighted total = sum(score x weight) / 5, out of 100. Re-weight freely.

| Criterion (weight) | Flask | FastAPI | Django | Next.js |
|---|---|---|---|---|
| Setup simplicity (25) | 5 | 3 | 4 | 2 |
| Testability (20) | 4 | 4 | 5 | 3 |
| Fit for AI assistants (20) | 3 | 3 | 3 | 3 |
| Login plus database (15) | 3 | 2 | 5 | 2 |
| Charting (10) | 5 | 5 | 5 | 3 |
| Learning curve (10) | 4 | 3 | 3 | 2 |
| **Weighted total** | **80** | **65** | **83** | **50** |

**The pick:** Django (83). **Runner-up:** Flask (80). Flask wins instead if setup simplicity is weighted around 35 and login plus database around 10, which gives Flask 83 against Django 81.

**Strongest argument against the pick.** Django's project structure, settings and migrations are more concepts than a small app needs, and the official tutorial does not show the virtual-environment and migrate steps, so the README must be written and tested by the group. Flask's tutorial gives a shorter path to a working login.

**Cheapest reversibility hedge.** Put the forecasting calculations in a package with plain-Python unit tests and no web imports, and keep seed data and its generator script outside the web app. If Django proves heavy, the web layer can be rewritten in Flask without touching the calculations.

## Recommendations

1. **Choose Django + SQLite for the web layer and keep the forecasting logic framework-free.** Feeds: architecture decision and PRD technical constraints. Basis: medium-low; narrow margin, single-publisher official docs.
2. **Define the isolation rule in the architecture: every query filters by the logged-in company, enforced in one data-access layer, with a two-account test that proves company A cannot read company B.** Feeds: architecture and test plan. Basis: medium; OWASP and Flask's ownership check [35][36][4], no framework pattern for companies.
3. **Write and test the README setup sequence yourselves** (virtual environment, install, migrate, seed, runserver), because the official Django tutorial does not give it [15]. Feeds: README. Basis: medium.
4. **Use Chart.js from a pinned CDN link or a vendored file for the charts** and pass data with `json_script`. Feeds: UX and architecture. Basis: medium [22][23]. Consider vendoring the file so the app works offline.
5. **Avoid Flask-Login and FastAPI as defaults.** If Flask is chosen later, use Flask's own session plus Werkzeug hashing [4][6]. Feeds: architecture. Basis: medium-high for Flask-Login [7][8].
6. **Record "AI-assistant fit not evidenced" as a known limitation** in the process documentation, and say that no framework got an advantage on it. Feeds: process documentation. Basis: high that no source exists.

## Open questions

- What is the PBKDF2 iteration count in Django 6.1, and is it adequate? The password page does not state it [16].
- Is there an official or well-regarded Django pattern for tying records to a company?
- Does Recharts 3.x support React 19 and Next.js 16? Only relevant if Next.js is reconsidered.
- What do developers report after 6 to 12 months with Django on a small app? No retrospective source was found.
- Which build prerequisites does `better-sqlite3` need on Windows and macOS? Not stated in the pages read.

## Source appendix

All sources accessed 2026-11-01. Pages were read through a fetch tool that summarises pages.

| [n] | Claim or finding it supports | Publisher | Pub date | Accessed | Confidence |
|---|---|---|---|---|---|
| [1] | Flask 3.1.3, release cadence | [PyPI, Flask](https://pypi.org/project/Flask/) | 2026-02-19 | 2026-11-01 | high |
| [2] | Flask installation path | [Pallets, Flask docs](https://flask.palletsprojects.com/en/stable/installation/) | undated | 2026-11-01 | high |
| [3] | Flask tutorial: sqlite3 and init-db command | [Pallets, Flask tutorial (database)](https://flask.palletsprojects.com/en/stable/tutorial/database/) | undated | 2026-11-01 | high |
| [4] | Flask tutorial: login, sessions, ownership check (views and blog) | [Pallets, Flask tutorial (views)](https://flask.palletsprojects.com/en/stable/tutorial/views/) | undated | 2026-11-01 | high |
| [5] | Flask testing | [Pallets, Flask docs (testing)](https://flask.palletsprojects.com/en/stable/testing/) | undated | 2026-11-01 | high |
| [6] | Werkzeug password hashing, scrypt default | [Pallets, Werkzeug docs](https://werkzeug.palletsprojects.com/en/stable/utils/) | undated | 2026-11-01 | high |
| [7] | Flask-Login release history | [PyPI, Flask-Login](https://pypi.org/project/Flask-Login/) | 2023-10-30 | 2026-11-01 | high |
| [8] | Flask-Login repository activity and changelog | [Flask-Login on GitHub](https://github.com/maxcountryman/flask-login) | 2025-08-27 (last commit) | 2026-11-01 | medium |
| [9] | FastAPI 0.162.0, Beta, dependencies | [PyPI, FastAPI](https://pypi.org/project/fastapi/) | 2026-10-23 | 2026-11-01 | high |
| [10] | FastAPI JWT login and pwdlib | [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) | undated | 2026-11-01 | high |
| [11] | FastAPI with SQLModel and SQLite | [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/) | undated | 2026-11-01 | high |
| [12] | SQLite limits do not constrain a local demo | [SQLite.org](https://www.sqlite.org/whentouse.html) | undated | 2026-11-01 | high |
| [13] | Django versions, LTS dates | [Django Software Foundation](https://www.djangoproject.com/download/) | undated | 2026-11-01 | high |
| [14] | Django Python support, SQLite default | [Django documentation (install FAQ)](https://docs.djangoproject.com/en/stable/faq/install/) | undated | 2026-11-01 | high |
| [15] | Django tutorial setup steps | [Django documentation (tutorial part 1)](https://docs.djangoproject.com/en/stable/intro/tutorial01/) | undated | 2026-11-01 | high |
| [16] | Django password hashing | [Django documentation (passwords)](https://docs.djangoproject.com/en/stable/topics/auth/passwords/) | undated | 2026-11-01 | high |
| [17] | Django SQLite requirements and limits | [Django documentation (databases)](https://docs.djangoproject.com/en/stable/ref/databases/) | undated | 2026-11-01 | high |
| [18] | Django test runner, in-memory database | [Django documentation (testing overview)](https://docs.djangoproject.com/en/stable/topics/testing/overview/) | undated | 2026-11-01 | high |
| [19] | Django login, sessions, decorators | [Django documentation (auth)](https://docs.djangoproject.com/en/stable/topics/auth/default/) | undated | 2026-11-01 | high |
| [20] | Django test client and TestCase | [Django documentation (testing tools)](https://docs.djangoproject.com/en/stable/topics/testing/tools/) | undated | 2026-11-01 | high |
| [21] | Django management commands for seeding | [Django documentation (custom commands)](https://docs.djangoproject.com/en/stable/howto/custom-management-commands/) | undated | 2026-11-01 | high |
| [22] | Chart.js CDN, no build step | [Chart.js documentation](https://www.chartjs.org/docs/latest/getting-started/) | undated | 2026-11-01 | high |
| [23] | `json_script` filter | [Django documentation (template builtins)](https://docs.djangoproject.com/en/stable/ref/templates/builtins/) | undated | 2026-11-01 | high |
| [24] | Next.js install path, Node version, AGENTS.md | [Next.js documentation](https://nextjs.org/docs/app/getting-started/installation) | 2026-10-02 | 2026-11-01 | high |
| [25] | Next.js 16 breaking changes | [Next.js upgrade guide](https://nextjs.org/docs/app/guides/upgrading/version-16) | undated | 2026-11-01 | high |
| [26] | Next.js and Vitest limits | [Next.js documentation (Vitest)](https://nextjs.org/docs/app/guides/testing/vitest) | 2026-08-25 | 2026-11-01 | high |
| [27] | Next.js authentication guide, data access layer | [Next.js documentation](https://nextjs.org/docs/app/guides/authentication) | 2026-09-16 | 2026-11-01 | high |
| [28] | Auth.js credentials limitations, move to Better Auth | [Auth.js documentation](https://authjs.dev/getting-started/authentication/credentials) | undated | 2026-11-01 | medium |
| [29] | Auth.js now maintained by Better Auth | [Better Auth blog](https://better-auth.com/blog/authjs-joins-better-auth) | 2025-09-22 | 2026-11-01 | high |
| [30] | Better Auth email/password, scrypt default | [Better Auth documentation](https://www.better-auth.com/docs/authentication/email-password) | undated | 2026-11-01 | high |
| [31] | better-sqlite3 is a native module | [better-sqlite3 on GitHub](https://github.com/WiseLibs/better-sqlite3) | undated | 2026-11-01 | medium |
| [32] | node:sqlite stability | [Node.js documentation](https://nodejs.org/api/sqlite.html) | undated | 2026-11-01 | medium |
| [33] | Next.js releases and security cadence | [Vercel, Next.js blog](https://nextjs.org/blog) | 2026-10-06 | 2026-11-01 | high |
| [34] | Recharts releases | [Recharts on GitHub](https://github.com/recharts/recharts/releases) | undated | 2026-11-01 | medium |
| [35] | Broken access control, record ownership, tests | [OWASP Top 10:2025, A01](https://top10.owasp.org/2025/A01_2025-Broken_Access_Control) | 2025 | 2026-11-01 | high |
| [36] | Check every request for the specific object | [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | undated | 2026-11-01 | high |
| [37] | Access checks even with random identifiers | [OWASP IDOR Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html) | undated | 2026-11-01 | high |
| [38] | Flask tutorial ownership check (`get_post`, 403 and 404) | [Pallets, Flask tutorial (blog)](https://flask.palletsprojects.com/en/stable/tutorial/blog/) | undated | 2026-11-01 | high |

## Staleness map

This is a selection report on a fast-moving topic: **re-check it before acting on it after 2027-05-01 (two quarters)**. Version claims age fastest ([1], [9], [13], [24], [33], [34]; re-check within 1 month, by **2026-12-01**); ecosystem signals such as Flask-Login activity and the Auth.js to Better Auth transition ([7], [8], [29]; 6 months, by **2027-05-01**). Earliest re-check: **2026-12-01**.
