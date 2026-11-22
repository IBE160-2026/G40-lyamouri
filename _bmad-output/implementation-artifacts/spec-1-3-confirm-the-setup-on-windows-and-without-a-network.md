---
title: 'Story 1.3: Confirm the setup on Windows and without a network'
type: 'chore'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
baseline_commit: '850250d172662cbcee1f9c18997da1a1cd3a6ce3'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The README's setup has run only on macOS with Apple M1, and nobody has started Prognose without a network, so an examiner on Windows x64 or offline cannot trust it (SM-2, NFR-1). Whether uv and Docker Desktop may be installed on the Windows x64 PC at work, under the employer's IT rules and Docker's license terms, is not confirmed (D-3).

**Approach:** Run three checks, fix in the README or the configuration whatever fails, and record each run in `docs/qa-logg.md` with the date, the operating system, the uv and Docker Desktop versions, the result and the time taken (DR-9):
- Offline start on macOS now: with Prognose started once, the database is stopped and Docker Desktop quit, the user switches the network off, and Docker Desktop, `docker compose up -d --wait` and `runserver --insecure` start again until `http://127.0.0.1:8000/` answers. A script records the versions, the steps and the times; the user switches the network.
- On 2026-11-25, on the Windows x64 PC at work if installing uv and Docker Desktop is allowed there: a group member follows the README's setup section from a fresh clone in Windows PowerShell, records the installation time with WSL 2 and any restart, runs the offline start, and checks with `icacls .secret_key` who can read the session secret (`issues.md`, EC-5 and BH-7). If it is not allowed, another Windows x64 computer is used if one is available; otherwise the QA log records the limitation, and the README and the status table say that Windows is untested.
- Afterwards the README names the tested platforms and, if the offline checks pass, says that no network is needed after the first setup. Story 1.3 builds no FR and changes no code unless a check fails.

</frozen-after-approval>

## Implementation Notes

- 2026-11-22, macOS offline start: the user ran a scratchpad script (not committed) in Terminal with the network off. The database was healthy after 5 s and `/` answered 200 with «Prognose» after 1 s; the QA log records it. Docker Desktop answered 1 s after `open -a Docker`, so it was probably not fully quit, and a cold Docker Desktop start offline is still unproven.
- Finding: Terminal had no `docker` on PATH, because Docker Desktop's CLI tools were in `~/.docker/bin`. The README now says how to fix `command not found: docker` (Settings → Advanced → System, or `~/.docker/bin` on PATH).
- 2026-11-22, later: the user cannot install anything on the work PC and has no other Windows x64 PC, so the Intent's fallback applies. The QA log records the limitation, and the README and the status table say that the setup with Docker Desktop and the offline start are untested on Windows. The user also chose a partial test: `.github/workflows/windows-setup.yml` runs the README's setup without Docker on GitHub's Windows Server 2025 x64 runner, with its PostgreSQL 17, in Windows PowerShell. It runs when the file changes in a pull request and by hand; `workflow_dispatch` alone would need the file on `main` first. The plan below for 2026-11-25 no longer applies. The user's wish to test the site in a Windows browser belongs to NFR-6 and the manual checklist in Story 4.4, not to this story.
- Windows run 1 (45006768015, PR #12, `0eaea95`) passed in 40 s on Windows Server 2025 x64 with Windows PowerShell 5.1, uv 0.12.13, CPython 3.13.17 and PostgreSQL 17.12. `icacls` showed that `.secret_key` inherits the folder's rules, and `BUILTIN\Users` could read it there, so the README now advises cloning into the user folder on a shared PC. The QA log, the README and the status table record the limitation (D-3). The «ø» in `load_seed`'s message showed as «�» in the CI log; the output goes through a pipe there, and an interactive console was not tried.
- Windows run 3 (45009667642, PR #12, `fedaef2`) ran the workflow as fixed after BMAD Code Review and passed in 57 s. It now also runs when `src/**`, `.python-version`, `pyproject.toml` or `uv.lock` change in a pull request. uv downloaded CPython 3.13.15 (`UV_PYTHON_PREFERENCE: only-managed`); run 1 had used the runner's own CPython 3.13.17. In a new clone in the user folder, only SYSTEM, Administrators and the user could read `.secret_key`.
- 2026-11-22, macOS run 2 (14.56–14.58, `fedaef2`), which the user chose in BMAD Code Review: a Terminal window found `~/.docker/bin/docker` after the README's PATH fix. With no Docker Desktop process left, `docker info` failing and the network off, Docker Desktop answered 6 s after `open -a Docker`, the database was healthy after 4 s, and `/` answered 200 with «Prognose» after 2 s. The README now says that no network is needed after the first setup on macOS, and that this is untested on Windows.
- The Windows workflow goes beyond the Intent's «changes no code unless a check fails»: it is CI configuration, not app code, and the user chose it on 2026-11-22 after the work PC was ruled out. The Intent is unchanged.
- Plan for 2026-11-25 on the Windows x64 PC, if IT allows uv and Docker Desktop (`issues.md`, the work-PC point):
  1. Time the installation of uv and Docker Desktop with WSL 2 and any restart.
  2. In PowerShell, run `Start-Transcript $HOME\prognose-test.txt`, then `uv --version`, `docker version`, `wsl --version` and `Get-ComputerInfo -Property OsName,OsVersion,OsArchitecture`.
  3. Clone `main` as the README says, run the five README commands one at a time, and open `http://127.0.0.1:8000/`.
  4. Run `icacls .secret_key` to see who can read the secret, and `Get-History | Format-Table CommandLine,StartExecutionTime,EndExecutionTime` for the times.
  5. Offline: stop the server with Ctrl+C, run `docker compose down`, quit Docker Desktop, switch the network off, start Docker Desktop, run `docker compose up -d --wait` and `uv run python src/manage.py runserver --insecure`, and open `/`. Then run `Stop-Transcript`.

## Review Triage Log

Review pass 1 (2026-11-22): Blind Hunter, run inline by the build session as in Story 1.2, on the branch diff from `850250d`; the independent review with subagents is BMAD Code Review.

| ID | Finding | Verdict | Evidence | Route |
|---|---|---|---|---|
| BH-1 | The Windows workflow starts the service `postgresql-x64-17` by name, so it fails when GitHub's image moves to a newer PostgreSQL | low | The image names the service after the major version, and Story 4.4 reruns the workflow two weeks later | patch: `Get-Service postgresql*` |
| BH-2 | The Windows workflow runs only when its own file changes, so a dependency without a Windows package would go unnoticed | low | `pull_request.paths` listed only the workflow file | patch: also `pyproject.toml` and `uv.lock` |
| BH-3 | `uv run pytest` does not run on Windows, so the README's «Tester» section is unchecked there | low | Outside the story's criteria, which cover the setup and the start | defer (`deferred-work.md`) |

Review pass 2 (2026-11-22): BMAD Code Review on PR #12 with four subagents (Blind Hunter, Edge Case Hunter, Verification Gap and Acceptance Auditor), on the branch diff from `850250d` with the BH-1 and BH-2 patches. 46 findings, grouped by cause into 24 items: 2 decision-needed, resolved by the user (rerun the macOS offline start with Docker Desktop quit; also run the Windows workflow for `src/**` and `.python-version`), 19 patches applied (`fedaef2` for the workflow, the test and the README; the documents in PR #12), 1 deferred (`deferred-work.md`) and 2 rejected. This spec has no Tasks section, so the findings and decisions are listed in the PR #12 comment, not under «Review Findings».
