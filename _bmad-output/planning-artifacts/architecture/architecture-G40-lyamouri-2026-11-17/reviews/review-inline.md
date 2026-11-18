# Reviewer Gate — inline review of the architecture spine

- **Spine:** `ARCHITECTURE-SPINE.md` (2026-11-17)
- **How:** run inline in the architecture session, without subagents, at the user's request. An inline review is less independent than the subagent review that BMAD describes.
- **Verdict:** the spine is ready for the epics. Twelve findings were fixed in the spine before it was set to `final`: the eight holes in section 4 and the four gaps in section 5. None needs a decision from the user.

## 1. Mechanical checks

- `lint_spine.py`: 0 findings. There are no placeholders, the AD IDs run from AD-1 to AD-17 without gaps, every AD has Binds, Prevents and Rule, and every Stack row has a version.
- **IDs:** all 64 IDs in `binds` exist in the PRD, and every FR, NFR, AG and DR in the PRD is in `binds`. Every FR, SM, R and E reference in the spine exists in the PRD, and every AD referenced is defined.
- **UX names:** the message names the spine uses (Database unavailable, Server error, Expired form, Not found) exist in the EXPERIENCE.md Message Catalogue.
- **Diagrams:** the three mermaid diagrams were checked by hand; there was no renderer in the session. No template comment is left.

## 2. Rubric (good-spine checklist)

| Check | Result |
|---|---|
| The real divergence points for the epics are fixed | Yes: compute path, rounding and format, wording, isolation, weeks, settings, state, rendering and URLs, errors, run modes, database, seed and reset, publishing, tests. |
| Every Rule is enforceable | Yes. AD-1 and AD-7 are checked by tests (AD-17), AD-16 by the build script, and AD-15 by `load_seed` itself. |
| Nothing under Deferred lets two stories diverge | Yes. The seed and answer-key schemas sit in one data story, and the Could items name the AD they would amend. |
| Named technology is verified | See section 3. |
| Brownfield | Not applicable: no application code on this branch. The archived code of story 1.1 is not an input. |
| The spec's capabilities are covered | Yes: every FR, NFR, AG and DR is bound and mapped. |
| Operational envelope | Decided: environments (AD-13), providers and topology (AD-14, AD-16, diagram), CI (AD-17). Monitoring and backups are deferred with a reason. |

## 3. Lens: verified technology (configured reviewer 1)

All entries were checked against the web or a test on 2026-11-17 (memlog): Django 5.2.19, Python 3.13 support in Django and Vercel, psycopg 3.3.9 with its wheels, PostgreSQL 18.7, the image `postgres:18.7`, Docker Desktop 4.99.0 with Compose v5.7.0, uv 0.13.9 (0.12.13 tested), pytest 9.2.0, pytest-django 4.14.0, Ruff 0.17.5 and openpyxl 3.1.5. On the Vercel side: the Django detection, the build script, the regions, `git.deploymentEnabled`, the Neon variables and Neon Postgres 18.

Not confirmed on the web in this session, and left as first-story checks in Deferred:
- Neon's Frankfurt region, which was confirmed on 2026-11-08 in the archived run;
- Docker and Compose on GitHub's Linux runners;
- how Vercel treats `uv.lock`.

openpyxl has had no release since June 2024. It is stable and used only in development.

## 4. Lens: adversarial (configured reviewer 2)

Pairs of stories that could follow every AD and still build incompatibly:

| # | Hole | Fix |
|---|---|---|
| 1 | The settings page and the switch could choose different products for the FR-21 before-and-after values, or none on the overview. | AD-2: compare the product the user came from; without one, show only the setting line. |
| 2 | Search could filter before or after R-12, which changes groups and figures. | AD-2: search only hides products from the computed overview. |
| 3 | The loader could read data without the company filter. | AD-2: the loader reads through `web/queries.py`. |
| 4 | Week labels such as «1/2027» could be formatted separately in the chart, the worksheet and the explanation. | AD-3: week labels come from `forecasting/display.py`. |
| 5 | One story could store the latest data week on the company while another derives it from the sales weeks. | AD-8: derived, never stored. |
| 6 | `load_seed` in the Vercel build could write a secret file into the deployment. | AD-13: in published mode `load_seed` never writes a secret file. |
| 7 | The return path after Innstillinger could become an open redirect. | AD-11: the return path must be inside the app. |
| 8 | Test writers could name tests differently, which breaks DR-5 traceability. | AD-17: every test names its FR-n or E-n. |

## 5. Reconciliation with the inputs

- **PRD:** the PostgreSQL decision and the user's condition on deleting data now stand in the PRD, with three rows in §12 dated 2026-11-17. The spine binds every requirement. One interpretation was noted: error pages show no company data and need no login (AD-6), and FR-1's rule for pages applies to the app's pages.
- **UX:** the spine follows the technology posture of EXPERIENCE.md. It fixes the URLs, as EXPERIENCE.md asked, and uses the Message Catalogue as the copy source. EXPERIENCE.md and DESIGN.md now cover the error pages (change log, 2026-11-17).
- **The teacher's feedback** (`tilbakemelding-prd.md`):

  | Point | Where the spine answers it |
  |---|---|
  | 4.1, the scope and cut line | The architecture stays at one app and one database, and the first story proves publishing early. |
  | 4.2, allowed numbers and placeholders | AD-5. |
  | 4.3, FR-17 and FR-17b | Both are bound, and the convention for optional features is set. |
  | 4.5, Should order and SM-10 | DR-6 order kept; SM-10 is checked by hand and logged. |
  | Reflection question 2, when the app and the spreadsheet disagree | AD-17: calculate the case again by hand, correct whichever was wrong, and log it. |

- **technology.md:** the teacher's note `teknologinotat.md` explains what was adopted, adapted and dropped.

Gaps found by the rubric and the reconciliation, all fixed in the spine:
1. AD-17: when a test and the spreadsheet disagree, the case is calculated again by hand, and the finding is logged (the teacher's reflection question 2, DR-9).
2. Conventions: each story on its own branch, merged through a reviewed pull request (DR-7).
3. Deferred: the operations envelope (no monitoring, backup or alerting service in v1) and rate limiting.
4. Deferred: check that Neon offers Postgres 18 in AWS Frankfurt when the project is created.

## 6. Left open

- Offline start and Windows setup: not tested (Deferred, QA log).
- The first-story checks listed in Deferred.
