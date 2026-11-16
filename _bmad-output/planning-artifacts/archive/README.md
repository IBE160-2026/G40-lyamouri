# Archive: planning artifacts superseded by the PRD update of 2026-11-15

These folders were moved here on 2026-11-15, on the branch `design/after-prd-feedback`, before new design work starts. They are kept for reference and traceability. Nothing was deleted, and `git log --follow <file>` shows each file's history from its original path.

| Folder | Original path | Created | Why it is superseded |
|---|---|---|---|
| `ux-G40-lyamouri-2026-11-06/` | `_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-06/` | 2026-11-06 | Built on the PRD before the teacher's feedback. It disagrees with the updated FR-24 (reason in the forecast column, «–» for the order quantity and weeks of cover), with FR-17b and with the explanation rule in FR-27. |
| `architecture-G40-lyamouri-2026-11-08/` | `_bmad-output/planning-artifacts/architecture/architecture-G40-lyamouri-2026-11-08/` | 2026-11-08 | Built on the PRD before the teacher's feedback. AD-10 describes the old number-and-label check, and `binds` lacks FR-17b. |

## The basis for new work

The new design and architecture start from the updated PRD:
- **File:** `_bmad-output/planning-artifacts/prds/prd-G40-lyamouri-2026-11-02/prd.md`.
- **Status:** `final`, updated 2026-11-15, merged into `main` in pull request #2.
- **Changes:** the change log in its §12 lists every change.
- **Disagreements:** `review-consistency-2026-11-15.md` in the same folder lists the statements in these archived documents that disagree with the PRD.

## The new design

The new UX was built from the updated PRD and set to `final` on 2026-11-16: `_bmad-output/planning-artifacts/ux-designs/ux-G40-lyamouri-2026-11-15/` (`DESIGN.md`, `EXPERIENCE.md` and `mockups/`). The new architecture is not made yet.

## Not archived

`architecture/technology.md` stays where it is. It is the teacher's description of another project's stack (added 2026-11-12) and is input for the new architecture.

## Still pointing at the old paths

These files were not changed:
- `epics.md`, which is updated after the new design and architecture.
- `.impeccable/config.json`, which holds detector exceptions for the archived mockups.
- The entries in `docs/arbeidslogg.md` and the session logs, which are history and stay as they were.
