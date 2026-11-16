# Archive: planning artifacts superseded by the PRD update of 2026-11-15

These folders were moved here on the branch `design/after-prd-feedback`: the UX and the architecture on 2026-11-15, before new design work started, and the epics and the sprint plan on 2026-11-16, before the new architecture. The work-log entries for story 1.1 were copied here on 2026-11-16. They are kept for reference and traceability. Nothing was deleted, and `git log --follow <file>` shows each file's history from its original path.

| Folder | Original path | Created | Why it is superseded |
|---|---|---|---|
| `ux-G40-lyamouri-2026-11-06/` | `_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-06/` | 2026-11-06 | Built on the PRD before the teacher's feedback. It disagrees with the updated FR-24 (reason in the forecast column, «–» for the order quantity and weeks of cover), with FR-17b and with the explanation rule in FR-27. |
| `architecture-G40-lyamouri-2026-11-08/` | `_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-08/` | 2026-11-08 | Built on the PRD before the teacher's feedback. AD-10 describes the old number-and-label check, and `binds` lacks FR-17b. |
| `epics-G40-lyamouri-2026-11-08/` | `_bmad-output/planning-artifacts/epics.md` and `_bmad-output/implementation-artifacts/sprint-status.yaml` | 2026-11-08 | Built on the archived UX and architecture and on the PRD before the teacher's feedback. The epics' input paths point to the old folders, and the sprint plan's first milestone (11 November) has passed. A new epics list and sprint plan are made after the new architecture. |
| `story-1-1-G40-lyamouri-2026-11-10/` | `docs/arbeidslogg.md` in the tag `archive/story-1-1-project-skeleton` | 2026-11-10 | A verbatim copy of the work-log entries for 10 and 11 November (story 1.1 and the GitHub CLI). Pull request #1 was closed without merging, so `docs/arbeidslogg.md` on this branch does not have them. |

## Old code (story 1.1)

The project skeleton from story 1.1 was built on 10 and 11 November on the archived architecture. It holds the Django apps, templates, static files, seed data, `manage.py`, `requirements.txt`, `ruff.toml`, `vercel.json` and `.env.example`. It is not on this branch, and it is not an input for the new architecture.
- **Kept unchanged:** on the branch `story/1-1-project-skeleton` (pull request #1, closed without merging on 2026-11-16) and in the annotated tag `archive/story-1-1-project-skeleton` (commit `ffc934c`). The tag keeps the code even if the branch is removed later.
- **Its documents** are in the same tag:
  - the story specification, epic context and deferred work in `_bmad-output/implementation-artifacts/`;
  - the session logs 991 and 992;
  - the work-log entries for 10 and 11 November, which are also copied verbatim into `story-1-1-G40-lyamouri-2026-11-10/arbeidslogg.md` in this folder.
- **To look at it** without changing any branch, run `git switch --detach archive/story-1-1-project-skeleton` or `git show archive/story-1-1-project-skeleton:<path>`.

## The basis for new work

The new design and architecture start from the updated PRD:
- **File:** `_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md`.
- **Status:** `final`, last updated 2026-11-16. The update of 2026-11-15 was merged into `main` in pull request #2. The changes of 2026-11-16 are on `design/after-prd-feedback` and not yet in `main`.
- **Changes:** the change log in its §12 lists every change.
- **Disagreements:** `review-consistency-2026-11-15.md` in the same folder lists the statements in these archived documents that disagree with the PRD.

## The new design

The new UX was built from the updated PRD and set to `final` on 2026-11-16: `_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/` (`DESIGN.md`, `EXPERIENCE.md` and `mockups/`). The new architecture is not made yet.

## Not archived

`architecture/technology.md` stays where it is. It is the teacher's description of another project's stack (added 2026-11-12) and is input for the new architecture.

## Still pointing at the old paths

These files were not changed:
- `prd.md` ends §12 with an open line about aligning `epics.md` and the architecture spine. The PRD is not changed now; the line is closed when the new architecture and epics exist.
- The entries in `docs/arbeidslogg.md` and the session logs, which are history and stay as they were.

`.impeccable/config.json`, which holds detector exceptions for the archived mockups, was pointed to their new paths in this folder on 2026-11-16.
