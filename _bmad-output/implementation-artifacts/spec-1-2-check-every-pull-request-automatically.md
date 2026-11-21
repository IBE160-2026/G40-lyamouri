---
title: 'Story 1.2: Check every pull request automatically'
type: 'feature'
created: '2026-11-21'
status: 'done'
route: 'dispatch'
baseline_commit: '374db817f0b7238147e7ac0692692ac09b549322'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Nothing checks a pull request before it is merged, so a failing test, a Ruff error, a forbidden core import or a model change without a migration can reach `main`. Story 1.1 was merged on local checks (D-9), its tests have never run on Linux, and only a manual `lsof` checks that the passwordless database is published on 127.0.0.1 (VG-4).

**Approach:** A GitHub Actions workflow runs the README's checks on Linux for every pull request and push to `main`: `uv sync --locked`, the database from `compose.yaml`, `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` (AD-17). pytest gains the AD-1 import test and a `docker compose config` test (VG-4) and keeps Story 1.1's `makemigrations --check` test. The QA log records the first run on this pull request and the organization check (D-1).

## Boundaries & Constraints

**Always:**
- Every check is a pytest test or a Ruff command, so it also runs locally; CI adds only setup (AD-17).
- Actions pinned to commit SHAs, version in a comment: `actions/checkout` v7.0.1 `3d3c42e5aac5ba805825da76410c181273ba90b1` (`persist-credentials: false`), `astral-sh/setup-uv` v10.3.3 `68559e99cc807c1eb7e9238fd43a15bba460eec2` with uv 0.12.13; `ubuntu-24.04`; `permissions: contents: read`; no secrets.
- New tests name their AD-n or NFR-n (D-10).
- A pull request is merged only after a passing run, by the merge routine: the group has no admin rights for a required status check, which would also block the local merges that keep the noreply address.
- The organization check (D-1) is the first passing run on this pull request, which shows that Actions and both actions are allowed in IBE160-2026; the QA log records it with the policy API's 403 (the user's decision, 2026-11-21).

**Never:**
- No change to `compose.yaml`, the dependencies, `uv.lock` or app code, except a minimal, QA-logged fix if Linux exposes a Story 1.1 defect.
- No static check of AD-1's clock, file and environment rule; the criteria cover imports.
- No deliberately failing commits: failure proofs are local mutations, reverted.
- No Story 1.3 work.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Standard library | `import datetime`, `from __future__ import annotations`, `from .display import x` | import test passes | N/A |
| explanation uses forecasting | `from forecasting import x` in `explanation/` | passes | N/A |
| Forbidden import | `import django`, `from web.models import Company`, `import openpyxl` in a function, `import explanation` in `forecasting/` | fails | names file and modules |
| Missing migration | new `web.Company` field, no migration | `test_migrations_match_the_models` fails | shows the change |
| Open port | a mapping without `127.0.0.1` | compose test fails | names the service |
| No docker locally | `docker` not on PATH | compose test skipped | CI always has docker |
| Failing test in CI | pytest fails | run fails; Ruff steps still run | N/A |

</frozen-after-approval>

## Code Map

- `compose.yaml` -- `db` on `"127.0.0.1:15432:5432"`; `docker compose config --format json` gives `services.<name>.ports[].host_ip`. Do not change.
- `pyproject.toml` -- pytest `pythonpath = ["src"]`, `testpaths = ["tests"]`; uv `>=0.12.13`; Python `==3.13.*`. Do not change.
- `tests/test_company.py` `test_migrations_match_the_models` -- the `makemigrations --check` test (AD-17), task 3.
- `tests/test_gitignore.py` -- skip-when-the-tool-is-missing pattern; `tests/test_manage.py` -- `REPO_ROOT`.
- `src/forecasting/`, `src/explanation/` -- empty core packages; `sys.stdlib_module_names` includes `__future__`.
- `README.md` «Tester»; `docs/qa-logg.md` 2026-11-21 clone-run entries (style); VG-4 in `deferred-work.md` and `.logs/mounia-03/issues.md`.

## Tasks & Acceptance

**Execution:**
- [x] `.github/workflows/ci.yml` -- «CI» on `pull_request`, `push` to `main`, `workflow_dispatch`; one job, 15-minute timeout, concurrency per ref (cancelling only pull requests); checkout, setup-uv, `uv sync --locked` (`id: sync`), `docker compose up -d --wait`, pytest, then both Ruff commands with `if: ${{ !cancelled() && steps.sync.outcome == 'success' }}` -- AD-17, NFR-2, DR-7.
- [x] `tests/test_core_imports.py` -- `ast` over every `*.py` in both packages; allowed: the standard library, the package itself, `forecasting` for `explanation`; relative imports stay inside; the checker tested in memory on the matrix rows; both packages read -- AD-1.
- [x] `tests/test_compose.py` -- `docker compose config --format json` at the repository root: at least one published port, each on 127.0.0.1; skip without `docker` -- NFR-3, AD-14.
- [x] `tests/test_ci_workflow.py` -- added by the matrix test audit: CI runs exactly the README's commands, a pytest failure still lets both Ruff steps run, and every action is pinned to a commit SHA -- AD-17, NFR-2, DR-7.
- [x] `README.md` -- «Tester»: CI runs the same commands on Linux for every pull request, which is merged only after a passing run; the compose test skips without `docker` -- AD-17, DR-1.
- [x] After the first run: `docs/qa-logg.md` (run, organization check, mutation proofs, any Linux fix); close VG-4 in `deferred-work.md` and `issues.md`.

**Acceptance Criteria:**
- Given this story's pull request, when GitHub Actions runs on Linux, then every step passes, Story 1.1's tests included.
- Given a local mutation (`import django` in `src/forecasting/__init__.py`, a new `web.Company` field, `compose.yaml` publishing `15432:5432`), when `uv run pytest` runs, then the import, migration and compose tests each fail, and the mutation is reverted.
- Given the first passing run, when the QA log is updated, then it records the run and the organization check (D-1).

### Review Findings

BMAD Code Review of the story branch (2026-11-22; PR #10): Blind Hunter (BH), Edge Case Hunter (EC), Verification Gap (VG) and Acceptance Auditor (AA), on 6 files from `374db81` to the working tree. The IDs continue the bmad-build pass (BH-9 and EC-4 onward). Findings with the same location and claim as a row in the Review Triage Log keep that verdict («carried»). Three layers stopped at a usage limit and were resumed where they stopped. Verification Gap filed no gap findings.

- [x] [Review][Decision] The AD-1 import test accepts the standard library's database and network modules (VG-1, EC-15, BH-20) — `forbidden_imports` returns `[]` for `sqlite3`, `urllib.request`, `http.client` and `socket`, because they are in `sys.stdlib_module_names`. AD-1 says that the core never imports a database driver or an HTTP library, and the module docstring promises that a database driver fails. Options: a denylist of those modules with example rows, or keep the story's criterion (anything outside the standard library) and correct the docstring. Resolved 2026-11-22: the user chose the denylist (patched).
- [x] [Review][Decision] A pending run on `main` can be cancelled (AA-3, EC-4, EC-16, BH-9) — every push to `main` uses the group `ci-refs/heads/main`, and GitHub cancels a pending run when a newer one queues. With one run in progress, a third quick push leaves the second unchecked, against «every push to `main`». Options: a group per run for events other than pull requests, or «the latest push to `main`» in the README and the workflow comment. Resolved 2026-11-22: the user chose a group per run (patched).
- [x] [Review][Patch] The README's expected result does not cover the skip it documents (AA-5, BH-10) [README.md:65]
- [x] [Review][Patch] The README states the merge rule as if GitHub enforced it, without naming the run that counts (BH-11, EC-5) [README.md:69]
- [x] [Review][Patch] The QA log lacks the defects in AI-written code that this story's reviews found (AA-1, BH-12) [docs/qa-logg.md]
- [x] [Review][Patch] The push constraint is not tracked: the keychain token lacks the `workflow` scope, so the merge of PR #10 to `main` and any change to `ci.yml` must go over SSH (AA-2, BH-14) [docs/qa-logg.md:460]
- [x] [Review][Patch] The QA log never explains VG-4, and two Story 1.1 entries still read as open (BH-13) [docs/qa-logg.md:398]
- [x] [Review][Patch] The run record is imprecise: the run ID is called a number, and the record lacks a link, a time zone and the 403 endpoints; its organization conclusion is broader than the evidence (BH-15) [docs/qa-logg.md:432]
- [x] [Review][Patch] `tests/test_ci_workflow.py` guards less than its docstrings and the commit message claim: job-level keys, triggers, the runner, permissions, credentials, `env`, extra actions and new README commands are unchecked, and pins with a subpath fail (AA-4, VG-2, EC-6, EC-7, EC-8, EC-9, EC-17, BH-16, BH-17, BH-18) [tests/test_ci_workflow.py]
- [x] [Review][Patch] The compose test does not read the configuration that `docker compose up` loads: a `compose.override.yaml` publishing 5432 on every address passed it, and the QA log calls the check a runtime fact (EC-11, BH-19) [tests/test_compose.py:26]
- [x] [Review][Patch] The compose test finds one docker binary with `shutil.which` and runs another by name (EC-13) [tests/test_compose.py:23]
- [x] [Review][Patch] The pull request does not say why the status table is unchanged (AA-6) [PR #10 description]

**Rejected**
- EC-10 — carried (EC-1, review pass 1): `docker compose config` runs without a timeout.
- EC-12 — low: `network_mode: host` would bypass the port check; unlikely in this compose file, and the fix adds a guard.
- EC-14 — carried (BH-3, review pass 1): dynamic imports pass the import test.

## Implementation Notes

- Implemented directly from the spec, without an implementation subagent, as the user chose for this run.
- `astral-sh/setup-uv` v10.3.3 (2026-10-28) was chosen over v10.4.0, which was one day old; `actions/checkout` v7.0.1 is from 2026-07-20.
- The matrix test audit found two rows without a covering test that ran: «No docker locally» and «Failing test in CI». It added `test_compose_test_is_skipped_without_docker` and `tests/test_ci_workflow.py`, which reads the workflow as text because no dependency parses YAML.
- Mutation proofs, each reverted with `git checkout` and checked with `git diff`: `import django` in `src/forecasting/__init__.py` failed `test_core_imports_only_the_standard_library[forecasting/__init__.py]`; a `nickname` field on `web.Company` failed `test_migrations_match_the_models`; `"15432:5432"` in `compose.yaml` failed the compose test.
- Locally, with `$HOME/.docker/bin` on PATH: 99 tests passed and none were skipped, and Ruff passed on 25 files. Without docker on PATH, the compose test was skipped with «docker is not on PATH».
- Left for the pull request, because step 3 makes no remote calls: the first CI run, its QA log entry with the organization check, and closing VG-4.
- The HTTPS token in the keychain lacks GitHub's `workflow` scope, and `gh auth refresh -s workflow` timed out twice, so the branch was pushed once over SSH with a key the user registered. The first run (44952275264, PR #10, `b2dd344`) passed on `ubuntu-24.04` in 36 s: 99 tests passed and none were skipped, both Ruff checks passed, and the QA log records it with the organization check. VG-4 is closed in `deferred-work.md` and `issues.md`.
- BMAD Code Review (2026-11-22): the user decided the two decision items and chose to apply every patch. After the fixes, 103 tests passed with none skipped, and Ruff passed on 25 files. Sixteen mutation checks behaved as expected: each of the 15 bypasses the reviewers showed now fails a test, and the `COMPOSE_FILE` control passes. The concurrency group now differs from Task 1's «per ref» outside pull requests.

## Spec Change Log

## Review Triage Log

Review pass 1 (2026-11-21): Blind Hunter (BH, floor 6 for a 31.7 kB diff), Edge Case Hunter (EC) and Verification Gap (VG), run inline by the build session, as the user chose; the independent review with subagents is BMAD Code Review. The build session applied both patches itself.

| ID | Finding | Verdict | Evidence | Route |
|---|---|---|---|---|
| BH-1 | The compose test reads whatever file `COMPOSE_FILE` names, from the environment or `.env`, not necessarily `compose.yaml` | low | Shown: with `COMPOSE_FILE=does-not-exist.yaml` the test read that file and failed | patch: `docker compose --file compose.yaml config` |
| EC-2 | `COMPOSE_FILE` is a path into the compose test that no guard handles | low | The same defect as BH-1 | patch, with BH-1 |
| EC-3 | Claim: the test checks «`docker compose config` at the repository root», but the working directory alone does not pin the file | low | The same defect as BH-1 | patch, with BH-1 |
| BH-2 | `tests/test_ci_workflow.py` misses an `if:` or `continue-on-error` on the install, database or pytest step, which would skip or ignore the tests | low | Shown: `if: false` on the pytest step left all three workflow tests passing | patch: assert those steps have neither key |
| BH-3 | Dynamic imports (`importlib.import_module`, `__import__`) pass the import test | low | Real, but unlikely in the pure core, and detecting calls adds a branch; the story's criteria name imports | reject |
| BH-4 | A BOM or an encoding cookie in a core file makes `ast.parse` raise | false | The test then errors loudly instead of passing, and no core file has either | reject |
| BH-5 | A Docker Hub rate limit or pull failure can fail a run | maybe-false | No run exists yet; a failed pull is fixed by re-running the job, so at most low | reject |
| BH-6 | `test_compose_test_is_skipped_without_docker` calls the other test function | low | Works as written; a helper would only move the same lines | reject |
| BH-7 | CI may install a newer Python 3.13 patch than the local 3.13.15 | false | `requires-python = "==3.13.*"` and `uv.lock` define the range, and a fresh local clone gets the same newest patch | reject |
| BH-8 | The regenerated epic context no longer lists AD-13's and AD-14's run-mode rules | low | They stay in the spine and are enforced by Story 1.1's settings tests, and step-02 reads the spine when the context is unclear | reject |
| EC-1 | `docker compose config` runs without a timeout | low | The command only reads files, CI's 15-minute job timeout bounds a hang, and a timeout adds a parameter | reject |
| VG | No verification gaps: the checker is covered by the example tests and the compose test by the real file and the mutation; the workflow is static configuration, verified by the run on the pull request | — | — | — |

## Design Notes

VG-4 is a pytest test, not a CI-only step, because AD-17 prevents checks that only some machines run; CI has docker, as it starts the database. The Ruff steps run after a pytest failure, so one run reports every broken check.

## Verification

**Commands:** (with `$HOME/.docker/bin` on PATH)
- `uv run pytest`, `uv run ruff check`, `uv run ruff format --check` -- pass, nothing skipped
- `uv run --no-project --with pyyaml python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"` -- parses
- the three mutations -- each named test fails; `git diff` shows none afterwards
- `gh pr checks --watch` on the story's pull request -- passes
